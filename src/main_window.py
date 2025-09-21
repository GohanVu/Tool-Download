"""
Main Window cho Video Downloader Tool
Chứa giao diện chính của ứng dụng
"""

import asyncio
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTableWidget, 
                             QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt
from .ui_components import InputSection, ControlSection
from .table_manager import VideoTableManager
from .platform_detector import PlatformDetector
from .database_manager import VideoDatabaseManager
from .constants import AppConfig

class VideoDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Khởi tạo các manager
        self.db_manager = VideoDatabaseManager()
        self.platform_detector = PlatformDetector()
        self.table_manager = None
        
        # Khởi tạo UI components
        self.input_section = None
        self.control_section = None
        
        self.init_ui()
        
    async def init_database(self):
        """Khởi tạo database và tạo bảng"""
        try:
            await self.db_manager.initialize('./video_downloader.db')
            # Tải dữ liệu sau khi khởi tạo database
            await self.load_data_from_db()
        except Exception as e:
            print(f"Lỗi khởi tạo database: {e}")
        
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        self.setWindowTitle(AppConfig.WINDOW_TITLE)
        self.setGeometry(100, 100, AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        
        # Khởi tạo các UI components
        self.input_section = InputSection()
        self.control_section = ControlSection()
        
        # Kết nối signals
        self.input_section.link_input.textChanged.connect(self.detect_platform)
        self.input_section.connect_start_button(self.start_download)
        self.control_section.connect_signals(
            self.pause_download,
            self.clear_all,
            self.search_videos,
            self.load_video_info
        )
        
        # Bảng hiển thị thông tin
        self.table = QTableWidget()
        self.table_manager = VideoTableManager(self.table)
        
        # Thêm các component vào layout
        main_layout.addWidget(self.input_section)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.control_section)
        
        
    def start_download(self):
        """Bắt đầu tải xuống"""
        QMessageBox.information(self, "Thông báo", "Chức năng tải xuống sẽ được triển khai!")
        
    def pause_download(self):
        """Tạm dừng tải xuống"""
        QMessageBox.information(self, "Thông báo", "Chức năng tạm dừng sẽ được triển khai!")
        
    def clear_all(self):
        """Xóa tất cả dữ liệu"""
        reply = QMessageBox.question(self, "Xác nhận", 
                                   "Bạn có chắc chắn muốn xóa tất cả dữ liệu?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            asyncio.create_task(self._clear_all_async())
            
    async def _clear_all_async(self):
        """Async function để xóa tất cả dữ liệu"""
        try:
            await self.db_manager.delete_all_videos()
            self.table_manager.clear_table()
            QMessageBox.information(self, "Thành công", "Đã xóa tất cả dữ liệu!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa dữ liệu: {str(e)}")
                
    def search_videos(self):
        """Tìm kiếm video"""
        keyword, ok = QInputDialog.getText(self, "Tìm kiếm", "Nhập từ khóa tìm kiếm:")
        if ok and keyword:
            asyncio.create_task(self._search_videos_async(keyword))
            
    def load_video_info(self):
        """Load thông tin video"""
        QMessageBox.information(self, "Thông báo", "Chức năng load thông tin video sẽ được triển khai!")
        
    def detect_platform(self, text):
        """Phát hiện platform từ link"""
        if not text.strip():
            display_text, style_sheet = self.platform_detector.get_default_display()
            self.input_section.set_platform_display(display_text, style_sheet)
            return
            
        display_text, style_sheet = self.platform_detector.get_platform_display_text(text)
        self.input_section.set_platform_display(display_text, style_sheet)
            
    async def _search_videos_async(self, keyword):
        """Async function để tìm kiếm video"""
        try:
            results = await self.db_manager.search_videos(keyword)
            self.table_manager.load_data(results)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm: {str(e)}")
            
    async def load_data_from_db(self):
        """Tải dữ liệu từ database vào bảng"""
        try:
            rows = await self.db_manager.get_all_videos()
            self.table_manager.load_data(rows)
        except Exception as e:
            print(f"Lỗi tải dữ liệu: {e}")
            
    async def update_video_status(self, record_id, status, progress=None):
        """Cập nhật trạng thái video"""
        try:
            await self.db_manager.update_video_status(record_id, status, progress)
            self.table_manager.update_video_status(record_id, status, progress)
        except Exception as e:
            print(f"Lỗi cập nhật trạng thái: {e}")
                    
    def closeEvent(self, event):
        """Đóng kết nối database khi đóng ứng dụng"""
        try:
            # Tạo event loop mới để đóng database
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.db_manager.close())
            loop.close()
        except Exception as e:
            print(f"Lỗi khi đóng database: {e}")
        event.accept()
