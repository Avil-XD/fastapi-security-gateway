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

## Quick Start

1. **Setup Python Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Run the Server**
```bash
# Option 1: Using python directly
python main.py

# Option 2: Using uvicorn with auto-reload (recommended for development)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **Access the Dashboard**
   - Open your browser and go to: `http://localhost:8000/dashboard`
   - The dashboard will automatically update every 2 seconds with real-time metrics

4. **Available Endpoints**
   - `http://localhost:8000/` - Basic system status
   - `http://localhost:8000/health` - Detailed system health metrics
   - `http://localhost:8000/metrics` - Download detailed metrics report
   - `http://localhost:8000/dashboard` - Web monitoring interface

## Configuration (Optional)

1. Configure security policies in `config/security_policies.yaml`
2. Adjust threat detection settings in `threat_detection/anomaly_detection.py`
3. Set environment variables in a `.env` file (see `.env.example` for options)

## Development

The project uses FastAPI with the following structure:
- `main.py` - Core FastAPI application and API endpoints
- `static/` - Frontend dashboard files (HTML, CSS)
- `security/` - Security and authentication logic
- `threat_detection/` - Threat detection algorithms
- `self_healing/` - Automatic recovery mechanisms

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