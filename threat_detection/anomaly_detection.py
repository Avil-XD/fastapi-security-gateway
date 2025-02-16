import warnings
from datetime import datetime

# Suppress numpy warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=UserWarning)

import numpy as np
from sklearn.ensemble import IsolationForest

class APIAnalyzer:
    """Analyzer for detecting API request anomalies using machine learning"""
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
        """Load and validate security policies from YAML"""
        try:
            import yaml
            with open(self.policy_path, 'r') as f:
                policies = yaml.safe_load(f)
            
            # Extract relevant policies with defaults
            behavioral = policies.get('policies', {}).get('behavioral_baseline', {})
            return {
                'training_window': behavioral.get('training_window', '14d'),
                'max_requests_per_minute': behavioral.get('max_requests_per_minute', 1000),
                'max_parameters': behavioral.get('max_parameters', 100),
                'max_request_size': policies.get('max_request_size', 1048576),  # 1MB default
                'metrics': behavioral.get('metrics', [
                    'request_frequency',
                    'parameter_variation',
                    'response_size'
                ])
            }
        except Exception as e:
            print(f"Error loading security policies: {e}")
            # Return safe defaults
            return {
                'training_window': '14d',
                'max_requests_per_minute': 1000,
                'max_parameters': 100,
                'max_request_size': 1048576,
                'metrics': [
                    'request_frequency',
                    'parameter_variation',
                    'response_size'
                ]
            }

    def analyze_request(self, request_data):
        """Real-time API request analysis"""
        try:
            # Basic validation
            if not isinstance(request_data, dict):
                print("Warning: Request data is not a dictionary")
                return True  # Fail open for invalid data
            
            # Extract and analyze features
            features = self._extract_features(request_data)
            anomalies = self._detect_anomalies(features)
            
            # Log the analysis
            if any(anomalies.values()):
                print(f"ALERT: Anomalies detected in request: {anomalies}")
                self._trigger_self_healing(request_data, anomalies)
                return False
            
            # Update metrics window for future analysis
            self.log_metrics({
                'status_code': 200,  # Assuming success
                'latency': 0,  # Will be updated by middleware
                'response_size': len(str(request_data))  # Basic size estimation
            })
            
            return True
            
        except Exception as e:
            print(f"Error in request analysis: {e}")
            return True  # Fail open on errors

    def _extract_features(self, data):
        """Convert raw request data to ML features"""
        try:
            # Get base features
            features = {
                'request_frequency': len(self.metrics_window),
                'parameter_variation': self._calc_param_variance(data),
                'response_size': data.get('response_size', 0)
            }
            
            # Load configuration limits
            policies = self.load_security_policies()
            max_freq = policies.get('max_requests_per_minute', 1000)
            max_params = policies.get('max_parameters', 100)
            max_size = policies.get('max_request_size', 1048576)  # 1MB default
            
            # Normalize features
            normalized_features = {
                'request_frequency': min(features['request_frequency'] / max_freq, 1.0),
                'parameter_variation': min(features['parameter_variation'] / max_params, 1.0),
                'response_size': min(features['response_size'] / max_size, 1.0)
            }
            
            print(f"Extracted normalized features: {normalized_features}")
            return normalized_features
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            # Return safe defaults
            return {
                'request_frequency': 0,
                'parameter_variation': 0,
                'response_size': 0
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