"""
Main Window cho Video Downloader Tool
Chứa giao diện chính của ứng dụng
"""

import asyncio
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QSpinBox, QTableWidget, 
                             QTableWidgetItem, QLabel, QProgressBar, QHeaderView, 
                             QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont
from .DBF import Database, insert_db, fetch_all, fetch_one, update_db
from .constants import (TableColumns, COLUMN_HEADERS, DownloadStatus, AppConfig)

class VideoDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = None
        self.init_ui()
        # Database sẽ được khởi tạo từ main.py
        
    async def init_database(self):
        """Khởi tạo database và tạo bảng"""
        try:
            self.db = await Database.get_instance('./video_downloader.db')
            await self.create_videos_table()
            # Tải dữ liệu sau khi khởi tạo database
            await self.load_data_from_db()
        except Exception as e:
            print(f"Lỗi khởi tạo database: {e}")
            
    async def create_videos_table(self):
        """Tạo bảng videos nếu chưa tồn tại"""
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                views INTEGER,
                likes INTEGER,
                duration TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                original_link TEXT,
                video_id TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        await self.db.execute_write(create_table_sql)
        
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        self.setWindowTitle(AppConfig.WINDOW_TITLE)
        self.setGeometry(100, 100, AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)
        
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chính
        main_layout = QVBoxLayout(central_widget)
        
        # Phần nhập liệu
        self.create_input_section(main_layout)
        
        # Bảng hiển thị thông tin
        self.create_table_section(main_layout)
        
        # Phần điều khiển
        self.create_control_section(main_layout)
        
    def create_input_section(self, parent_layout):
        """Tạo phần nhập liệu"""
        input_layout = QHBoxLayout()
        
        # Line edit cho link
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("Nhập link video...")
        self.link_input.setMinimumHeight(35)
        
        # Button để thêm video
        self.add_button = QPushButton("Thêm Video")
        self.add_button.setMinimumHeight(35)
        self.add_button.clicked.connect(self.add_video)
        
        # Spinbox cho số luồng tải xuống
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setRange(AppConfig.MIN_THREADS, AppConfig.MAX_THREADS)
        self.threads_spinbox.setValue(AppConfig.DEFAULT_THREADS)
        self.threads_spinbox.setMinimumHeight(35)
        
        threads_label = QLabel("Số luồng:")
        threads_label.setMinimumHeight(35)
        
        # Thêm các widget vào layout
        input_layout.addWidget(QLabel("Link Video:"))
        input_layout.addWidget(self.link_input)
        input_layout.addWidget(self.add_button)
        input_layout.addWidget(threads_label)
        input_layout.addWidget(self.threads_spinbox)
        
        parent_layout.addLayout(input_layout)
        
    def create_table_section(self, parent_layout):
        """Tạo phần bảng hiển thị"""
        self.table = QTableWidget()
        self.setup_table()
        parent_layout.addWidget(self.table)
        
    def create_control_section(self, parent_layout):
        """Tạo phần điều khiển"""
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Bắt đầu tải")
        self.start_button.clicked.connect(self.start_download)
        
        self.pause_button = QPushButton("Tạm dừng")
        self.pause_button.clicked.connect(self.pause_download)
        
        self.clear_button = QPushButton("Xóa tất cả")
        self.clear_button.clicked.connect(self.clear_all)
        
        self.search_button = QPushButton("Tìm kiếm")
        self.search_button.clicked.connect(self.search_videos)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addWidget(self.search_button)
        control_layout.addStretch()
        
        parent_layout.addLayout(control_layout)
        
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
        
    def add_video(self):
        """Thêm video mới vào bảng"""
        link = self.link_input.text().strip()
        if not link:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập link video!")
            return
            
        # Chạy async function
        asyncio.create_task(self._add_video_async(link))
        
    async def _add_video_async(self, link):
        """Async function để thêm video"""
        try:
            # Thêm vào database
            insert_sql = '''
                INSERT INTO videos (title, views, likes, duration, status, 
                                  progress, original_link, video_id, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            record_id = await insert_db(
                insert_sql,
                "Đang tải thông tin...", 0, 0, "00:00",
                DownloadStatus.PENDING, 0, link, "", ""
            )
            
            if record_id:
                # Thêm vào bảng
                self.add_row_to_table(record_id, "Đang tải thông tin...", 0, 0, "00:00", 
                                     DownloadStatus.PENDING, 0, link, "", "")
                
                # Xóa link input
                self.link_input.clear()
                
                QMessageBox.information(self, "Thành công", "Video đã được thêm vào danh sách!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể thêm video vào database!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi thêm video: {str(e)}")
        
    def add_row_to_table(self, record_id, title, views, likes, duration, 
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
            await self.db.execute_write("DELETE FROM videos")
            self.table.setRowCount(0)
            QMessageBox.information(self, "Thành công", "Đã xóa tất cả dữ liệu!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa dữ liệu: {str(e)}")
                
    def search_videos(self):
        """Tìm kiếm video"""
        keyword, ok = QInputDialog.getText(self, "Tìm kiếm", "Nhập từ khóa tìm kiếm:")
        if ok and keyword:
            asyncio.create_task(self._search_videos_async(keyword))
            
    async def _search_videos_async(self, keyword):
        """Async function để tìm kiếm video"""
        try:
            search_sql = '''
                SELECT * FROM videos 
                WHERE title LIKE ? OR original_link LIKE ? OR video_id LIKE ?
                ORDER BY id
            '''
            results = await fetch_all(search_sql, f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
            self.display_search_results(results)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi tìm kiếm: {str(e)}")
            
    def display_search_results(self, results):
        """Hiển thị kết quả tìm kiếm"""
        self.table.setRowCount(0)
        for row in results:
            self.add_row_to_table(*row)
            
    async def load_data_from_db(self):
        """Tải dữ liệu từ database vào bảng"""
        try:
            rows = await fetch_all("SELECT * FROM videos ORDER BY id")
            self.table.setRowCount(0)
            
            for row in rows:
                self.add_row_to_table(*row)
        except Exception as e:
            print(f"Lỗi tải dữ liệu: {e}")
            
    async def update_video_status(self, record_id, status, progress=None):
        """Cập nhật trạng thái video"""
        try:
            if progress is not None:
                await update_db(
                    "UPDATE videos SET status = ?, progress = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    status, progress, record_id
                )
            else:
                await update_db(
                    "UPDATE videos SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    status, record_id
                )
            
            # Cập nhật giao diện
            for row in range(self.table.rowCount()):
                if self.table.item(row, TableColumns.RECORD_ID).text() == str(record_id):
                    self.table.item(row, TableColumns.STATUS).setText(status)
                    if progress is not None:
                        self.table.item(row, TableColumns.PROGRESS).setText(f"{progress}%")
                        progress_bar = self.table.cellWidget(row, TableColumns.PROGRESS)
                        if progress_bar:
                            progress_bar.setValue(progress)
                    break
        except Exception as e:
            print(f"Lỗi cập nhật trạng thái: {e}")
                    
    def closeEvent(self, event):
        """Đóng kết nối database khi đóng ứng dụng"""
        if self.db:
            try:
                # Tạo event loop mới để đóng database
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.db.close())
                loop.close()
            except Exception as e:
                print(f"Lỗi khi đóng database: {e}")
        event.accept()
