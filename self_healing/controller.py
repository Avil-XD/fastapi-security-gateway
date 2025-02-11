import time
from datetime import timedelta
from schema import Schema, And, Or, Optional

class SelfHealingController:
    def __init__(self, policy_loader):
        self.circuit_states = {}
        self.policy_loader = policy_loader
        self.active_measures = {
            'circuit_breaker': self.handle_circuit_breaker,
            'rate_limit': self.enforce_rate_limit,
            'schema_validation': self.validate_schema
        }
        
    def apply_measures(self, request):
        """Apply all active self-healing measures"""
        try:
            policies = self.policy_loader.get_policies('self_healing')
            if not policies or 'actions' not in policies:
                return True  # No policies means no restrictions
            
            for measure in policies.get('actions', []):
                measure_type = measure.get('type')
                if not measure_type:
                    continue
                
                if measure_type in self.active_measures:
                    try:
                        if not self.active_measures[measure_type](request, measure):
                            return False
                    except Exception as e:
                        print(f"Error applying measure {measure_type}: {e}")
                        # Don't fail on individual measure errors
                        continue
            return True
        except Exception as e:
            print(f"Error in self-healing: {e}")
            return True  # Fail open on errors

    def handle_circuit_breaker(self, request, config):
        """Implement circuit breaker pattern"""
        endpoint = request['path']
        current_state = self.circuit_states.get(endpoint, 'closed')
        
        if current_state == 'open':
            if time.time() > self.circuit_states[endpoint]['until']:
                self.circuit_states[endpoint] = {'state': 'half-open'}
            return False
            
        try:
            threshold = float(config.get('threshold', 500))  # Convert to float
            if request.get('latency', 0) > threshold:
                self.circuit_states[endpoint] = {
                    'state': 'open',
                    'until': time.time() + float(config.get('reset_time', 30))  # Use seconds directly
                }
                return False
        except Exception as e:
            print(f"Circuit breaker error: {e}")
            return True  # Fail open
            
        return True

    def enforce_rate_limit(self, request, config):
        """Dynamic rate limiting based on policies"""
        # TODO: Implement token bucket algorithm
        return True  # Temporary implementation

    def validate_schema(self, request, config):
        """Schema validation using defined API contracts"""
        try:
            if config.get('strict', False):
                return Schema({
                    'path': And(str, len),
                    'method': str,
                    'headers': dict,
                    'query_params': dict,
                    Optional('body'): object,
                    Optional('client_ip'): str
                }).validate(request)
            return True
        except Exception as e:
            print(f"Schema validation warning: {e}")
            return True  # Fail open

    def reset_measures(self, endpoint):
        """Manual reset for circuit breakers"""
        if endpoint in self.circuit_states:
            del self.circuit_states[endpoint]