import os
import io
import base64
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///signatures.db')
# Fix for Render.com postgres URL
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Admin password for viewing signatures
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

db = SQLAlchemy(app)

# Database Models
class Ranger(db.Model):
    __tablename__ = 'rangers'
    id = db.Column(db.Integer, primary_key=True)
    ranger_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    signature = db.relationship('Signature', backref='ranger', uselist=False, cascade='all, delete-orphan')

class Signature(db.Model):
    __tablename__ = 'signatures'
    id = db.Column(db.Integer, primary_key=True)
    ranger_id = db.Column(db.Integer, db.ForeignKey('rangers.id'), nullable=False, unique=True)
    image_data = db.Column(db.LargeBinary, nullable=False)
    image_format = db.Column(db.String(10), default='PNG')
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Approval workflow
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    approved_at = db.Column(db.DateTime, nullable=True)
    rejected_at = db.Column(db.DateTime, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)

# Create tables
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def process_signature_image(file):
    """Process and optimize signature image"""
    img = Image.open(file)
    
    # Convert to RGB if needed
    if img.mode in ('RGBA', 'LA'):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'RGBA':
            bg.paste(img, mask=img.split()[3])
        else:
            bg.paste(img, mask=img.split()[1])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize if too large (max 800x400)
    max_width, max_height = 800, 400
    if img.width > max_width or img.height > max_height:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # Save to bytes
    output = io.BytesIO()
    img.save(output, format='PNG', optimize=True)
    output.seek(0)
    return output.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ranger_id = request.form.get('ranger_id', '').strip()
        
        if not ranger_id:
            flash('Please enter your Ranger ID', 'error')
            return redirect(url_for('login'))
        
        ranger = Ranger.query.filter_by(ranger_id=ranger_id).first()
        
        if not ranger:
            # Create new ranger if ID doesn't exist
            ranger = Ranger(ranger_id=ranger_id)
            db.session.add(ranger)
            db.session.commit()
            flash('Welcome! Please upload your signature.', 'success')
        
        session['ranger_id'] = ranger.id
        return redirect(url_for('ranger_dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('ranger_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def ranger_dashboard():
    if 'ranger_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))
    
    ranger = Ranger.query.get(session['ranger_id'])
    if not ranger:
        session.pop('ranger_id', None)
        flash('Invalid session. Please log in again.', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', ranger=ranger)

@app.route('/upload', methods=['POST'])
def upload_signature():
    if 'ranger_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    if 'signature' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['signature']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or GIF'}), 400
    
    try:
        # Process image
        image_data = process_signature_image(file)
        
        ranger = Ranger.query.get(session['ranger_id'])
        
        # Update or create signature
        if ranger.signature:
            ranger.signature.image_data = image_data
            ranger.signature.uploaded_at = datetime.utcnow()
            # Reset approval status when uploading new signature
            ranger.signature.status = 'pending'
            ranger.signature.approved_at = None
            ranger.signature.rejected_at = None
            ranger.signature.rejection_reason = None
        else:
            signature = Signature(ranger_id=ranger.id, image_data=image_data, status='pending')
            db.session.add(signature)
        
        db.session.commit()
        flash('Signature uploaded successfully!', 'success')
        return jsonify({'success': True, 'redirect': url_for('ranger_dashboard')})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/signature/<int:ranger_id>')
def view_signature(ranger_id):
    signature = Signature.query.filter_by(ranger_id=ranger_id).first()
    if not signature:
        return 'No signature found', 404
    
    return send_file(
        io.BytesIO(signature.image_data),
        mimetype='image/png',
        as_attachment=False
    )

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_authenticated'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('report'))
        else:
            flash('Invalid password', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_authenticated', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/report')
def report():
    # Check if admin is authenticated
    if not session.get('admin_authenticated'):
        flash('Please login to view signatures', 'error')
        return redirect(url_for('admin_login'))
    
    rangers = Ranger.query.join(Signature).all()
    return render_template('report.html', rangers=rangers)

@app.route('/approve_signature/<int:signature_id>', methods=['POST'])
def approve_signature(signature_id):
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    signature = Signature.query.get_or_404(signature_id)
    signature.status = 'approved'
    signature.approved_at = datetime.utcnow()
    signature.rejected_at = None
    signature.rejection_reason = None
    db.session.commit()
    return jsonify({'status': 'approved', 'approved_at': signature.approved_at.strftime('%B %d, %Y at %I:%M %p')})

@app.route('/reject_signature/<int:signature_id>', methods=['POST'])
def reject_signature(signature_id):
    if not session.get('admin_authenticated'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    rejection_reason = data.get('reason', '').strip()
    
    signature = Signature.query.get_or_404(signature_id)
    signature.status = 'rejected'
    signature.rejected_at = datetime.utcnow()
    signature.approved_at = None
    signature.rejection_reason = rejection_reason
    db.session.commit()
    return jsonify({'status': 'rejected', 'rejected_at': signature.rejected_at.strftime('%B %d, %Y at %I:%M %p'), 'reason': rejection_reason})

@app.route('/print_pdf')
def print_pdf():
    if not session.get('admin_authenticated'):
        flash('Please login to generate PDF', 'error')
        return redirect(url_for('admin_login'))
    
    # Get approved signatures only
    signatures = Signature.query.filter_by(status='approved').all()
    
    if not signatures:
        flash('No approved signatures available for printing', 'error')
        return redirect(url_for('report'))
    
    # PDF generation settings
    page = landscape(letter)
    page_w, page_h = page
    margin = 0.5 * inch
    gutter = 0.20 * inch
    target_w = 2.4 * inch
    target_h = 1.2 * inch
    
    # Calculate grid
    avail_w = page_w - 2 * margin
    avail_h = page_h - 2 * margin
    cols = max(1, int((avail_w + gutter) // (target_w + gutter)))
    rows = max(1, int((avail_h + gutter) // (target_h + gutter)))
    cell_w = (avail_w - (cols - 1) * gutter) / cols
    cell_h = (avail_h - (rows - 1) * gutter) / rows
    cells_per_page = cols * rows
    
    # Create PDF
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=page)
    c.setTitle("Ranger Signatures")
    
    for page_index in range(math.ceil(len(signatures) / cells_per_page)):
        start = page_index * cells_per_page
        chunk = signatures[start:start + cells_per_page]
        
        for idx, sig in enumerate(chunk):
            r = idx // cols
            q = idx % cols
            x = margin + q * (cell_w + gutter)
            y_top = page_h - margin - r * (cell_h + gutter)
            y = y_top - cell_h
            
            try:
                # Load image from database
                img = Image.open(io.BytesIO(sig.image_data))
                img_w, img_h = img.size
                
                # Fit within cell
                scale = min(cell_w / img_w, cell_h / img_h)
                fit_w, fit_h = img_w * scale, img_h * scale
                
                # Center within cell
                img_x = x + (cell_w - fit_w) / 2
                img_y = y + (cell_h - fit_h) / 2
                
                c.drawInlineImage(img, img_x, img_y, width=fit_w, height=fit_h)
            except Exception as e:
                # Fallback text
                c.setFont("Helvetica-Oblique", 8)
                c.drawString(x + 4, y + cell_h / 2, f"[Error loading signature]")
        
        c.showPage()
    
    c.save()
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'ranger_signatures_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
