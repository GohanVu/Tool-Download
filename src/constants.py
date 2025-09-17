"""
Constants cho Video Downloader Tool
Chứa các hằng số và cấu hình cho ứng dụng
"""

# Constants cho index các cột trong bảng
class TableColumns:
    TITLE = 0          # Tiêu đề
    VIEWS = 1          # Lượt view
    LIKES = 2          # Lượt like
    DURATION = 3       # Duration
    STATUS = 4         # Tình trạng download
    PROGRESS = 5       # Thanh % tải xuống
    ORIGINAL_LINK = 6  # Link gốc của video
    VIDEO_ID = 7       # ID của video
    FILE_PATH = 8      # Đường dẫn tệp file video đã được tải xuống
    RECORD_ID = 9      # ID bản ghi

# Tên các cột hiển thị
COLUMN_HEADERS = [
    "Tiêu đề",
    "Lượt view", 
    "Lượt like",
    "Duration",
    "Tình trạng",
    "Tiến độ",
    "Link gốc",
    "Video ID",
    "Đường dẫn file",
    "ID bản ghi"
]

# Trạng thái download
class DownloadStatus:
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

# Cấu hình ứng dụng
class AppConfig:
    WINDOW_TITLE = "Video Downloader Tool"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    DATABASE_NAME = "video_downloader.db"
    DEFAULT_THREADS = 4
    MIN_THREADS = 1
    MAX_THREADS = 10
