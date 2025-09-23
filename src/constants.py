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

# Định nghĩa các platform được hỗ trợ
PLATFORMS = {
    'facebook': {
        'keywords': ['facebook.com', 'fb.com', 'm.facebook.com'],
        'emoji': '📘',
        'name': 'Facebook'
    },
    'tiktok': {
        'keywords': ['tiktok.com', 'vm.tiktok.com'],
        'emoji': '🎵',
        'name': 'TikTok'
    },
    'instagram': {
        'keywords': ['instagram.com', 'instagr.am'],
        'emoji': '📷',
        'name': 'Instagram'
    },
    'youtube': {
        'keywords': ['youtube.com', 'youtu.be', 'm.youtube.com'],
        'emoji': '📺',
        'name': 'YouTube'
    },
    'douyin': {
        'keywords': ['douyin.com', 'iesdouyin.com'],
        'emoji': '🎭',
        'name': 'Douyin'
    }
}

# Cấu hình ứng dụng
class AppConfig:
    WINDOW_TITLE = "Video Downloader Tool"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    DATABASE_NAME = "video_downloader.db"
    DEFAULT_THREADS = 4
    MIN_THREADS = 1
    MAX_THREADS = 10
    CONFIG_FILE = "app_config.json"
    
# Giá trị mặc định cho filter
class FilterDefaults:
    MAX_VIDEOS = 9999
    MIN_VIEWS = 0
    MIN_LIKES = 0
    MIN_DURATION = 0
