"""
Main Window cho Video Downloader Tool
Chứa giao diện chính của ứng dụng
"""

import asyncio
import time
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTableWidget, 
                             QInputDialog)
from PyQt6.QtCore import Qt, QTimer

from src.yt_loader import YoutuberAssistant
from .ui_components import InputSection, ControlSection, MultipleLinksDialog
from .table_manager import VideoTableManager
from .platform_detector import PlatformDetector
from .database_manager import VideoDatabaseManager
from .message_manager import MessageManager
from .constants import AppConfig

class VideoDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Khởi tạo các manager
        self.db_manager = VideoDatabaseManager()
        self.platform_detector = PlatformDetector()
        self.message_manager = MessageManager(self)
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
        self.input_section.connect_multiple_links_title(self.open_multiple_links_dialog)
        self.input_section.connect_clear_multiple_links_button(self.clear_multiple_links)
        self.input_section.connect_edit_multiple_links_button(self.edit_multiple_links)
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
        # Cập nhật trạng thái loading
        self.control_section.set_loading_status("Đang bắt đầu tải...")
        
        # Lấy giá trị filter
        filter_values = self.input_section.get_filter_values()
        
        if self.input_section.is_multiple_links_mode():
            links_count = self.input_section.get_multiple_links_count()
            self.message_manager.download_started(links_count)
            self.control_section.set_loading_status(f"Đang tải {links_count} video...")
            print(f"Filter values: {filter_values}")
        else:
            self.message_manager.download_started()
            self.control_section.set_loading_status("Đang tải video...")
            print(f"Filter values: {filter_values}")
        
    def open_multiple_links_dialog(self):
        """Mở cửa sổ nhập nhiều link"""
        # Kiểm tra nếu đã ở chế độ multiple links
        if self.input_section.is_multiple_links_mode():
            links_count = self.input_section.get_multiple_links_count()
            self.message_manager.multiple_links_already_exists(links_count)
            return
            
        dialog = MultipleLinksDialog(self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            links = dialog.get_links()
            if links:
                # Chuyển sang chế độ multiple links
                self.input_section.set_multiple_links_mode(len(links), links)
                self.message_manager.multiple_links_added_success(len(links))
                print(f"Danh sách link: {links}")
            else:
                self.message_manager.multiple_links_empty_warning()
                
    def clear_multiple_links(self):
        """Xóa chế độ multiple links"""
        if self.message_manager.multiple_links_clear_confirm():
            self.input_section.clear_multiple_links_mode()
            self.message_manager.multiple_links_cleared_success()
        
    def edit_multiple_links(self):
        """Chỉnh sửa danh sách multiple links"""
        if not self.input_section.is_multiple_links_mode():
            return
            
        # Lấy danh sách links hiện tại
        current_links = self.input_section.get_current_links()
        
        # Mở dialog với links hiện tại
        dialog = MultipleLinksDialog(self)
        dialog.set_links(current_links)
        
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_links = dialog.get_links()
            if new_links:
                # Cập nhật danh sách links mới
                self.input_section.set_multiple_links_mode(len(new_links), new_links)
                self.message_manager.multiple_links_updated_success(len(new_links))
                print(f"Danh sách link mới: {new_links}")
            else:
                self.message_manager.multiple_links_edit_empty_warning()
        
    def pause_download(self):
        """Tạm dừng tải xuống"""
        try:
            self.yt_assistant._isForceClosed = True
        except Exception as e:
            pass
        self.message_manager.download_paused()
        self.control_section.set_info_status("Đã tạm dừng")
        
    def clear_all(self):
        """Xóa tất cả dữ liệu"""
        if self.message_manager.clear_all_confirm():
            asyncio.create_task(self._clear_all_async())
            
    async def _clear_all_async(self):
        """Async function để xóa tất cả dữ liệu"""
        try:
            self.control_section.set_loading_status("Đang xóa dữ liệu...")
            await self.db_manager.delete_all_videos()
            self.table_manager.clear_table()
            self.message_manager.clear_all_success()
            self.control_section.set_success_status("Đã xóa tất cả")
        except Exception as e:
            self.message_manager.clear_all_error(str(e))
            self.control_section.set_error_status("Lỗi xóa dữ liệu")
                
    def search_videos(self):
        """Tìm kiếm video"""
        keyword, ok = QInputDialog.getText(self, "Tìm kiếm", "Nhập từ khóa tìm kiếm:")
        if ok and keyword:
            self.control_section.set_loading_status("Đang tìm kiếm...")
            asyncio.create_task(self._search_videos_async(keyword))
            
    def load_video_info(self):
        """Load thông tin video"""
        # Cập nhật trạng thái loading
        self.control_section.set_loading_status("Đang load thông tin...")
        
        # Lấy 7 giá trị từ các ô input và filter
        platform = self.input_section.platform_display.text()
        link = self.input_section.link_input.text()
        threads = self.input_section.threads_spinbox.value()
        
        # Lấy giá trị từ filter
        filter_values = self.input_section.get_filter_values()
        max_videos = filter_values['max_videos']
        min_views = filter_values['min_videos']  # Lưu ý: tên method là get_min_videos nhưng thực tế là min_views
        min_likes = filter_values['min_likes']
        min_duration = filter_values['min_duration']
        
        
        self.yt_assistant = YoutuberAssistant(platform, link, threads, max_videos, min_views, min_likes, min_duration)
        self.yt_assistant.load_info_signal.connect(self.load_info_signal)
        self.yt_assistant.update_rowInfo_signal.connect(self.update_rowInfo_signal)
        # self.mang.append(yt_assistant)
        self.yt_assistant.start()
        
        # self.message_manager.load_info_placeholder()
    
    def update_rowInfo_signal(self, data, dal):
        """Cập nhật dữ liệu vào bảng và database"""
        # Cập nhật bảng UI trước
        self.table_manager.add_video_row(data)
        
        # Tự động insert vào database sử dụng QTimer
        def insert_to_db():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._insert_video_to_db(data))
                loop.close()
            except Exception as e:
                print(f"Lỗi insert video vào database: {e}")
        
        QTimer.singleShot(0, insert_to_db)
    
    
    def load_info_signal(self, value, message):
        # print(f'load_info_signal: {value}')
        # Cập nhật trạng thái khi nhận signal
        if value:
            # self.control_section.set_success_status("Load thông tin thành công")
            self.control_section.status_label.show()
            self.control_section.status_label.setText(message)
        else:
            self.control_section.status_label.hide()
            # self.control_section.set_error_status("Load thông tin thất bại")
        
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
            self.control_section.set_success_status(f"Tìm thấy {len(results)} kết quả")
        except Exception as e:
            self.message_manager.search_error(str(e))
            self.control_section.set_error_status("Lỗi tìm kiếm")
            
    async def load_data_from_db(self):
        """Tải dữ liệu từ database vào bảng"""
        try:
            rows = await self.db_manager.get_all_videos()
            self.table_manager.load_data(rows)
        except Exception as e:
            print(f"Lỗi tải dữ liệu: {e}")
            
    async def _insert_video_to_db(self, video_data):
        """Insert video data vào database"""
        try:
            await self.db_manager.insert_video(video_data)
            print(f"Đã lưu video: {video_data.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Lỗi lưu video vào database: {e}")
            
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
