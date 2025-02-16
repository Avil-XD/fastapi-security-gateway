# API Security Gateway

A comprehensive API security solution that provides zero-trust security, anomaly detection, and self-healing capabilities for modern APIs.

## Features

- **Zero-Trust Security**
  - Request validation and sanitization
  - JWT token validation
  - Rate limiting and burst control
  - GraphQL depth and complexity control

- **AI-Driven Anomaly Detection**
  - Machine learning-based request analysis
  - Behavioral baseline modeling
  - Real-time anomaly detection
  - Configurable thresholds and metrics

- **Self-Healing Capabilities**
  - Circuit breaker pattern
  - Automatic rate limiting
  - Schema validation
  - Adaptive security measures

- **Monitoring and Analytics**
  - Real-time metrics dashboard
  - Detailed logging
  - Performance analytics
  - Security incident tracking

## Requirements

- Python 3.10+
- Dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Avil-XD/fastapi-security-gateway.git
cd fastapi-security-gateway
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # For Linux/Mac
# OR
.venv\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure security policies:
- Copy config/security_policies.yaml.example to config/security_policies.yaml
- Update the settings according to your needs
- Set up your JWT secret in the environment variable JWT_SECRET

## Usage

1. Start the server:
```bash
# For development with debug mode:
python debug_fastapi.py

# For production:
uvicorn main:app --host 127.0.0.1 --port 8000
```

2. Access the dashboard:
- Open http://localhost:8000/dashboard in your browser
- View real-time metrics and security analytics

3. API Endpoints:
- GET / - Basic system information
- GET /health - Detailed health check
- GET /metrics - System metrics and analytics
- POST /api/* - Protected API endpoints with security features
- GET /docs - Interactive API documentation
- GET /settings - View current security settings
- POST /settings - Update security settings

## Testing

The project includes several test utilities:

1. Basic API Tests:
```bash
python test_fastapi.py
```

2. Startup Tests:
```bash
python test_startup.py  # With all warnings
python test_startup_no_warn.py  # Without warnings
```

3. Minimal Example:
```bash
python minimal.py  # Runs a minimal version of the API for testing
```

## Configuration

The system is configured through security_policies.yaml with the following sections:

1. **GraphQL Control**
   - max_depth: Maximum query depth
   - query_complexity: Maximum query complexity

2. **Parameter Sanitization**
   - Custom patterns and rules for request sanitization
   - Field-specific sanitization rules

3. **Behavioral Baseline**
   - Machine learning parameters
   - Anomaly detection thresholds
   - Training window configuration

4. **Self-Healing**
   - Circuit breaker thresholds
   - Rate limiting rules
   - Schema validation settings

## Development

To extend or modify the system:

1. Anomaly Detection:
   - Modify threat_detection/anomaly_detection.py
   - Update behavioral baselines in config/

2. Self-Healing:
   - Customize self_healing/controller.py
   - Add new healing strategies

3. API Endpoints:
   - Add routes to main.py
   - Implement new security features

4. Testing:
   - Add new test cases to test_fastapi.py
   - Use debug_fastapi.py for development testing
   - Create minimal examples in minimal.py

## Production Deployment

For production deployment:

1. Security Considerations:
   - Set proper rate limits
   - Configure strict CORS settings
   - Use secure JWT settings
   - Enable HTTPS

2. Performance Optimization:
   - Adjust behavioral baseline parameters
   - Fine-tune anomaly detection thresholds
   - Configure appropriate resource limits

3. Monitoring Setup:
   - Configure logging
   - Set up alerts
   - Monitor system metrics

## License

This project is licensed under the MIT License - see the LICENSE file for details.
