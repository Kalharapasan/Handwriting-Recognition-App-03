# How to Run the Handwriting Recognition Application

## Quick Start (Recommended)

### Option 1: Using the Batch File (Windows - Easiest)

1. **Simply double-click** `run_windows.bat` in the project folder
   - OR open PowerShell/Command Prompt in the project folder and run:
   ```cmd
   run_windows.bat
   ```

2. **Wait** for the server to start (takes 10-20 seconds due to TensorFlow loading)

3. **Open your browser** and go to:
   - http://localhost:8000
   - OR http://127.0.0.1:8000

### Option 2: Manual Start (PowerShell)

1. **Open PowerShell** in the project directory

2. **Activate the virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. **Run the application:**
   ```powershell
   python fastapi_app.py
   ```

4. **Wait for startup** - You should see:
   ```
   INFO:fastapi_app:Starting Handwriting Recognition API...
   INFO:fastapi_app:Model loaded successfully: v2.0
   INFO:fastapi_app:API ready to accept requests
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   ```

5. **Open browser** at http://localhost:8000

### Option 3: Using Uvicorn Directly

```powershell
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1

# Run with uvicorn
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
```

## Troubleshooting

### Problem: "Dashboard loading..." and nothing appears

**Solution:**
- Make sure the server is fully started (wait 15-20 seconds)
- Check that `templates/index.html` exists
- Open browser console (F12) and check for errors
- Try refreshing the page (Ctrl+F5)

### Problem: Port 8000 already in use

**Solution:**
```powershell
# Check what's using port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill the process if needed
Stop-Process -Id <ProcessId> -Force

# Or change the port in fastapi_app.py (last line)
uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8001, reload=False)
```

### Problem: TensorFlow import errors or KeyboardInterrupt during startup

**Solution:**
- This is normal during the initial import phase
- Just **wait patiently** - TensorFlow takes time to load
- Don't interrupt the process during startup
- If it fails, try running again

### Problem: Virtual environment not found

**Solution:**
```powershell
# Create a new virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Features Available

Once the application is running, you can:

1. **Draw handwritten digits** on the canvas
2. **Upload images** of handwritten digits
3. **Get AI predictions** with confidence scores
4. **View analytics** and prediction history
5. **Train custom models** (advanced)
6. **Export data** for analysis

## Stopping the Server

- Press **CTRL+C** in the terminal/PowerShell window
- Wait a few seconds for graceful shutdown

## API Documentation

While the server is running, visit:
- **Interactive API docs:** http://localhost:8000/docs
- **Alternative API docs:** http://localhost:8000/redoc

## System Requirements

- **Python:** 3.8 or higher (3.10+ recommended)
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 2GB for dependencies
- **OS:** Windows 10/11

## Performance Notes

- **First startup:** Takes 15-30 seconds (TensorFlow initialization)
- **Subsequent requests:** Fast (model is already loaded)
- **Auto-reload disabled:** For stability with TensorFlow
  - You must restart the server manually after code changes

## Need Help?

1. Check the logs in the terminal for error messages
2. Review `PROJECT_SUMMARY.md` for project details
3. Check `QUICKSTART.md` for more information
4. Verify all dependencies are installed: `pip list`
