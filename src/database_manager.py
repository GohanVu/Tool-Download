"""
Database Manager cho Video Downloader Tool
Quản lý các thao tác với database
"""

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
        
    async def insert_video(self, title, views, likes, duration, original_link, 
                          video_id=None, file_path=None, status=DownloadStatus.PENDING):
        """
        Thêm video mới vào database
        
        Args:
            title (str): Tiêu đề video
            views (int): Lượt xem
            likes (int): Lượt like
            duration (str): Thời lượng
            original_link (str): Link gốc
            video_id (str): ID video
            file_path (str): Đường dẫn file
            status (str): Trạng thái
            
        Returns:
            int: ID của record vừa tạo
        """
        insert_sql = '''
            INSERT INTO videos (title, views, likes, duration, original_link, 
                              video_id, file_path, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return await insert_db(insert_sql, title, views, likes, duration, 
                              original_link, video_id, file_path, status)
                              
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
