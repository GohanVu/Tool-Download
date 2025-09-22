"""
UI Components cho Video Downloader Tool
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, 
                             QLabel, QCheckBox, QSpinBox, QDialog,
                             QTextEdit, QSplitter, QFrame)
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
        self.multiple_links_title = None
        self.clear_multiple_links_button = None
        self.edit_multiple_links_button = None
        self.multiple_links_count = 0
        self.current_links = []
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
        self.link_input.setFixedWidth(620)  # Tăng từ 300px lên 620px (300 * 1.4 = 620)
        
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
        
        # Thêm tiêu đề "Tải nhiều link" căn giữa
        self.multiple_links_title = QLabel("Tải nhiều link ?")
        self.multiple_links_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.multiple_links_title.setStyleSheet("""
            QLabel {
                color: #4A90E2;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
            }
            QLabel:hover {
                color: #5BA0F2;
                text-decoration: underline;
            }
        """)
        self.multiple_links_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Layout cho tiêu đề căn giữa
        title_layout = QHBoxLayout()
        title_layout.addStretch()
        title_layout.addWidget(self.multiple_links_title)
        
        # Nút chỉnh sửa để edit multiple links (ẩn ban đầu)
        self.edit_multiple_links_button = QPushButton("...")
        self.edit_multiple_links_button.setFixedSize(25, 25)
        self.edit_multiple_links_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: 1px solid #388E3C;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
                border-color: #43A047;
            }
            QPushButton:pressed {
                background-color: #388E3C;
                border-color: #2E7D32;
            }
        """)
        self.edit_multiple_links_button.hide()  # Ẩn ban đầu
        
        # Nút X đỏ để xóa multiple links (ẩn ban đầu)
        self.clear_multiple_links_button = QPushButton("✕")
        self.clear_multiple_links_button.setFixedSize(25, 25)
        self.clear_multiple_links_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                border: 1px solid #CC0000;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FF6666;
                border-color: #FF0000;
            }
            QPushButton:pressed {
                background-color: #CC0000;
                border-color: #990000;
            }
        """)
        self.clear_multiple_links_button.hide()  # Ẩn ban đầu
        
        title_layout.addWidget(self.edit_multiple_links_button)
        title_layout.addWidget(self.clear_multiple_links_button)
        title_layout.addStretch()
        
        main_layout.addLayout(title_layout)
        
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
        # Không cho phép thay đổi platform display khi đang ở chế độ multiple links
        if self.is_multiple_links_mode():
            return
            
        self.platform_display.setText(text)
        if style_sheet:
            self.platform_display.setStyleSheet(style_sheet)
            
    def connect_start_button(self, callback):
        """Kết nối signal cho button bắt đầu tải"""
        self.start_button.clicked.connect(callback)
        
    def connect_multiple_links_title(self, callback):
        """Kết nối signal cho tiêu đề tải nhiều link"""
        self.multiple_links_title.mousePressEvent = lambda event: callback()
        
    def connect_clear_multiple_links_button(self, callback):
        """Kết nối signal cho nút xóa multiple links"""
        self.clear_multiple_links_button.clicked.connect(callback)
        
    def connect_edit_multiple_links_button(self, callback):
        """Kết nối signal cho nút chỉnh sửa multiple links"""
        self.edit_multiple_links_button.clicked.connect(callback)
        
    def set_multiple_links_mode(self, links_count, links_list=None):
        """Chuyển sang chế độ multiple links"""
        self.multiple_links_count = links_count
        if links_list:
            self.current_links = links_list.copy()
        
        # Clear text hiện tại và cập nhật link input placeholder
        self.link_input.clear()
        self.link_input.setPlaceholderText(f"✅ Đã thêm {links_count} link")
        self.link_input.setReadOnly(True)
        self.link_input.setStyleSheet("""
            QLineEdit {
                background-color: #1A3A1A;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                color: #4CAF50;
                font-weight: bold;
                padding: 8px 12px;
                font-size: 13px;
            }
        """)
        
        # Cập nhật platform display để hiển thị "Chế độ tải nhiều"
        self.platform_display.setText("Chế độ tải nhiều")
        self.platform_display.setStyleSheet("""
            QLabel {
                padding: 6px 8px;
                border: 1px solid #666666;
                border-radius: 8px;
                background-color: #2A2A2A;
                color: #CCCCCC;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        
        # Vô hiệu hóa tiêu đề multiple links
        self.multiple_links_title.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                font-weight: bold;
                cursor: default;
            }
        """)
        self.multiple_links_title.setCursor(Qt.CursorShape.ArrowCursor)
        
        # Hiển thị nút chỉnh sửa và nút X đỏ
        self.edit_multiple_links_button.show()
        self.clear_multiple_links_button.show()
        
        # Cập nhật text button bắt đầu tải
        self.start_button.setText(f"Bắt đầu tải ({links_count})")
        
    def clear_multiple_links_mode(self):
        """Xóa chế độ multiple links, trở về bình thường"""
        self.multiple_links_count = 0
        self.current_links = []
        
        # Khôi phục link input
        self.link_input.setPlaceholderText("Nhập link video...")
        self.link_input.setReadOnly(False)
        self.link_input.setStyleSheet("""
            QLineEdit {
                background-color: #2A2A2A;
                border: 1px solid #666666;
                border-radius: 8px;
                color: #CCCCCC;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                background-color: #333333;
            }
        """)
        
        # Khôi phục platform display về trạng thái mặc định
        self.platform_display.setText("Chưa chọn platform")
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
        
        # Khôi phục tiêu đề multiple links
        self.multiple_links_title.setStyleSheet("""
            QLabel {
                color: #4A90E2;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
            }
            QLabel:hover {
                color: #5BA0F2;
                text-decoration: underline;
            }
        """)
        self.multiple_links_title.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Ẩn nút chỉnh sửa và nút X đỏ
        self.edit_multiple_links_button.hide()
        self.clear_multiple_links_button.hide()
        
        # Khôi phục text button bắt đầu tải
        self.start_button.setText("Bắt đầu tải")
        
    def get_multiple_links_count(self):
        """Lấy số lượng multiple links"""
        return self.multiple_links_count
        
    def is_multiple_links_mode(self):
        """Kiểm tra có đang ở chế độ multiple links không"""
        return self.multiple_links_count > 0
        
    def get_current_links(self):
        """Lấy danh sách links hiện tại"""
        return self.current_links.copy()
            


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


class MultipleLinksDialog(QDialog):
    """Cửa sổ nhập nhiều link video"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.links_text_edit = None
        self.confirm_button = None
        self.cancel_button = None
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện cửa sổ nhiều link"""
        self.setWindowTitle("Tải nhiều link video")
        self.setFixedSize(800, 600)
        self.setModal(True)
        
        # Layout chính
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Tạo splitter để chia 2/8
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Phần hướng dẫn (2/10)
        instruction_frame = QFrame()
        instruction_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        instruction_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border: 1px solid #666666;
                border-radius: 8px;
            }
        """)
        
        instruction_layout = QVBoxLayout(instruction_frame)
        instruction_layout.setContentsMargins(15, 15, 15, 15)
        
        instruction_title = QLabel("Hướng dẫn")
        instruction_title.setStyleSheet("""
            QLabel {
                color: #4A90E2;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        
        instruction_text = QLabel("""
• Nhập mỗi link video trên một dòng
• Hỗ trợ các platform: YouTube, TikTok, Instagram, Facebook
• Có thể nhập tối đa 50 link cùng lúc
• Các link không hợp lệ sẽ được bỏ qua
• Nhấn Enter để xuống dòng mới
        """)
        instruction_text.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        instruction_text.setWordWrap(True)
        
        instruction_layout.addWidget(instruction_title)
        instruction_layout.addWidget(instruction_text)
        instruction_layout.addStretch()
        
        # Phần nhập link (8/10)
        links_frame = QFrame()
        links_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        links_frame.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border: 1px solid #666666;
                border-radius: 8px;
            }
        """)
        
        links_layout = QVBoxLayout(links_frame)
        links_layout.setContentsMargins(15, 15, 15, 15)
        
        links_title = QLabel("Danh sách link video")
        links_title.setStyleSheet("""
            QLabel {
                color: #4A90E2;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        
        self.links_text_edit = QTextEdit()
        self.links_text_edit.setPlaceholderText("Nhập các link video, mỗi link trên một dòng...")
        self.links_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1A1A1A;
                border: 1px solid #666666;
                border-radius: 6px;
                color: #CCCCCC;
                font-size: 13px;
                padding: 10px;
                selection-background-color: #4A90E2;
            }
            QTextEdit:focus {
                border-color: #4A90E2;
            }
        """)
        
        links_layout.addWidget(links_title)
        links_layout.addWidget(self.links_text_edit)
        
        # Thêm vào splitter với tỷ lệ 2:8
        splitter.addWidget(instruction_frame)
        splitter.addWidget(links_frame)
        splitter.setSizes([160, 640])  # 2:8 ratio (200:800 total)
        
        main_layout.addWidget(splitter)
        
        # Phần button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Hủy")
        self.cancel_button.setFixedSize(100, 35)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                border: 1px solid #555555;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        
        self.confirm_button = QPushButton("Xác nhận")
        self.confirm_button.setFixedSize(100, 35)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                border: 1px solid #2E5BBA;
                border-radius: 6px;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5BA0F2;
            }
            QPushButton:pressed {
                background-color: #2E5BBA;
            }
        """)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.confirm_button)
        
        main_layout.addLayout(button_layout)
        
        # Kết nối signals
        self.cancel_button.clicked.connect(self.reject)
        self.confirm_button.clicked.connect(self.accept)
        
    def get_links(self):
        """Lấy danh sách các link từ text edit"""
        text = self.links_text_edit.toPlainText().strip()
        if not text:
            return []
        
        # Tách các link theo dòng và loại bỏ dòng trống
        links = [link.strip() for link in text.split('\n') if link.strip()]
        return links
        
    def set_links(self, links):
        """Đặt danh sách links vào text edit"""
        if links:
            links_text = '\n'.join(links)
            self.links_text_edit.setPlainText(links_text)
        else:
            self.links_text_edit.clear()
