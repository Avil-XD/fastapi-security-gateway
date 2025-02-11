import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

class APIAnalyzer:
    def __init__(self, policy_path='config/security_policies.yaml'):
        self.models = {}
        self.policy_path = policy_path
        self.baseline_established = False
        self.metrics_window = []
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models with error handling"""
        try:
            self.models = {
                'request_frequency': IsolationForest(contamination=0.01, random_state=42),
                'parameter_variation': IsolationForest(contamination=0.01, random_state=42),
                'response_size': IsolationForest(contamination=0.01, random_state=42)
            }
            # Fit models with initial empty data to avoid first-call errors
            for model in self.models.values():
                model.fit([[0]])
        except Exception as e:
            print(f"Error initializing ML models: {e}")
            # Initialize with dummy models that always return -1 (normal)
            self.models = {
                'request_frequency': lambda x: [-1],
                'parameter_variation': lambda x: [-1],
                'response_size': lambda x: [-1]
            }
        
    def load_security_policies(self):
        # TODO: Implement YAML policy loader
        return {'training_window': '14d'}  # Temporary stub

    def analyze_request(self, request_data):
        """Real-time API request analysis"""
        features = self._extract_features(request_data)
        anomalies = self._detect_anomalies(features)
        
        if any(anomalies):
            self._trigger_self_healing(request_data, anomalies)
            return False
        return True

    def _extract_features(self, data):
        """Convert raw request data to ML features"""
        return {
            'request_frequency': len(self.metrics_window),  # Simple request count
            'parameter_variation': self._calc_param_variance(data),
            'response_size': data.get('response_size', 0)
        }

    def _calc_param_variance(self, data):
        """Calculate variance in request parameters"""
        # Count number of parameters in query and body
        param_count = len(data.get('query_params', {}))
        if 'body' in data:
            param_count += len(data['body'])
        return param_count

    def _detect_anomalies(self, features):
        """Run ML models on features"""
        try:
            anomalies = {}
            for (metric, model), value in zip(self.models.items(), features.values()):
                try:
                    if callable(model):
                        # Handle lambda functions (dummy models)
                        result = model([[value]])[0]
                    else:
                        # Handle IsolationForest models
                        result = model.predict([[value]])[0]
                    anomalies[metric] = result == -1
                except Exception as e:
                    print(f"Error detecting anomaly for {metric}: {e}")
                    anomalies[metric] = False
            return anomalies
        except Exception as e:
            print(f"Error in anomaly detection: {e}")
            return {metric: False for metric in self.models.keys()}

    def _trigger_self_healing(self, request_data, anomalies):
        """Interface with self-healing subsystem"""
        print(f"ALERT: Anomalies detected {anomalies}")
        # TODO: Implement integration with self-healing module

    def log_metrics(self, response_data):
        """Log metrics for analysis"""
        try:
            self.metrics_window.append({
                'timestamp': datetime.now().timestamp(),
                'status_code': response_data.get('status_code', 0),
                'latency': response_data.get('latency', 0),
                'response_size': response_data.get('response_size', 0)
            })
            # Keep only last 1000 requests
            if len(self.metrics_window) > 1000:
                self.metrics_window = self.metrics_window[-1000:]
        except Exception as e:
            print(f"Error logging metrics: {e}")