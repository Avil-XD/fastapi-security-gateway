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

# Test components individually
def test_fastapi():
    print("\n=== Testing FastAPI Setup ===")
    app = test_component("Create FastAPI app", lambda: FastAPI())
    return app

def test_security_policies():
    print("\n=== Testing Security Policies ===")
    def load_policies():
        config_path = Path("config/security_policies.yaml")
        print(f"Config path exists: {config_path.exists()}")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    return test_component("Load security policies", load_policies)

def test_controller():
    print("\n=== Testing Controller ===")
    def import_controller():
        from self_healing.controller import SelfHealingController
        return SelfHealingController
    return test_component("Import controller", import_controller)

def test_analyzer():
    print("\n=== Testing Analyzer ===")
    def import_analyzer():
        from threat_detection.anomaly_detection import APIAnalyzer
        return APIAnalyzer
    return test_component("Import analyzer", import_analyzer)

def main():
    print("Starting component tests...")
    
    # Test each component
    app = test_fastapi()
    if not app:
        return
    
    policies = test_security_policies()
    if not policies:
        return
        
    ControllerClass = test_controller()
    if not ControllerClass:
        return
        
    AnalyzerClass = test_analyzer()
    if not AnalyzerClass:
        return
    
    # Try instantiating components
    print("\n=== Testing Component Initialization ===")
    
    try:
        print("\nCreating PolicyLoader...")
        class PolicyLoader:
            def __init__(self, policies):
                self.policies = policies
            def get_policies(self, section):
                return self.policies.get(section, {})
        
        policy_loader = PolicyLoader(policies)
        print("PolicyLoader created successfully")
        
        print("\nInitializing SelfHealingController...")
        controller = ControllerClass(policy_loader)
        print("SelfHealingController initialized successfully")
        
        print("\nInitializing APIAnalyzer...")
        analyzer = AnalyzerClass()
        print("APIAnalyzer initialized successfully")
        
        print("\nAll components initialized successfully!")
        
    except Exception as e:
        print(f"\nError during component initialization:")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        return

    # If we get here, everything worked
    print("\nAll tests passed successfully!")
    
if __name__ == "__main__":
    main()