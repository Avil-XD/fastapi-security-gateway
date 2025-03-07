# System Monitoring Gateway

A lightweight system monitoring gateway built with FastAPI that provides real-time system metrics and a web dashboard.

## Features

- Real-time system metrics monitoring (CPU, Memory, Disk)
- Web-based dashboard for easy visualization
- Simple REST API endpoints
- Metric export capabilities in JSON format
- Zero-configuration setup

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8080
   ```

3. **Access the Dashboard**
   - Open http://127.0.0.1:8080/dashboard in your browser

## API Endpoints

### GET /
Basic system status and uptime information
```bash
curl http://127.0.0.1:8080/
```

### GET /health
Detailed system health metrics
```bash
curl http://127.0.0.1:8080/health
```

### GET /metrics
Export complete system metrics report
```bash
curl http://127.0.0.1:8080/metrics -o metrics.json
```

### GET /dashboard
Web-based monitoring dashboard

## System Requirements

- Python 3.8 or higher
- Required packages:
  - fastapi
  - uvicorn
  - psutil

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run with reload for development:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8080
   ```

## Project Structure

```
.
├── main.py              # Main application file
├── static/             # Static files
│   ├── dashboard.html  # Web dashboard
│   └── index.html      # Landing page
├── requirements.txt    # Project dependencies
└── README.md          # Documentation
```

## License

MIT License - Feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
