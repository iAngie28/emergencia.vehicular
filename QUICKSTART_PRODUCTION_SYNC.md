# VialIA Production Sync - Quick Reference Guide

**Last Updated**: April 28, 2026  
**Status**: ✅ Ready for Pull Request  
**Target**: Render Deployment with Flutter Integration

---

## 🎯 What You've Accomplished

You now have a **production-ready VialIA backend** with:

- ✅ **AI Integration**: Hugging Face API for audio transcription + image detection
- ✅ **Production CORS**: Configured for Flutter mobile + web frontends
- ✅ **Environment Variables**: Secure configuration for Render
- ✅ **Health Checks**: Monitoring endpoints for deployment verification
- ✅ **Comprehensive Documentation**: 5 guides covering all scenarios
- ✅ **Mobile Ready**: Flutter app can connect locally and in production
- ✅ **Backwards Compatible**: No breaking changes to existing code

---

## 📂 Files Changed/Created

### **Modified**
```
backend/app/main.py ✏️ Updated
  - Added CORS configuration for production
  - Added health/readiness check endpoints
  - Added startup/shutdown event handlers
  - Environment variable support
```

### **New - AI Features**
```
backend/app/services/ai_service.py ✨ New
  - Hugging Face Inference API integration
  - Audio transcription (Whisper Tiny)
  - Object detection (Facebook DETR ResNet-50)
  - Error handling and logging

backend/app/api/v1/endpoints/emergencia.py ✨ New
  - Emergency reporting endpoint
  - File validation and security
  - Priority assessment
  - Multimodal analysis
```

### **New - Configuration/Documentation**
```
backend/.env.example 📝 Template
  - Environment variables reference
  - Local development setup

PRODUCTION_DEPLOYMENT_GUIDE.md 📖 Guide
  - Step-by-step Render deployment
  - Environment configuration
  - Mobile connectivity setup

PULL_REQUEST_SUMMARY.md 📋 Checklist
  - PR template and guidelines
  - Pre-submission checklist
  - Integration verification

FLUTTER_INTEGRATION_GUIDE.md 📱 Mobile Guide
  - Flutter configuration for production
  - HTTP client implementation
  - Build commands
  - Troubleshooting

QUICKSTART_PRODUCTION_SYNC.md 🚀 This File
  - Master overview and quick reference
```

### **Unchanged** (DO NOT MODIFY)
```
✅ All existing models, endpoints, database code
✅ Seeder and initialization scripts
✅ Frontend and other applications
```

---

## 🚀 Quick Start: 3-Step Deployment

### **1. Update Environment Variables**

Get your Hugging Face token:
- Go to https://huggingface.co/settings/tokens
- Create "Fine-grained token" with Inference API access
- Copy your token

### **2. Push to GitHub**

```bash
cd emergencia_vehicular_reconstruido

# Create feature branch
git checkout -b feature/ai-integration

# Stage changes
git add backend/app/main.py
git add backend/app/services/ai_service.py
git add backend/app/api/v1/endpoints/emergencia.py
git add backend/.env.example
git add *.md  # Documentation files

# Commit with clear message
git commit -m "feat: Add Hugging Face AI integration for emergency reporting"

# Push to origin
git push origin feature/ai-integration
```

### **3. Create Pull Request**

- Go to GitHub repository
- Create PR to `main` branch
- Use template from `PULL_REQUEST_SUMMARY.md`
- Reference this guide in the PR description

After merge, Render auto-deploys! 🎉

---

## ⚙️ Environment Variables Required on Render

**Set in Render Dashboard → Environment:**

```bash
# AI Features (Required for new emergencia endpoint)
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx

# Environment Identifier
ENVIRONMENT=production

# Auto-provided by Render (don't set manually)
# RENDER_EXTERNAL_URL=https://vialia-backend.onrender.com
# DATABASE_URL=postgresql://...

# Optional: Custom Frontend URL
# FRONTEND_URL=https://vialia-frontend.onrender.com
```

---

## 📱 Flutter App Configuration

### **Current Setup** (Already Good!)

Your `lib/backend_config.dart` already handles:
- Android Emulator: `http://10.0.2.2:8000`
- iOS Simulator: `http://localhost:8000`
- Physical Device: `http://192.168.56.1:8000`
- Environment Variable: `--dart-define=BACKEND_URL=...`
- Production: `--dart-define=PRODUCTION_BUILD=true`

### **Update for Production**

