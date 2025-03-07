from sklearn.ensemble import IsolationForest
import numpy as np
import time
from typing import List, Dict, Any

class APIAnalyzer:
    """Analyzer for detecting API request anomalies using machine learning"""
    def __init__(self, policy_path='config/security_policies.yaml'):
        self.models = {}
        self.policy_path = policy_path
        self.baseline_established = False
        self.metrics_window = []
        self.total_requests = 0
        self.blocked_requests = 0
        self.threats_detected = []
        self.request_timestamps = []
        self._initialize_models()
        self.start_time = time.time()

    def get_total_requests(self):
        """Get total number of requests processed"""
        return self.total_requests

    def get_blocked_requests(self):
        """Get number of requests blocked"""
        return self.blocked_requests

    def get_threat_count(self):
        """Get total number of threats detected"""
        return len(self.threats_detected)

    def get_recent_threats(self, count=5):
        """Get most recent threats with details"""
        return self.threats_detected[-count:]

    def get_current_request_rate(self):
        """Calculate current requests per second"""
        now = time.time()
        # Keep only requests from last minute
        self.request_timestamps = [ts for ts in self.request_timestamps 
                                 if now - ts <= 60]
        return len(self.request_timestamps) / 60 if self.request_timestamps else 0

    def _initialize_models(self):
        """Initialize ML models"""
        try:
            self.models = {
                'request_frequency': IsolationForest(contamination=0.01, random_state=42),
                'parameter_variation': IsolationForest(contamination=0.01, random_state=42),
                'response_size': IsolationForest(contamination=0.01, random_state=42)
            }
            # Initialize models with dummy data
            for model in self.models.values():
                model.fit([[0]])
        except Exception as e:
            print(f"Error initializing models: {e}")
            # Fallback to simple threshold-based detection
            self.models = None

    def analyze_request(self, request_data: Dict[str, Any]) -> bool:
        """Analyze request for anomalies"""
        try:
            self.total_requests += 1
            self.request_timestamps.append(time.time())

            if not isinstance(request_data, dict):
                self._record_threat("validation_error", "Invalid request format", "high")
                self.blocked_requests += 1
                return False

            # Extract features
            features = self._extract_features(request_data)
            
            # Detect anomalies
            if self.models:
                predictions = {
                    name: model.predict([features[name]])[0]
                    for name, model in self.models.items()
                }
                
                if -1 in predictions.values():
                    self._record_threat(
                        "anomaly_detected",
                        f"Anomalous behavior detected: {predictions}",
                        "medium"
                    )
                    self.blocked_requests += 1
                    return False

            return True

        except Exception as e:
            print(f"Error analyzing request: {e}")
            return True  # Fail open on errors

    def _extract_features(self, request_data: Dict[str, Any]) -> Dict[str, float]:
        """Extract numerical features from request data"""
        try:
            # Basic feature extraction
            return {
                'request_frequency': self.get_current_request_rate(),
                'parameter_variation': len(request_data.get('query_params', {})),
                'response_size': len(str(request_data))
            }
        except Exception as e:
            print(f"Error extracting features: {e}")
            return {'request_frequency': 0, 'parameter_variation': 0, 'response_size': 0}

    def _record_threat(self, threat_type: str, details: str, severity: str):
        """Record detected threat"""
        self.threats_detected.append({
            'timestamp': time.time(),
            'type': threat_type,
            'details': details,
            'severity': severity
        })
        
        # Keep only last 1000 threats
        if len(self.threats_detected) > 1000:
            self.threats_detected = self.threats_detected[-1000:]