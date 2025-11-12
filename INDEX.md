# Project Index - Burning Man Ranger Signature Manager

## 📋 Quick Navigation

### 🚀 Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 3 steps
- **[README](README)** - Full documentation and features
- **[test_setup.py](test_setup.py)** - Verify your installation

### 🏗️ Development
- **[app.py](app.py)** - Main Flask application (8,983 bytes)
- **[templates/](templates/)** - HTML templates (5 files)
- **[run.sh](run.sh)** - Quick start script for local dev

### 🌐 Deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Step-by-step Render.com guide
- **[Procfile](Procfile)** - Render.com process configuration
- **[runtime.txt](runtime.txt)** - Python version specification
- **[requirements.txt](requirements.txt)** - Python dependencies

### 📚 Documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What was built and why
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and diagrams
- **[README](README)** - Comprehensive project documentation

### ⚙️ Configuration
- **[.env.example](.env.example)** - Environment variables template
- **[.gitignore](.gitignore)** - Git ignore rules

### 📦 Reference
- **[chat-gpt5-condense.py](chat-gpt5-condense.py)** - Original PDF script (reference)

---

## 📁 File Descriptions

### Application Files

#### `app.py` (Main Application)
- Flask web application
- Database models (Rangers, Signatures)
- Routes and controllers
- Image processing logic
- PDF generation
- Session management

#### `templates/` (HTML Templates)
- `base.html` - Base template with navigation and styles
- `index.html` - Home page with welcome message
- `login.html` - Ranger login form
- `dashboard.html` - Ranger dashboard with upload
- `report.html` - All signatures view with PDF export

### Configuration Files

#### `requirements.txt`
Python dependencies:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- psycopg2-binary 2.9.9
- Pillow 10.1.0
- reportlab 4.0.7
- python-dotenv 1.0.0
- gunicorn 21.2.0

#### `.env.example`
Environment variables template:
- SECRET_KEY - Session encryption key
- DATABASE_URL - Database connection string

#### `Procfile`
Render.com deployment configuration:
```
web: gunicorn app:app
```

#### `runtime.txt`
Python version for deployment:
```
python-3.11.6
```

#### `.gitignore`
Excludes:
- Python cache files
- Virtual environments
- Database files
- IDE files
- OS files

### Documentation Files

#### `README`
- Project overview
- Features list
- Database schema
- Local setup instructions
- Deployment guide
- Usage instructions
- Technology stack

#### `QUICKSTART.md`
- 3-step setup
- Quick test guide
- One-line setup command
- Troubleshooting tips

#### `DEPLOYMENT.md`
- Render.com deployment steps
- Database setup
- Environment configuration
- Post-deployment testing
- Scaling considerations
- Cost estimates

#### `PROJECT_SUMMARY.md`
- What was built
- Technical stack
- Design decisions
- Security considerations
- Future enhancements
- Testing recommendations

#### `ARCHITECTURE.md`
- System overview diagrams
- Request flow diagrams
- Component details
- Data flow diagrams
- Security architecture
- Performance considerations

### Utility Files

#### `run.sh`
Quick start script that:
- Creates virtual environment
- Installs dependencies
- Creates .env file
- Starts the application

#### `test_setup.py`
Verification script that checks:
- All dependencies installed
- Templates exist
- Configuration files present
- No syntax errors in app.py

#### `chat-gpt5-condense.py`
Original PDF generation script (reference):
- ReportLab PDF creation
- Image grid layout
- Signature condensing logic

---

## 🎯 Common Tasks

### First Time Setup
```bash
# Quick method
./run.sh

# Manual method
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### Verify Installation
```bash
python test_setup.py
```

### Run Locally
```bash
python app.py
# or
./run.sh
```

### Deploy to Render.com
1. Push to GitHub
2. Follow [DEPLOYMENT.md](DEPLOYMENT.md)

### Test the Application
1. Open http://localhost:5000
2. Login with test Ranger ID
3. Upload signature
4. View report page
5. Generate PDF

---

## 📊 Project Statistics

- **Total Files**: 18
- **Python Files**: 3 (app.py, test_setup.py, chat-gpt5-condense.py)
- **HTML Templates**: 5
- **Documentation Files**: 6
- **Configuration Files**: 5
- **Lines of Code**: ~500 (app.py + templates)
- **Dependencies**: 7 Python packages

---

## 🔗 Quick Links

### Local Development
- Application: http://localhost:5000
- Login: http://localhost:5000/login
- Report: http://localhost:5000/report

### Documentation
- [README](README) - Start here
- [QUICKSTART.md](QUICKSTART.md) - Get running fast
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy to production

### External Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render.com Docs](https://render.com/docs)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [ReportLab Docs](https://www.reportlab.com/docs/)

---

## 🎨 Features Implemented

✅ **Authentication**
- Ranger ID-based login
- Session management
- Auto-registration

✅ **Signature Management**
- Upload signatures (PNG, JPG, GIF, WEBP)
- View current signature
- Update/replace signatures
- Image optimization

✅ **Report Dashboard**
- Grid view of all signatures
- Select/deselect signatures
- Bulk operations
- Real-time updates

✅ **PDF Generation**
- Condensed grid layout
- Selected signatures only
- Automatic scaling
- Timestamp in filename

✅ **Database**
- PostgreSQL for production
- SQLite for development
- Automatic table creation
- Binary image storage

---

## 🛠️ Technology Stack

**Backend**
- Flask 3.0.0 (Web framework)
- SQLAlchemy 3.1.1 (ORM)
- Gunicorn 21.2.0 (WSGI server)

**Image Processing**
- Pillow 10.1.0 (Image manipulation)
- ReportLab 4.0.7 (PDF generation)

**Database**
- PostgreSQL (Production)
- SQLite (Development)

**Frontend**
- HTML5
- CSS3 (Modern gradients)
- Vanilla JavaScript (No frameworks)

**Deployment**
- Render.com (PaaS)
- Git (Version control)

---

## 📝 Notes

### Lint Warnings
The JavaScript linter may show errors in `templates/report.html` at line 94. These are false positives from Jinja2 template syntax within JavaScript and can be safely ignored.

### Database
- Local development uses SQLite (automatic)
- Production uses PostgreSQL (Render.com)
- Database tables created automatically on first run

### Security
- Change SECRET_KEY in production
- Ranger IDs are case-sensitive
- No password authentication (by design)
- File uploads limited to 5MB

### Performance
- Images automatically resized to 800x400px max
- Binary storage in database
- Session-based authentication
- Efficient PDF generation

---

## 🎓 Learning Resources

### Flask
- Official Tutorial: https://flask.palletsprojects.com/tutorial/
- Mega Tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

### SQLAlchemy
- ORM Tutorial: https://docs.sqlalchemy.org/en/20/orm/tutorial.html
- Relationships: https://docs.sqlalchemy.org/en/20/orm/relationships.html

### Deployment
- Render.com Guide: https://render.com/docs/deploy-flask
- PostgreSQL Setup: https://render.com/docs/databases

---

## 📞 Support

For issues or questions:
1. Check the documentation files
2. Review the code comments in app.py
3. Run test_setup.py to verify installation
4. Check Render.com logs for deployment issues

---

## 🚀 Next Steps

1. **Local Testing**: Run `./run.sh` and test locally
2. **Verify Setup**: Run `python test_setup.py`
3. **Deploy**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Customize**: Modify templates and styles as needed
5. **Enhance**: Add features from PROJECT_SUMMARY.md

---

*This project was built for Burning Man rangers to manage and print signature collections.*
