# Advanced Handwriting Recognition System - FastAPI Edition

## 🚀 Overview

A modern, production-ready handwriting recognition system built with FastAPI, featuring real-time digit recognition, advanced analytics, and a beautiful web interface.

## ✨ Features

### Core Functionality
- **Real-time Drawing Recognition**: Draw digits directly in the browser
- **Image Upload Support**: Upload and process handwritten digit images
- **Batch Processing**: Process multiple images simultaneously
- **Advanced Preprocessing**: Multiple enhancement levels for optimal recognition

### Analytics & Monitoring
- **System Dashboard**: Real-time statistics and performance metrics
- **User Analytics**: Track individual user performance and history
- **Prediction History**: Complete audit trail of all predictions
- **Confidence Tracking**: Detailed confidence scores for each prediction

### Model Management
- **Model Training**: Train custom models with configurable parameters
- **Hyperparameter Tuning**: Automated hyperparameter optimization
- **Data Augmentation**: Built-in data augmentation for better performance
- **Model Versioning**: Track different model versions

### Advanced Features
- **User Feedback System**: Collect and analyze user feedback
- **Export Functionality**: Export data in CSV and JSON formats
- **Multi-user Support**: Handle multiple users with separate tracking
- **RESTful API**: Complete API for integration with other systems

## 📋 Requirements

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended for training)
- 2GB free disk space

### Dependencies
All dependencies are listed in `requirements_fastapi.txt`

## 🛠️ Installation

### 1. Clone or Download the Project
```bash
# If using git
git clone https://github.com/Kalharapasan/Handwriting-Recognition-App-03.git
cd Handwriting-Recognition-App-03

# Or extract the uploaded files to a directory
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
# The database will be automatically created on first run
# Or manually create it:
python -c "from database import db_manager; print('Database initialized')"
```

### 5. Train Initial Model (Optional)
```bash
# Train a model before starting the server
python model_trainer.py
```

## 🚀 Running the Application

### Development Mode
```bash
python fastapi_app.py
```

The application will start on `http://localhost:8000`

### Production Mode with Gunicorn
```bash
gunicorn fastapi_app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Uvicorn Directly
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 API Documentation

Once the server is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### Prediction Endpoints

**POST /api/predict**
Predict digit from base64 encoded image
```json
{
  "image_data": "data:image/png;base64,...",
  "user_id": 1,
  "enhancement_level": 1.0
}
```

**POST /api/predict-upload**
Predict digit from uploaded file
```bash
curl -X POST "http://localhost:8000/api/predict-upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@digit.png" \
  -F "user_id=1"
```

**POST /api/predict-batch**
Process multiple images at once
```bash
curl -X POST "http://localhost:8000/api/predict-batch" \
  -F "files=@digit1.png" \
  -F "files=@digit2.png" \
  -F "user_id=1"
```

#### Analytics Endpoints

**GET /api/analytics/system**
Get system-wide analytics

**GET /api/analytics/user/{user_id}**
Get user-specific statistics

**GET /api/analytics/predictions**
Get prediction history

#### User Management

**POST /api/users**
Create a new user
```json
{
  "username": "john_doe",
  "email": "john@example.com"
}
```

**GET /api/users/{user_id}**
Get user information

#### Feedback

**POST /api/feedback**
Submit feedback for a prediction
```json
{
  "prediction_id": 1,
  "user_id": 1,
  "actual_digit": 5,
  "confidence_rating": 4,
  "comments": "Good prediction"
}
```

#### Model Training

**POST /api/train**
Start model training
```json
{
  "use_hyperparameter_tuning": false,
  "use_augmentation": true,
  "epochs": 50,
  "batch_size": 32
}
```

**GET /api/model/status**
Check model loading status

#### Export

**GET /api/export/user/{user_id}?format=json**
Export user data (json or csv)

## 🎨 Web Interface

### Dashboard
- System statistics overview
- Real-time performance metrics
- Quick action buttons

### Draw & Predict
- Interactive canvas for drawing digits
- Real-time prediction
- Confidence visualization
- All class probabilities display

### Upload Image
- Drag-and-drop file upload
- Image preview
- Instant prediction results

### Analytics
- Detailed prediction history
- Performance trends
- User statistics

### Model Training
- Configure training parameters
- Start training jobs
- Monitor training progress

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model Settings
IMG_HEIGHT = 28
IMG_WIDTH = 28
BATCH_SIZE = 32
EPOCHS = 100

# Paths
MODEL_PATH = 'models/handwriting_model.h5'
UPLOAD_FOLDER = 'data/uploaded'

# Application Settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
```

