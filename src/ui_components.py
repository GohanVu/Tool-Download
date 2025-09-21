"""
UI Components cho Video Downloader Tool
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, 
                             QLabel, QCheckBox, QSpinBox)
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
        self.start_button = None
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện phần nhập liệu"""
        # Layout chính - căn giữa
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Container cho hàng đầu tiên (platform + input)
        first_row_layout = QHBoxLayout()
        first_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Khu vực hiển thị platform (di chuyển sang trái)
        self.platform_display = QLabel("Chưa chọn platform")
        self.platform_display.setMinimumHeight(47)
        self.platform_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.platform_display.setFixedWidth(140)  # Tăng chiều rộng một chút
        self.platform_display.setWordWrap(True)  # Cho phép xuống dòng
        self.platform_display.setStyleSheet("""
            QLabel {
                padding: 6px 8px;
                border: 1px solid #666666;
                border-radius: 8px;
                background-color: #2A2A2A;
                color: #CCCCCC;
                font-size: 10px;
                font-weight: 500;
            }
        """)
        
        # Line edit cho link
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Nhập link video...")
        self.link_input.setMinimumHeight(35)
        self.link_input.setFixedWidth(420)  # Tăng từ 300px lên 420px (300 * 1.4 = 420)
        
        # Spinbox cho số luồng
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setMinimum(AppConfig.MIN_THREADS)
        self.threads_spinbox.setMaximum(AppConfig.MAX_THREADS)
        self.threads_spinbox.setValue(AppConfig.DEFAULT_THREADS)
        self.threads_spinbox.setMinimumHeight(35)
        self.threads_spinbox.setFixedWidth(120)
        self.threads_spinbox.setPrefix("Số luồng: ")
        
        # Áp dụng styling cho spinbox với màu sáng hơn
        self.threads_spinbox.setStyleSheet("""
            QSpinBox {
                padding: 6px 8px;
                border: 1px solid #999999;
                border-radius: 8px;
                background-color: #F5F5F5;
                color: #333333;
                font-size: 11px;
                font-weight: 600;
                text-align: center;
            }
            
            QSpinBox:focus {
                border-color: #4A90E2;
                background-color: #FFFFFF;
            }
            
            QSpinBox::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 18px;
                border-left: 1px solid #CCCCCC;
                border-bottom: 1px solid #CCCCCC;
                border-top-right-radius: 8px;
                background-color: #E8E8E8;
            }
            
            QSpinBox::up-button:hover {
                background-color: #D0D0D0;
            }
            
            QSpinBox::up-button:pressed {
                background-color: #B8B8B8;
            }
            
            QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 18px;
                border-left: 1px solid #CCCCCC;
                border-top: 1px solid #CCCCCC;
                border-bottom-right-radius: 8px;
                background-color: #E8E8E8;
            }
            
            QSpinBox::down-button:hover {
                background-color: #D0D0D0;
            }
            
            QSpinBox::down-button:pressed {
                background-color: #B8B8B8;
            }
        """)
        
        # Thêm vào hàng đầu tiên (platform + input + spinbox)
        first_row_layout.addWidget(self.platform_display)
        first_row_layout.addSpacing(10)  # Thêm khoảng cách giữa platform và input
        first_row_layout.addWidget(self.link_input)
        first_row_layout.addSpacing(10)  # Thêm khoảng cách giữa input và spinbox
        first_row_layout.addWidget(self.threads_spinbox)
        
        # Thêm hàng đầu tiên vào layout chính
        main_layout.addLayout(first_row_layout)
        
        # Thêm button "Bắt đầu tải" căn giữa
        self.start_button = QPushButton("Bắt đầu tải")
        self.start_button.setMinimumHeight(45)  # Tăng chiều cao 40%
        self.start_button.setMinimumWidth(150)  # Tăng chiều rộng 40%
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                border: 2px solid #2E5BBA;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5BA0F2;
                border-color: #3E6BCA;
            }
            QPushButton:pressed {
                background-color: #2E5BBA;
                border-color: #1E4A8A;
            }
        """)
        
        # Layout cho button căn giữa
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
    def get_link_text(self):
        """Lấy text từ input link"""
        return self.link_input.text()
        
    def get_threads_count(self):
        """Lấy số luồng từ spinbox"""
        return self.threads_spinbox.value()
        
    def set_platform_display(self, text, style_sheet=None):
        """Cập nhật hiển thị platform"""
        self.platform_display.setText(text)
        if style_sheet:
            self.platform_display.setStyleSheet(style_sheet)
            
    def connect_start_button(self, callback):
        """Kết nối signal cho button bắt đầu tải"""
        self.start_button.clicked.connect(callback)
            


class ControlSection(QWidget):
    """Phần điều khiển với các nút bấm"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.pause_button = QPushButton("Tạm dừng")
        self.clear_button = QPushButton("Xóa tất cả")
        self.search_button = QPushButton("Tìm kiếm")
        self.load_info_button = QPushButton("Load thông tin")
        
        # Checkbox cho tải ngay sau khi load
        self.auto_download_checkbox = QCheckBox("Tải ngay sau khi load")
        
        # Thêm vào layout
        layout.addWidget(self.pause_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.load_info_button)
        layout.addWidget(self.auto_download_checkbox)
        layout.addStretch()
        
    def connect_signals(self, pause_callback, clear_callback, 
                       search_callback, load_info_callback):
        """Kết nối các signal với callback functions"""
        self.pause_button.clicked.connect(pause_callback)
        self.clear_button.clicked.connect(clear_callback)
        self.search_button.clicked.connect(search_callback)
        self.load_info_button.clicked.connect(load_info_callback)
        
    def is_auto_download_enabled(self):
        """Kiểm tra xem auto download có được bật không"""
        return self.auto_download_checkbox.isChecked()
