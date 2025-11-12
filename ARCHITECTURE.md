# Application Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Burning Man Ranger                       │
│                   Signature Manager System                   │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Rangers    │────────▶│  Web Browser │────────▶│   Internet   │
│  (Users)     │         │              │         │              │
└──────────────┘         └──────────────┘         └──────────────┘
                                │                         │
                                │                         │
                                ▼                         ▼
                         ┌─────────────────────────────────────┐
                         │     Render.com Web Service          │
                         │  ┌───────────────────────────────┐  │
                         │  │      Flask Application        │  │
                         │  │         (app.py)              │  │
                         │  │                               │  │
                         │  │  ┌─────────────────────────┐ │  │
                         │  │  │   Routes & Controllers  │ │  │
                         │  │  │  - Login/Logout         │ │  │
                         │  │  │  - Upload Signature     │ │  │
                         │  │  │  - View Dashboard       │ │  │
                         │  │  │  - Report Page          │ │  │
                         │  │  │  - PDF Generation       │ │  │
                         │  │  └─────────────────────────┘ │  │
                         │  │                               │  │
                         │  │  ┌─────────────────────────┐ │  │
                         │  │  │   Business Logic        │ │  │
                         │  │  │  - Image Processing     │ │  │
                         │  │  │  - Session Management   │ │  │
                         │  │  │  - PDF Generation       │ │  │
                         │  │  └─────────────────────────┘ │  │
                         │  │                               │  │
                         │  │  ┌─────────────────────────┐ │  │
                         │  │  │   Database Layer        │ │  │
                         │  │  │  - SQLAlchemy ORM       │ │  │
                         │  │  │  - Models (Rangers,     │ │  │
                         │  │  │    Signatures)          │ │  │
                         │  │  └─────────────────────────┘ │  │
                         │  └───────────────────────────────┘  │
                         └─────────────────────────────────────┘
                                         │
                                         │
                                         ▼
                         ┌─────────────────────────────────────┐
                         │   Render.com PostgreSQL Database    │
                         │  ┌───────────────────────────────┐  │
                         │  │     Rangers Table             │  │
                         │  │  - id (PK)                    │  │
                         │  │  - ranger_id (unique)         │  │
                         │  │  - name                       │  │
                         │  │  - created_at                 │  │
                         │  └───────────────────────────────┘  │
                         │                                     │
                         │  ┌───────────────────────────────┐  │
                         │  │   Signatures Table            │  │
                         │  │  - id (PK)                    │  │
                         │  │  - ranger_id (FK)             │  │
                         │  │  - image_data (binary)        │  │
                         │  │  - image_format               │  │
                         │  │  - uploaded_at                │  │
                         │  │  - selected (boolean)         │  │
                         │  └───────────────────────────────┘  │
                         └─────────────────────────────────────┘
```

## Request Flow

### 1. Ranger Login Flow
```
User → Login Page → Enter Ranger ID → Flask validates → 
  → Check database → Create/Load Ranger → Set session → 
  → Redirect to Dashboard
```

### 2. Signature Upload Flow
```
User → Dashboard → Select Image → Drag/Drop or Click → 
  → JavaScript preview → Submit form → Flask receives → 
  → Process image (resize, optimize) → Save to database → 
  → Update signature record → Redirect to Dashboard
```

### 3. Report View Flow
```
User → Report Page → Flask queries all signatures → 
  → Render grid with images → User clicks to select/deselect → 
  → AJAX call to toggle → Update database → Return status → 
  → Update UI
```

### 4. PDF Generation Flow
```
User → Report Page → Click "Generate PDF" → 
  → Flask queries selected signatures → Load images from database → 
  → ReportLab creates PDF → Calculate grid layout → 
  → Place signatures in cells → Stream PDF to browser
```

## Component Details

### Frontend (Templates)

```
templates/
├── base.html           # Base template with navigation
│   ├── Navigation bar
│   ├── Flash messages
│   └── Common styles
│
├── index.html          # Home page
│   └── Welcome message and links
│
├── login.html          # Login form
│   └── Ranger ID input
│
├── dashboard.html      # Ranger dashboard
│   ├── Current signature display
│   ├── Upload area (drag-drop)
│   └── Image preview
│
└── report.html         # All signatures view
    ├── Signature grid
    ├── Selection controls
    └── PDF generation button
```

### Backend (Flask Routes)

```
app.py
├── / (index)                    # Home page
├── /login (GET, POST)           # Login/register
├── /logout                      # Logout
├── /dashboard                   # Ranger dashboard
├── /upload (POST)               # Upload signature
├── /signature/<id>              # View signature image
├── /report                      # All signatures view
├── /toggle_signature/<id>       # Toggle selection
└── /print_pdf                   # Generate PDF
```

### Database Models

```
Rangers Model
├── id: Integer (Primary Key)
├── ranger_id: String (Unique, Required)
├── name: String (Optional)
├── created_at: DateTime
└── signature: Relationship (One-to-One)

