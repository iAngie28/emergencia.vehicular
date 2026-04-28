# VialIA Production Deployment Guide

## Overview

This guide covers deploying the VialIA backend with AI integration to Render, ensuring your Flutter mobile app can connect successfully.

---

## 1. Environment Variables for Render

Set these environment variables in your Render service dashboard:

### **Critical: AI/Hugging Face Configuration**

```bash
# Hugging Face API Token (Required for AI features)
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx

# Get your token from: https://huggingface.co/settings/tokens
# Choose "Fine-grained tokens" with inference API read access
```

### **Database Configuration**

```bash
# PostgreSQL Connection (Render provides this)
DATABASE_URL=postgresql://user:password@host:port/database

# Example on Render (will be auto-provided):
# DATABASE_URL=postgresql://vialia_user:xxxxx@oregn-pg.render.com:5432/vialia_db
```

### **Deployment Environment**

```bash
# Environment identifier
ENVIRONMENT=production

# Render Service URL (automatically provided)
RENDER_EXTERNAL_URL=https://vialia-backend.onrender.com

# Optional: If you have a separate frontend domain
FRONTEND_URL=https://vialia-frontend.onrender.com
```

### **Optional: Email/Notifications**

```bash
# If your app uses email notifications (existing functionality)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

---

## 2. Main.py Configuration Strategy

Your updated `main.py` handles multiple deployment scenarios:

### **Local Development**
- ✅ Angular: `http://localhost:4200`
- ✅ Flutter Android Emulator: `http://10.0.2.2:8000`
- ✅ Flutter iOS Simulator: `http://localhost:8000`
- ✅ Physical Device: `http://192.168.56.1:8000`

### **Production (Render)**
- ✅ Auto-detected from `RENDER_EXTERNAL_URL`
- ✅ Custom frontend via `FRONTEND_URL`
- ✅ All Flutter configurations still work

### **How It Works**

```python
# main.py automatically:
1. Reads RENDER_EXTERNAL_URL from Render's environment
2. Adds it to CORS allowed origins
3. Logs the configuration on startup
4. Falls back to local origins if not in production
```

---

## 3. Flutter Configuration for Production

### **Update `lib/backend_config.dart`**

Your current config is excellent! Update it to support production:

```dart
import 'package:flutter/foundation.dart';

class BackendConfig {
  static const String _defaultPort = '8000';
  static const String _localNetworkIp = '192.168.56.1';
  static const String _androidEmulatorHost = '10.0.2.2';
  
  // Production URL - set this after Render deployment
  static const String _productionUrl = 'https://vialia-backend.onrender.com';

  static String get baseUrl {
    // 1. Check environment variable first (best practice)
    const fromEnv = String.fromEnvironment('BACKEND_URL');
    if (fromEnv.isNotEmpty) {
      debugPrint('[CONFIG] URL from environment: $fromEnv');
      return fromEnv;
    }

    // 2. Production release build
    if (const bool.fromEnvironment('PRODUCTION_BUILD') == true) {
      debugPrint('[CONFIG] Production build: $_productionUrl');
      return _productionUrl;
    }

    // 3. Development: Platform-specific
    if (kIsWeb) {
      return 'http://localhost:$_defaultPort';
    }

    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        // Check if running on emulator or physical device
        return _isEmulator() ? 
            'http://$_androidEmulatorHost:$_defaultPort' :
            'http://$_localNetworkIp:$_defaultPort';
      case TargetPlatform.iOS:
        return 'http://$_localNetworkIp:$_defaultPort';
      default:
        return 'http://localhost:$_defaultPort';
    }
  }

  static bool _isEmulator() {
    // Add logic to detect emulator
    // For now, assume emulator on local network
    return false;
  }

  static void printDebugInfo() {
    print('[CONFIG] Base URL: $baseUrl');
    print('[CONFIG] Production URL: $_productionUrl');
    print('[CONFIG] Local Network: $_localNetworkIp:$_defaultPort');
    print('[CONFIG] Emulator: $_androidEmulatorHost:$_defaultPort');
  }
}
```

### **Build Commands for Production**

```bash
# Android (APK)
flutter build apk --release \
  -DBACKEND_URL=https://vialia-backend.onrender.com \
  --build-number=1.0.0

# Android (App Bundle for Play Store)
flutter build appbundle --release \
  -DPRODUCTION_BUILD=true \
  --build-number=1.0.0

# iOS
flutter build ios --release \
  -DPRODUCTION_BUILD=true \
  --build-number=1.0.0
```

---

## 4. Deploy to Render

### **Step 1: Connect GitHub Repository**

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository: `iAngie28/emergencia.vehicular`
4. Select `main` branch

### **Step 2: Configure Service**

```
Name: vialia-backend
Environment: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Step 3: Set Environment Variables**

In Render dashboard → Environment:

```bash
ENVIRONMENT=production
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx  # Your Hugging Face token
DATABASE_URL=postgresql://...         # Render provides this
RENDER_EXTERNAL_URL=https://vialia-backend.onrender.com
```

### **Step 4: Deploy**

```bash
# Push to main branch
git push origin main

# Render auto-deploys on push
# Monitor: Dashboard → Logs
```

---

## 5. Verify Production Deployment

### **Test Backend Health**

```bash
# Health check
curl https://vialia-backend.onrender.com/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "vialia-backend",
#   "ai_enabled": true
# }

# Readiness check
curl https://vialia-backend.onrender.com/ready

