"""
Platform Detector cho Video Downloader Tool
Phát hiện và quản lý các platform được hỗ trợ
"""

from .constants import PLATFORMS


class PlatformDetector:
    """Phát hiện platform từ URL"""
    
    def __init__(self):
        self.platforms = PLATFORMS
        
    def detect_platform(self, url):
        """
        Phát hiện platform từ URL
        
        Args:
            url (str): URL cần phát hiện
            
        Returns:
            dict: Thông tin platform hoặc None nếu không tìm thấy
        """
        if not url or not url.strip():
            return None
            
        url_lower = url.lower()
        
        for platform_key, platform_info in self.platforms.items():
            for keyword in platform_info['keywords']:
                if keyword in url_lower:
                    return {
                        'key': platform_key,
                        'name': platform_info['name'],
                        'emoji': platform_info['emoji'],
                        'info': platform_info
                    }
        
        return None
        
    def get_platform_display_text(self, url):
        """
        Lấy text hiển thị cho platform
        
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
            display_text = f"{platform['emoji']} {platform['name']}"
            
        return display_text, self._get_success_style()
        
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
