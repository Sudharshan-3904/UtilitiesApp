"""
Work TO BE Completed:
//TODO - Audio noise removal
//TODO - Text to PDF
//TODO - Word to pdf
//TODO - Monitor Testing
-------

Working Components
1. Image file conversion 
2. Spreadsheet file conversion
3. Password Creation
4. Network Speed Test
5. Youtube Video Download
6. Video to audio converter
"""

import os
from PIL import Image
import pandas as pd
import random
import string
import time
import speedtest as st
from pytube import YouTube
import moviepy.editor as mp
import threading

class FileConverter:
    def __init__(self, file_obj="") -> None:
        self.file = file_obj
        self.files=""
        self.IMAGE_FORMATS = [".tiff", ".png", ".jpg", ".jpeg"]
        self.SPREADSHEET_FORMATS = [".xlsx", ".csv"]

    def getFilename(self):
        self.file = fb.askopenfilename()
        return self.file

    def getFilenames(self):
        self.files = fb.askopenfilenames()
        return self.files
    
    def convertImgFile(self, extension=""):
        if self.file == "":
            img_file = self.getFilename()
        else:
            img_file = self.file

        img_name = img_file.split(".", maxsplit=2)[0]
        im_obj = Image.open(img_file)
        save_name = img_name + extension
        im_obj.save(save_name)
    
    def convertToSpreadSheet(self, extension=""):
        if self.file == "":
            spreadSheetFile = self.getFilename()
        else:
            spreadSheetFile = self.file

        if extension == ".csv":
            newFrame = pd.read_csv(spreadSheetFile)
            newExcel = pd.ExcelWriter(spreadSheetFile.replace(".xlsx", ".csv"))
            newFrame.to_csv(newExcel, index=False)
            newExcel.save()
        elif extension == ".xlsx":
            newFrame = pd.read_csv(spreadSheetFile)
            newExcel = pd.ExcelWriter(spreadSheetFile.replace(".csv", ".xlsx"))
            newFrame.to_excel(newExcel, index=False)
            newExcel.save()
    
    def convertVideoToAudio(self, fileObjects=[]):
        if fileObjects==[]:
            fileObjects = self.getFilenames()
        for fileObject in fileObjects:
            filename, extension = os.path.splitext(fileObject)
            clip = mp.VideoFileClip(fileObject)
            clip.audio.write_audiofile(f"{filename}.mp3")
    
    def convertTextToPDF(self):
        ...
    
    def convertWordToPDF(self):
        ...


class Passwords:
    def __init__(self) -> None:
        self.__password = []

        characters = [string.ascii_letters, string.digits, "!@#$%^&*(<>,.?/\\|{}[])"]
        self.chars =[]

        for char_list in characters:
            for item in char_list:
                self.chars.append(item)

    def generatePassword(self, wordLength):
        self.__password = []
        for _ in range(wordLength):
            randChar = random.choice(self.chars)
            self.__password.append(randChar)
        
        return "".join(self.__password)
    
    def getPassword(self):
        return self.generatePassword()


class NetworkOperation:
    def speedTest(self):
        server = st.Speedtest()
        server.get_best_server()

        down = server.download()
        down = down / 1000000

        up = server.upload()
        up = up / 1000000

        ping = server.results.ping
        return {"Download": down, "Upload" : up, "Ping" : ping}
    
    def ytVideoDownload(self, url, saveLocation):
        video_download = YouTube(url)
        video_download = video_download.streams.get_highest_resolution()
        video_download.download(saveLocation)
        print('Video Downloaded', url)


class FileOPerations:
    def __init__(self) -> None:
        pass

    def monitorTest(self):
        ...



