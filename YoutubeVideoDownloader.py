# used to create GUI
from tkinter import *

from tkinter import ttk

# used to select path
from tkinter.filedialog import askdirectory

# used to download video/playlist
from pytube import YouTube, Playlist

# used to divide process into different threads
from threading import Thread

# used to find local date and time
from time import strftime, localtime, gmtime

# used to download thumbnail
from urllib import request

# used to default download path in computer
from pathlib import Path

# used to create subprocess and open other application
import subprocess, sys, os


class YouTubeDownloader:

    def __init__(self):

        self.url = None

        self.title = None

        self.duration = None

        self.rating = None

        self.views = None

        self.length = None

        self.fileName = None

        self.fileSize = None

        self.numberOfVideos = None

        self.path = None

        self.sizes = None

        self.quality = None

        self.index = None

        self.playlistURLs = None

    def history(self):

        try:

            print("\n\n<<<<<<<<<<<<<<<<< Default Path >>>>>>>>>>>>>>>>>>\n")

            defaultPath = str(os.path.join(Path.home(), "Downloads"))

            print(
                'your default path to download video is : ' + defaultPath + "\n\n However you can change it any time "
                                                                            "by clicking choose folder Button:)")

            print("\n<<<<<<<<<<<<<<<<< ||||||||||| >>>>>>>>>>>>>>>>>>\n")

            self.path = defaultPath

            with open("history.txt", "a") as fp:

                if os.stat("history.txt").st_size == 0:
                    fp.write("Date-Time , File Name , Video Type , Location , Video Link \n")

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def onProgressOne(self, stream, chunk, bytesRemaining):

        try:

            videoDownloaded = (self.fileSize - bytesRemaining)

            downloadedPercent = (float(videoDownloaded / self.fileSize)) * float(100)

            progressBar['value'] = downloadedPercent

            root.update_idletasks()

            print(downloadedPercent)

            historyButton.config(text="{:.2f} % Downloaded".format(downloadedPercent))

            label2.config(text="{}/{} Videos downloaded [{:.2f}/{:.2f}] MB".format(self.index, self.numberOfVideos,
                                                                                   videoDownloaded / (1024 * 1024),
                                                                                   self.fileSize / (1024 * 1024)))

            root.update_idletasks()

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def onProgressTwo(self, current, total):

        try:

            progressBar['value'] = (current / total * 100)

            root.update_idletasks()

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def updateHistory(self, extension, url):

        try:

            if sys.platform.startswith('win32'):

                location = self.path + "\\" + self.fileName + extension

            else:

                location = self.path + "/" + self.fileName + extension

            print("\n>>>>>>>>>>>>>>> download location <<<<<<<<<<<<<<<<< \n" + location)

            with open("history.txt", "a") as fp:

                fp.write("\n" + str(strftime("%Y-%m-%d %H:%M:%S", localtime())) + " , " + self.fileName + " , " +
                        choices['values'][choices.current()] + " ," + location + ", " + url)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def downloadHD(self):

        try:

            yt = YouTube(self.url, on_progress_callback=self.onProgressOne())

            self.fileName = re.sub(r"[^a-zA-Z0-9]", "", str(self.title)) + str(
                choices['values'][choices.current()]) + str(self.index)

            root.update_idletasks()

            itag = self.selectQuality()

            stream = yt.streams.get_by_itag("140")

            self.fileSize = yt.streams.get_by_itag("140").filesize + yt.streams.get_by_itag(itag).filesize

            # progress_bar["maximum"] = self.file_size

            print("audio download started")

            if sys.platform.startswith('win32'):

                Audio = "\\" + self.fileName + "audio"

            else:

                Audio = "/" + self.fileName + "audio"

            if sys.platform.startswith('win32'):

                Video = "\\" + self.fileName + "video"

            else:

                Video = "/" + self.fileName + "video"

            stream.download(self.path, filename=Audio)

            print("audio downloaded ,,,,,,,")

            print(self.path)

            os.rename(self.path + Audio + ".mp4", self.path + Audio + ".mp3")

            stream = yt.streams.get_by_itag(itag)

            print("Video download started")

            stream.download(self.path, filename=Video)

            print("Video download completed ,,,,,,,")

            print(self.path)
            print()

            print(
                "merging audio and Video file with ffmpeg as pytube does not support 1080p and higher stream with audio")
            print()

            location = None

            if sys.platform.startswith('win32'):

                location = self.path + "\\" + self.fileName + ".mkv"

            else:

                location = self.path + "/" + self.fileName + ".mkv"

            if itag == "137":

                cmd = 'ffmpeg -y -i ' + self.path + Audio + '.mp3  -r 30 -i ' + self.path + Video + '.mp4  -filter:a ' \
                                                                                                    'aresample=async=1 ' \
                                                                                                    '-c:a flac -c:v ' \
                                                                                                    'copy ' + location

                subprocess.call(cmd, shell=True)

                os.remove(self.path + Video + '.mp4')

            else:

                cmd = 'ffmpeg -y -i ' + self.path + Audio + '.mp3  -r 30 -i ' + self.path + Video + '.webm  -filter:a ' \
                                                                                                    'aresample=async=1 ' \
                                                                                                    '-c:a flac -c:v ' \
                                                                                                    'copy ' + location

                subprocess.call(cmd, shell=True)

                os.remove(self.path + Video + '.webm')

            os.remove(self.path + Audio + '.mp3')

            self.updateHistory(".mkv", self.url)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occor <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def singleDownload(self):

        try:

            if self.selectQuality() in ("313", "271", "137"):

                self.downloadHD()

            elif self.selectQuality() == "1":

                self.fileName = re.sub(r"[^a-zA-Z0-9_-]", "", self.title)

                label2.config(text="{}/{} thumbnail downloaded".format(0, 1))

                if sys.platform.startswith('win32'):

                    request.urlretrieve(self.thumbnail_url, self.path + "\\" + self.fileName + ".jpeg")

                else:

                    request.urlretrieve(self.thumbnail_url, self.path + "/" + self.fileName + ".jpeg")

                self.onProgressTwo(1, 1)

                self.updateHistory(".jpeg", self.url)

            else:

                yt = YouTube(self.url, on_progress_callback=self.onProgressOne)

                self.fileName = re.sub(r"[^a-zA-Z0-9_-]", "", self.title) + str(choices['values'][choices.current()])

                root.update_idletasks()

                itag = self.selectQuality()

                print(itag)

                stream = yt.streams.get_by_itag(itag)

                print(stream.title)

                self.fileSize = stream.filesize

                print(stream.filesize // (1024 * 1024))

                print("download started")

                stream.download(self.path, filename=self.fileName)

                print("download completed ,,,,,,,")

                print(self.path)

                location = None

                if sys.platform.startswith('win32'):

                    location = self.path + "\\" + self.fileName

                else:

                    location = self.path + "/" + self.fileName

                if itag == "140":

                    os.rename(location + ".mp4", location + ".mp3")

                    self.updateHistory(".mp3", self.url)

                elif itag == "251":

                    os.rename(location + ".webm", location + ".mp3")

                    self.updateHistory(".mp3", self.url)

                else:

                    self.updateHistory(".mp4", self.url)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def multipleDownload(self):

        try:

            print("\n>>>>>>>>>>>>>>> Number of videos in playlist <<<<<<<<<<<<<<<<< \n" + str(self.numberOfVideos))

            if self.selectQuality() in ("313", "271", "137"):

                self.index = 0

                for url in self.playlistURLs:
                    self.url = url

                    print("\n>>>>>>>>>>>>>>> Video url<<<<<<<<<<<<<<<<< \n" + self.url)

                    self.downloadHD()

                    self.index += 1

            elif self.selectQuality() == "1":

                self.index = 0

                label2.config(text="{}/{} thumbnail downloaded".format(self.index, self.numberOfVideos))

                for url in self.playlistURLs:

                    self.index += 1

                    print("\n>>>>>>>>>>>>>>> Vedio url<<<<<<<<<<<<<<<<< \n" + url)

                    yt = YouTube(url)

                    self.fileName = re.sub(r"[^a-zA-Z0-9_-]", "", yt.title) + str(
                        choices['values'][choices.current()]) + str(self.index)

                    root.update_idletasks()

                    if sys.platform.startswith('win32'):

                        request.urlretrieve(yt.thumbnail_url, self.path + "\\" + self.fileName + ".jpeg")

                    else:

                        request.urlretrieve(yt.thumbnail_url, self.path + "/" + self.fileName + ".jpeg")

                    root.update_idletasks()

                    label2.config(text="{}/{} thumbnail downloaded".format(self.index, self.numberOfVideos))

                    self.onProgressTwo(self.index, self.numberOfVideos)

                    label2.config(text="{}/{} thumbnail downloaded".format(self.index, self.numberOfVideos))

                    self.updateHistory(".jpeg", url)

            else:

                self.index = 0

                for url in self.playlistURLs:

                    # label2.config(text = "{}/{} Vedios downloaded".format(i,self.no_of_vedios))

                    yt = YouTube(url, on_progress_callback=self.onProgressOne)

                    self.fileName = re.sub(r"[^a-zA-Z0-9_-]", " ", yt.title) + str(
                        choices['values'][choices.current()]) + str(self.index)

                    label4.config(text="wait for vedio to download completly")

                    label3.config(
                        text="RATING : " + str(yt.rating) + " VIEWS : " + str(yt.views) + " DURATION : " + strftime(
                            "%H:%M:%S", gmtime(yt.length)), font=("Arial", 14, "bold"))

                    itag = self.selectQuality()

                    root.update_idletasks()

                    print(itag)

                    stream = yt.streams.get_by_itag(itag)

                    print(stream.title)

                    self.fileSize = stream.filesize

                    print(stream.filesize)

                    print("download started")

                    stream.download(self.path, filename=self.fileName)

                    # print("{} vedio downloaded \n ".format(i+1))

                    location = None

                    if sys.platform.startswith('win32'):

                        location = self.path + "\\" + self.fileName

                    else:

                        location = self.path + "/" + self.fileName

                    if itag == "140":

                        os.rename(location + ".mp4", location + ".mp3")

                        self.updateHistory(".mp3", url)

                    elif itag == "251":

                        os.rename(location + ".webm", location + ".mp3")

                        self.updateHistory(",mp3", url)

                    else:

                        self.updateHistory(".mp4", url)

                    self.index += 1

            print("\n<<<<<<<<<<<< entire playlist downloaded >>>>>>>>>>>>>>>>\n")

            print("\n>>>>>>>>>>>>>>> download path <<<<<<<<<<<<<<<<< \n" + self.path)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def startDownloading(self):

        try:

            ch = radioVar.get()

            progressBar['value'] = 0

            if ch == "1":

                print("\n>>>>>>>>>>>>> You are downloading a single vedio <<<<<<<<<<<<\n")

                self.singleDownload()

            else:

                print("\n>>>>>>>>>>>>> You are downloading a playlist <<<<<<<<<<<<<<<\n")

                self.multipleDownload()

            downloadButton.config(text="Download")

            downloadButton.config(state=NORMAL)

            clearURLButton.config(text="clear")

            clearURLButton.config(state=NORMAL)

            selectPathButton.config(state=NORMAL)

            playVideoButton.config(state=NORMAL)

            redButton.config(state=NORMAL)

            greenButton.config(state=NORMAL)

            orangeButton.config(state=NORMAL)

            violetButton.config(state=NORMAL)

            pinkButton.config(state=NORMAL)

            brownButton.config(state=NORMAL)

            yellowButton.config(state=NORMAL)

            lightgreenButton.config(state=NORMAL)

            blueButton.config(state=NORMAL)

            greyButton.config(state=NORMAL)

            iconButton.config(state=NORMAL)

            historyButton.config(text="History")

            label1.config(text=" Your download completed enjoy :) ", fg="green",
                          font=("Arial", 15, "bold"))

            label2.config(text="select download location", fg="black",  font=("Arial", 15, "bold"))

            label3.config(text="select quality of Video to download", fg="black", font=("Arial", 15, "bold"))

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def startDownlodingThread(self):

        try:

            if len(self.url) < 2:
                label1.config(text=" Url field is empty ", fg="black")

                print("\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> url field is empty <<<<<<<<<<<<<<<<<<\n")

                return

            if "https://www.youtube.com/" not in self.url:
                label1.config(text=" Please Enter Valid Url ", fg="black")

                return

            if radioVar.get() == "1" and "playlist" in self.url:
                label1.config(text="link not match with its type", fg="black")

                print(
                    "\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> you are trying to download playlist by selecting "
                    "single video Radiobutton <<<<<<<<<<<<<<<<<<\n")

                return

            if radioVar.get() == "2" and "watch" in self.url:
                label1.config(text=" link not match with its type ", fg="red")

                print(
                    "\nERROR MESSAGE : >>>>>>>>>>>>>>>>>>>>>>>>> you are trying to download single video by selecting "
                    "playlist Radiobutton <<<<<<<<<<<<<<<<<<\n")

                return

            print("\n>>>>>>>>>>>>>>>> Video Download Started :) <<<<<<<<<<<<<<<<< \n")

            label1.config(text=" 		Your download started :) 		", fg="blue",
                        font=("Arial", 15, "bold"))

            clearURLButton.config(text="please")

            clearURLButton.config(state=DISABLED)

            downloadButton.config(text="Wait...")

            downloadButton.config(state=DISABLED)

            selectPathButton.config(state=DISABLED)

            playVideoButton.config(state=DISABLED)

            redButton.config(state=DISABLED)

            brownButton.config(state=DISABLED)

            greenButton.config(state=DISABLED)

            orangeButton.config(state=DISABLED)

            violetButton.config(state=DISABLED)

            iconButton.config(state=DISABLED)

            pinkButton.config(state=DISABLED)

            greyButton.config(state=DISABLED)

            blueButton.config(state=DISABLED)

            yellowButton.config(state=DISABLED)

            lightgreenButton.config(state=DISABLED)

            root.update_idletasks()

            thread = Thread(target=self.startDownloading())

            thread.start()

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def select_path(self, defaultPath=None):

        try:

            self.path = askdirectory()

            if len(self.path) <= 1:
                self.path = defaultPath

            tmp = self.path

            if len(tmp) > 55:
                tmp = tmp[:55]

            label2.config(text="Path : " + str(tmp), font=("Arial", 14, "bold"))

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def selectQuality(self, event=None):

        try:

            choice = choices.current()

            itag = None

            if choice == 7:

                itag = '313'  # itag for 2160p video

            elif choice == 6:

                itag = '271'  # itag for 1440p video

            elif choice == 5:

                itag = '137'  # itag for 1080p video

            elif choice == 4:

                itag = '22'  # itag for 720p video

            elif choice == 3:

                itag = '18'  # itag for 360p video

            elif choice == 2:

                itag = '251'  # itag for webm audio 160 kbps

            elif choice == 1:

                itag = '140'  # itag for mp4 audio

            else:

                itag = '1'  # for video thumbnail download

            if radioVar.get() == "1":
                label3.config(
                    text="Quality : " + choices['values'][choice] + " Size : {:.2f} MB".format(self.sizes[choice]))

            return itag

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def check_url(self, urlVar):

        try:

            self.url = urlVar.get()

            if len(self.url) < 1:
                label1.config(text=" Url field is empty ", fg="yellow")

                # print("url field is empty")

                return

            if "https://www.youtube.com/" not in self.url:
                label1.config(text=" Please Enter Valid Url ", fg="yellow")

                # print("invlaid url")

                return

            if radioVar.get() == "1" and "playlist" in self.url:
                urlField.delete(0, END)

                label1.config(text="Error link not match with its type ", fg="yellow")

                print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error link not match with its type >>>>>>>>>>>>>>>>>>>>>>>>\n")

                print("you are trying to download playlist by selecting single video Radiobutton")

                return

            if radioVar.get() == "2" and "watch" in self.url:
                self.clearUrlField()

                label1.config(text="Error link not match with its type ", fg="yellow")

                print("\n<<<<<<<<<<<<<<<<<<<<<<<< Error link not match with its type >>>>>>>>>>>>>>>>>>>>>>>>\n")

                print("you are trying to download single video by selecting playlist Radiobutton")

                return

            if radioVar.get() == "1" and "watch" in self.url:

                label1.config(text="	 processing Video link wait ... 	", fg="black")

                root.update_idletasks()

                print("\n<<<<<<<<<<<<<<<<<<<< video Url >>>>>>>>>>>>>>>>>\n\n" + self.url)

                yt = YouTube(self.url)

                self.title = re.sub(r'[^a-zA-Z0-9_-]', '', yt.title)

                self.description = yt.description

                self.rating = yt.rating

                self.views = yt.views

                self.length = strftime("%H:%M:%S", gmtime(yt.length))

                self.thumbnail_url = yt.thumbnail_url

                self.index = 0

                self.numberOfVideos = 1

                print("\n<<<<<<<<<<<<<<<<<<<< Video Title >>>>>>>>>>>>>>>>>\n\n" + self.title)
                print()

                print("\n<<<<<<<<<<<<<<<<<<<< DESCRIPTION >>>>>>>>>>>>>>>>>\n\n" + self.description)
                print()

                print("\n>>>>>>>>>>>>>>> Rating : {:.2f}".format(self.rating))
                print()

                print("\n>>>>>>>>>>>>>>> Views : {}".format(self.views))
                print()

                print("\n>>>>>>>>>>>>>>> Duration : " + self.length)
                print()

                print("\n>>>>>>>>>>>>>>> video thumbnail : " + self.thumbnail_url)
                print()

                self.quality = ["thumbnail"]

                self.sizes = [0.5]

                if yt.streams.get_by_itag("140") is not None:
                    self.quality.append("mp3")

                    self.sizes.append(yt.streams.get_by_itag("140").filesize / (1024 * 1024))

                if yt.streams.get_by_itag("251") is not None:
                    self.quality.append("webm")

                    self.sizes.append(yt.streams.get_by_itag("251").filesize / (1024 * 1024))

                if yt.streams.get_by_itag("18") is not None:
                    self.quality.append("360p")

                    self.sizes.append(yt.streams.get_by_itag("18").filesize / (1024 * 1024))

                if yt.streams.get_by_itag("22") is not None:
                    self.quality.append("720p")

                    self.sizes.append(yt.streams.get_by_itag("22").filesize / (1024 * 1024))

                if yt.streams.get_by_itag("137") is not None:
                    self.quality.append("1080p")

                    self.sizes.append(
                        (yt.streams.get_by_itag("137").filesize + yt.streams.get_by_itag("140").filesize) / (
                                1024 * 1024))

                if yt.streams.get_by_itag("271") is not None:
                    self.quality.append("1440p")

                    self.sizes.append(
                        (yt.streams.get_by_itag("271").filesize + yt.streams.get_by_itag("140").filesize) / (
                                1024 * 1024))

                if yt.streams.get_by_itag("313") is not None:
                    self.quality.append("2160p")

                    self.sizes.append(
                        (yt.streams.get_by_itag("313").filesize + yt.streams.get_by_itag("140").filesize) / (
                                1024 * 1024))

                choices['values'] = self.quality

                if "2160p_FULL_HD_video" in self.quality:

                    choices.current(7)

                elif "1440p_video" in self.quality:

                    choices.current(6)

                elif "1080p_HD_video" in self.quality:

                    choices.current(5)

                elif "720p_video" in self.quality:

                    choices.current(4)

                elif "360p_video" in self.quality:

                    choices.current(3)

                elif "webm_audio" in self.quality:

                    choices.current(2)

                elif "mp3_audio" in self.quality:

                    choices.current(1)

                else:

                    choices.current(0)

                choice = choices.current()

                print("\n<<<<<<<<<<<<<< video Available at Quality >>>>>>>>>>>>>>\n")

                print(self.quality)

                print("\n<<<<<<<<<<<<<< Size correspond to Quality >>>>>>>>>>>>>>\n")

                print(self.sizes)

                if len(self.title) > 40:
                    self.title = self.title[:40]

                label1.config(text="Title : " + self.title, fg="black", font=("Arial", 14, "bold"))

                tmp = self.path

                if len(tmp) > 55:
                    tmp = tmp[:55]

                label2.config(text="Path : " + str(tmp), font=("Arial", 14, "bold"))

                label3.config(
                    text=" Quality : " + choices['values'][choice] + " Size : {:.2f} MB".format(self.sizes[choice]),
                    font=("Arial", 14, "bold"))

                label4.config(text=" Rating : {:.2f}".format(self.rating) + " Views : " + str(
                    self.views) + " Duration : " + self.length + " ", font=("Arial", 14, "bold"))

                downloadButton.config(state=NORMAL)

            elif radioVar.get() == "2" and "playlist" in self.url:

                label1.config(text="	processing playlist link wait ...	", fg="yellow")

                root.update_idletasks()

                self.playlistURLs = Playlist(self.url)

                print("\n <<<<<<<<<<<< list of url in Playlist >>>>>>>>>>>>>> \n")

                print(self.playlistURLs)

                print("\n <<<<<<<<<<<< ----------------------- >>>>>>>>>>>>>> \n")

                self.numberOfVideos = len(self.playlistURLs)

                if self.numberOfVideos == 0:
                    self.clearUrlField()

                    label1.config(text="playlist is empty try again ", fg="yellow")

                    print(
                        "\n<<<<<<<<<<<<<<<<<<<<<<<< Error playlist is empty please try again by entering the same "
                        "link >>>>>>>>>>>>>>>>>>>>>>>>\n")

                    return

                self.quality = ["thumbnail"]

                self.sizes = [0.5]

                yt = None

                for url in self.playlistURLs:
                    yt = YouTube(url)

                    break

                if yt.streams.get_by_itag("140") is not None:
                    self.quality.append("mp3_audio")

                # self.sizes.append((yt.streams.get_by_itag("140").filesize)/(1024*1024))

                if yt.streams.get_by_itag("251") is not None:
                    self.quality.append("webm_audio")

                # self.sizes.append((yt.streams.get_by_itag("251").filesize)/(1024*1024))

                if yt.streams.get_by_itag("18") is not None:
                    self.quality.append("360p_video")

                # self.sizes.append((yt.streams.get_by_itag("18").filesize)/(1024*1024))

                if yt.streams.get_by_itag("22") is not None:
                    self.quality.append("720p_video")

                # self.sizes.append((yt.streams.get_by_itag("22").filesize)/(1024*1024))

                if yt.streams.get_by_itag("137") is not None:
                    self.quality.append("1080p_HD_video")

                # self.sizes.append((yt.streams.get_by_itag("137").filesize + yt.streams.get_by_itag(
                # "140").filesize)/(1024*1024))

                if yt.streams.get_by_itag("271") is not None:
                    self.quality.append("1440p_video")

                # self.sizes.append((yt.streams.get_by_itag("271").filesize + yt.streams.get_by_itag(
                # "140").filesize)/(1024*1024))

                if yt.streams.get_by_itag("313") is not None:
                    self.quality.append("2160p_FULL_HD_video")

                # self.sizes.append((yt.streams.get_by_itag("313").filesize + yt.streams.get_by_itag(
                # "140").filesize)/(1024*1024))

                choices['values'] = self.quality

                if "2160p_FULL_HD_video" in self.quality:

                    choices.current(7)

                elif "1440p_video" in self.quality:

                    choices.current(6)

                elif "1080p_HD_video" in self.quality:

                    choices.current(5)

                elif "720p_video" in self.quality:

                    choices.current(4)

                elif "360p_video" in self.quality:

                    choices.current(3)

                elif "webm_audio" in self.quality:

                    choices.current(2)

                elif "mp3_audio" in self.quality:

                    choices.current(1)

                else:

                    choices.current(0)

                choice = choices.current()

                print("\n<<<<<<<<<<<<<< video available at Quality >>>>>>>>>>>>>>\n")

                print(self.quality)

                # print("\n<<<<<<<<<<<<<< Size corresponding to Quality >>>>>>>>>>>>>>\n")

                # print(self.sizes)

                label1.config(text=" Playlist contain total {} videos ".format(self.numberOfVideos), fg="red",
                            font=("", 14, "bold"))

                downloadButton.config(state=NORMAL)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def clearUrlField(self):

        try:

            urlField.delete(0, END)

            label1.config(text="paste YouTube video link here", fg="black", font=("Arial", 15, "bold"))

            label2.config(text="select download location", font=("Arial", 15, "bold"), fg="black")

            label3.config(text="select Quality of video to download", font=("Arial", 15, "bold"), fg="black")

            label4.config(text="Open Downloaded video", fg="black", font=("Arial", 15, "bold"))

            downloadButton.config(state=DISABLED)

            choices['values'] = [" please insert link first "]

            choices.current(0)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def openDownloadedVideo(self):

        try:

            tmp = ""

            with open("history.txt", "r") as f:

                data = f.readlines()

                lastline = data[-1]

                tmp = lastline.split(",")

                print("\n <<<<<<<<<<<<< file details >>>>>>>>>>>>>>\n")

                print("\n\tdownload date and time: " + tmp[0] + "\n\t file name : " + tmp[
                    1] + "\n\t download quality : " + tmp[2] + "\n\tdownload at location: " + tmp[
                          3] + "\ndownload from url : " + tmp[4])

                print("\n <<<<<<<<<<<<< end of file details >>>>>>>>>>>>>>\n")

                tmp = tmp[3]

            if sys.platform.startswith('linux'):

                subprocess.Popen(['xdg-open', tmp],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif sys.platform.startswith('win32'):

                os.startfile(tmp)

            elif sys.platform.startswith('cygwin'):

                os.startfile(tmp)

            elif sys.platform.startswith('darwin'):

                subprocess.Popen(['open', tmp],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:

                subprocess.Popen(['xdg-open', tmp],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print(
                "\n    Be patient your video will play soon \n You can also go to this " + self.path + "in your file "
                                                                                                    "manager to "
                                                                                                    "open it "
                                                                                                    "manualy")

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def openYoutube(self):

        try:

            url = "https://www.youtube.com/"

            if sys.platform.startswith('linux'):

                subprocess.Popen(['xdg-open', url],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            elif sys.platform.startswith('win32'):

                os.startfile(url)

            elif sys.platform.startswith('cygwin'):

                os.startfile(url)

            elif sys.platform.startswith('darwin'):

                subprocess.Popen(['open', url],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:

                subprocess.Popen(['xdg-open', url],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except Exception as e:

            print("\n>>>>>>>>>>>>>>> Error Occur <<<<<<<<<<<<<<<<< \n\n" + str(e))

    def openHistory(self):

        file = "history.txt"

        if sys.platform.startswith('linux'):

            subprocess.Popen(['xdg-open', file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        elif sys.platform.startswith('win32'):

            os.startfile(file)

        elif sys.platform.startswith('cygwin'):

            os.startfile(file)

        elif sys.platform.startswith('darwin'):

            subprocess.Popen(['open', file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:

            subprocess.Popen(['xdg-open', file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def setBgToGrey():
    root.configure(background="grey")

    topframe.configure(background="grey")

    middleframe.configure(background="grey")


def setBgToRed():
    root.configure(background="red")

    topframe.configure(background="red")

    middleframe.configure(background="red")


def setBgToPink():
    root.configure(background="pink")

    topframe.configure(background="pink")

    middleframe.configure(background="pink")


def setBgToBrown():
    root.configure(background="brown")

    topframe.configure(background="brown")

    middleframe.configure(background="brown")


def setBgToGreen():
    root.configure(background="green")

    topframe.configure(background="green")

    middleframe.configure(background="green")


def setBgToBlue():
    root.configure(background="lightblue")

    topframe.configure(background="lightblue")

    middleframe.configure(background="lightblue")


def setBgToOrange():
    root.configure(background="orange")

    topframe.configure(background="orange")

    middleframe.configure(background="orange")


def setBgToViolet():
    root.configure(background="violet")

    topframe.configure(background="violet")

    middleframe.configure(background="violet")


def setBgToYellow():
    root.configure(background="yellow")

    topframe.configure(background="yellow")

    middleframe.configure(background="yellow")


def setBgToLightGreen():
    root.configure(background="lightgreen")

    topframe.configure(background="lightgreen")

    middleframe.configure(background="lightgreen")


if __name__ == '__main__':
    yd = YouTubeDownloader()

    print(yd.__doc__)

    yd.history()

    root = Tk()

    root.title("YouTubeDownloader")

    root.geometry("800x700")

    root.resizable(width=False, height=False)

    root.configure(background="lightblue")

    label1 = Label(root, text="YouTube Video Downloader", fg="black", font=("Times new roman", 15, "bold"))

    label1.pack(side=TOP, pady=20)

    topframe = Frame(root, background="lightblue")

    topframe.pack()

    darkcolor = Frame(topframe)

    darkcolor.pack(side=LEFT)

    iconImage = PhotoImage(file="images/youtubedownloader.png")

    iconImage = iconImage.subsample(1, 1)

    iconButton = Button(topframe, image=iconImage, command=yd.openYoutube)

    iconButton.pack(side=LEFT, padx=75)

    lightcolor = Frame(topframe)

    lightcolor.pack(side=LEFT)

    redImage = PhotoImage(file="images/red.png")

    brownImage = PhotoImage(file="images/brown.png")

    pinkImage = PhotoImage(file="images/pink.png")

    greyImage = PhotoImage(file="images/grey.png")

    greenImage = PhotoImage(file="images/green.png")

    blueImage = PhotoImage(file="images/blue.png")

    violetImage = PhotoImage(file="images/violet.png")

    orangeImage = PhotoImage(file="images/orange.png")

    yellowImage = PhotoImage(file="images/yellow.png")

    lightGreenImage = PhotoImage(file="images/lightgreen.png")

    redImage = redImage.subsample(4, 4)

    brownImage = brownImage.subsample(4, 4)

    pinkImage = pinkImage.subsample(4, 4)

    greyImage = greyImage.subsample(4, 4)

    greenImage = greenImage.subsample(4, 4)

    blueImage = blueImage.subsample(4, 4)

    violetImage = violetImage.subsample(4, 4)

    orangeImage = orangeImage.subsample(4, 4)

    yellowImage = yellowImage.subsample(4, 4)

    lightGreenImage = lightGreenImage.subsample(4, 4)

    redButton = Button(darkcolor, image=redImage, command=setBgToRed)

    redButton.pack(side=LEFT)

    brownButton = Button(darkcolor, image=brownImage, command=setBgToBrown)

    brownButton.pack(side=LEFT)

    greenButton = Button(darkcolor, image=greenImage, command=setBgToGreen)

    greenButton.pack(side=LEFT)

    orangeButton = Button(darkcolor, image=orangeImage, command=setBgToOrange)

    orangeButton.pack(side=LEFT)

    violetButton = Button(darkcolor, image=violetImage, command=setBgToViolet)

    violetButton.pack(side=LEFT)

    pinkButton = Button(lightcolor, image=pinkImage, command=setBgToPink)

    pinkButton.pack(side=LEFT)

    greyButton = Button(lightcolor, image=greyImage, command=setBgToGrey)

    greyButton.pack(side=LEFT)

    blueButton = Button(lightcolor, image=blueImage, command=setBgToBlue)

    blueButton.pack(side=LEFT)

    yellowButton = Button(lightcolor, image=yellowImage, command=setBgToYellow)

    yellowButton.pack(side=LEFT)

    lightgreenButton = Button(lightcolor, image=lightGreenImage, command=setBgToLightGreen)

    lightgreenButton.pack(side=LEFT)

    label1 = Label(root, text="paste YouTube video link here", fg="black", font=("Arial", 15, "bold"))

    label1.pack(side=TOP, padx=20, pady=10)

    s = ttk.Style()

    s.theme_use('clam')

    s.configure("red.Horizontal.TProgressbar", foreground='blue', background='black')

    progressBar = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient=HORIZONTAL, length=300,
                                mode='determinate')

    progressBar.pack(side=TOP, pady=(0, 10))

    frame = Frame(root, background="black")

    frame.pack()

    radioVar = StringVar(frame, "1")

    single = Radiobutton(frame, text="single video", variable=radioVar, value="1", fg="black",
                        font=("Arial", 10, "bold"))

    single.pack(side=LEFT)

    multiple = Radiobutton(frame, text="playlist", variable=radioVar, value="2", fg="black",
                        font=("Arial", 10, "bold"))

    multiple.pack(side=LEFT)

    url_var = StringVar()

    url_var.trace("w", lambda name, index, mode, sv=url_var: yd.check_url(url_var))

    urlField = Entry(frame, width=50, font=("Arial", "15"), textvariable=url_var)

    urlField.pack(side=LEFT)

    middleframe = Frame(root)

    middleframe.pack(pady=10)

    downloadButton = Button(middleframe, fg="black", text="Download",  font=("Arial", 10, "bold"),
                            state=DISABLED, width=15, height=1, command=yd.startDownlodingThread)

    downloadButton.pack(side=LEFT)

    clearURLButton = Button(middleframe, fg="black", text="clear", font=("Arial", 10, "bold"), width=15,
                            height=1, command=yd.clearUrlField)

    clearURLButton.pack(side=LEFT)

    historyButton = Button(middleframe, text="History", fg="black", font=("Arial", 10, "bold"), width=15,
                        height=1, command=yd.openHistory)

    historyButton.pack(side=LEFT)

    label2 = Label(root, text="select download location", fg="black", font=("Arial", 15, "bold"))

    label2.pack(pady=10)

    selectPathButton = Button(root, width=20, fg="black", text="choose folder", font=("Arial", 10, "bold"),
                            command=yd.select_path)

    selectPathButton.pack()

    label3 = Label(root, text="select Quality of video to download", font=("Arial", 15, "bold"), fg="black")

    label3.pack(pady=10)

    # Quality = ["thumbnail","mp3 audio only","webm audio only","mp4 360p","mp4 720p","mp4 1080p video only",
    # "mkv 1080p HD","mkv 1440p","mkv 2160p FULL HD"]

    quality = StringVar()

    choices = ttk.Combobox(root, textvariable=quality, values=["please insert link first "], width=30)

    choices.pack()

    choices.bind("<<ComboboxSelected>>", yd.selectQuality)

    label4 = Label(root, text="open downloaded video", font=("Arial", 15, "bold"), fg="black")

    label4.pack(pady=(10, 0))

    videoImage = PhotoImage(file="images/video.png")

    videoImage = videoImage.subsample(1, 1)

    playVideoButton = Button(root, image=videoImage, state=NORMAL, command=yd.openDownloadedVideo)

    playVideoButton.pack(side=TOP, pady=10)

    root.mainloop()
