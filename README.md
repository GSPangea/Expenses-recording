# Expense Recorder 💰

A modern web application to quickly capture receipt images using OCR, organize expenses, and generate professional PDF reports for business expense justification.

## Features

✨ **Core Features:**
- 📸 **Receipt OCR**: Upload receipt photos and automatically extract vendor, amount, and date information
- ✏️ **Manual Entry**: Add expenses manually or edit extracted data
- 📊 **Categorization**: Organize expenses into predefined business categories
- 📄 **PDF Reports**: Generate professional expense reports grouped by category with totals
- 📋 **Expense Management**: View, edit, and delete individual expenses
- 📈 **Summary Dashboard**: See expense totals by category at a glance

## Tech Stack

- **Backend**: Python with Flask
- **OCR**: EasyOCR for receipt text extraction
- **PDF Generation**: ReportLab for professional report creation
- **Database**: SQLite for expense storage
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Image Processing**: Pillow

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone or navigate to the repository:**
   ```bash
   cd Expenses-recording
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   *Note: First run will download the EasyOCR model (~100MB), which may take a few minutes.*

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   Navigate to `http://127.0.0.1:5000` or `http://localhost:5000`

## Usage

### Uploading Receipts

1. Click the **"Upload Receipt"** section or drag & drop an image
2. The app will automatically extract:
   - Amount/total
   - Vendor/store name
   - Date
3. Review and edit the extracted information if needed
4. Select a category and add optional notes
5. Click **"Add Expense"**

### Manual Entry

1. Use the **"Add Expense"** form to enter expenses manually
2. Fill in:
   - Vendor/Store Name
   - Amount
   - Date
   - Category
   - Description (optional)
3. Click **"Add Expense"**

### Expense Management

- **View**: All expenses appear in the list with date, vendor, category, and amount
- **Edit**: Click the "Edit" button to modify any expense
- **Delete**: Click "Delete" to remove an expense

### Generating Reports

1. Go to the **"Generate Report"** tab
2. Enter (optional):
   - Report Title
   - Prepared By (your name)
   - Invoice/Reference Number
3. Click **"Generate & Download PDF"**
4. The PDF will contain:
   - Detailed expense list grouped by category
   - Subtotals for each category
   - Grand total
   - Summary table with expense counts

## Project Structure

```
Expenses-recording/
├── app.py                    # Flask web server and API endpoints
├── models.py                 # Database models and SQL operations
├── receipt_processor.py      # OCR logic for receipt processing
├── report_generator.py       # PDF generation utilities
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web interface
├── uploads/                 # Temporary receipt image storage
├── expenses.db              # SQLite database (created on first run)
└── README.md               # This file
```

## Supported Image Formats

- PNG, JPG/JPEG, GIF, BMP
- Maximum file size: 10MB

## Expense Categories

- Accommodation
- Transportation
- Meals
- Internet/Communications
- Office Supplies
- Entertainment/Client Meeting
- Other

## Tips for Best Results

1. **Receipt Quality**: Use clear, well-lit photos of receipts
2. **Angle**: Photograph receipts straight-on, not at an angle
3. **Focus**: Ensure the amount and vendor name are clearly visible
4. **Review**: Always review OCR-extracted data for accuracy before saving

## Features Coming Soon

- 🔐 Multi-user support with authentication
- 📱 Mobile app (React Native)
- 🏢 Team expense tracking
- 🔗 Integration with popular accounting software
- 🎨 Customizable expense categories
- 📧 Email report delivery
- 💾 Cloud backup and sync

## Troubleshooting

### OCR Not Extracting Amount

- Ensure the receipt has a clear total/amount shown
- Try different lighting or angles when photographing
- Manually enter the amount if OCR fails

### SQLite Database Errors

Delete `expenses.db` and restart the app to reset the database

### Large File Upload Issues

Ensure your receipt images are under 10MB. Compress if needed.

## License

This project is open source and available for personal and business use.

## Support

For issues or suggestions, please create an issue in the repository.

---

**Built with ❤️ for business expense tracking**