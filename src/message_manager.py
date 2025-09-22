"""
Message Manager cho Video Downloader Tool
Quản lý tất cả các thông báo và dialog trong ứng dụng
"""

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject


class MessageManager(QObject):
    """Quản lý tất cả các thông báo trong ứng dụng"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
    
    def show_info(self, title, message):
        """Hiển thị thông báo thông tin"""
        QMessageBox.information(self.parent, title, message)
    
    def show_warning(self, title, message):
        """Hiển thị thông báo cảnh báo"""
        QMessageBox.warning(self.parent, title, message)
    
    def show_error(self, title, message):
        """Hiển thị thông báo lỗi"""
        QMessageBox.critical(self.parent, title, message)
    
    def show_question(self, title, message, default_button=QMessageBox.StandardButton.No):
        """Hiển thị câu hỏi xác nhận"""
        reply = QMessageBox.question(
            self.parent, 
            title, 
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            default_button
        )
        return reply == QMessageBox.StandardButton.Yes
    
    # Các thông báo cụ thể cho ứng dụng
    def download_started(self, links_count=None):
        """Thông báo bắt đầu tải"""
        if links_count:
            self.show_info("Thông báo", f"Bắt đầu tải {links_count} link. Chức năng tải xuống sẽ được triển khai!")
        else:
            self.show_info("Thông báo", "Chức năng tải xuống sẽ được triển khai!")
    
    def download_paused(self):
        """Thông báo tạm dừng tải"""
        self.show_info("Thông báo", "Chức năng tạm dừng sẽ được triển khai!")
    
    def clear_all_confirm(self):
        """Xác nhận xóa tất cả dữ liệu"""
        return self.show_question(
            "Xác nhận", 
            "Bạn có chắc chắn muốn xóa tất cả dữ liệu?",
            QMessageBox.StandardButton.No
        )
    
    def clear_all_success(self):
        """Thông báo xóa tất cả thành công"""
        self.show_info("Thành công", "Đã xóa tất cả dữ liệu!")
    
    def clear_all_error(self, error_msg):
        """Thông báo lỗi khi xóa tất cả"""
        self.show_error("Lỗi", f"Không thể xóa dữ liệu: {error_msg}")
    
    def search_placeholder(self):
        """Thông báo tìm kiếm"""
        self.show_info("Thông báo", "Chức năng tìm kiếm sẽ được triển khai!")
    
    def search_error(self, error_msg):
        """Thông báo lỗi tìm kiếm"""
        self.show_error("Lỗi", f"Lỗi tìm kiếm: {error_msg}")
    
    def load_info_placeholder(self):
        """Thông báo load thông tin"""
        self.show_info("Thông báo", "Chức năng load thông tin video sẽ được triển khai!")
    
    # Multiple Links Messages
    def multiple_links_already_exists(self, links_count):
        """Thông báo đã có multiple links"""
        self.show_info(
            "Thông báo",
            f"Đã có {links_count} link.\n"
            "Nhấn nút X đỏ để xóa và thêm link mới.\n"
            "Nhấn nút ... để chỉnh sửa."
        )
    
    def multiple_links_added_success(self, links_count):
        """Thông báo thêm multiple links thành công"""
        self.show_info("Thành công", f"Đã thêm {links_count} link vào danh sách tải!")
    
    def multiple_links_empty_warning(self):
        """Cảnh báo chưa nhập link"""
        self.show_warning("Cảnh báo", "Vui lòng nhập ít nhất một link!")
    
    def multiple_links_clear_confirm(self):
        """Xác nhận xóa danh sách links"""
        return self.show_question(
            "Xác nhận xóa", 
            "Bạn có chắc chắn muốn xóa danh sách link hiện tại?",
            QMessageBox.StandardButton.No
        )
    
    def multiple_links_cleared_success(self):
        """Thông báo xóa danh sách links thành công"""
        self.show_info("Thông báo", "Đã xóa danh sách link!")
    
    def multiple_links_updated_success(self, links_count):
        """Thông báo cập nhật danh sách links thành công"""
        self.show_info("Thành công", f"Đã cập nhật {links_count} link!")
    
    def multiple_links_edit_empty_warning(self):
        """Cảnh báo chỉnh sửa với danh sách trống"""
        self.show_warning("Cảnh báo", "Vui lòng nhập ít nhất một link!")
