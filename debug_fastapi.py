import sys
import site
print("Python Path:")
for path in sys.path:
    print(f"- {path}")

print("\nTrying to locate FastAPI:")
try:
    import fastapi
    print(f"FastAPI location: {fastapi.__file__}")
    print(f"FastAPI version: {fastapi.__version__}")
    print(f"FastAPI package contents: {dir(fastapi)}")
except Exception as e:
    print(f"Error importing FastAPI: {e}")