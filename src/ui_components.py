"""
UI Components cho Video Downloader Tool
Chứa các thành phần giao diện người dùng
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QSpinBox, 
                             QLabel, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .constants import AppConfig


class InputSection(QWidget):
    """Phần nhập liệu cho link video và cài đặt"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.link_input = None
        self.platform_display = None
        self.threads_spinbox = None
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện phần nhập liệu"""
        layout = QHBoxLayout(self)
        
        # Line edit cho link
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Nhập link video...")
        self.link_input.setMinimumHeight(35)
        
        # Khu vực hiển thị platform
        self.platform_display = QLabel("Chưa chọn platform")
        self.platform_display.setMinimumHeight(35)
        self.platform_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.platform_display.setStyleSheet("""
            QLabel {
                padding: 8px 12px;
                border: 1px solid #666666;
                border-radius: 8px;
                background-color: #2A2A2A;
                color: #CCCCCC;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        
        # Spinbox cho số luồng tải xuống
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setRange(AppConfig.MIN_THREADS, AppConfig.MAX_THREADS)
        self.threads_spinbox.setValue(AppConfig.DEFAULT_THREADS)
        self.threads_spinbox.setMinimumHeight(35)
        
        threads_label = QLabel("Số luồng:")
        threads_label.setMinimumHeight(35)
        
        # Thêm các widget vào layout
        layout.addWidget(QLabel("Link Video:"))
        layout.addWidget(self.link_input)
        layout.addWidget(self.platform_display)
        layout.addWidget(threads_label)
        layout.addWidget(self.threads_spinbox)
        
    def get_link_text(self):
        """Lấy text từ input link"""
        return self.link_input.text()
        
    def set_platform_display(self, text, style_sheet=None):
        """Cập nhật hiển thị platform"""
        self.platform_display.setText(text)
        if style_sheet:
            self.platform_display.setStyleSheet(style_sheet)
            
    def get_threads_count(self):
        """Lấy số luồng được chọn"""
        return self.threads_spinbox.value()


class ControlSection(QWidget):
    """Phần điều khiển với các nút bấm"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_button = None
        self.pause_button = None
        self.clear_button = None
        self.search_button = None
        self.load_info_button = None
        self.auto_download_checkbox = None
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện phần điều khiển"""
        layout = QHBoxLayout(self)
        
        # Các nút điều khiển
        self.start_button = QPushButton("Bắt đầu tải")
        self.pause_button = QPushButton("Tạm dừng")
        self.clear_button = QPushButton("Xóa tất cả")
        self.search_button = QPushButton("Tìm kiếm")
        self.load_info_button = QPushButton("Load thông tin")
        
        # Checkbox cho tải ngay sau khi load
        self.auto_download_checkbox = QCheckBox("Tải ngay sau khi load")
        
        # Thêm vào layout
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.load_info_button)
        layout.addWidget(self.auto_download_checkbox)
        layout.addStretch()
        
    def connect_signals(self, start_callback, pause_callback, clear_callback, 
                       search_callback, load_info_callback):
        """Kết nối các signal với callback functions"""
        self.start_button.clicked.connect(start_callback)
        self.pause_button.clicked.connect(pause_callback)
        self.clear_button.clicked.connect(clear_callback)
        self.search_button.clicked.connect(search_callback)
        self.load_info_button.clicked.connect(load_info_callback)
        
    def is_auto_download_enabled(self):
        """Kiểm tra xem auto download có được bật không"""
        return self.auto_download_checkbox.isChecked()
