@echo off
echo Setting up FastAPI Security Gateway...

:: Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run the server
echo Starting server...
echo Dashboard will be available at: http://localhost:8000/dashboard
python main.py