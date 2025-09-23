"""
ConfigManager - Quản lý cấu hình ứng dụng
Lưu trữ và tải các thiết lập filter vào file JSON
"""

import json
import os
from typing import Dict, Any
from .constants import AppConfig, FilterDefaults


class ConfigManager:
    """Quản lý cấu hình ứng dụng với khả năng lưu/load từ file JSON"""
    
    def __init__(self):
        self.config_file = AppConfig.CONFIG_FILE
        self.config_data = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Tạo cấu hình mặc định"""
        return {
            "filter": {
                "max_videos": FilterDefaults.MAX_VIDEOS,
                "min_views": FilterDefaults.MIN_VIEWS,
                "min_likes": FilterDefaults.MIN_LIKES,
                "min_duration": FilterDefaults.MIN_DURATION
            }
        }
    
    def _load_config(self):
        """Tải cấu hình từ file JSON"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # Merge với default config để đảm bảo có đầy đủ các key
                    self._merge_config(loaded_data)
            else:
                # Tạo file config mới với giá trị mặc định
                self.save_config()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Lỗi khi tải cấu hình: {e}")
            # Sử dụng config mặc định nếu có lỗi
            self.config_data = self._load_default_config()
    
    def _merge_config(self, loaded_data: Dict[str, Any]):
        """Merge dữ liệu đã tải với config mặc định"""
        default_config = self._load_default_config()
        
        # Merge cấu hình filter
        if "filter" in loaded_data:
            for key, value in loaded_data["filter"].items():
                if key in default_config["filter"]:
                    default_config["filter"][key] = value
            self.config_data = default_config
        else:
            self.config_data = default_config
    
    def save_config(self):
        """Lưu cấu hình hiện tại vào file JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Lỗi khi lưu cấu hình: {e}")
    
    def get_filter_config(self) -> Dict[str, int]:
        """Lấy cấu hình filter hiện tại"""
        return self.config_data.get("filter", {})
    
    def update_filter_config(self, max_videos: int = None, min_views: int = None, 
                           min_likes: int = None, min_duration: int = None):
        """Cập nhật cấu hình filter"""
        filter_config = self.config_data.setdefault("filter", {})
        
        if max_videos is not None:
            filter_config["max_videos"] = max_videos
        if min_views is not None:
            filter_config["min_views"] = min_views
        if min_likes is not None:
            filter_config["min_likes"] = min_likes
        if min_duration is not None:
            filter_config["min_duration"] = min_duration
        
        self.save_config()
    
    def get_max_videos(self) -> int:
        """Lấy giá trị tối đa số video"""
        return self.config_data.get("filter", {}).get("max_videos", FilterDefaults.MAX_VIDEOS)
    
    def get_min_views(self) -> int:
        """Lấy giá trị tối thiểu views"""
        return self.config_data.get("filter", {}).get("min_views", FilterDefaults.MIN_VIEWS)
    
    def get_min_likes(self) -> int:
        """Lấy giá trị tối thiểu likes"""
        return self.config_data.get("filter", {}).get("min_likes", FilterDefaults.MIN_LIKES)
    
    def get_min_duration(self) -> int:
        """Lấy giá trị tối thiểu duration"""
        return self.config_data.get("filter", {}).get("min_duration", FilterDefaults.MIN_DURATION)