# Expected response:
# {
#   "ready": true,
#   "database": "connected",
#   "ai_service": "available"
# }
```

### **Test AI Endpoint (with files)**

```bash
curl -X POST https://vialia-backend.onrender.com/api/v1/emergencia/reportar \
  -F "audio=@emergency.mp3" \
  -F "imagen=@scene.jpg"

# Expected: Emergency report with AI analysis
```

### **Flutter App Test**

Update your Flutter app's `main.dart` to point to production:

```dart
// In your service/API initialization
const String apiUrl = 'https://vialia-backend.onrender.com/api/v1';
// or use the BackendConfig.baseUrl from environment
```

Then test:

```bash
flutter run --release --dart-define=PRODUCTION_BUILD=true
```

---

## 6. AI Feature Verification

### **Hugging Face API Requirements**

Your AI service uses:
- **Audio Model**: openai/whisper-tiny (200MB)
- **Vision Model**: facebook/detr-resnet-50 (350MB)

These models are hosted by Hugging Face, so:
- ✅ No need to download locally
- ✅ API calls are made from Render
- ✅ Token is the only requirement

### **Testing AI Features**

```python
# Backend test script
import requests

# 1. Upload audio and image to emergency endpoint
files = {
    'audio': open('emergency.mp3', 'rb'),
    'imagen': open('scene.jpg', 'rb'),
}

response = requests.post(
    'https://vialia-backend.onrender.com/api/v1/emergencia/reportar',
    files=files
)

print(response.json())
# Should return transcription + detected objects + priority
```

---

## 7. Database Seeding (Don't Alter!)

⚠️ **IMPORTANT**: Keep existing seeder as-is

The repository's database seeder is functional on Render. Do **NOT** modify:
- `backend/app/models/` - existing models
- `backend/init_db.py` - database initialization
- `backend/reset_db.py` - reset scripts

Your local AI features are **additive only**:
- New `services/ai_service.py` - doesn't touch database
- New `api/v1/endpoints/emergencia.py` - new endpoint, no seeder changes
- Updated `main.py` - configuration only

---

## 8. Troubleshooting

### **CORS Error from Flutter App**

**Error**: `No 'Access-Control-Allow-Origin' header`

**Solution**:
1. Check RENDER_EXTERNAL_URL is set correctly
2. Verify your Flutter baseUrl matches CORS origins
3. Restart Render service

```bash
# Check logs in Render dashboard
# Look for: "CORS Origins: ..."
```

### **AI Service Returns 503 (Model Unavailable)**

**Cause**: Hugging Face model is loading (first call takes time)

**Solution**:
1. Retry after 30-60 seconds
2. Verify HF_API_TOKEN is valid
3. Check Hugging Face status: https://huggingface.co/status

### **Database Connection Failed**

**Error**: `Connection refused` or `Database error`

**Solution**:
1. Verify DATABASE_URL is set in Render env
2. Check Render PostgreSQL service is running
3. Run migrations: `alembic upgrade head`

### **High Memory Usage**

**Note**: Render free tier has 512MB RAM limit

**If exceeding:**
1. Reduce model complexity (already using Whisper Tiny)
2. Upgrade to Render paid plan
3. Implement request queuing

---

## 9. Performance Optimization for Render

### **Current Implementation**
- ✅ Memory-efficient (no temp files)
- ✅ Streaming file reads
- ✅ Async/await for concurrent requests
- ✅ Model caching by Hugging Face

### **Additional Optimizations**

```python
# main.py already includes these:
# 1. CORS preflight caching (3600 seconds)
# 2. Startup/shutdown event handlers
# 3. Health check endpoints for monitoring
# 4. Structured logging for debugging
```

---

## 10. Security Checklist

- [ ] HF_API_TOKEN is set (never commit to git)
- [ ] DATABASE_URL uses Render's PostgreSQL
- [ ] CORS origins don't include `*` (already configured)
- [ ] RENDER_EXTERNAL_URL matches your Render domain
- [ ] Environment set to `production`
- [ ] API key rotation policy established
- [ ] Error messages don't leak sensitive info (already handled)

---

## 11. Monitoring and Logs

### **View Logs in Render**

```bash
# Dashboard → Service → Logs
# Filter by:
# - [INFO] for startup messages
# - [WARNING] for issues
# - [ERROR] for failures
```

### **Monitor Key Metrics**

- CPU usage (should be <30% at idle)
- Memory usage (should be <400MB on free tier)
- Request count and latency
- Error rate

---

## 12. Production Checklist

- [ ] Push code to GitHub main branch
- [ ] Set all environment variables in Render
- [ ] Test health endpoint
- [ ] Test readiness endpoint
- [ ] Test AI endpoint with sample files
- [ ] Test from Flutter app
- [ ] Verify CORS works
- [ ] Monitor logs for errors
- [ ] Document any issues

---

## Quick Summary

| Component | Development | Production |
|-----------|-------------|-----------|
| Backend URL | `http://10.0.2.2:8000` (emulator) | `https://vialia-backend.onrender.com` |
| CORS Origins | Local + 192.168.x.x | Render URL + production frontend |
| Database | Local PostgreSQL | Render PostgreSQL |
| HF Token | Optional (AI disabled) | **Required** (set in env) |
| Environment | `development` | `production` |

---

## Support

If you encounter issues:
1. Check Render logs
2. Verify environment variables
3. Test endpoints with curl
4. Check Hugging Face API status
5. Review error messages in logs

Good luck with your deployment! 🚀
