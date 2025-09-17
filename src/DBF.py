import asyncio
import aiosqlite
import logging

# Cấu hình logging để theo dõi các sự kiện
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    _instance = None
    def __init__(self, db_path, timeout=30):
        self.db_path = db_path
        self.timeout = timeout
        self.connection = None

    @classmethod
    async def get_instance(cls, db_path='./video_downloader.db', timeout=30):
        if cls._instance is None:
            cls._instance = Database(db_path, timeout)
            await cls._instance.connect()
        return cls._instance

    async def connect(self):
        if self.connection is None:
            self.connection = await aiosqlite.connect(self.db_path, timeout=self.timeout)
            await self.connection.execute("PRAGMA journal_mode=WAL;")
            await self.connection.commit()
            logger.info("Connected to the database and set journal_mode to WAL.")

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
            logger.info("Database connection closed.")

    async def execute_query(self, query, params=None, fetch=False, fetchone=False, commit=False):
        """
        Thực thi một truy vấn SQL với cơ chế retry khi gặp lỗi "database is locked".

        :param query: Chuỗi truy vấn SQL
        :param params: Tham số cho truy vấn SQL
        :param fetch: Nếu True, sẽ lấy tất cả kết quả
        :param fetchone: Nếu True, sẽ lấy một kết quả
        :param commit: Nếu True, sẽ gọi commit sau khi thực thi truy vấn
        :return: Kết quả truy vấn nếu fetch hoặc fetchone được đặt
        """
        params = params or ()
        max_retries = 10
        retry_delay = 1  # Giây

        for attempt in range(max_retries):
            try:
                async with self.connection.execute(query, params) as cursor:
                    if fetch:
                        results = await cursor.fetchall()
                        if commit:
                            await self.connection.commit()
                        return results
                    if fetchone:
                        result = await cursor.fetchone()
                        if commit:
                            await self.connection.commit()
                        return result
                if commit:
                    await self.connection.commit()
                break  # Nếu thành công, thoát vòng lặp
            except aiosqlite.OperationalError as e:
                if "locked" in str(e).lower():
                    logger.warning(f"Database is locked. Retrying {attempt + 1}/{max_retries} in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"OperationalError: {e}")
                    raise
        else:
            logger.error("Max retries exceeded. Could not execute the query.")
            raise Exception("Database is locked and max retries exceeded.")

    async def execute_read(self, query, params=None, fetch=False, fetchone=False):
        """
        Thực thi một truy vấn đọc (SELECT) mà không cần commit.
        """
        return await self.execute_query(
            query,
            params=params,
            fetch=fetch,
            fetchone=fetchone,
            commit=False
        )

    async def execute_write(self, query, params=None):
        """
        Thực thi một truy vấn ghi (INSERT, UPDATE, DELETE) và cần commit.
        """
        await self.execute_query(
            query,
            params=params,
            commit=True
        )


# Helper functions sử dụng lớp Database với các phương thức mới
async def update_db(sql_query, *args):
    """
    Thực thi một truy vấn UPDATE.
    """
    db = await Database.get_instance()  # Lấy kết nối duy nhất
    await db.execute_write(sql_query, args)

async def insert_db(sql_query, *args):
    """
    Thực thi một truy vấn INSERT và trả về ID của dòng vừa chèn.
    """
    db = await Database.get_instance()  # Lấy kết nối duy nhất
    await db.execute_write(sql_query, args)
    # Lấy lastrowid bằng cách thực thi một truy vấn SELECT sau INSERT
    last_id = await db.execute_query("SELECT last_insert_rowid()", fetchone=True)
    return last_id[0] if last_id else None

async def fetch_one(sql_query, *args):
    """
    Thực thi một truy vấn SELECT và trả về một dòng kết quả.
    """
    db = await Database.get_instance()  # Lấy kết nối duy nhất
    return await db.execute_read(sql_query, params=args, fetchone=True)

async def fetch_all(sql_query, *args):
    """
    Thực thi một truy vấn SELECT và trả về tất cả các dòng kết quả.
    """
    db = await Database.get_instance()  # Lấy kết nối duy nhất
    return await db.execute_read(sql_query, params=args, fetch=True)
