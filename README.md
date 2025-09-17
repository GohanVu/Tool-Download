# 🎥 Video Downloader Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.9.1-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ứng dụng tải xuống video với giao diện đồ họa thân thiện, sử dụng PyQt6 và cơ sở dữ liệu SQLite. Hỗ trợ quản lý danh sách video, tải xuống đa luồng và lưu trữ thông tin video.

## ✨ Tính năng

- 🖥️ **Giao diện đồ họa** - Sử dụng PyQt6 với layout hiện đại
- 📊 **Quản lý database** - SQLite với async operations
- 🔍 **Tìm kiếm video** - Tìm kiếm theo tiêu đề, link, ID
- 📈 **Theo dõi tiến độ** - Progress bar real-time
- 🧵 **Đa luồng** - Hỗ trợ tải xuống song song (1-10 luồng)
- 💾 **Lưu trữ persistent** - Dữ liệu được lưu giữa các phiên

## 🏗️ Cấu trúc dự án

```
tool_download/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── constants.py         # Constants và configuration
│   ├── DBF.py              # Database management (SQLite)
│   └── main_window.py       # Main GUI application
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## 🚀 Cài đặt và Sử dụng

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Windows/macOS/Linux
- 100MB dung lượng trống

### Cài đặt

1. **Clone repository:**
```bash
git clone https://github.com/yourusername/video-downloader-tool.git
cd video-downloader-tool
```

2. **Tạo virtual environment (khuyến nghị):**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Chạy ứng dụng:**
```bash
python main.py
```

## 📋 Hướng dẫn sử dụng

### Giao diện chính
- **Nhập link:** Gõ URL video vào ô "Link Video"
- **Thêm video:** Nhấn nút "Thêm Video" để thêm vào danh sách
- **Cấu hình luồng:** Chọn số luồng tải xuống (1-10) bằng SpinBox
- **Bảng quản lý:** Hiển thị tất cả video với thông tin chi tiết

### Bảng thông tin
| Cột | Mô tả |
|-----|-------|
| **Tiêu đề** | Tên video |
| **Lượt view** | Số lượt xem |
| **Lượt like** | Số lượt thích |
| **Duration** | Thời lượng video |
| **Tình trạng** | Trạng thái tải xuống |
| **Tiến độ** | Thanh % tải xuống |
| **Link gốc** | URL video gốc |
| **Video ID** | ID của video |
| **Đường dẫn file** | Vị trí file đã tải |
| **ID bản ghi** | ID trong database |

### Các chức năng
- 🔍 **Tìm kiếm:** Tìm video theo tiêu đề, link hoặc ID
- ▶️ **Bắt đầu tải:** Khởi động quá trình tải xuống
- ⏸️ **Tạm dừng:** Tạm dừng tải xuống
- 🗑️ **Xóa tất cả:** Xóa toàn bộ dữ liệu
- 💾 **Tự động lưu:** Dữ liệu được lưu tự động

## 🏗️ Kiến trúc Code

### Core Components

#### `src/constants.py`
- **TableColumns**: Định nghĩa index các cột trong bảng
- **COLUMN_HEADERS**: Tên hiển thị các cột
- **DownloadStatus**: Các trạng thái tải xuống (pending, downloading, completed, etc.)
- **AppConfig**: Cấu hình ứng dụng (kích thước cửa sổ, số luồng mặc định)

#### `src/DBF.py`
- **Database Class**: Singleton pattern cho SQLite connection
- **Async Operations**: Sử dụng aiosqlite cho non-blocking database operations
- **Helper Functions**: `insert_db()`, `fetch_all()`, `update_db()`, `fetch_one()`
- **Retry Logic**: Tự động retry khi database bị locked

#### `src/main_window.py`
- **VideoDownloaderApp**: Main GUI class kế thừa từ QMainWindow
- **UI Components**: Layout, widgets, event handlers
- **Database Integration**: Tương tác với database thông qua async functions
- **Progress Tracking**: Real-time progress updates

#### `main.py`
- **Application Entry Point**: Khởi tạo QApplication và main window
- **Database Initialization**: Async database setup với QTimer

## 🔧 Phát triển

### Cài đặt môi trường phát triển
```bash
# Clone repository
git clone https://github.com/yourusername/video-downloader-tool.git
cd video-downloader-tool

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python main.py
```

### Roadmap
- [ ] Tích hợp yt-dlp cho download thực tế
- [ ] Multi-threading cho download
- [ ] Progress callbacks real-time
- [ ] Format selection (MP4, MP3, etc.)
- [ ] Download queue management
- [ ] Error handling và retry logic
- [ ] Settings panel
- [ ] Export/Import danh sách video

## 📝 Lưu ý

- Database file `video_downloader.db` được tạo tự động
- Dữ liệu persistent giữa các phiên làm việc
- Hỗ trợ sắp xếp bảng theo cột
- Async operations để tránh block UI

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Liên hệ

- **Author**: Your Name
- **Email**: your.email@example.com
- **Project Link**: [https://github.com/yourusername/video-downloader-tool](https://github.com/yourusername/video-downloader-tool)
