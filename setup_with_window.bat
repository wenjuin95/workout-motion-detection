@echo off
echo Setting up Python virtual environment...

:: Create virtual environment
python -m venv venv

echo Virtual environment created.

:: Activate virtual environment
call venv\Scripts\activate

echo Installing dependencies...

:: Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Dependencies installed successfully!
echo.
echo To activate the virtual environment in future sessions, run:
echo venv\Scripts\activate
echo.
echo To run the application:
echo python main.py
echo.
echo To deactivate:
echo deactivate

echo To activate:
echo venv\Scripts\activate
