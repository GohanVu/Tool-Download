"""
Entry point cho Video Downloader Tool
"""

import sys
import asyncio
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from src.main_window import VideoDownloaderApp

def main():
    app = QApplication(sys.argv)
    window = VideoDownloaderApp()
    
    # Sử dụng QTimer để khởi tạo database sau khi event loop đã chạy
    def init_database_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(window.init_database())
        loop.close()
    
    # Chạy init database sau 100ms
    QTimer.singleShot(100, init_database_async)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