Signatures Model
├── id: Integer (Primary Key)
├── ranger_id: Integer (Foreign Key)
├── image_data: LargeBinary (Required)
├── image_format: String
├── uploaded_at: DateTime
└── selected: Boolean (Default: True)
```

## Technology Stack Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  HTML5, CSS3, JavaScript                │
│  - Responsive design                    │
│  - Drag-and-drop upload                 │
│  - Real-time preview                    │
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         Application Layer               │
│  Flask 3.0.0                            │
│  - Routing                              │
│  - Session management                   │
│  - Request handling                     │
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         Business Logic Layer            │
│  Python                                 │
│  - Image processing (Pillow)            │
│  - PDF generation (ReportLab)           │
│  - Authentication                       │
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         Data Access Layer               │
│  SQLAlchemy ORM                         │
│  - Model definitions                    │
│  - Query building                       │
│  - Relationship management              │
└─────────────────────────────────────────┘
                  │
┌─────────────────────────────────────────┐
│         Database Layer                  │
│  PostgreSQL (Production)                │
│  SQLite (Development)                   │
│  - Data persistence                     │
│  - ACID transactions                    │
└─────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐
│  Ranger  │
└────┬─────┘
     │
     │ 1. Upload Image
     ▼
┌─────────────┐
│   Flask     │
│  Receives   │
│   Request   │
└─────┬───────┘
      │
      │ 2. Process Image
      ▼
┌─────────────┐
│   Pillow    │
│  - Resize   │
│  - Optimize │
│  - Convert  │
└─────┬───────┘
      │
      │ 3. Save Binary
      ▼
┌─────────────┐
│ SQLAlchemy  │
│   Insert/   │
│   Update    │
└─────┬───────┘
      │
      │ 4. Store Data
      ▼
┌─────────────┐
│ PostgreSQL  │
│  Database   │
└─────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│  1. HTTPS (Render.com)                  │
│     - Encrypted transport               │
├─────────────────────────────────────────┤
│  2. Session Management                  │
│     - SECRET_KEY encryption             │
│     - Secure cookies                    │
├─────────────────────────────────────────┤
│  3. Input Validation                    │
│     - File type checking                │
│     - File size limits                  │
│     - Image format validation           │
├─────────────────────────────────────────┤
│  4. SQL Injection Protection            │
│     - SQLAlchemy ORM                    │
│     - Parameterized queries             │
├─────────────────────────────────────────┤
│  5. Database Security                   │
│     - Environment variables             │
│     - No hardcoded credentials          │
└─────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         GitHub Repository               │
│  - Source code                          │
│  - Version control                      │
└─────────────┬───────────────────────────┘
              │
              │ Git Push
              ▼
┌─────────────────────────────────────────┐
│         Render.com                      │
│  ┌───────────────────────────────────┐  │
│  │   Automatic Build                 │  │
│  │  1. Clone repository              │  │
│  │  2. Install dependencies          │  │
│  │  3. Start gunicorn                │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   Web Service                     │  │
│  │  - Flask app running              │  │
│  │  - Gunicorn WSGI server           │  │
│  │  - Auto-scaling                   │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   PostgreSQL Database             │  │
│  │  - Managed database               │  │
│  │  - Automatic backups              │  │
│  │  - Connection pooling             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## File Structure

```
remote-sign/
│
├── Configuration Files
│   ├── .env.example          # Environment template
│   ├── .gitignore            # Git ignore rules
│   ├── Procfile              # Render.com process
│   ├── requirements.txt      # Python dependencies
│   └── runtime.txt           # Python version
│
├── Application Code
│   ├── app.py                # Main Flask application
│   └── templates/            # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── dashboard.html
│       └── report.html
│
├── Documentation
│   ├── README                # Main documentation
│   ├── QUICKSTART.md         # Quick start guide
│   ├── DEPLOYMENT.md         # Deployment guide
│   ├── PROJECT_SUMMARY.md    # Project summary
│   └── ARCHITECTURE.md       # This file
│
├── Utilities
│   ├── run.sh                # Quick start script
│   ├── test_setup.py         # Setup verification
│   └── chat-gpt5-condense.py # Original reference
│
└── Runtime (Generated)
    ├── signatures.db         # SQLite database (local)
    └── __pycache__/          # Python cache
```

## Performance Considerations

### Image Processing
- Images resized to max 800x400px
- Automatic format conversion to PNG
- Optimization on upload
- Binary storage in database

### Database
- Indexed on ranger_id for fast lookups
- One-to-one relationship (no N+1 queries)
- Connection pooling via SQLAlchemy
- Efficient binary storage

### PDF Generation
- Streaming output (no temp files)
- Grid calculation optimized
- Image scaling cached
- Only selected signatures processed

### Caching Opportunities
- Session-based authentication (no DB hit per request)
- Static assets (CSS/JS inline for simplicity)
- Image thumbnails (future enhancement)
- PDF templates (future enhancement)
