# 🚀 How to Run - Step by Step Guide

## Prerequisites
- Python 3.8 or higher installed
- Internet connection (for installing packages)

---

## Method 1: Quick Start (Easiest)

### Step 1: Extract Files
Extract all the files from `handwriting-fastapi` folder to your computer.

### Step 2: Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac/Linux**: Open Terminal application

### Step 3: Navigate to the Folder
```bash
cd path/to/handwriting-fastapi
```
Replace `path/to/handwriting-fastapi` with your actual folder path.

### Step 4: Install Dependencies
```bash
pip install -r requirements_fastapi.txt
```
Wait for all packages to install (takes 2-5 minutes).

### Step 5: Run the Server
```bash
python start_server.py
```

### Step 6: Open Your Browser
Go to: **http://localhost:8000**

✅ **Done! The application is running!**

---

## Method 2: Using Install Script (Recommended)

### On Mac/Linux:
```bash
# Make script executable
chmod +x install.sh

# Run installation
./install.sh

# Start server
python start_server.py
```

### On Windows:
```bash
# Install dependencies
pip install -r requirements_fastapi.txt

# Start server
python start_server.py
```

---

## Method 3: Using Docker (Advanced)

### If you have Docker installed:
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8000
```

---

## 🎯 What to Do After Starting

### 1. Access the Web Interface
Open your browser and go to: **http://localhost:8000**

### 2. Try Drawing
- Click on "✏️ Draw & Predict" tab
- Draw a digit (0-9) on the canvas
- Click "🔍 Predict" button
- See the result!

### 3. Upload an Image
- Click on "📁 Upload Image" tab
- Drag and drop an image with a handwritten digit
- Or click "Choose File" to browse
- Get instant prediction!

### 4. View API Documentation
Go to: **http://localhost:8000/docs**

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Command not found: python"
**Solution:** Try `python3` instead of `python`
```bash
python3 start_server.py
```

### Issue 2: "Port 8000 already in use"
**Solution:** Use a different port
```bash
python start_server.py --port 8001
```
Then access: http://localhost:8001

### Issue 3: "No module named 'fastapi'"
**Solution:** Install dependencies again
```bash
pip install --upgrade pip
pip install -r requirements_fastapi.txt
```

### Issue 4: "Permission denied"
**Solution (Mac/Linux):** 
```bash
chmod +x start_server.py
python start_server.py
```

### Issue 5: Model not found warning
**Solution:** This is normal on first run. You can:
- Use the app without a model (will show error on predictions)
- Train a model through the web interface (Model Training tab)
- Or run: `python model_trainer.py` (takes 10-20 minutes)

---

## 📱 Testing the API

### Using Browser
Just go to: **http://localhost:8000/docs**

### Using cURL (Command Line)
```bash
# Health check
curl http://localhost:8000/health

# System stats
curl http://localhost:8000/api/analytics/system
```

### Using Python
```python
import requests

# Get system status
response = requests.get('http://localhost:8000/health')
print(response.json())
```

---

## 🛑 How to Stop

Press `Ctrl + C` in the terminal where the server is running.

---

## 🔄 How to Restart

Just run again:
```bash
python start_server.py
```

---

## 📊 Project Structure

```
handwriting-fastapi/
├── fastapi_app.py       ← Main application
├── start_server.py      ← Run this to start!
├── requirements_fastapi.txt  ← Dependencies list
├── templates/
│   └── index.html       ← Web interface
├── config.py           ← Settings
├── database.py         ← Database
├── model_trainer.py    ← Model training
└── utils.py            ← Helper functions
```

---

## 🎓 What Each File Does

- **fastapi_app.py** - The main FastAPI server with all API endpoints
- **start_server.py** - Smart startup script (checks everything and starts server)
- **templates/index.html** - The web page you see in browser
- **requirements_fastapi.txt** - List of Python packages needed
- **config.py** - Configuration settings
- **database.py** - Handles saving predictions and user data
- **model_trainer.py** - Trains the AI model
- **utils.py** - Image processing tools

---

## ✨ Quick Command Reference

```bash
# Install everything
pip install -r requirements_fastapi.txt

# Start server
python start_server.py

# Start on different port
python start_server.py --port 8001

# Test the API
python test_api.py

# Train a model
python model_trainer.py
```

---

## 🆘 Still Need Help?

### Check the logs
The server prints detailed information. Look for:
- ✓ Green checkmarks = Good!
- ✗ Red X marks = Problems
- ⚠ Yellow warnings = Minor issues

### Read more documentation
- **QUICKSTART.md** - Quick start guide
- **README_FASTAPI.md** - Detailed documentation
- **PROJECT_SUMMARY.md** - Project overview

### Check if server is running
Open browser and try these:
- http://localhost:8000 (web interface)
- http://localhost:8000/health (health check)
- http://localhost:8000/docs (API documentation)

---

## 🎉 Success Checklist

✅ Installed Python 3.8+
✅ Installed dependencies (`pip install -r requirements_fastapi.txt`)
✅ Started server (`python start_server.py`)
✅ Opened browser (http://localhost:8000)
✅ Saw the web interface
✅ Drew a digit and got prediction!

**You're all set! Enjoy your handwriting recognition system! 🚀**
