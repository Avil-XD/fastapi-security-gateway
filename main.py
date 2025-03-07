"""
Simple System Monitoring Gateway
-------------------------------
A lightweight API gateway that provides system metrics and monitoring capabilities.

Endpoints:
- GET /: Basic system status
- GET /health: Detailed system health metrics
- GET /metrics: Export system metrics as JSON
- GET /dashboard: Web interface for monitoring

Author: Your Name
Version: 1.0.0
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import psutil
import time
import datetime

# Initialize FastAPI
app = FastAPI(
    title="System Monitor",
    description="Simple system monitoring gateway",
    version="1.0.0"
)

# Serve static files (dashboard)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Store startup time
STARTUP_TIME = time.time()

def format_bytes(bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024

def format_number(n):
    """Format large numbers with K, M suffix"""
    if n < 1000:
        return str(n)
    elif n < 1000000:
        return f"{n/1000:.1f}K"
    else:
        return f"{n/1000000:.1f}M"

@app.get("/")
async def root():
    """Root endpoint - Basic system status"""
    return {
        "status": "operational",
        "uptime": str(datetime.timedelta(seconds=int(time.time() - STARTUP_TIME)))
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "status": "healthy" if cpu < 80 and memory.percent < 80 else "warning",
        "metrics": {
            "cpu_usage": f"{cpu}%",
            "memory_usage": f"{memory.percent}%",
            "disk_usage": f"{disk.percent}%",
            "memory_available": format_bytes(memory.available)
        }
    }

@app.get("/metrics")
async def metrics():
    """Export detailed system metrics"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    network = psutil.net_io_counters()
    
    report = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_status": {
            "health": "healthy" if cpu < 80 and memory.percent < 80 else "warning",
            "summary": "All systems operating normally" if cpu < 80 and memory.percent < 80 
                      else "High resource usage detected"
        },
        "resources": {
            "cpu": {
                "usage": f"{cpu}%",
                "cores": psutil.cpu_count(),
                "frequency_mhz": f"{psutil.cpu_freq().current:.0f}" if psutil.cpu_freq() else "N/A"
            },
            "memory": {
                "total": format_bytes(memory.total),
                "available": format_bytes(memory.available),
                "used": format_bytes(memory.used),
                "usage": f"{memory.percent}%"
            },
            "disk": {
                "total": format_bytes(disk.total),
                "free": format_bytes(disk.free),
                "used": format_bytes(disk.used),
                "usage": f"{disk.percent}%"
            },
            "network": {
                "bytes_sent": format_bytes(network.bytes_sent),
                "bytes_received": format_bytes(network.bytes_recv),
                "packets_sent": format_number(network.packets_sent),
                "packets_received": format_number(network.packets_recv)
            }
        }
    }
    
    return JSONResponse(
        content=report,
        headers={
            "Content-Disposition": 
                f"attachment; filename=metrics-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
            "Content-Type": "application/json"
        }
    )

@app.get("/dashboard")
async def dashboard():
    """Web Dashboard"""
    return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)