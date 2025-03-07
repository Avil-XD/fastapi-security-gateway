# FastAPI Security Gateway

A robust security gateway built with FastAPI that provides real-time monitoring, threat detection, and protection for your APIs.

## Features

- Real-time traffic monitoring
- Security event tracking
- Threat detection and blocking
- System health monitoring
- Performance metrics tracking
- Self-healing capabilities
- Downloadable security reports

## Requirements

- Python 3.8+
- FastAPI
- Additional dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/fastapi-security-gateway.git
cd fastapi-security-gateway
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration

1. Configure security policies in `config/security_policies.yaml`
2. (Optional) Adjust threat detection settings in `threat_detection/anomaly_detection.py`
3. Environment variables can be set in a `.env` file (see `.env.example` for available options)

## Usage

Start the server:
```bash
uvicorn main:app --reload
```

Access the monitoring dashboard at `http://localhost:8000/static/index.html`

## Project Structure

```
fastapi-security-gateway/
├── config/
│   └── security_policies.yaml    # Security configuration
├── security/
│   └── auth.py                  # Authentication handlers
├── self_healing/
│   └── controller.py            # Self-healing mechanisms
├── static/
│   ├── index.html              # Main monitoring dashboard
│   └── styles.css              # Dashboard styles
├── threat_detection/
│   └── anomaly_detection.py    # Threat detection logic
├── main.py                     # FastAPI application
├── requirements.txt            # Project dependencies
└── .gitignore                 # Git ignore rules
```

## API Endpoints

- `/health` - Get system health and security metrics
- `/metrics/export` - Download detailed security report

## Security Features

1. **Real-time Monitoring**
   - Request rate tracking
   - Threat detection
   - System resource usage

2. **Threat Protection**
   - Rate limiting
   - IP blocking
   - Request validation
   - Anomaly detection

3. **Self-healing**
   - Automatic threat mitigation
   - Performance optimization
   - Resource management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.