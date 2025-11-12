# Quick Start Guide

## 🚀 Get Running in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
cp .env.example .env
# Edit .env and set SECRET_KEY to a random string
```

### 3. Run the App
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 🎯 Quick Test

1. Click "Ranger Login"
2. Enter any Ranger ID (e.g., "TEST001")
3. Upload a signature image
4. Go to "View All Signatures"
5. Click "Generate PDF"

---

## 📦 One-Line Setup (Mac/Linux)

```bash
./run.sh
```

This script will:
- Create virtual environment
- Install dependencies
- Create .env file
- Start the application

---

## 🔍 Verify Installation

```bash
python test_setup.py
```

This checks:
- All dependencies installed
- Templates exist
- Configuration files present
- No syntax errors

---

## 🌐 Deploy to Render.com

See **DEPLOYMENT.md** for detailed instructions.

**Quick version:**
1. Push code to GitHub
2. Create PostgreSQL database on Render.com
3. Create Web Service on Render.com
4. Set environment variables (SECRET_KEY, DATABASE_URL)
5. Deploy!

---

## 📚 Documentation

- **README**: Full documentation and features
- **DEPLOYMENT.md**: Render.com deployment guide
- **PROJECT_SUMMARY.md**: Technical details and architecture

---

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "No such file or directory: .env"
```bash
cp .env.example .env
```

### Database errors
- For local dev, SQLite is used automatically
- For production, set DATABASE_URL environment variable

### Port already in use
- Change port in app.py: `app.run(port=5001)`
- Or kill existing process: `lsof -ti:5000 | xargs kill`

---

## 🎨 Features

✅ Ranger login with ID  
✅ Upload/update signatures  
✅ View all signatures  
✅ Select/deselect for printing  
✅ Generate PDF packets  
✅ Database storage  
✅ Drag-and-drop upload  
✅ Image optimization  

---

## 📞 Need Help?

Check the documentation files:
- README - General information
- DEPLOYMENT.md - Deployment help
- PROJECT_SUMMARY.md - Technical details

Or review the code:
- app.py - Main application logic
- templates/ - HTML pages
