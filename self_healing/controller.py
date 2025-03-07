from schema import Schema, And, Or, Optional
from typing import Dict, Any
import time

class SelfHealingController:
    def __init__(self, policy_loader):
        self.policy_loader = policy_loader
        self.request_counts = {}
        self.blocked_ips = set()
        
    def apply_measures(self, request_context: Dict[str, Any]) -> bool:
        """Apply self-healing measures to the request"""
        try:
            # Get current policies
            policies = self.policy_loader.get_policies("rate_limiting")
            
            # Validate request
            if not self._validate_request(request_context):
                return False
                
            # Check rate limits
            client_ip = request_context.get('headers', {}).get('x-forwarded-for', 'unknown')
            if not self._check_rate_limit(client_ip, policies):
                return False
                
            # All checks passed
            return True
            
        except Exception as e:
            print(f"Error in self-healing measures: {str(e)}")
            return True  # Fail open on errors
            
    def _validate_request(self, request_context: Dict[str, Any]) -> bool:
        """Validate request against security policies"""
        try:
            schema = Schema({
                'path': str,
                'method': str,
                'headers': dict,
                Optional('query_params'): dict,
                Optional('body'): Or(dict, None)
            })
            
            schema.validate(request_context)
            return True
            
        except Exception as e:
            print(f"Request validation failed: {str(e)}")
            return False
            
    def _check_rate_limit(self, client_ip: str, policies: Dict[str, Any]) -> bool:
        """Check if client has exceeded rate limits"""
        current_time = time.time()
        
        # Initialize or clean up old records
        if client_ip not in self.request_counts:
            self.request_counts[client_ip] = {
                'count': 0,
                'window_start': current_time
            }
        
        # Check if client is blocked
        if client_ip in self.blocked_ips:
            return False
            
        # Get rate limit settings
        max_requests = policies.get('requests_per_minute', 100)
        window_size = 60  # 1 minute window
        
        client_data = self.request_counts[client_ip]
        
        # Reset window if expired
        if current_time - client_data['window_start'] > window_size:
            client_data.update({
                'count': 1,
                'window_start': current_time
            })
            return True
            
        # Increment request count
        client_data['count'] += 1
        
        # Check if limit exceeded
        if client_data['count'] > max_requests:
            self.blocked_ips.add(client_ip)
            return False
            
        return True