Update the constant in `backend_config.dart`:

```dart
static const String _productionUrl = 'https://vialia-backend.onrender.com';
```

### **Build Commands**

```bash
# Development
flutter run

# Production (Render)
flutter build apk --release --dart-define=PRODUCTION_BUILD=true
flutter build ios --release --dart-define=PRODUCTION_BUILD=true

# Custom URL
flutter build apk --release --dart-define=BACKEND_URL=https://your-url.com
```

---

## ✅ Pre-PR Verification Checklist

- [ ] **Code Quality**
  - [ ] `python -m flake8 backend/` (no style errors)
  - [ ] All imports are used
  - [ ] No hardcoded secrets in code
  - [ ] Proper error handling

- [ ] **Local Testing**
  - [ ] Backend runs: `python main.py`
  - [ ] No startup errors in logs
  - [ ] Health check works: `curl http://localhost:8000/health`
  - [ ] Readiness check works: `curl http://localhost:8000/ready`

- [ ] **AI Integration Testing**
  - [ ] Set `HF_API_TOKEN` locally
  - [ ] Test emergency endpoint: `curl -X POST http://localhost:8000/api/v1/emergencia/reportar -F "audio=@file.mp3" -F "imagen=@image.jpg"`
  - [ ] Response includes: status, transcription, detections, priority

- [ ] **Flutter Connectivity** (if you have a local build)
  - [ ] App connects to local backend
  - [ ] No CORS errors
  - [ ] API responses are received

- [ ] **Documentation**
  - [ ] All guide files are in repository root
  - [ ] `.env.example` reflects actual variables needed
  - [ ] Documentation is up-to-date

- [ ] **Git Hygiene**
  - [ ] No `.env` file committed (use `.env.example`)
  - [ ] No `__pycache__` committed
  - [ ] No API tokens in code
  - [ ] `.gitignore` is proper

---

## 🔍 Testing AI Features Locally

### **Setup**

```bash
# 1. Create .env file from template
cp backend/.env.example backend/.env

# 2. Add your HF token
# Edit backend/.env and add:
# HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx

# 3. Start backend
cd backend
python main.py
```

### **Test Emergency Endpoint**

```bash
# Create test files (or use your own)
# emergency.mp3 - audio file
# scene.jpg - image file

# Post to emergency endpoint
curl -X POST http://localhost:8000/api/v1/emergencia/reportar \
  -F "audio=@emergency.mp3" \
  -F "imagen=@scene.jpg" \
  -v

# Expected response:
# {
#   "status": "success",
#   "data": {
#     "transcription": "Help, car accident at...",
#     "detections": [...],
#     "detection_summary": ["car", "person", ...],
#     "priority": "Alta",
#     "processing_status": "success"
#   },
#   "message": "Emergency report processed successfully..."
# }
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         Flutter Mobile App                      │
│  (Android, iOS, Web)                            │
└──────────────┬──────────────────────────────────┘
               │
               ├─ Points to: http://10.0.2.2:8000 (dev)
               ├─ Points to: https://vialia-backend.onrender.com (prod)
               │
┌──────────────▼──────────────────────────────────┐
│    FastAPI Backend (main.py)                    │
│  - CORS Configuration (env-aware)               │
│  - Health/Readiness Checks                      │
│  - Existing Endpoints (unchanged)               │
│  - NEW: /api/v1/emergencia/reportar             │
└──────────────┬──────────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌──────▼──────────────┐
│ PostgreSQL │    │ Hugging Face API    │
│ Database   │    │ - Whisper Tiny      │
│            │    │ - DETR ResNet-50    │
└────────────┘    └─────────────────────┘
```

---

## 🎓 Key Concepts

### **CORS (Cross-Origin Resource Sharing)**
- Allows frontend apps to call backend API
- Your config supports local dev + production
- Auto-detects Render URL from environment

### **Environment Variables**
- `HF_API_TOKEN`: Hugging Face credentials (not hardcoded)
- `ENVIRONMENT`: Identifies dev/staging/production
- `RENDER_EXTERNAL_URL`: Auto-provided by Render

### **Multimodal AI Processing**
- **Audio Path**: Audio file → Whisper Tiny → Transcribed text
- **Image Path**: Image file → DETR ResNet-50 → Detected objects
- **Priority**: Combined analysis → Priority level (Alta/Media/Baja)

### **Memory Efficiency**
- No temporary files stored
- Streaming reads from client
- Direct memory processing
- Critical for Render's 512MB RAM limit

