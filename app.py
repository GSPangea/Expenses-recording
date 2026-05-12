from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from models import Expense, init_db
from receipt_processor import ReceiptProcessor
from report_generator import ReportGenerator
import io

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# Initialize database
init_db()

# Initialize processors
receipt_processor = ReceiptProcessor()
report_generator = ReportGenerator()

# Expense categories
EXPENSE_CATEGORIES = [
    'Accommodation',
    'Transportation',
    'Meals',
    'Internet/Communications',
    'Office Supplies',
    'Entertainment/Client Meeting',
    'Other'
]

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main dashboard page."""
    expenses = Expense.get_all()
    summary = Expense.get_summary_by_category()
    return render_template('index.html', expenses=expenses, summary=summary, categories=EXPENSE_CATEGORIES)

@app.route('/api/upload', methods=['POST'])
def upload_receipt():
    """Upload and process a receipt image."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, PDF'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validate it's a real image
        if not receipt_processor.validate_file(filepath):
            os.remove(filepath)
            return jsonify({'success': False, 'error': 'Invalid or unreadable file'}), 400
        
        # Process receipt with OCR
        result = receipt_processor.process_receipt(filepath)
        
        if not result['success']:
            os.remove(filepath)
            return jsonify({'success': False, 'error': result['error']}), 400
        
        return jsonify({
            'success': True,
            'amount': result['amount'],
            'date': result['date'],
            'vendor': result['vendor'],
            'raw_text': result['raw_text'],
            'filepath': filepath
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses."""
    expenses = Expense.get_all()
    return jsonify([dict(exp) for exp in expenses])

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    """Create a new expense record."""
    data = request.json
    
    try:
        expense = Expense(
            vendor=data.get('vendor', 'Unknown'),
            amount=float(data.get('amount', 0)),
            date=data.get('date', ''),
            category=data.get('category', 'Other'),
            description=data.get('description', ''),
            receipt_image_path=data.get('filepath', ''),
            extracted_text=data.get('raw_text', '')
        )
        expense_id = expense.save()
        return jsonify({'success': True, 'id': expense_id})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an expense record."""
    data = request.json
    
    try:
        Expense.update(
            expense_id,
            vendor=data.get('vendor'),
            amount=float(data.get('amount')),
            date=data.get('date'),
            category=data.get('category'),
            description=data.get('description', '')
        )
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense."""
    try:
        Expense.delete(expense_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/report', methods=['POST'])
def generate_report():
    """Generate and download expense report as PDF."""
    data = request.json
    
    try:
        # Generate report to bytes
        report_path = 'expense_report.pdf'
        
        report_generator.generate_report(
            report_path,
            title=data.get('title', 'Business Expense Report'),
            preparer=data.get('preparer', ''),
            invoice_number=data.get('invoice_number', '')
        )
        
        return send_file(report_path, as_attachment=True, download_name='expense_report.pdf')
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get expense summary by category."""
    summary = Expense.get_summary_by_category()
    return jsonify([{'category': cat, 'total': total, 'count': count} for cat, total, count in summary])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
