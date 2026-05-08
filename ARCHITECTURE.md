# Architecture & Development Notes

## System Architecture

```
┌─────────────────────────────────────────────┐
│          Web Browser (HTML/CSS/JS)          │
│         - Upload receipts                   │
│         - Manage expenses                   │
│         - Generate/download reports         │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST API
                   ▼
┌─────────────────────────────────────────────┐
│          Flask Web Server (app.py)          │
│  ┌─────────────────────────────────────┐    │
│  │      API Routes & Request Handler   │    │
│  └──────────────┬──────────────────────┘    │
│                 │                            │
│  ┌──────────────┴─────────┬────────────┐    │
│  ▼                        ▼            ▼    │
│ Upload          Database          File      │
│ Processing      Operations        I/O       │
└─────────────────────────────────────────────┘
       │                │              │
       ▼                ▼              ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ Receipt      │ │  SQLite DB  │ │ Image Files  │
│ Processor    │ │             │ │ (receipts)   │
│ (EasyOCR)    │ │ expenses.db │ │              │
└──────────────┘ └─────────────┘ └──────────────┘
       │
       ▼
┌──────────────────┐
│  Report Generator│
│  (ReportLab)     │
└────────┬─────────┘
         ▼
    PDF Files
```

## Module Breakdown

### 1. **app.py** - Flask Web Server
**Responsibility**: Central application hub
- **Routes**: Handles all HTTP requests
  - `/` - Serves the web interface
  - `/api/upload` - Receives receipt photos
  - `/api/expenses` - CRUD operations for expenses
  - `/api/summary` - Category totals
  - `/api/report` - PDF generation trigger

- **Key Features**:
  - File upload validation (size, type)
  - CORS handling (if needed)
  - Error handling and logging
  - Static file serving

- **Dependencies**: Flask, Werkzeug (file handling)

### 2. **models.py** - Database Layer
**Responsibility**: Data persistence
- **Database Initialization**: `init_db()` - Creates SQLite schema
- **Expense Model**: CRUD operations on expenses
  - `save()` - Insert new expense
  - `get_all()` - Retrieve all expenses
  - `update()` - Modify existing expense
  - `delete()` - Remove expense
  - `get_summary_by_category()` - Aggregated data

- **Database Schema**:
  ```
  expenses (table)
  ├── id (PRIMARY KEY)
  ├── vendor (TEXT)
  ├── amount (REAL)
  ├── date (TEXT) - YYYY-MM-DD format
  ├── category (TEXT)
  ├── description (TEXT)
  ├── receipt_image_path (TEXT)
  ├── extracted_text (TEXT) - OCR output
  └── created_at (TIMESTAMP)
  ```

### 3. **receipt_processor.py** - OCR Engine
**Responsibility**: Extract data from receipt images
- **ReceiptProcessor Class**:
  - `extract_text()` - Runs EasyOCR on image
  - `parse_amount()` - Regex to find currency amounts
  - `parse_date()` - Regex to find dates
  - `parse_vendor()` - Extract store name (first non-empty line)
  - `process_receipt()` - Orchestrates extraction
  - `validate_image()` - Ensure valid image file

- **OCR Logic**:
  - Uses EasyOCR with English language model
  - Falls back to manual entry if parsing fails
  - Regex patterns for common amount/date formats

