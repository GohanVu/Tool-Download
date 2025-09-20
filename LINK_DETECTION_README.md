# 🔍 Link Detection System

Hệ thống nhận diện và phân loại link video từ các platform khác nhau cho Video Downloader Tool.

## 📋 Tổng quan

Hệ thống này được xây dựng dựa trên nội dung mô tả chi tiết về các loại link video và sử dụng regex patterns để nhận diện chính xác từng loại link.

## 🎯 Các Platform được hỗ trợ

### 📺 YouTube
- **Video chuẩn**: `https://www.youtube.com/watch?v=VIDEO_ID`
- **Link rút gọn**: `https://youtu.be/VIDEO_ID`
- **YouTube Shorts**: `https://www.youtube.com/shorts/VIDEO_ID`
- **YouTube Live**: `https://www.youtube.com/live/VIDEO_ID`
- **YouTube Music**: `https://music.youtube.com/watch?v=VIDEO_ID`
- **Playlist**: `https://www.youtube.com/playlist?list=PLAYLIST_ID`
- **Channel**: `https://www.youtube.com/c/CHANNEL_NAME` hoặc `https://www.youtube.com/@USERNAME`
- **Mobile**: `https://m.youtube.com/watch?v=VIDEO_ID`

### 📘 Facebook
- **Video Watch**: `https://www.facebook.com/watch/?v=VIDEO_ID`
- **Video Watch (Web)**: `https://web.facebook.com/watch?v=VIDEO_ID`
- **Video từ Page**: `https://www.facebook.com/PAGE_NAME/videos/VIDEO_ID/`
- **Facebook Reel**: `https://www.facebook.com/reel/VIDEO_ID/`
- **Shortlink**: `https://fb.watch/SHORT_ID/`
- **Mobile**: `https://m.facebook.com/PAGE_NAME/videos/VIDEO_ID/`
- **Web Mobile**: `https://web.facebook.com/PAGE_NAME/videos/VIDEO_ID/`
- **Watch Page**: `https://web.facebook.com/watch/USERNAME/`
- **Profile**: `https://web.facebook.com/USERNAME`
- **Share Link**: `https://web.facebook.com/share/v/SHARE_ID/`

### 📷 Instagram
- **Post/Carousel**: `https://www.instagram.com/p/SHORTCODE/`
- **Instagram Reel**: `https://www.instagram.com/reel/SHORTCODE/`
- **IGTV**: `https://www.instagram.com/tv/SHORTCODE/`
- **Profile**: `https://www.instagram.com/USERNAME/`
- **Stories**: `https://www.instagram.com/stories/USERNAME/STORY_ID/`

### 🎵 TikTok
- **Video chuẩn**: `https://www.tiktok.com/@USERNAME/video/VIDEO_ID`
- **Video ID ngắn**: `https://www.tiktok.com/video/VIDEO_ID`
- **Shortlink (vm)**: `https://vm.tiktok.com/SHORT_ID/`
- **Shortlink (vt)**: `https://vt.tiktok.com/SHORT_ID/`
- **Profile**: `https://www.tiktok.com/@USERNAME/`
- **Playlist**: `https://www.tiktok.com/@USERNAME/playlist/PLAYLIST_NAME-ID`
- **Live**: `https://www.tiktok.com/@USERNAME/live`

### 🎭 Douyin
- **Video**: `https://www.douyin.com/video/VIDEO_ID`
- **Profile**: `https://www.douyin.com/user/USERNAME`
- **Shortlink**: `https://v.douyin.com/SHORT_ID/`

## 🚀 Cách sử dụng

### Khởi tạo

```python
from src.platform_detector import PlatformDetector

# Khởi tạo detector
detector = PlatformDetector()
```

### Nhận diện platform cơ bản

```python
# Nhận diện platform từ URL
platform_info = detector.detect_platform(url)

if platform_info:
    print(f"Platform: {platform_info['name']}")
    print(f"Type: {platform_info['link_type']}")
    print(f"ID: {platform_info['content_id']}")
else:
    print("Platform không được hỗ trợ")
```

### Lấy text hiển thị

```python
# Lấy text hiển thị với style
display_text, style = detector.get_platform_display_text(url)
print(display_text)  # Ví dụ: "📺 YouTube - Video"
```

### Kiểm tra các tính năng đặc biệt

```python
# Kiểm tra playlist
is_playlist = detector.is_playlist_link(url)

# Kiểm tra channel/profile
is_channel = detector.is_channel_link(url)

# Kiểm tra live stream
is_live = detector.is_live_link(url)

# Trích xuất video ID
video_id = detector.extract_video_id(url)
```

### Lấy thông tin chi tiết

```python
# Lấy thông tin chi tiết về link
link_info = detector.get_detailed_link_info(url)

print(f"Platform: {link_info['platform']}")
print(f"Type: {link_info['link_type']}")
print(f"Content ID: {link_info['content_id']}")
print(f"Description: {link_info['description']}")
print(f"Supported: {link_info['is_supported']}")
```

## 📊 Cấu trúc dữ liệu trả về

