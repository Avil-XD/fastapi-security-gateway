# FastAPI Security Gateway

🛡️ A lightweight, production-ready API security gateway built with FastAPI. Protect your APIs with zero-trust security, AI-driven anomaly detection, and self-healing capabilities.

## 🌟 Features

- 🔒 **Zero-Trust Security**
  - Request validation & sanitization
  - JWT authentication
  - Rate limiting
  - GraphQL query control

- 🤖 **AI-Driven Protection**
  - ML-based anomaly detection
  - Behavioral analysis
  - Real-time threat detection

- 🔄 **Self-Healing**
  - Circuit breaker pattern
  - Automatic rate limiting
  - Schema validation

## 🚀 Quick Start

1. **Install**
```bash
# Clone repository
git clone https://github.com/Avil-XD/fastapi-security-gateway.git
cd fastapi-security-gateway

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

2. **Configure**
```bash
# Copy example config
cp config/security_policies.yaml.example config/security_policies.yaml

# Set JWT secret
export JWT_SECRET="your-secret-key"  # Linux/Mac
# OR
set JWT_SECRET="your-secret-key"     # Windows
```

3. **Run**
```bash
# Development mode
python debug_fastapi.py

# Production mode
uvicorn main:app --host 127.0.0.1 --port 8000
```

4. **Test**
```bash
# Run test suite
python test_fastapi.py

# Or try minimal example
python minimal.py
```

## 📚 Documentation

Visit http://localhost:8000/docs after starting the server for interactive API documentation.

### Core Components

- `main.py` - Main application & API endpoints
- `threat_detection/` - Anomaly detection system
- `self_healing/` - Automatic mitigation strategies
- `config/` - Security policies & configuration

### Common Use Cases

1. **API Protection**
```python
from fastapi import FastAPI, Depends
from main import security_gateway

app = FastAPI()

@app.get("/api/protected")
async def protected_endpoint(security=Depends(security_gateway)):
    return {"message": "Protected data"}
```

2. **Custom Security Rules**
```yaml
# config/security_policies.yaml
policies:
  - name: rate_limit
    rules:
      - max_requests_per_minute: 1000
        action: throttle
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python test_fastapi.py`)
5. Commit changes (`git commit -am 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

1. Install development requirements:
```bash
pip install -r requirements.txt
```

2. Use the debug mode for development:
```bash
python debug_fastapi.py
```

3. Follow code style:
- Use type hints
- Add docstrings for functions
- Keep code modular
- Add tests for new features

## 📝 License

This project is MIT licensed - see [LICENSE](LICENSE) for details.

## ⭐ Support

Give a ⭐️ if this project helped you!

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Security Best Practices](https://owasp.org/www-project-api-security/)
- [Rate Limiting Explained](https://en.wikipedia.org/wiki/Rate_limiting)
