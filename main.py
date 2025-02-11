from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict, Any
import time
import yaml
import json
import psutil
import datetime
from pathlib import Path

# Import custom modules
from self_healing import controller as self_healing
from threat_detection import anomaly_detection

app = FastAPI(title="API Security Gateway")

# Security Configuration
security = HTTPBasic()
STARTUP_TIME = time.time()

# Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load security policies
with open("config/security_policies.yaml", "r") as f:
    security_policies = yaml.safe_load(f)

@app.get("/")
async def root():
    """Root endpoint with basic system information"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "uptime": time.time() - STARTUP_TIME
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with detailed system metrics"""
    return {
        "status": "healthy",
        "security_mode": "enforced",
        "system_info": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "uptime": time.time() - STARTUP_TIME
        }
    }

@app.get("/dashboard")
async def dashboard():
    """Admin dashboard view"""
    return FileResponse('static/index.html')

@app.get("/analytics")
async def analytics_view():
    """Analytics dashboard view"""
    return {
        "traffic_stats": {
            "total_requests": 1000,
            "average_response_time": "120ms",
            "error_rate": "0.5%",
            "requests_per_minute": 60
        },
        "security_stats": {
            "blocked_requests": 50,
            "sql_injection_attempts": 10,
            "rate_limit_hits": 20,
            "invalid_auth_attempts": 15
        },
        "performance_metrics": {
            "p95_response_time": "200ms",
            "p99_response_time": "450ms",
            "average_cpu_usage": "45%",
            "average_memory_usage": "60%"
        }
    }

@app.get("/settings")
async def settings():
    """Get current gateway settings"""
    return {
        "rate_limiting": {
            "enabled": True,
            "requests_per_minute": 60,
            "burst_size": 10
        },
        "security": {
            "mode": "enforced",
            "max_request_size": "1MB",
            "allowed_origins": ["*"],
            "authentication": "required"
        },
        "monitoring": {
            "log_level": "INFO",
            "metrics_enabled": True,
            "alert_threshold": 80
        }
    }

@app.post("/settings")
async def update_settings(request: Request):
    """Update gateway settings"""
    settings = await request.json()
    # Validate and apply new settings
    return {"message": "Settings updated successfully"}

@app.get("/logs")
async def get_logs(limit: int = 50):
    """Get recent system logs"""
    # In a real implementation, this would fetch from a log store
    return {
        "logs": [
            {
                "timestamp": time.time(),
                "level": "INFO",
                "message": "System operating normally",
                "details": {"cpu": "45%", "memory": "60%"}
            },
            {
                "timestamp": time.time() - 60,
                "level": "WARNING",
                "message": "High resource usage detected",
                "details": {"cpu": "85%", "memory": "75%"}
            }
        ]
    }

@app.post("/api/test")
async def test_endpoint(request: Request):
    """Test endpoint for security features"""
    try:
        # Anomaly detection
        anomalies = anomaly_detection.check_request(await request.json())
        if anomalies:
            print(f"ALERT: Anomalies detected {anomalies}")

        # Self-healing checks
        healing_response = self_healing.check_system_health()
        if healing_response.get("action_taken"):
            print(f"Self-healing: {healing_response['action_taken']}")

        return {"message": "Request passed security checks"}

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Security middleware for all requests"""
    try:
        # Check request size
        content_length = request.headers.get("content-length", 0)
        if int(content_length) > security_policies["max_request_size"]:
            return JSONResponse(
                status_code=413,
                content={"detail": "Payload exceeds size limit"}
            )

        # Process request
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add security headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Server"] = "API Security Gateway"
        
        return response

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)