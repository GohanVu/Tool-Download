"""
Link Detector cho Video Downloader Tool
Nhận diện và phân loại các loại link video từ các platform khác nhau
"""

import re
from urllib.parse import urlparse, parse_qs, unquote
from typing import Dict, Optional, Tuple, List
from .constants import PLATFORMS


class LinkDetector:
    """Nhận diện và phân loại link video"""
    
    def __init__(self):
        self.platforms = PLATFORMS
        self._init_regex_patterns()
        
    def _init_regex_patterns(self):
        """Khởi tạo các regex patterns cho từng platform"""
        
        # YouTube patterns
        self.youtube_patterns = {
            'video_standard': r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            'video_short': r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})',
            'shorts': r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
            'live': r'(?:https?://)?(?:www\.)?youtube\.com/live/([a-zA-Z0-9_-]{11})',
            'music': r'(?:https?://)?music\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
            'playlist': r'(?:https?://)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)',
            'channel': r'(?:https?://)?(?:www\.)?youtube\.com/(?:c/|channel/|user/|@)([a-zA-Z0-9_-]+)',
            'mobile': r'(?:https?://)?m\.youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})'
        }
        
        # Facebook patterns
        self.facebook_patterns = {
            'video_watch': r'(?:https?://)?(?:www\.)?facebook\.com/watch/\?v=(\d+)',
            'video_watch_web': r'(?:https?://)?web\.facebook\.com/watch\?v=(\d+)',
            'video_page': r'(?:https?://)?(?:www\.)?facebook\.com/([^/]+)/videos/(\d+)/?',
            'reel': r'(?:https?://)?(?:www\.)?facebook\.com/reel/(\d+)/?',
            'shortlink': r'(?:https?://)?fb\.watch/([a-zA-Z0-9_-]+)/?',
            'mobile': r'(?:https?://)?m\.facebook\.com/([^/]+)/videos/(\d+)/?',
            'web_mobile': r'(?:https?://)?web\.facebook\.com/([^/]+)/videos/(\d+)/?',
            'web_watch_page': r'(?:https?://)?web\.facebook\.com/watch/([^/]+)/?',
            'web_profile': r'(?:https?://)?web\.facebook\.com/([^/]+)/?',
            'web_share': r'(?:https?://)?web\.facebook\.com/share/v/([a-zA-Z0-9_-]+)/?'
        }
        
        # Instagram patterns
        self.instagram_patterns = {
            'post': r'(?:https?://)?(?:www\.)?instagram\.com/p/([a-zA-Z0-9_-]+)/?',
            'reel': r'(?:https?://)?(?:www\.)?instagram\.com/reel/([a-zA-Z0-9_-]+)/?',
            'igtv': r'(?:https?://)?(?:www\.)?instagram\.com/tv/([a-zA-Z0-9_-]+)/?',
            'profile': r'(?:https?://)?(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?',
            'stories': r'(?:https?://)?(?:www\.)?instagram\.com/stories/([a-zA-Z0-9_.]+)/(\d+)/?'
        }
        
        # TikTok patterns
        self.tiktok_patterns = {
            'video_standard': r'(?:https?://)?(?:www\.)?tiktok\.com/@([^/]+)/video/(\d+)',
            'video_id': r'(?:https?://)?(?:www\.)?tiktok\.com/video/(\d+)',
            'shortlink_vm': r'(?:https?://)?vm\.tiktok\.com/([a-zA-Z0-9]+)/?',
            'shortlink_vt': r'(?:https?://)?vt\.tiktok\.com/([a-zA-Z0-9]+)/?',
            'profile': r'(?:https?://)?(?:www\.)?tiktok\.com/@([^/]+)/?',
            'playlist': r'(?:https?://)?(?:www\.)?tiktok\.com/@([^/]+)/playlist/([^/]+)',
            'live': r'(?:https?://)?(?:www\.)?tiktok\.com/@([^/]+)/live'
        }
        
        # Douyin patterns
        self.douyin_patterns = {
            'video': r'(?:https?://)?(?:www\.)?douyin\.com/video/(\d+)',
            'user': r'(?:https?://)?(?:www\.)?douyin\.com/user/([a-zA-Z0-9_-]+)',
            'shortlink': r'(?:https?://)?v\.douyin\.com/([a-zA-Z0-9]+)/?'
        }
        
    def detect_link_type(self, url: str) -> Dict:
        """
        Nhận diện loại link video từ URL
        
        Args:
            url (str): URL cần phân tích
            
        Returns:
            dict: Thông tin chi tiết về link
        """
        if not url or not url.strip():
            return self._create_result(None, None, None, "URL trống")
            
        # Chuẩn hóa URL
        normalized_url = self._normalize_url(url)
        
        # Kiểm tra từng platform
        for platform_key in ['youtube', 'facebook', 'instagram', 'tiktok', 'douyin']:
            result = self._check_platform(normalized_url, platform_key)
            if result['platform']:
                return result
                
        return self._create_result(None, None, None, "Platform không được hỗ trợ")
        
    def _normalize_url(self, url: str) -> str:
        """Chuẩn hóa URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Loại bỏ trailing slash
        url = url.rstrip('/')
        
        return url
        
    def _check_platform(self, url: str, platform: str) -> Dict:
        """Kiểm tra platform cụ thể"""
        
        if platform == 'youtube':
            return self._check_youtube(url)
        elif platform == 'facebook':
            return self._check_facebook(url)
        elif platform == 'instagram':
            return self._check_instagram(url)
        elif platform == 'tiktok':
            return self._check_tiktok(url)
        elif platform == 'douyin':
            return self._check_douyin(url)
            
        return self._create_result(None, None, None, "Platform không xác định")
        
    def _check_youtube(self, url: str) -> Dict:
        """Kiểm tra YouTube links"""
        
        # Video chuẩn
        match = re.search(self.youtube_patterns['video_standard'], url)
        if match:
            return self._create_result('youtube', 'video', match.group(1), "Video YouTube")
            
        # Link rút gọn
        match = re.search(self.youtube_patterns['video_short'], url)
        if match:
            return self._create_result('youtube', 'video', match.group(1), "Video YouTube (rút gọn)")
            
        # YouTube Shorts
        match = re.search(self.youtube_patterns['shorts'], url)
        if match:
            return self._create_result('youtube', 'shorts', match.group(1), "YouTube Shorts")
            
        # Live stream
        match = re.search(self.youtube_patterns['live'], url)
        if match:
            return self._create_result('youtube', 'live', match.group(1), "YouTube Live")
            
        # YouTube Music
        match = re.search(self.youtube_patterns['music'], url)
        if match:
            return self._create_result('youtube', 'music', match.group(1), "YouTube Music")
            
        # Playlist
        match = re.search(self.youtube_patterns['playlist'], url)
        if match:
            return self._create_result('youtube', 'playlist', match.group(1), "YouTube Playlist")
            
        # Channel
        match = re.search(self.youtube_patterns['channel'], url)
        if match:
            return self._create_result('youtube', 'channel', match.group(1), "YouTube Channel")
            
        # Mobile
        match = re.search(self.youtube_patterns['mobile'], url)
        if match:
            return self._create_result('youtube', 'video', match.group(1), "Video YouTube (mobile)")
            
        return self._create_result(None, None, None, "Không phải link YouTube hợp lệ")
        
    def _check_facebook(self, url: str) -> Dict:
        """Kiểm tra Facebook links"""
        
        # Video Watch (www.facebook.com)
        match = re.search(self.facebook_patterns['video_watch'], url)
        if match:
            return self._create_result('facebook', 'video', match.group(1), "Video Facebook")
            
        # Video Watch (web.facebook.com)
        match = re.search(self.facebook_patterns['video_watch_web'], url)
        if match:
            return self._create_result('facebook', 'video', match.group(1), "Video Facebook (web)")
            
        # Video từ Page
        match = re.search(self.facebook_patterns['video_page'], url)
        if match:
            return self._create_result('facebook', 'video', match.group(2), f"Video Facebook từ {match.group(1)}")
            
        # Facebook Reel
        match = re.search(self.facebook_patterns['reel'], url)
        if match:
            return self._create_result('facebook', 'reel', match.group(1), "Facebook Reel")
            
        # Shortlink
        match = re.search(self.facebook_patterns['shortlink'], url)
        if match:
            return self._create_result('facebook', 'shortlink', match.group(1), "Facebook Shortlink")
            
        # Mobile
        match = re.search(self.facebook_patterns['mobile'], url)
        if match:
            return self._create_result('facebook', 'video', match.group(2), f"Video Facebook (mobile) từ {match.group(1)}")
            
        # Web mobile
        match = re.search(self.facebook_patterns['web_mobile'], url)
        if match:
            return self._create_result('facebook', 'video', match.group(2), f"Video Facebook (web mobile) từ {match.group(1)}")
            
        # Web watch page (web.facebook.com/watch/username/)
        match = re.search(self.facebook_patterns['web_watch_page'], url)
        if match:
            return self._create_result('facebook', 'watch_page', match.group(1), f"Facebook Watch Page: {match.group(1)}")
            
        # Web share link
        match = re.search(self.facebook_patterns['web_share'], url)
        if match:
            return self._create_result('facebook', 'share', match.group(1), f"Facebook Share Link: {match.group(1)}")
            
        # Web profile (web.facebook.com/username)
        match = re.search(self.facebook_patterns['web_profile'], url)
        if match:
            # Kiểm tra xem có phải là profile không (không chứa các từ khóa khác)
            username = match.group(1)
            if not any(keyword in url for keyword in ['/watch/', '/videos/', '/reel/', '/share/']):
                return self._create_result('facebook', 'profile', username, f"Facebook Profile: {username}")
            
        return self._create_result(None, None, None, "Không phải link Facebook hợp lệ")
        
    def _check_instagram(self, url: str) -> Dict:
        """Kiểm tra Instagram links"""
        
        # Post/Carousel
        match = re.search(self.instagram_patterns['post'], url)
        if match:
            return self._create_result('instagram', 'post', match.group(1), "Instagram Post")
            
        # Reel
        match = re.search(self.instagram_patterns['reel'], url)
        if match:
            return self._create_result('instagram', 'reel', match.group(1), "Instagram Reel")
            
        # IGTV
        match = re.search(self.instagram_patterns['igtv'], url)
        if match:
            return self._create_result('instagram', 'igtv', match.group(1), "Instagram IGTV")
            
        # Profile
        match = re.search(self.instagram_patterns['profile'], url)
        if match and not any(keyword in url for keyword in ['/p/', '/reel/', '/tv/', '/stories/']):
            return self._create_result('instagram', 'profile', match.group(1), "Instagram Profile")
            
        # Stories
        match = re.search(self.instagram_patterns['stories'], url)
        if match:
            return self._create_result('instagram', 'stories', match.group(2), f"Instagram Stories từ {match.group(1)}")
            
        return self._create_result(None, None, None, "Không phải link Instagram hợp lệ")
        
    def _check_tiktok(self, url: str) -> Dict:
        """Kiểm tra TikTok links"""
        
        # Video chuẩn
        match = re.search(self.tiktok_patterns['video_standard'], url)
        if match:
            return self._create_result('tiktok', 'video', match.group(2), f"TikTok Video từ @{match.group(1)}")
            
        # Video ID ngắn
        match = re.search(self.tiktok_patterns['video_id'], url)
        if match:
            return self._create_result('tiktok', 'video', match.group(1), "TikTok Video")
            
        # Shortlink vm.tiktok.com
        match = re.search(self.tiktok_patterns['shortlink_vm'], url)
        if match:
            return self._create_result('tiktok', 'shortlink', match.group(1), "TikTok Shortlink (vm)")
            
        # Shortlink vt.tiktok.com
        match = re.search(self.tiktok_patterns['shortlink_vt'], url)
        if match:
            return self._create_result('tiktok', 'shortlink', match.group(1), "TikTok Shortlink (vt)")
            
        # Profile
        match = re.search(self.tiktok_patterns['profile'], url)
        if match and not any(keyword in url for keyword in ['/video/', '/playlist/', '/live']):
            return self._create_result('tiktok', 'profile', match.group(1), f"TikTok Profile @{match.group(1)}")
            
        # Playlist
        match = re.search(self.tiktok_patterns['playlist'], url)
        if match:
            playlist_id = match.group(2)
            username = match.group(1)
            
            # Decode URL để hiển thị tên playlist đẹp hơn
            try:
                decoded_playlist_id = unquote(playlist_id)
                # Tách tên playlist và ID số (nếu có)
                if '-' in decoded_playlist_id:
                    playlist_name, playlist_num_id = decoded_playlist_id.rsplit('-', 1)
                    description = f"TikTok Playlist '{playlist_name}' từ @{username}"
                else:
                    description = f"TikTok Playlist từ @{username}"
            except:
                description = f"TikTok Playlist từ @{username}"
                
            return self._create_result('tiktok', 'playlist', playlist_id, description)
            
        # Live
        match = re.search(self.tiktok_patterns['live'], url)
        if match:
            return self._create_result('tiktok', 'live', match.group(1), f"TikTok Live từ @{match.group(1)}")
            
        return self._create_result(None, None, None, "Không phải link TikTok hợp lệ")
        
    def _check_douyin(self, url: str) -> Dict:
        """Kiểm tra Douyin links"""
        
        # Video
        match = re.search(self.douyin_patterns['video'], url)
        if match:
            return self._create_result('douyin', 'video', match.group(1), "Douyin Video")
            
        # User
        match = re.search(self.douyin_patterns['user'], url)
        if match:
            return self._create_result('douyin', 'profile', match.group(1), f"Douyin Profile {match.group(1)}")
            
        # Shortlink
        match = re.search(self.douyin_patterns['shortlink'], url)
        if match:
            return self._create_result('douyin', 'shortlink', match.group(1), "Douyin Shortlink")
            
        return self._create_result(None, None, None, "Không phải link Douyin hợp lệ")
        
    def _create_result(self, platform: Optional[str], link_type: Optional[str], 
                      content_id: Optional[str], description: str) -> Dict:
        """Tạo kết quả nhận diện"""
        
        result = {
            'platform': platform,
            'link_type': link_type,
            'content_id': content_id,
            'description': description,
            'is_supported': platform is not None,
            'platform_info': None
        }
        
        if platform and platform in self.platforms:
            result['platform_info'] = {
                'key': platform,
                'name': self.platforms[platform]['name'],
                'emoji': self.platforms[platform]['emoji']
            }
            
        return result
        
    def get_supported_link_types(self) -> Dict:
        """Lấy danh sách các loại link được hỗ trợ"""
        return {
            'youtube': [
                'Video chuẩn (youtube.com/watch?v=)',
                'Link rút gọn (youtu.be/)',
                'YouTube Shorts',
                'YouTube Live',
                'YouTube Music',
                'Playlist',
                'Channel'
            ],
            'facebook': [
                'Video Watch',
                'Video từ Page',
                'Facebook Reel',
                'Shortlink (fb.watch/)',
                'Mobile/Web mobile'
            ],
            'instagram': [
                'Post/Carousel',
                'Instagram Reel',
                'IGTV',
                'Profile',
                'Stories'
            ],
            'tiktok': [
                'Video chuẩn',
                'Video ID ngắn',
                'Shortlink (vm.tiktok.com)',
                'Shortlink (vt.tiktok.com)',
                'Profile',
                'Playlist',
                'Live'
            ],
            'douyin': [
                'Video',
                'Profile',
                'Shortlink'
            ]
        }
        
    def validate_url(self, url: str) -> bool:
        """Kiểm tra URL có hợp lệ không"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
            
    def extract_video_id(self, url: str) -> Optional[str]:
        """Trích xuất video ID từ URL"""
        result = self.detect_link_type(url)
        return result.get('content_id')
        
    def is_playlist_link(self, url: str) -> bool:
        """Kiểm tra có phải link playlist không"""
        result = self.detect_link_type(url)
        return result.get('link_type') == 'playlist'
        
    def is_channel_link(self, url: str) -> bool:
        """Kiểm tra có phải link channel/profile không"""
        result = self.detect_link_type(url)
        return result.get('link_type') in ['channel', 'profile']
        
    def is_live_link(self, url: str) -> bool:
        """Kiểm tra có phải link live stream không"""
        result = self.detect_link_type(url)
        return result.get('link_type') == 'live'
