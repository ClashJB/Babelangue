import webview
import threading
import sys
import os
from flasktest_2 import app

def start_flask():
    """Start Flask server in a separate thread"""
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def main():
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    import time
    time.sleep(1)
    
    window = webview.create_window(
        'BABELANGUE',
        'http://127.0.0.1:5000',
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False,
        min_size=(800, 600)
    )
    
    webview.start()

if __name__ == '__main__':
    main()