"""
Database Manager cho Video Downloader Tool
Quản lý các thao tác với database
"""

import json
from .DBF import Database, insert_db, fetch_all, fetch_one, update_db
from .constants import DownloadStatus


class VideoDatabaseManager:
    """Quản lý các thao tác database cho video"""
    
    def __init__(self):
        self.db = None
        
    async def initialize(self, db_path='./video_downloader.db'):
        """Khởi tạo database và tạo bảng"""
        try:
            self.db = await Database.get_instance(db_path)
            await self.create_videos_table()
        except Exception as e:
            print(f"Lỗi khởi tạo database: {e}")
            raise
            
    async def create_videos_table(self):
        """Tạo bảng videos nếu chưa tồn tại"""
        create_table_sql = '''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE,
                title TEXT,
                desc TEXT,
                tags TEXT,
                duration TEXT,
                thumb_url TEXT,
                views INTEGER,
                likes INTEGER,
                url TEXT,
                pvf TEXT,
                paf TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        await self.db.execute_write(create_table_sql)
        
    async def insert_video(self, video_data):
        """
        Thêm video mới vào database từ dict data
        
        Args:
            video_data (dict): Dữ liệu video từ yt_loader
            
        Returns:
            int: ID của record vừa tạo
        """
        insert_sql = '''
            INSERT OR REPLACE INTO videos (video_id, title, desc, tags, duration, 
                              thumb_url, views, likes, url, pvf, paf, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        # Chuyển đổi tags từ list thành string
        tags_str = json.dumps(video_data.get('tags', [])) if video_data.get('tags') else None
        
        return await insert_db(insert_sql, 
                              video_data.get('id'),
                              video_data.get('title'),
                              video_data.get('desc'),
                              tags_str,
                              video_data.get('duration'),
                              video_data.get('thumb_url'),
                              video_data.get('views'),
                              video_data.get('likes'),
                              video_data.get('url'),
                              video_data.get('pvf'),
                              video_data.get('paf'),
                              DownloadStatus.PENDING)
                              
    async def get_all_videos(self):
        """Lấy tất cả video từ database"""
        sql = "SELECT * FROM videos ORDER BY id"
        return await fetch_all(sql)
        
    async def get_video_by_id(self, video_id):
        """Lấy video theo ID"""
        sql = "SELECT * FROM videos WHERE id = ?"
        return await fetch_one(sql, video_id)
        
    async def search_videos(self, keyword):
        """
        Tìm kiếm video theo từ khóa
        
        Args:
            keyword (str): Từ khóa tìm kiếm
            
        Returns:
            list: Danh sách video tìm được
        """
        search_sql = '''
            SELECT * FROM videos 
            WHERE title LIKE ? OR original_link LIKE ? OR video_id LIKE ?
            ORDER BY id
        '''
        return await fetch_all(search_sql, f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
        
    async def update_video_status(self, record_id, status, progress=None):
        """
        Cập nhật trạng thái video
        
        Args:
            record_id (int): ID của record
            status (str): Trạng thái mới
            progress (int): Tiến độ (tùy chọn)
        """
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
            
    async def update_video_file_path(self, record_id, file_path):
        """Cập nhật đường dẫn file video"""
        await update_db(
            "UPDATE videos SET file_path = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            file_path, record_id
        )
        
    async def delete_video(self, record_id):
        """Xóa video theo ID"""
        await self.db.execute_write("DELETE FROM videos WHERE id = ?", record_id)
        
    async def delete_all_videos(self):
        """Xóa tất cả video"""
        await self.db.execute_write("DELETE FROM videos")
        
    async def get_videos_by_status(self, status):
        """Lấy danh sách video theo trạng thái"""
        sql = "SELECT * FROM videos WHERE status = ? ORDER BY id"
        return await fetch_all(sql, status)
        
    async def get_videos_count(self):
        """Lấy tổng số video"""
        result = await fetch_one("SELECT COUNT(*) as count FROM videos")
        return result[0] if result else 0
        
    async def get_videos_by_platform(self, platform_key):
        """Lấy video theo platform (dựa trên URL)"""
        # Tìm kiếm dựa trên keywords trong URL
        from .platform_detector import PlatformDetector
        detector = PlatformDetector()
        platform_info = detector.platforms.get(platform_key)
        
        if not platform_info:
            return []
            
        # Tạo điều kiện LIKE cho mỗi keyword
        conditions = []
        params = []
        for keyword in platform_info['keywords']:
            conditions.append("original_link LIKE ?")
            params.append(f'%{keyword}%')
            
        if conditions:
            sql = f"SELECT * FROM videos WHERE {' OR '.join(conditions)} ORDER BY id"
            return await fetch_all(sql, *params)
        else:
            return []
            
    async def close(self):
        """Đóng kết nối database"""
        if self.db:
            await self.db.close()
