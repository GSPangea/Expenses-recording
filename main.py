import threading
import webview
from app import app

def _run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=_run_flask, daemon=True)
    t.start()

    webview.create_window(
        'Expense Tracker',
        'http://localhost:5000',
        width=1200,
        height=800,
        min_size=(800, 600),
    )
    webview.start()
