"""
Platform Detector cho Video Downloader Tool
Phát hiện và quản lý các platform được hỗ trợ
"""

from .constants import PLATFORMS
from .link_detector import LinkDetector


class PlatformDetector:
    """Phát hiện platform từ URL"""
    
    def __init__(self):
        self.platforms = PLATFORMS
        self.link_detector = LinkDetector()
        
    def detect_platform(self, url):
        """
        Phát hiện platform từ URL (sử dụng LinkDetector mới)
        
        Args:
            url (str): URL cần phát hiện
            
        Returns:
            dict: Thông tin platform hoặc None nếu không tìm thấy
        """
        if not url or not url.strip():
            return None
            
        # Sử dụng LinkDetector để phân tích chi tiết
        link_info = self.link_detector.detect_link_type(url)
        
        if link_info['is_supported'] and link_info['platform_info']:
            return {
                'key': link_info['platform_info']['key'],
                'name': link_info['platform_info']['name'],
                'emoji': link_info['platform_info']['emoji'],
                'link_type': link_info['link_type'],
                'content_id': link_info['content_id'],
                'description': link_info['description'],
                'info': self.platforms[link_info['platform_info']['key']]
            }
        
        return None
        
    def get_platform_display_text(self, url):
        """
        Lấy text hiển thị cho platform với thông tin chi tiết
        
        Args:
            url (str): URL cần phát hiện
            
        Returns:
            tuple: (display_text, style_sheet)
        """
        platform = self.detect_platform(url)
        
        if not platform:
            return "❌ Platform không hỗ trợ", self._get_error_style()
            
        # Xử lý trường hợp đặc biệt cho Douyin
        if platform['key'] == 'douyin':
            display_text = f"{platform['emoji']} {platform['name']} đang phát triển"
        else:
            # Hiển thị thông tin chi tiết về loại link
            link_type_info = self._get_link_type_display(platform['link_type'])
            display_text = f"{platform['emoji']} {platform['name']} - {link_type_info}"
            
        return display_text, self._get_success_style()
        
    def _get_link_type_display(self, link_type):
        """Chuyển đổi link type thành text hiển thị"""
        type_mapping = {
            'video': 'Video',
            'shorts': 'Shorts',
            'reel': 'Reel',
            'live': 'Live',
            'music': 'Music',
            'playlist': 'Playlist',
            'channel': 'Channel',
            'profile': 'Profile',
            'post': 'Post',
            'igtv': 'IGTV',
            'stories': 'Stories',
            'shortlink': 'Shortlink',
            'watch_page': 'Watch Page',
            'share': 'Share Link'
        }
        return type_mapping.get(link_type, 'Content')
        
    def get_default_display(self):
        """Lấy hiển thị mặc định khi chưa có URL"""
        return "Chưa chọn platform", self._get_default_style()
        
    def is_platform_supported(self, url):
        """
        Kiểm tra xem platform có được hỗ trợ không
        
        Args:
            url (str): URL cần kiểm tra
            
        Returns:
            bool: True nếu được hỗ trợ, False nếu không
        """
        return self.detect_platform(url) is not None
        
    def get_supported_platforms(self):
        """
        Lấy danh sách các platform được hỗ trợ
        
        Returns:
            list: Danh sách thông tin platform
        """
        return [
            {
                'key': key,
                'name': info['name'],
                'emoji': info['emoji'],
                'keywords': info['keywords']
            }
            for key, info in self.platforms.items()
        ]
        
    def get_detailed_link_info(self, url):
        """
        Lấy thông tin chi tiết về link
        
        Args:
            url (str): URL cần phân tích
            
        Returns:
            dict: Thông tin chi tiết về link
        """
        return self.link_detector.detect_link_type(url)
        
    def is_playlist_link(self, url):
        """Kiểm tra có phải link playlist không"""
        return self.link_detector.is_playlist_link(url)
        
    def is_channel_link(self, url):
        """Kiểm tra có phải link channel/profile không"""
        return self.link_detector.is_channel_link(url)
        
    def is_live_link(self, url):
        """Kiểm tra có phải link live stream không"""
        return self.link_detector.is_live_link(url)
        
    def extract_video_id(self, url):
        """Trích xuất video ID từ URL"""
        return self.link_detector.extract_video_id(url)
        
    def get_supported_link_types(self):
        """Lấy danh sách các loại link được hỗ trợ"""
        return self.link_detector.get_supported_link_types()
        
    def _get_default_style(self):
        """Style mặc định cho platform display"""
        return """
            QLabel {
                padding: 8px 12px;
                border: 1px solid #666666;
                border-radius: 8px;
                background-color: #2A2A2A;
                color: #CCCCCC;
                font-size: 12px;
                font-weight: 500;
            }
        """
        
    def _get_success_style(self):
        """Style cho platform được hỗ trợ"""
        return """
            QLabel {
                padding: 8px 12px;
                border: 1px solid #666666;
                border-radius: 8px;
                background-color: #2A2A2A;
                color: #FFFFFF;
                font-size: 12px;
                font-weight: 500;
            }
        """
        
    def _get_error_style(self):
        """Style cho platform không được hỗ trợ"""
        return """
            QLabel {
                padding: 8px 12px;
                border: 1px solid #666666;
                border-radius: 8px;
                background-color: #2A2A2A;
                color: #FF6B6B;
                font-size: 12px;
                font-weight: 500;
            }
        """
