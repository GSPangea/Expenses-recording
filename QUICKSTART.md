# Quick Start Guide 🚀

Get up and running with Expense Recorder in 5 minutes!

## One-Command Setup (Linux/Mac)

```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python app.py
```

## Step-by-Step Setup (All Platforms)

### 1. Create & Activate Virtual Environment
```bash
# Create
python -m venv venv

# Activate (choose based on your OS)
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

⏳ *First time may take 2-3 minutes as it downloads the OCR model*

### 3. Run the Application
```bash
python app.py
```

✅ You should see:
```
WARNING in app.run_simple: This is a development server. Do not use it in production deployments.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```

### 4. Open in Browser
Go to: **http://localhost:5000**

## First Use Walkthrough

### Upload Your First Receipt

1. **Click the upload area** or drag & drop a receipt photo
2. **Wait for processing** (a few seconds for OCR)
3. **Review extracted data**:
   - Vendor name
   - Amount
   - Date
4. **Select category** (e.g., "Meals", "Transportation")
5. **Add notes** (optional)
6. **Click "Add Expense"** ✅

### Manual Entry

1. **Fill in the form** on the right side
2. **Add Expense** - Done!

### Generate a Report

1. **Go to "Expenses"** tab
2. **Click "Generate Report"** tab
3. **Download PDF** with all expenses by category

## File Locations

- **Database**: `expenses.db` (auto-created in project folder)
- **Uploads**: `uploads/` folder (temporary storage)
- **Generated PDFs**: Downloaded to your Downloads folder

## Keyboard Shortcuts

- `Ctrl+Shift+C` - Focus upload area
- `Tab` - Navigate between form fields
- `Enter` - Submit form

## Common Issues & Solutions

### Issue: ModuleNotFoundError for easyocr
**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: OCR not extracting the amount
**Solution**: 
- Try a clearer photo of the receipt
- Ensure total/amount is clearly visible
- Manually enter if needed

### Issue: Port 5000 already in use
**Solution**: Edit `app.py` line near bottom, change port:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

### Issue: Database locked
**Solution**: Delete `expenses.db` and restart the app

## Performance Tips

- **Larger receipts** (high resolution) = Slower OCR (up to 10 seconds)
- **Clear lighting** in photos = Better extraction accuracy
- Keep **uploads folder** clean to free up storage

## Next Steps

1. ✅ Add a few sample expenses
2. ✅ Try generating a PDF report
3. ✅ Edit an expense to see validation
4. ✅ Categorize expenses properly for reports

## For Production Deployment

Not recommended for production use yet, but to deploy:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up a proper database (PostgreSQL)
3. Enable authentication
4. Use HTTPS/SSL

## Need Help?

- Check the full [README.md](README.md)
- Review [app.py](app.py) comments
- Check browser console (F12) for JavaScript errors

---

**Happy expense tracking! 💰**
