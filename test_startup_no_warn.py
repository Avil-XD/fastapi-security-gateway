import warnings
import numpy as np

# Suppress all numpy warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=UserWarning)

from fastapi import FastAPI
from pathlib import Path
import yaml
import sys
import traceback

def test_component(name, func):
    print(f"\nTesting: {name}")
    try:
        result = func()
        print(f"Success: {name}")
        return result
    except Exception as e:
        print(f"Error in {name}:")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        return None

def main():
    print("Starting tests with numpy warnings suppressed...")
    
    print("\n=== Testing Components ===")
    
    app = test_component("Create FastAPI app", lambda: FastAPI())
    if not app:
        return
    
    def load_policies():
        config_path = Path("config/security_policies.yaml")
        print(f"Config path exists: {config_path.exists()}")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    
    policies = test_component("Load security policies", load_policies)
    if not policies:
        return
    
    def create_policy_loader():
        class PolicyLoader:
            def __init__(self, policies):
                self.policies = policies
            def get_policies(self, section):
                return self.policies.get(section, {})
        return PolicyLoader(policies)
    
    policy_loader = test_component("Create PolicyLoader", create_policy_loader)
    if not policy_loader:
        return
    
    def import_controller():
        from self_healing.controller import SelfHealingController
        return SelfHealingController(policy_loader)
    
    controller = test_component("Initialize SelfHealingController", import_controller)
    if not controller:
        return
    
    def import_analyzer():
        from threat_detection.anomaly_detection import APIAnalyzer
        analyzer = APIAnalyzer()
        # Test if analyzer works
        test_data = {"test": "data"}
        result = analyzer.analyze_request(test_data)
        print(f"Analyzer test result: {result}")
        return analyzer
    
    analyzer = test_component("Initialize APIAnalyzer", import_analyzer)
    if not analyzer:
        return
    
    print("\nAll components initialized successfully!")

if __name__ == "__main__":
    main()