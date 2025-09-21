"""
UI Components cho Video Downloader Tool
Chứa các thành phần giao diện người dùng
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, 
                             QLabel, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class InputSection(QWidget):
    """Phần nhập liệu cho link video và cài đặt"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.link_input = None
        self.platform_display = None
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
        self.platform_display.setMinimumHeight(35)
        self.platform_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.platform_display.setFixedWidth(140)  # Tăng chiều rộng một chút
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
        
        # Thêm vào hàng đầu tiên (platform + input)
        first_row_layout.addWidget(self.platform_display)
        first_row_layout.addSpacing(10)  # Thêm khoảng cách giữa platform và input
        first_row_layout.addWidget(self.link_input)
        
        # Thêm hàng đầu tiên vào layout chính
        main_layout.addLayout(first_row_layout)
        
    def get_link_text(self):
        """Lấy text từ input link"""
        return self.link_input.text()
        
    def set_platform_display(self, text, style_sheet=None):
        """Cập nhật hiển thị platform"""
        self.platform_display.setText(text)
        if style_sheet:
            self.platform_display.setStyleSheet(style_sheet)
            


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
        
        # Các nút điều khiển với style 3D
        self.start_button = QPushButton("Bắt đầu tải")
        self.pause_button = QPushButton("Tạm dừng")
        self.clear_button = QPushButton("Xóa tất cả")
        self.search_button = QPushButton("Tìm kiếm")
        self.load_info_button = QPushButton("Load thông tin")
        
        # Áp dụng style 3D cho tất cả button
        button_style = self.get_3d_button_style()
        self.start_button.setStyleSheet(button_style)
        self.pause_button.setStyleSheet(button_style)
        self.clear_button.setStyleSheet(button_style)
        self.search_button.setStyleSheet(button_style)
        self.load_info_button.setStyleSheet(button_style)
        
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
        
    def get_3d_button_style(self):
        """Tạo style CSS cho button với màu xanh và border đậm hơn"""
        return """
            QPushButton {
                background-color: #4A90E2;
                border: 2px solid #2E5BBA;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 10px 16px;
                min-height: 18px;
                text-align: center;
            }
            
            QPushButton:hover {
                background-color: #5BA0F2;
                border-color: #3E6BCA;
            }
            
            QPushButton:pressed {
                background-color: #2E5BBA;
                border-color: #1E4A8A;
            }
            
            QPushButton:disabled {
                background-color: #999999;
                border-color: #666666;
                color: #CCCCCC;
            }
        """