- **Amount Detection**:
  - Looks for patterns like `$12.99`, `12,99`, `USD 50`
  - Returns the **largest amount** (assumes it's the total)

- **Date Detection**:
  - Supports multiple formats: MM/DD/YYYY, YYYY-MM-DD, etc.
  - Defaults to today if no date found

### 4. **report_generator.py** - PDF Creation
**Responsibility**: Generate professional expense reports
- **ReportGenerator Class**:
  - `generate_report()` - Main report creation
    - Fetches all expenses from database
    - Groups by category
    - Calculates subtotals and grand total
    - Formats with ReportLab styling

- **Report Components**:
  - Title and metadata section
  - Detailed table with date/vendor/amount/category
  - Subtotals by category
  - Summary table with counts
  - Professional styling and colors

- **Output**: PDF file saved to disk and returned to browser

### 5. **templates/index.html** - Frontend
**Responsibility**: User interface and interactions
- **Upload Section**:
  - Drag & drop or click to upload
  - Sends to `/api/upload` endpoint
  - Shows loading indicator

- **Expense Form**:
  - Manual entry of expenses
  - Category dropdown
  - Form validation
  - POST to `/api/expenses`

- **Expense Table**:
  - Lists all recorded expenses
  - Edit/Delete buttons
  - Sortable display

- **Report Generation**:
  - Tab to generate PDFs
  - Customizable title/preparer/invoice number
  - Downloads PDF to user's computer

- **JavaScript Features**:
  - Async API calls with Fetch
  - Real-time form validation
  - Modal dialog for editing
  - Tab switching
  - Automatic reload of data

## Data Flow

### Upload Receipt Flow:
1. User drops/selects image in browser
2. JavaScript sends file to `/api/upload`
3. Flask saves file and calls `ReceiptProcessor.process_receipt()`
4. EasyOCR extracts text from image
5. Regex patterns parse amount/date/vendor
6. JSON response sent to browser with extracted data
7. User reviews and edits if needed
8. Submit adds to database via `/api/expenses` POST
9. Expense saved to SQLite
10. UI refreshes to show new expense

### Generate Report Flow:
1. User clicks "Generate Report" button
2. Browser sends report options to `/api/report` POST
3. Flask fetches all expenses: `Expense.get_all()`
4. `ReportGenerator.generate_report()` called
5. ReportLab creates PDF with:
   - All expenses grouped by category
   - Category subtotals
   - Grand total
6. PDF saved to `expense_report.pdf`
7. Browser downloads file via `send_file()`
8. PDF ready to email with invoice

## Database Queries

### Get all expenses:
```sql
SELECT * FROM expenses ORDER BY date DESC
```

### Summary by category:
```sql
SELECT category, SUM(amount) as total, COUNT(*) as count
FROM expenses
GROUP BY category
ORDER BY category
```

### Get single expense:
```sql
SELECT * FROM expenses WHERE id = ?
```

## Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Server | Flask | REST API and web server |
| OCR | EasyOCR | Extract text from receipts |
| PDF Creation | ReportLab | Generate professional PDFs |
| Database | SQLite | Persistent data storage |
| Frontend | HTML/CSS/JS | User interface |
| Image Process | Pillow | Validate and handle images |

## Configuration

### app.py Settings:
```python
UPLOAD_FOLDER = 'uploads'              # Temp receipt storage
ALLOWED_EXTENSIONS = {'png', 'jpg', ...}  # Allowed file types
MAX_FILE_SIZE = 10 * 1024 * 1024       # 10MB limit
```

### Expense Categories (hardcoded):
```python
EXPENSE_CATEGORIES = [
    'Accommodation', 'Transportation', 'Meals',
    'Internet/Communications', 'Office Supplies',
    'Entertainment/Client Meeting', 'Other'
]
```

Make editable in future versions!

## Future Enhancements

### Phase 2 - Mid-term:
- [ ] Multi-user support with login
- [ ] Cloud storage for receipts
- [ ] Edit expense categories
- [ ] Recurring expenses
- [ ] Budget alerts

### Phase 3 - Long-term:
- [ ] Mobile app (React Native)
- [ ] Team collaboration
- [ ] Integration with accounting software
- [ ] Real-time expense sync
- [ ] Advanced analytics/reporting

## Performance Considerations

- **OCR Speed**: 2-10 seconds depending on image quality/size
- **Database**: SQLite fine for <10k expenses
- **File Uploads**: Limited to 10MB max
- **Caching**: Consider caching category summaries

## Security Notes

⚠️ **Current Status**: Development use only
- No authentication implemented yet
- All changes allowed (no role-based access)
- File uploads not sanitized for production
- Database not encrypted

**For production**:
- Add user authentication
- Implement role-based access control
- Use HTTPS/SSL
- Move to PostgreSQL
- Add input validation/sanitization
- Implement audit logging

## Debugging Tips

### Enable Flask Debug Mode:
```python
app.run(debug=True)  # Already enabled in app.py
```

### Check OCR Output:
```python
from receipt_processor import ReceiptProcessor
rp = ReceiptProcessor()
text = rp.extract_text('path/to/image.jpg')
print(text)
```

### Database Issues:
```bash
# Reset database
rm expenses.db
python app.py
```

### View Network Requests:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Watch API calls as you interact

---

**Happy coding! This is a solid foundation for building out more features.**
