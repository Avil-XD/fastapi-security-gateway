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

### Easy Run

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
# Make script executable (first time only)
chmod +x run.sh

# Run the script
./run.sh
```

The script will automatically:
1. Create a Python virtual environment
2. Install required dependencies
3. Start the server
4. Display the dashboard URL

Once running, open your browser to: `http://localhost:8000/dashboard`

### Manual Setup (Alternative)

If you prefer to run commands manually:

1. Create and activate virtual environment:
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start server:
```bash
python main.py
```

### Available Endpoints
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