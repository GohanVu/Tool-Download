"""
Table Manager cho Video Downloader Tool
Quản lý bảng hiển thị dữ liệu video
"""

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QProgressBar, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .constants import TableColumns, COLUMN_HEADERS


class VideoTableManager:
    """Quản lý bảng hiển thị video"""
    
    def __init__(self, table_widget):
        self.table = table_widget
        self.setup_table()
        
    def setup_table(self):
        """Thiết lập bảng hiển thị"""
        self.table.setColumnCount(len(COLUMN_HEADERS))
        self.table.setHorizontalHeaderLabels(COLUMN_HEADERS)
        
        # Thiết lập kích thước cột
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(TableColumns.TITLE, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(TableColumns.ORIGINAL_LINK, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(TableColumns.FILE_PATH, QHeaderView.ResizeMode.Stretch)
        
        # Thiết lập font
        font = QFont()
        font.setPointSize(9)
        self.table.setFont(font)
        
        # Cho phép sắp xếp
        self.table.setSortingEnabled(True)
        
    def add_row(self, record_id, title, views, likes, duration, 
                status, progress, original_link, video_id, file_path):
        """Thêm một dòng mới vào bảng"""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        # Tạo progress bar cho cột tiến độ
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(progress)
        
        # Tạo các item cho bảng
        items = [
            QTableWidgetItem(str(title)),
            QTableWidgetItem(str(views)),
            QTableWidgetItem(str(likes)), 
            QTableWidgetItem(str(duration)),
            QTableWidgetItem(str(status)),
            QTableWidgetItem(f"{progress}%"),
            QTableWidgetItem(str(original_link)),
            QTableWidgetItem(str(video_id)),
            QTableWidgetItem(str(file_path)),
            QTableWidgetItem(str(record_id))
        ]
        
        for i, item in enumerate(items):
            self.table.setItem(row_position, i, item)
            
        self.table.setCellWidget(row_position, TableColumns.PROGRESS, progress_bar)
        
    def clear_table(self):
        """Xóa tất cả dữ liệu trong bảng"""
        self.table.setRowCount(0)
        
    def load_data(self, data_rows):
        """Tải dữ liệu vào bảng"""
        self.clear_table()
        for row in data_rows:
            self.add_row(*row)
            
    def update_video_status(self, record_id, status, progress=None):
        """Cập nhật trạng thái video trong bảng"""
        for row in range(self.table.rowCount()):
            if self.table.item(row, TableColumns.RECORD_ID).text() == str(record_id):
                self.table.item(row, TableColumns.STATUS).setText(status)
                if progress is not None:
                    self.table.item(row, TableColumns.PROGRESS).setText(f"{progress}%")
                    progress_bar = self.table.cellWidget(row, TableColumns.PROGRESS)
                    if progress_bar:
                        progress_bar.setValue(progress)
                break
                
    def get_selected_rows(self):
        """Lấy danh sách các dòng được chọn"""
        selected_rows = []
        for item in self.table.selectedItems():
            row = item.row()
            if row not in selected_rows:
                selected_rows.append(row)
        return selected_rows
        
    def get_row_data(self, row):
        """Lấy dữ liệu của một dòng"""
        if row >= self.table.rowCount():
            return None
            
        data = {}
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                data[col] = item.text()
            else:
                data[col] = ""
        return data
        
    def find_row_by_record_id(self, record_id):
        """Tìm dòng theo record ID"""
        for row in range(self.table.rowCount()):
            if self.table.item(row, TableColumns.RECORD_ID).text() == str(record_id):
                return row
        return -1
        
    def remove_row(self, row):
        """Xóa một dòng khỏi bảng"""
        if 0 <= row < self.table.rowCount():
            self.table.removeRow(row)
            
    def get_row_count(self):
        """Lấy số dòng trong bảng"""
        return self.table.rowCount()