### Platform Info
```python
{
    'key': 'youtube',                    # Key của platform
    'name': 'YouTube',                   # Tên hiển thị
    'emoji': '📺',                      # Emoji
    'link_type': 'video',               # Loại link
    'content_id': 'dQw4w9WgXcQ',       # ID của content
    'description': 'Video YouTube',     # Mô tả
    'info': {...}                       # Thông tin platform từ constants
}
```

### Link Info (Detailed)
```python
{
    'platform': 'youtube',              # Platform
    'link_type': 'video',               # Loại link
    'content_id': 'dQw4w9WgXcQ',       # ID content
    'description': 'Video YouTube',     # Mô tả
    'is_supported': True,               # Có được hỗ trợ không
    'platform_info': {                  # Thông tin platform
        'key': 'youtube',
        'name': 'YouTube',
        'emoji': '📺'
    }
}
```

## 🔧 Các phương thức hữu ích

### PlatformDetector
- `detect_platform(url)` - Nhận diện platform
- `get_platform_display_text(url)` - Lấy text hiển thị
- `is_platform_supported(url)` - Kiểm tra hỗ trợ
- `get_supported_platforms()` - Lấy danh sách platform
- `is_playlist_link(url)` - Kiểm tra playlist
- `is_channel_link(url)` - Kiểm tra channel/profile
- `is_live_link(url)` - Kiểm tra live stream
- `extract_video_id(url)` - Trích xuất video ID
- `get_detailed_link_info(url)` - Lấy thông tin chi tiết
- `get_supported_link_types()` - Lấy danh sách loại link

### LinkDetector
- `detect_link_type(url)` - Nhận diện loại link
- `validate_url(url)` - Kiểm tra URL hợp lệ
- `extract_video_id(url)` - Trích xuất video ID
- `is_playlist_link(url)` - Kiểm tra playlist
- `is_channel_link(url)` - Kiểm tra channel/profile
- `is_live_link(url)` - Kiểm tra live stream
- `get_supported_link_types()` - Lấy danh sách loại link

## 🎨 Tích hợp với UI

Hệ thống được thiết kế để tích hợp dễ dàng với PyQt6 UI:

```python
# Trong UI component
def on_url_changed(self, url):
    display_text, style = self.detector.get_platform_display_text(url)
    self.platform_label.setText(display_text)
    self.platform_label.setStyleSheet(style)
    
    # Kiểm tra các tính năng đặc biệt
    if self.detector.is_playlist_link(url):
        self.show_playlist_options()
    elif self.detector.is_channel_link(url):
        self.show_channel_options()
    elif self.detector.is_live_link(url):
        self.show_live_warning()
```

## 🔍 Regex Patterns

Hệ thống sử dụng các regex patterns được tối ưu hóa để nhận diện chính xác:

- **YouTube**: Hỗ trợ tất cả biến thể URL
- **Facebook**: Xử lý các domain khác nhau (m.facebook.com, web.facebook.com)
- **Instagram**: Nhận diện chính xác các loại content
- **TikTok**: Hỗ trợ shortlink và các biến thể
- **Douyin**: Xử lý shortlink và profile links

## 🚨 Lưu ý

1. **URL Normalization**: Hệ thống tự động chuẩn hóa URL (thêm https:// nếu cần)
2. **Case Insensitive**: Regex patterns không phân biệt hoa thường
3. **Flexible Matching**: Hỗ trợ cả URL có và không có protocol
4. **Error Handling**: Xử lý gracefully các URL không hợp lệ
5. **Unicode Support**: Tự động decode Unicode trong URL (ví dụ: TikTok playlist)
6. **Smart Parsing**: Tách tên playlist từ ID phức tạp

## 🔮 Mở rộng

Để thêm platform mới:

1. Thêm regex patterns vào `LinkDetector._init_regex_patterns()`
2. Thêm method `_check_NEWPLATFORM()` 
3. Cập nhật `PLATFORMS` trong `constants.py`
4. Test với các URL mẫu

## 📝 Ví dụ sử dụng

```python
# Ví dụ đầy đủ
from src.platform_detector import PlatformDetector

detector = PlatformDetector()

# Test với các URL khác nhau
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.facebook.com/watch/?v=123456789012345",
    "https://www.instagram.com/p/ABC123def456/",
    "https://www.tiktok.com/@username/video/1234567890123456789",
    "https://www.tiktok.com/@phuongmychiofficial/playlist/SING!ASIA-7513205916029930248"
]

for url in urls:
    print(f"\nURL: {url}")
    
    # Nhận diện cơ bản
    platform_info = detector.detect_platform(url)
    if platform_info:
        print(f"✅ {platform_info['name']} - {platform_info['link_type']}")
        print(f"   ID: {platform_info['content_id']}")
        
        # Kiểm tra tính năng đặc biệt
        if detector.is_playlist_link(url):
            print("   📝 Đây là playlist")
        if detector.is_channel_link(url):
            print("   👤 Đây là channel/profile")
        if detector.is_live_link(url):
            print("   🔴 Đây là live stream")
    else:
        print("❌ Platform không được hỗ trợ")
```

Hệ thống này cung cấp một giải pháp toàn diện và linh hoạt để nhận diện và phân loại các loại link video từ nhiều platform khác nhau.
