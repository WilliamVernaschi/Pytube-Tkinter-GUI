import os
import sys
import pytube
import threading
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog


class YtDownloaderApp(tk.Tk):
    small_font = ('courier 10 pitch', 15)
    medium_font = ('courier 10 pitch', 20)
    title_font = ('courier 10 pitch', 30)

    def __init__(self):
        super().__init__()
        
        self.title('Pytube Downloader')
        self.geometry('960x540')
        
        if (sys.platform.startswith('win')): 
            self.iconbitmap('appIcon.ico')
        else:
            logo = tk.PhotoImage(file='appIcon.gif')
            self.call('wm', 'iconphoto', self._w, logo)
        self.initialize_widgets()

        
    def initialize_widgets(self):
        current_path = Path(__name__).parent

        #Loading all the images
        self.direct_link_img = tk.PhotoImage(file=f'{current_path}/directLink.png')
        self.from_playlist_img = tk.PhotoImage(file=f'{current_path}/fromPlaylist.png')
        self.from_txt_file_img = tk.PhotoImage(file=f'{current_path}/txtFile.png')
        self.exit_program_img = tk.PhotoImage(file=f'{current_path}/exitProgram.png')
        self.main_menu_img = tk.PhotoImage(file=f'{current_path}/mainMenuSmall.png')
        self.download_MP4_img = tk.PhotoImage(file=f'{current_path}/downloadMP4.png')
        self.download_MP3_img = tk.PhotoImage(file=f'{current_path}/downloadMP3.png')
        self.load_video_info_img = tk.PhotoImage(file=f'{current_path}/loadVideoInfo.png')
        self.select_file_img = tk.PhotoImage(file=f'{current_path}/selectFile.png')
        self.select_output_img = tk.PhotoImage(file=f'{current_path}/selectOutput.png')

        #Creating the main menu widgets
        self.app_title = tk.Label(self, text='Pytube Downloader', font=self.title_font)
        self.direct_link = tk.Button(self, image=self.direct_link_img, border=0, 
         activebackground='#CCCCCC', command=self.direct_dl_screen)
        self.from_playlist = tk.Button(self, image=self.from_playlist_img, border=0,
         activebackground='#CCCCCC', command=self.playlist_dl_screen)
        self.from_txt_file = tk.Button(self, image=self.from_txt_file_img, border=0, 
         activebackground='#CCCCCC', command=self.txt_dl_screen)
        self.exit_program = tk.Button(self, image=self.exit_program_img, border=0,
         activebackground='#CCCCCC', command=quit)
        
        #Placing the main menu widgets
        self.app_title.pack(side=tk.TOP)
        self.direct_link.pack(side=tk.TOP)
        self.from_playlist.pack(side=tk.TOP)
        self.from_txt_file.pack(side=tk.TOP)
        self.exit_program.pack(side=tk.TOP)
        

        #Creating the other widgets
        self.url_frame = tk.LabelFrame(self, text='1. Enter an URL')

        self.text_input = tk.Entry(self.url_frame, width=42, font=self.medium_font, bd=2)
        self.type_instruction = tk.Label(self.url_frame, font=self.medium_font,
         text='Type in the URL of the video below:')
        self.load_video_info = tk.Button(self.url_frame, image=self.load_video_info_img, border=0,
         activebackground='#CCCCCC')
        self.main_menu = tk.Button(self.url_frame, image=self.main_menu_img, border=0,
         activebackground='#CCCCCC', command=self.go_to_main_menu)

        self.select_options_frame = tk.LabelFrame(self, text='2. Select an option and click download')

        self.download_MP4 = tk.Button(self.select_options_frame, image=self.download_MP4_img, border=0,
         activebackground='#CCCCCC')
        self.download_MP3 = tk.Button(self.select_options_frame, image=self.download_MP3_img, border=0,
         activebackground='#CCCCCC')
        self.selected_resolution = tk.StringVar()
        self.selected_resolution.set('240p')

        self.resolutions = ['']
        self.dropdown_resolution = tk.OptionMenu(self.select_options_frame, self.selected_resolution, 
         *self.resolutions)

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        self.dropdown_resolution['state'] = tk.DISABLED
        self.dropdown_resolution['font'] = self.small_font

        self.operation_error_URL = tk.Label(self, text='ERROR: Invalid URL or network error.', fg='red',
        font=self.small_font)
        self.operation_error_network = tk.Label(self, text="ERROR: Couldn't connect to YouTube.", fg='red',
        font=self.small_font)
        self.operation_success = tk.Label(self, text='Your file has been downloaded.', fg='green',
        font=self.small_font)
        self.operation_in_progress = tk.Label(self, text='Your file is being downloaded, please wait.', fg='blue',
        font=self.small_font)

        self.txt_file_instructions = tk.Label(self.url_frame, text='The text file should have one URL for each line and nothing else.',
        font=self.small_font)
        self.select_file = tk.Button(self.url_frame, image=self.select_file_img, border=0,
          activebackground='#CCCCCC', command=self.select_txt_file)
        self.file_selected = tk.Label(self, text='File selected successfully', border=0,
        font=self.small_font)

        
    @staticmethod
    def clear_screen(widget):
        allWidgets = widget.pack_slaves()
        for widget in allWidgets:
            widget.pack_forget()
    

    def go_to_main_menu(self):

        self.clear_screen(self)
        self.clear_screen(self.url_frame)
        self.clear_screen(self.select_options_frame)
        self.app_title.pack(side=tk.TOP)
        self.direct_link.pack(side=tk.TOP)
        self.from_playlist.pack(side=tk.TOP)
        self.from_txt_file.pack(side=tk.TOP)
        self.exit_program.pack(side=tk.TOP)

        self.url_frame['text'] = '1. Type in the URL of the video below:'

    
    def direct_dl_screen(self):

        self.clear_screen(self)
        self.url_frame.pack_forget()
        self.select_options_frame.pack_forget()

        self.app_title.pack(side=tk.TOP)
        self.type_instruction.pack(side=tk.TOP, pady=(10, 10))
        self.text_input.pack(side=tk.TOP)
        self.load_video_info['command'] = self.load_direct_info
        self.load_video_info.pack(side=tk.LEFT, pady=(20, 20), padx=(130,0))
        self.main_menu.pack(side=tk.RIGHT, padx=(0,175))
        self.url_frame.pack(fill=tk.X)

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        self.dropdown_resolution['state'] = tk.DISABLED

        self.download_MP3['command'] = lambda: self.get_output_path_and_start('direct_MP3')
        self.download_MP4['command'] = lambda: self.get_output_path_and_start('direct_MP4')

        self.dropdown_resolution.pack(side=tk.TOP)
        self.download_MP3.pack(side=tk.LEFT, padx=(155, 0))
        self.download_MP4.pack(side=tk.RIGHT, padx=(0, 155))
        self.select_options_frame.pack(fill=tk.X)

        
    def load_direct_info(self):
        
        youtube_url = self.text_input.get().strip()
        self.direct_dl_screen()

        try:
            self.yt_object = pytube.YouTube(youtube_url)
            mp4_streams = self.yt_object.streams.filter(file_extension='mp4', progressive=False)
        except Exception as e:
            print(e)
            print('invalid URL or network error')
            self.download_MP3['state'] = tk.DISABLED
            self.download_MP4['state'] = tk.DISABLED
            self.dropdown_resolution['state'] = tk.DISABLED
            self.operation_error_URL.pack(side=tk.TOP, pady=(30, 0))
        else:
            self.download_MP3['state'] = tk.ACTIVE
            self.download_MP4['state'] = tk.ACTIVE
            self.dropdown_resolution['state'] = tk.ACTIVE
           
            self.streams_dict = dict()
            for item in mp4_streams:
                if item.resolution is not None:
                    self.streams_dict[str(item.resolution)] = str(item.itag)
            
            self.resolutions = list(self.streams_dict.keys())
            self.resolutions = sorted(self.resolutions, key=lambda x: int(x[:-1]), reverse=True)
            self.update_option_menu()
            self.selected_resolution.set(self.resolutions[0])

            self.default_title = self.yt_object.title
            self.default_title = self.default_title.replace('/', '-')
            self.output_path = ''


    def update_option_menu(self):

        menu = self.dropdown_resolution ["menu"]
        menu.delete(0, "end")
        for string in self.resolutions:
            menu.add_command(label=string, 
                             command=lambda value=string: self.selected_resolution.set(value))


    def download_direct_mp3(self):
        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED

        self.operation_in_progress.pack(side=tk.TOP)

        try:
            self.audio_streams = self.yt_object.streams.filter(only_audio=True, file_extension='mp4')
            self.audio_streams[0].download(self.output_path, filename=self.yt_object.title + '(AUDIO)')
        except Exception as e:
            print(e)
            self.operation_error_network.pack(side=tk.TOP)
        else: 
            self.operation_in_progress.pack_forget()
            self.operation_success.pack(side=tk.TOP)
            
        self.output_path = ''
        self.download_MP3['state'] = tk.ACTIVE
        self.download_MP4['state'] = tk.ACTIVE


    def download_direct_mp4(self):

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        self.operation_in_progress.pack(side=tk.TOP)
        self.resolution = self.selected_resolution.get()
        try:
            video_streams = self.yt_object.streams.filter(resolution=self.resolution)
            video_streams[0].download(self.output_path, filename='cachedvideo')
            self.audio_streams = self.yt_object.streams.filter(only_audio=True, file_extension='mp4')
            self.audio_streams[0].download(self.output_path, filename='cachedaudio')
        except Exception as e:
            print(e)
            self.operation_error_network.pack(side=tk.TOP)
        else:
            self.operation_success.pack(side=tk.TOP)
            self.operation_in_progress.pack_forget()
            self.merge_audio_and_video()

        self.output_path = ''
        self.download_MP3['state'] = tk.ACTIVE
        self.download_MP4['state'] = tk.ACTIVE


    def get_output_path_and_start(self, option):
        
        self.output_path = filedialog.askdirectory()
        if isinstance(self.output_path, tuple) is False:
            self.output_path = self.output_path.strip()
            if self.output_path != '' and self.output_path != '/':
                if option == 'direct_MP4':
                    threading.Thread(target=self.download_direct_mp4).start()
                elif option == 'direct_MP3':
                    threading.Thread(target=self.download_direct_mp3).start()
                elif option == 'playlist_MP4':
                    threading.Thread(target=self.download_playlist_MP4).start()
                elif option == 'playlist_MP3':
                    threading.Thread(target=self.download_playlist_MP3).start()
                elif option == 'txt_MP3':
                    threading.Thread(target=self.download_txt_MP3).start()
                elif option == 'txt_MP4':
                    threading.Thread(target=self.download_txt_MP4).start()


    def merge_audio_and_video(self):

        self.cmd = f'ffmpeg -i "{self.output_path}/cachedaudio.mp4" -i "{self.output_path}/cachedvideo.mp4"\
        -y -codec:a copy -codec:v copy "{self.output_path}/cachedcomplete.mp4"'
        subprocess.run(self.cmd, shell=True)
        os.remove(f'{self.output_path}/cachedaudio.mp4')
        os.remove(f'{self.output_path}/cachedvideo.mp4')
        os.rename(f'{self.output_path}/cachedcomplete.mp4', f'{self.output_path}/{self.default_title}.mp4')

            

    def playlist_dl_screen(self):

        self.clear_screen(self)
        self.clear_screen(self.select_options_frame)
        self.clear_screen(self.url_frame)

        self.app_title.pack(side=tk.TOP)
        self.type_instruction['text'] = 'Type in the URL of the playlist below'
        self.type_instruction.pack(side=tk.TOP, pady=(10, 10))
        self.text_input.pack(side=tk.TOP)
        self.load_video_info['command'] = self.load_playlist_info
        self.load_video_info.pack(side=tk.LEFT, pady=(20, 20), padx=(130,0))
        self.main_menu.pack(side=tk.RIGHT, padx=(0,175))
        self.url_frame.pack(fill=tk.X)

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        

        self.download_MP3['command'] = lambda: self.get_output_path_and_start('playlist_MP3')
        self.download_MP4['command'] = lambda: self.get_output_path_and_start('playlist_MP4')

        self.download_MP3.pack(side=tk.LEFT, padx=(155, 0), pady=30)
        self.download_MP4.pack(side=tk.RIGHT, padx=(0, 155), pady=30)
        self.select_options_frame.pack(fill=tk.X)


    def load_playlist_info(self):

        self.playlist_dl_screen()
        youtube_url = self.text_input.get()
        try:
            self.first_title = pytube.Playlist(youtube_url).video_urls[0]
            self.yt_object = pytube.Playlist(youtube_url)
        except Exception as e:
            print(e)    
            print('invalid URL or network error')
            self.download_MP3['state'] = tk.DISABLED
            self.download_MP4['state'] = tk.DISABLED
            self.operation_error_URL.pack(side=tk.TOP, pady=(30, 0))
        else:
            self.download_MP3['state'] = tk.ACTIVE
            self.download_MP4['state'] = tk.ACTIVE

            self.default_title = self.yt_object.title
            self.output_path = ''


    def download_playlist_MP4(self):

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        self.operation_in_progress.pack(side=tk.TOP)
        self.resolution = self.selected_resolution.get()
        self.operation_success['text'] = 'Your playlist has been downloaded.'
        try:
            for video in self.yt_object.videos:
                video.streams.first().download(self.output_path)
        except Exception as e:
            print(e)
            self.operation_error_network.pack(side=tk.TOP)
        else:
            self.operation_success.pack(side=tk.TOP)
            self.operation_in_progress.pack_forget()

        self.output_path = ''
        self.download_MP3['state'] = tk.ACTIVE
        self.download_MP4['state'] = tk.ACTIVE


    def download_playlist_MP3(self):

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        self.operation_in_progress.pack(side=tk.TOP)
        self.resolution = self.selected_resolution.get()
        self.operation_success['text'] = 'Your playlist has been downloaded.'
        try:
            video_objects = self.yt_object.videos
            for video in video_objects:
                audio_streams = video.streams.filter(only_audio=True, file_extension='mp4')
                title = video.title
                audio_streams[0].download(self.output_path, filename=title + ' (AUDIO)')
        except Exception as e:
            print(e)
            self.operation_error_network.pack(side=tk.TOP)
        else:
            self.operation_success.pack(side=tk.TOP)
            self.operation_in_progress.pack_forget()

        self.output_path = ''
        self.download_MP3['state'] = tk.ACTIVE
        self.download_MP4['state'] = tk.ACTIVE


    def txt_dl_screen(self):

        self.clear_screen(self)
        self.clear_screen(self.select_options_frame)
        self.clear_screen(self.url_frame)

        self.app_title.pack(side=tk.TOP)
        self.txt_file_instructions.pack(side=tk.TOP)
        self.select_file.pack(side=tk.LEFT, pady=10, padx=(250, 0))
        self.main_menu.pack(side=tk.RIGHT, padx=(0, 250))
        self.url_frame['text'] = '1. Select a text file'
        self.url_frame.pack(fill=tk.X)

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        
        self.download_MP3['command'] = lambda: self.get_output_path_and_start('txt_MP3')
        self.download_MP4['command'] = lambda: self.get_output_path_and_start('txt_MP4')

        self.download_MP3.pack(side=tk.LEFT, padx=(155, 0), pady=30)
        self.download_MP4.pack(side=tk.RIGHT, padx=(0, 155), pady=30)
        self.select_options_frame.pack(fill=tk.X, pady=50)
    

    def select_txt_file(self):

        self.txt_dl_screen()
        self.txt_file = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if self.txt_file != '' and self.txt_file != ():
            self.txt_file = open(self.txt_file)

            self.select_options_frame.pack_forget()
            self.file_selected.pack(side=tk.TOP, pady=30)
            self.select_options_frame.pack(side=tk.TOP, fill=tk.X)
            self.download_MP3['state'] = tk.ACTIVE
            self.download_MP4['state'] = tk.ACTIVE
    

    def download_txt_MP3(self):

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        for line in self.txt_file:
            try:
                self.yt_object = pytube.YouTube(line.strip())
                self.operation_in_progress.pack(side=tk.TOP)
                self.operation_success.pack_forget()
                self.yt_object.streams.filter(only_audio=True)[0].download(self.output_path)
                self.operation_in_progress.pack_forget()
                self.operation_success.pack(side=tk.TOP)
            except:
                self.operation_error_URL.pack(side=tk.TOP)
        self.download_MP3['state'] = tk.ACTIVE
        self.download_MP4['state'] = tk.ACTIVE


    def download_txt_MP4(self):

        self.download_MP3['state'] = tk.DISABLED
        self.download_MP4['state'] = tk.DISABLED
        for line in self.txt_file:
            try:
                self.yt_object = pytube.YouTube(line.strip())
                self.operation_in_progress.pack(side=tk.TOP)
                self.operation_success.pack_forget()
                self.yt_object.streams.get_highest_resolution().download(self.output_path)
                self.operation_in_progress.pack_forget()
                self.operation_success.pack(side=tk.TOP)
            except:
                self.operation_error_URL.pack(side=tk.TOP)
        self.download_MP3['state'] = tk.ACTIVE
        self.download_MP4['state'] = tk.ACTIVE

if __name__ == "__main__":
    root = YtDownloaderApp()
    root.mainloop()
    
