import os
import threading
from time import sleep
# from time import *             #meaning from time import EVERYTHING
import time
import multiprocessing as mp
# from xml_stream import read_xml_file
# from pytube import Channel, YouTube, Playlist
from pytubefix import YouTube as YouTubeFix
from pytubefix import Channel
# from pytube.helpers import DeferredGeneratorList
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import  urlparse
import urllib
import asyncio,aiohttp


from typing import Union, List, Any

import yt_dlp,re,json,bs4,traceback,requests
import datetime
from multiprocessing import Queue, Process
import random

def log_traceback_to_file(traceback_info: str):
    
    """
    Hàm này nhận vào chuỗi thông tin traceback và ghi nó vào một file.

    Args:
    traceback_info (str): Chuỗi thông tin traceback.
    file_path (str): Đường dẫn đến file nhật ký. Mặc định là 'traceback_log.txt'.
    """
    print(f"==>> traceback_info: {traceback_info}")
    filename = 'traceback_logs'
    log_directory = "data/errorlog"
    file_path = os.path.join(log_directory, filename+".txt")

    with open(file_path, "a", encoding='utf-8') as file:
        file.write(traceback_info + "\n\n")

class YoutuberAssistant(QThread):
    
    load_info_signal = pyqtSignal(bool, str)
    errors_signal = pyqtSignal(str)
    update_rowInfo_signal = pyqtSignal(dict, bool)

    def __init__(self,platform, link, threads, max_videos, min_views, min_likes, min_duration ):
        super().__init__()
        self.platform = platform
        self.link = link
        self.threads = threads
        self.max_videos = max_videos
        self.min_views = min_views
        self.min_likes = min_likes
        self.min_duration = min_duration
        self.api = 'NoAPI'
        self.dal = False
        self.type = 'video'
        self.real = 0
        self._isForceClosed = False
        # self.load_info_signal = pyqtSignal(bool, str)
    
        
        
    
    def run(self):
        
        
        self.load_info_signal.emit(True, 'CCC')
        
        try:
            check = self.check_youtube_link(self.link)
            if check =='error':
                self.errors_signal.emit('Đường link bạn đưa vào không phải là link Youtube, vui lòng kiểm tra lại!')
                return
            
            elif check =='video':
                print('Link dạng video')
                id_video = self.takeVideoIDFromUrl(self.link)
                
                
                if self.api == 'NoAPI':
                    # chạy hàm loading mà không có api
                    print('chạy hàm loading mà không có api video')
            
                    theInfo = self.getMetadataFromYtdlp(f'https://www.youtube.com/watch?v={id_video}',True)   
                    # self.update_rowInfo_signal.emit(
                    #                 theInfo,self.dal)
                else:
                    print('chạy hàm loading có api')
                    # theInfo = self.getVideoInfoByRequest(id_video,self.source)
                    # self.update_rowInfo_signal.emit(
                    #                 theInfo,self.dal)
                    
            elif check =='playlist':
                print('Link dạng playlist')
                self.getAllVideosFromPlaylist(self.link)
        

            elif check == 'channel':
                print('Link dạng channel')
                id_channel = self.turnChannelUrlToId(self.link)
                print(f"==>> id_channel: {id_channel}")
                if id_channel == False:
                    self.errors_signal.emit('Kênh không tồn tại hoặc đường dẫn sai! Vui lòng kiểm tra lại!!!')
                    return
                
                if self.api == 'NoAPI':
                    print('chạy hàm loading mà không có api')
                    self.getAllVideosUrlFromChannelToTable(id_channel)
                else:
                    print('chạy hàm loading có api')
                    # self.getAllVideosUrlFromChannelToTableWithAPI(id_channel)
            
        except Exception as e:
            # self.load_info_signal.emit(False)
            return
        
        finally:
            self.load_info_signal.emit(False,'')
    
    def getAllVideosFromPlaylist(self, url_playlist):

        self.real = 0

        def callit(v,pll:Playlist):
            print(v)

           
            if self.real == self.countVideosLimit or self._isForceClosed:
                pll.needToStop = True
                print('dừng cái pll lại')
                return 

            if self.api == 'NoAPI':
                # print(' chạy hàm loading mà không có api')
                
                rs = self.getMetadataFromYtdlp(v)
                
            else:
                print('chạy hàm loading mà có api')
                rs = self.getVideoInfoByRequest(self.takeVideoIDFromUrl(v),v)

            rs = self.getMetadataFromYtdlp(v)
            if rs is None:
                return v
            views = rs.get('views')
            likes = rs.get('likes')

            
            if int(views) >= self.xThousandViews and int(likes) >= self.xLikes and self.real < self.countVideosLimit:
                
                self.update_rowInfo_signal.emit(rs,self.dal)
                self.real +=1
                
            # return v

        try:
            
            delay = 0.6
            
            pll = Playlist(url_playlist,None,callit)
            
            for video in pll.url_generator1():
                thread = threading.Thread(target=callit,args=(video,pll))
                thread.start()
                sleep(delay)
            
         
           
        except Exception as e:
            log_traceback_to_file(traceback.format_exc())
            self.toggleLoadingWindow_signal.emit(False) 
            self.error = True
            self.errors_signal.emit(f'Lỗi xảy ra khi thu thập đường link từ channel, lý do:<br>{str(e)}')
            
    
    
    def turnChannelUrlToId(self, url):
        try:
            rs = requests.get(url)
            soup = bs4.BeautifulSoup(rs.text, 'html.parser')
            tag = soup.findAll('meta', property="og:url")
            url = tag[0]['content']
            id = url.split('channel/')[1]
            return id
        except:
            return False
    
    def convert_duration(self,duration_str):
        if duration_str == '':
            return 'None'
        
        # Kiểm tra nếu duration_str là số giây
        if duration_str.isdigit():
            total_seconds = int(duration_str)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Xử lý chuỗi duration_str để lấy ra giá trị số của giờ, phút và giây
        duration = re.findall(r'\d+[HMS]', duration_str)
        
        hours = 0
        minutes = 0
        seconds = 0
        
        for d in duration:
            if 'H' in d:
                hours = int(d.replace('H', ''))
            elif 'M' in d:
                minutes = int(d.replace('M', ''))
            elif 'S' in d:
                seconds = int(d.replace('S', ''))
        
        # Định dạng lại thời gian theo định dạng hh:mm:ss
        formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return formatted_duration
    
    def getAllVideosUrlFromChannelToTable(self, id_channel):
        
         
        urlWithID = "https://www.youtube.com/channel/"+id_channel

        self.real = 0

        def callit(theVideo:YouTubeFix,channel:Channel):
            
            # print(v)
      

            if self.real == self.max_videos or self._isForceClosed:
                channel.needToStop = True
                return
            
            if self.api == 'NoAPI':
                # print('chạy hàm loading mà không có api youtube')
                
                # theVideo = YouTubeFix(v)
                # title = theVideo.title
                views = theVideo.views
                # likes = theVideo.likes
                rs = {
                    'id': theVideo.video_id,
                    'title': theVideo.title,
                    'desc': theVideo.description,
                    'tags' : [],
                    'duration' : self.convert_duration(str(theVideo.length)),
                    'thumb_url': theVideo.thumbnail_url,
                    'views': views,
                    'likes': theVideo.likes,
                    'url': theVideo.watch_url,
                    'pvf': None,
                    'paf': None
                }
                # print(f"==>> rs: {rs}")
            else:
                print('chạy hàm loading mà có api')
                # rs = self.getVideoInfoByRequest(self.takeVideoIDFromUrl(v),v)
                

                # if rs is None:
                #     return v
            
        
                # views = int(rs.get('views'))
                # likes = int(rs.get('likes'))

            
            if int(views) >= self.min_views and self.real < self.max_videos:
                self.update_rowInfo_signal.emit(rs,self.dal)
                self.real +=1
             
        
        channel = Channel(urlWithID)
        
          
        try:
            if self.type == "shorts":
                channel.html_url = channel.shorts_url
            else:
                channel.html_url = channel.videos_url
        
            for video in channel.url_generator():
                if self._isForceClosed:
                    return
                # video : YouTubeFix
                # video.get_info()
                # title = video.title
                # print(f"==>> title: {title}")
                thread = threading.Thread(target=callit,args=(video,channel))
                thread.start()
                sleep(0.1)
                
        except Exception as e:
            log_traceback_to_file(traceback.format_exc())
            self.error = True
            self.errors_signal.emit(f'Lỗi xảy ra khi thu thập đường link từ channel 123, lý do:<br>{str(e)}')
  

    

    def getMetadataFromYtdlp(self,url,returnIfFalse = None):


        def findVideoStreamYtDlp(formats, res):
            # quality_list = ['4320p','2160p','1440p','1080p','720p','480p','360p','240p','144p']
            quality_list = ['4320p','4320p60','2160p','2160p60','1440p','1440p60','1080p','1080p60','720p','720p60', '480p','360p','240p','144p']
            index = quality_list.index(res)
            for i in range(index, len(quality_list)):
                for fmt in formats:
                    if fmt.get('format_note') == quality_list[i]:
                        return fmt['url']
            return ''

        def findHighestAudioStreamYtDlp(objects,requested_formats):
            # First try to get audio from requested_formats
            for fmt in requested_formats:
                if fmt.get("fps") is None and fmt.get("audio_channels") == 2:
                    return fmt['url']
            
            # If not found in requested_formats, check objects list
            filtered_objects = [obj for obj in objects if obj.get("fps") is None and obj.get("audio_channels") == 2]
            if filtered_objects:
                rs = max(filtered_objects, key=lambda obj: obj.get("abr", 0))
                return rs['url']
            
            return None
        
        try:
            
            ydl_opts = {
                'extract_flat': True,
                'skip_download': True,
                'quiet': True,
            }
            ytt = yt_dlp.YoutubeDL(ydl_opts)
            info = ytt.extract_info(url, download=False)
            # print(f"==>> info: {info}")
           
            with open('video_info.json', 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=4, ensure_ascii=False)
            return
            media = info['formats']
            requested_formats = info['requested_formats']
            thumb_url = 'http://img.youtube.com/vi/' + \
                info['id'] + '/maxresdefault.jpg'
            video = findVideoStreamYtDlp(media,'1080p')
            audio = findHighestAudioStreamYtDlp(media,requested_formats)

            try:
                views = info['view_count']
                if views == None:
                    views = 0
            except:
                views = 0
            try:
                likes = info['like_count']
                if likes == None:
                    likes = 0
            except:
                likes = 0

            dataVideo = {
                'id': info['id'],
                'title': info['title'],
                'desc': info['description'],
                'tags' : info['tags'],
                'duration' : self.convert_to_hms(info['duration']),
                'thumb_url': "None",
                'views': views,
                'likes': likes,
                'url': url,
                'pvf':video,
                'paf' :audio
            }
        except Exception as e:
            log_traceback_to_file(traceback.format_exc())
            if not returnIfFalse:
                return None
            self.error = True
            self.errors_signal.emit(f'Không thể lấy thông tin của link: {url} bởi vì:<br>{str(e)}')
            dataVideo = {
                'id': f'LỖI! KHÔNG THỂ LẤY LINK {url}',
                'title': f'LỖI! KHÔNG THỂ LẤY LINK {url}',
                'desc': f'LỖI! KHÔNG THỂ LẤY LINK {url}',
                'tags' : "None",
                'duration' : "None",
                'thumb_url': "None",
                'views': "None",
                'likes': "None",
                'url': "None",
                'pvf':"None",
                'paf' :"None"

            }
        
        return dataVideo          
      
    
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
    
    
    def convert_to_hms(self,seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"