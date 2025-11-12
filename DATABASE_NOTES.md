# Database Notes

## Initial Setup

The Flask application is designed with the approval workflow from the start. No migration is needed.

### First Run

When you first run the application:

```bash
python app.py
```

The database tables will be created automatically with the correct schema including:
- `status` field (default: 'pending')
- `approved_at` field
- `rejected_at` field  
- `rejection_reason` field

### Database Creation

The `db.create_all()` command in `app.py` handles table creation:

```python
# Create tables
with app.app_context():
    db.create_all()
```

This runs automatically when the application starts.

### Fresh Installation

For a fresh installation:

1. **SQLite (Development)**
   - No setup needed
   - Database file created automatically as `signatures.db`
   - Tables created on first run

2. **PostgreSQL (Production/Render.com)**
   - Create database on Render.com
   - Set `DATABASE_URL` environment variable
   - Tables created automatically on first deployment

### Resetting the Database

If you need to start fresh:

**SQLite:**
```bash
rm signatures.db
python app.py  # Tables recreated
```

**PostgreSQL:**
```bash
# Connect to database and drop tables
DROP TABLE signatures;
DROP TABLE rangers;
# Restart app - tables will be recreated
```

### Schema Details

All new signatures automatically get:
- `status = 'pending'`
- `approved_at = NULL`
- `rejected_at = NULL`
- `rejection_reason = NULL`

When a signature is approved:
- `status = 'approved'`
- `approved_at = current timestamp`
- `rejected_at = NULL`
- `rejection_reason = NULL`

When a signature is rejected:
- `status = 'rejected'`
- `rejected_at = current timestamp`
- `approved_at = NULL`
- `rejection_reason = admin's reason text`

When a signature is re-uploaded:
- All fields reset to pending state

### No Migration Needed

Since this is the initial version with the approval workflow built-in, there's no need for database migrations. The schema is correct from the start.

### Future Changes

If you need to modify the schema in the future, consider using Flask-Migrate:

```bash
pip install Flask-Migrate
```

Add to `app.py`:
```python
from flask_migrate import Migrate
migrate = Migrate(app, db)
```

Then use:
```bash
flask db init
flask db migrate -m "Description of changes"
flask db upgrade
```

But for the initial deployment, this is not necessary.