## 📁 Project Structure

```
handwriting-recognition-fastapi/
├── fastapi_app.py          # Main FastAPI application
├── config.py               # Configuration settings
├── database.py             # Database models and manager
├── model_trainer.py        # Model training utilities
├── utils.py                # Image processing and utilities
├── requirements.txt # Dependencies
├── templates/
│   └── index.html         # Web interface
├── models/                 # Trained models
├── data/
│   ├── uploaded/          # Uploaded files
│   ├── custom_dataset/    # Custom training data
│   └── exports/           # Exported data
└── static/                # Static files
```

## 🔐 Security Considerations

### Production Deployment
1. **Enable HTTPS**: Always use HTTPS in production
2. **Authentication**: Implement proper authentication (JWT, OAuth2)
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Input Validation**: All inputs are validated via Pydantic models
5. **File Upload Security**: Validate file types and sizes

### Example: Adding Authentication
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Implement your token verification logic
    if not verify_jwt_token(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

## 🚀 Performance Optimization

### Async Operations
The FastAPI application supports async operations. For CPU-intensive tasks like model training, consider:

```python
from fastapi import BackgroundTasks

@app.post("/api/train-async")
async def train_async(config: TrainingConfig, background_tasks: BackgroundTasks):
    background_tasks.add_task(train_model_background, config)
    return {"message": "Training started in background"}
```

### Caching
Add Redis caching for frequently accessed data:

```python
import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
```

### Load Balancing
For production, use multiple workers:

```bash
gunicorn fastapi_app:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

## 🐳 Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_fastapi.txt .
RUN pip install --no-cache-dir -r requirements_fastapi.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - DATABASE_URL=sqlite:///data/handwriting_db.sqlite
```

Run with:
```bash
docker-compose up -d
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/
```

### Example Test
```python
from fastapi.testclient import TestClient
from fastapi_app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    # Test prediction endpoint
    pass
```

## 📊 Monitoring & Logging

### Logging Configuration
Logs are configured in the application. View logs:

```bash
# Follow logs in real-time
tail -f logs/app.log
```

### Health Monitoring
Monitor application health:
```bash
curl http://localhost:8000/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 [License](./LICENSE.md): Proprietary – Permission Required

## 🆘 Troubleshooting

### Common Issues

**Model Not Loading**
```bash
# Train a new model
python model_trainer.py
```

**Database Errors**
```bash
# Reset database
rm handwriting_db.sqlite
python -c "from database import db_manager; print('Database reset')"
```

**Port Already in Use**
```bash
# Use a different port
uvicorn fastapi_app:app --port 8001
```

**Memory Issues During Training**
```python
# Reduce batch size in config.py
BATCH_SIZE = 16  # Instead of 32
```

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the logs for error messages

## 🎯 Roadmap

- [ ] Add support for multiple languages
- [ ] Implement advanced authentication
- [ ] Add WebSocket support for real-time updates
- [ ] Mobile app integration
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] Advanced model architectures (Transformer-based)
- [ ] A/B testing framework for models

## 🙏 Acknowledgments

- TensorFlow team for the ML framework
- FastAPI team for the excellent web framework
- MNIST dataset creators
- All contributors and users

---

Made with ❤️ using FastAPI and TensorFlow