---

## 🐛 Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| `Connection refused` | Backend not running or wrong URL |
| `CORS error` | Check RENDER_EXTERNAL_URL environment variable |
| `AI returns 503` | Hugging Face model loading (retry after 30s) |
| `File too large` | Check 25MB audio / 10MB image limits |
| `HF_API_TOKEN missing` | Set in Render environment variables |
| `Database error` | Verify DATABASE_URL set on Render |

**Full troubleshooting**: See `PRODUCTION_DEPLOYMENT_GUIDE.md` Section 8

---

## 📖 Document Map

Where to find what you need:

| Need | Document |
|------|----------|
| Render deployment steps | `PRODUCTION_DEPLOYMENT_GUIDE.md` |
| PR submission checklist | `PULL_REQUEST_SUMMARY.md` |
| Flutter integration | `FLUTTER_INTEGRATION_GUIDE.md` |
| Environment variables | `backend/.env.example` |
| This overview | `QUICKSTART_PRODUCTION_SYNC.md` |

---

## 🚀 Next Steps

### **Immediate (Today)**
1. [ ] Review updated `main.py`
2. [ ] Test locally: `python main.py`
3. [ ] Test health endpoint
4. [ ] Set HF_API_TOKEN locally
5. [ ] Test AI endpoint

### **Before PR (This Week)**
1. [ ] Update Flutter `backend_config.dart` with production URL
2. [ ] Commit all changes to feature branch
3. [ ] Create PR with template from `PULL_REQUEST_SUMMARY.md`
4. [ ] Request review from team

### **After Merge (Deployment)**
1. [ ] Render auto-deploys on merge
2. [ ] Monitor Render logs
3. [ ] Verify health endpoint
4. [ ] Update Flutter build for production
5. [ ] Test from deployed backend

### **Production (Release)**
1. [ ] Distribute Flutter APK/IPA to users
2. [ ] Users point to production backend
3. [ ] Monitor error rates and performance
4. [ ] Collect feedback from beta testers

---

## 💡 Pro Tips

1. **Testing Without HF Token**
   - Leave `HF_API_TOKEN` empty locally
   - All non-AI endpoints still work
   - Perfect for testing other features

2. **Local Network Debugging**
   - Use same WiFi for device and machine
   - Run `ifconfig` (Mac/Linux) or `ipconfig` (Windows) to find your IP
   - Use that IP in Flutter app

3. **Production URL Updates**
   - Always use `https://` in production
   - Render provides free SSL certificates
   - CORS automatically includes your Render URL

4. **Monitoring on Render**
   - Check logs daily after deployment
   - Set up alerts for high error rates
   - Monitor AI endpoint latency

5. **Version Control Best Practices**
   - Never commit `.env` files (use `.env.example`)
   - Use meaningful commit messages
   - Keep documentation updated with code

---

## ✨ Success Criteria

Your production sync is complete when:

- ✅ main.py updated with CORS + env vars
- ✅ AI service and emergency endpoint integrated
- ✅ All documentation is clear and accurate
- ✅ Local testing passes (health, readiness, AI)
- ✅ PR passes code review
- ✅ Render deployment succeeds
- ✅ Flutter app connects to production backend
- ✅ AI endpoint works end-to-end

---

## 📞 Questions?

Refer to the comprehensive guides:
1. **Backend Setup**: `PRODUCTION_DEPLOYMENT_GUIDE.md`
2. **Mobile App**: `FLUTTER_INTEGRATION_GUIDE.md`
3. **PR Process**: `PULL_REQUEST_SUMMARY.md`

Or check the inline comments in:
- `backend/app/main.py` - Annotated configuration
- `backend/app/services/ai_service.py` - AI service logic
- `backend/app/api/v1/endpoints/emergencia.py` - Emergency endpoint
- `movil/lib/backend_config.dart` - Flutter configuration

---

## 🎉 You're Ready!

Your VialIA backend is now production-ready with:
- Integrated AI features
- Mobile app connectivity
- Render deployment support
- Comprehensive documentation

**Time to ship!** 🚀

```
   _____     ___    _ _   ___    _
  |  __ \   |_ _|  / \  | |    | |
  | |  | |   | |  / _ \ | |    | |
  | |_| |   | | / ___ \| |___ | |___
  |____/   |___/_/   \_\|_____||_____|

  Emergency Vehicle Assistance System
         Production Ready v1.0
```
