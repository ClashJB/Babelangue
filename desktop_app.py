import webview
import threading
import sys
import os
from flasktest_2 import app

def start_flask():
    """Start Flask server in a separate thread"""
    # Disable Flask's reloader and debug mode for production
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def main():
    # Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    import time
    time.sleep(1)
    
    # Create desktop window
    window = webview.create_window(
        'BABELANGUE',
        'http://127.0.0.1:5000',
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600)
    )
    
    # Start the GUI loop
    webview.start()

if __name__ == '__main__':
    main()