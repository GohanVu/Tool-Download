import json
import re
import time
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *



class YoutuberAssistant(QThread):
    

    def __init__(self,platform, link, threads, max_videos, min_views, min_likes, min_duration ):
        super().__init__()
        self.platform = platform
        self.link = link
        self.threads = threads
        self.max_videos = max_videos
        self.min_views = min_views
        self.min_likes = min_likes
        self.min_duration = min_duration
    
        
        
    
    def run(self):
        
        self.update_inProcess_signal.emit(True)
        check = self.check_youtube_link(self.source)
        if check =='error':
            self.errors_signal.emit('Đường link bạn đưa vào không phải là link Youtube, vui lòng kiểm tra lại!')
            return
        
        elif check =='video':
            print('Link dạng video')
            id_video = self.takeVideoIDFromUrl(self.source)
            if self.api == 'NoAPI':
                # chạy hàm loading mà không có api
                print('chạy hàm loading mà không có api video')
         
                theInfo = asyncio.run(self.getMetadataFromYtdlp(f'https://www.youtube.com/watch?v={id_video}',True))    
                self.update_rowInfo_signal.emit(
                                theInfo,self.dal)
            else:
                print('chạy hàm loading có api')
                theInfo = self.getVideoInfoByRequest(id_video,self.source)
                self.update_rowInfo_signal.emit(
                                theInfo,self.dal)
                
        elif check =='playlist':
            print('Link dạng playlist')
            self.getAllVideosFromPlaylist(self.source)
    

        elif check == 'channel':
            print('Link dạng channel')
            id_channel = self.turnChannelUrlToId(self.source)
            if id_channel == False:
                self.errors_signal.emit('Kênh không tồn tại hoặc đường dẫn sai! Vui lòng kiểm tra lại!!!')
                return
            if self.api == 'NoAPI':
                print('chạy hàm loading mà không có api')
                self.getAllVideosUrlFromChannelToTable(id_channel)
            else:
                print('chạy hàm loading có api')
                self.getAllVideosUrlFromChannelToTableWithAPI(id_channel)
    
    def check_youtube_link(self,link):
        
        video_pattern = r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[^&]+'
        channel_pattern = r'(https?://)?(www\.)?youtube\.com/(channel/|@)[^&]+'
        playlist_pattern = r'(https?://)?(www\.)?youtube\.com/.*list=[^&]+'

        if re.match(playlist_pattern, link):
            return 'playlist'
        elif re.match(channel_pattern, link):
            return 'channel'
        elif re.match(video_pattern, link):
            return 'video'
        else:
            return 'error'
    
    
    def takeVideoIDFromUrl(self, url):
        patterns = [r'watch\?v=([a-zA-Z0-9_-]+)', r'shorts/([a-zA-Z0-9_-]+)']
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    
    def getAndCheckApiCookie(self,mode):
        f = open('./last_location/api_cookie.json', 'r')
        data = json.load(f)

        if mode == 'api_captcha':
            try:
                api = data['api_captcha']
                if api != "":
                    return api
                else:
                    return 'NoAPI'
            except:
                data['api'] = ''
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return 'NoAPI'

        if mode == 'YT':
            try:
                api = data['api']
                if api != "":
                    return api
                else:
                    return 'NoAPI'
            except:
                data['api'] = ''
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return 'NoAPI'
        elif mode == 'FB':
            try:
                cookie = data['cookie']
                if cookie != "":
                    return cookie
                else:
                    return 'NoCookie'
            except:
                data['cookie'] = ''
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return 'NoCookie'
            
        elif mode == 'INSTAGRAM':
            try:
                instagram = data['instagram']
                if instagram != "":
                    return instagram
                else:
                    return 'NoCookie'
            except:
                data['instagram'] = ''
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return 'NoCookie'
            
        elif mode == 'DOUYIN':
            try:
                douyin = data['douyin']
                if douyin != "":
                    return douyin
                else:
                    return 'NoCookie'
            except:
                data['douyin'] = ''
                f.seek(0)
                f.write(json.dumps(data))
                f.truncate()
                return 'NoCookie'
            