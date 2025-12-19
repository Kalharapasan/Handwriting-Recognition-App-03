# Quick Start Guide - Handwriting Recognition FastAPI

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Initialize Application
```bash
# Run the startup script (handles all initialization)
python server.py
```

The server will automatically:
- ✓ Check all dependencies
- ✓ Create necessary directories
- ✓ Initialize the database
- ✓ Start the web server

### Step 3: Access the Application
Open your browser and go to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📝 What You Can Do

### 1. Draw and Recognize Digits
1. Go to the "Draw & Predict" tab
2. Draw a digit (0-9) on the canvas
3. Click "Predict" to see the result
4. View confidence scores for all digits

### 2. Upload Images
1. Go to the "Upload Image" tab
2. Drag and drop an image or click to browse
3. Get instant prediction results

### 3. View Analytics
1. Go to the "Analytics" tab
2. See prediction history
3. View system statistics

### 4. Train Custom Model
1. Go to the "Model Training" tab
2. Configure training parameters
3. Click "Start Training"
4. Wait for training to complete

## 🔧 Configuration

### Basic Configuration
Edit `config.py` to change:
- Image dimensions
- Batch size
- Training epochs
- File size limits

### Environment Variables
Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
# Edit .env with your settings
```

## 📊 Using the API

### Make a Prediction (Python)
```python
import requests
import base64

# Read and encode image
with open('digit.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

# Make prediction
response = requests.post(
    'http://localhost:8000/api/predict',
    json={
        'image_data': f'data:image/png;base64,{image_data}',
        'user_id': 1
    }
)

result = response.json()
print(f"Predicted digit: {result['predicted_digit']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### Make a Prediction (cURL)
```bash
# Upload file
curl -X POST "http://localhost:8000/api/predict-upload" \
  -F "file=@digit.png" \
  -F "user_id=1"

# Get analytics
curl "http://localhost:8000/api/analytics/system"
```

### Make a Prediction (JavaScript)
```javascript
// From canvas
const canvas = document.getElementById('canvas');
const imageData = canvas.toDataURL('image/png');

fetch('http://localhost:8000/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        image_data: imageData,
        user_id: 1
    })
})
.then(response => response.json())
.then(data => {
    console.log('Predicted:', data.predicted_digit);
    console.log('Confidence:', data.confidence);
});
```

## 🐳 Docker Quick Start

### Using Docker
```bash
# Build and run
docker build -t handwriting-recognition .
docker run -p 8000:8000 handwriting-recognition
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🎯 Common Tasks

### Train a New Model
```bash
# Using the web interface
# Go to http://localhost:8000 → Model Training tab

# Using the API
curl -X POST "http://localhost:8000/api/train" \
  -H "Content-Type: application/json" \
  -d '{
    "use_hyperparameter_tuning": false,
    "use_augmentation": true,
    "epochs": 50,
    "batch_size": 32
  }'

# Using Python directly
python model_trainer.py
```

### Export User Data
```bash
# Export as JSON
curl "http://localhost:8000/api/export/user/1?format=json"

# Export as CSV
curl "http://localhost:8000/api/export/user/1?format=csv"
```

### Check System Status
```bash
# Health check
curl "http://localhost:8000/health"

# Model status
curl "http://localhost:8000/api/model/status"

# System analytics
curl "http://localhost:8000/api/analytics/system"
```

## 🔍 Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Use different port
python server.py --port 8001
```

### Dependencies Missing
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt
```

### Model Not Found
```bash
# Train a new model
python model_trainer.py

# Or use the web interface:
# http://localhost:8000 → Model Training
```

### Database Errors
```bash
# Reset database
rm handwriting_db.sqlite

# Restart server (database will be recreated)
python start_server.py
```

## 📚 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the full README**: Check README_FASTAPI.md
3. **Customize settings**: Edit config.py and .env
4. **Train your model**: Use the training interface
5. **Integrate with your app**: Use the REST API

## 💡 Tips

- **Better Accuracy**: Train with data augmentation enabled
- **Faster Predictions**: Use a pre-trained model
- **Monitor Performance**: Check the analytics dashboard
- **Batch Processing**: Use the batch endpoint for multiple images
- **Custom Data**: Add your own training data to improve results

## 🆘 Getting Help

- Check the logs: `logs/app.log`
- View API docs: http://localhost:8000/docs
- Read README: `README_FASTAPI.md`
- Check issues on GitHub

## 🎉 You're Ready!

The application is now running at http://localhost:8000

Start by:
1. Drawing a digit on the canvas
2. Uploading an image
3. Exploring the analytics
4. Training a custom model

Have fun! 🚀
