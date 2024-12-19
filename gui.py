from tkinter import *
from tkinter import filedialog as fb
from CTkMessagebox import CTkMessagebox
import pandas as pd
import customtkinter as ctk
import time
import threading
import app


class Interface: 
    def __init__(self) -> None:
        self.__selected_mode = "System"
        self.__selected_theme = "dark-blue"
        self.__menuOption = ["Home", "File Conversion", "Password Generation", 
                            "Speedtest", "YT Video Download", "Convert To Audio"]
        self.__fileConvObj = app.FileConverter()
        self.__pwdObj = app.Passwords()
        self.__netOpeObj = app.NetworkOperation()

        self.__root = ctk.CTk()
        self.__root.title("Utilities App")
        self.__root._set_appearance_mode(self.__selected_mode)
        ctk.set_default_color_theme(self.__selected_theme)

        self.__pwdLenIntVar = ctk.IntVar()
        self.__mode_switch_string_var = ctk.StringVar()

        self.__menuFrame = ctk.CTkFrame(master=self.__root)
        self.__menuFrame.pack(anchor="s")

        self.__section_options = ctk.CTkOptionMenu(master=self.__menuFrame, command=self.updateSection, values=self.__menuOption)
        self.__section_options.grid(row=0, padx=10, pady=10)
        self.__section_options.set("Section")

        self.__appearance_mode_switch = ctk.CTkSwitch(master=self.__menuFrame, text="Mode Switch", command=self.updateMode ,variable=self.__mode_switch_string_var, offvalue="dark", onvalue="light")
        self.__appearance_mode_switch.grid(row=0, column=1, padx=10, pady=10)

        self.__section_content = ctk.CTkFrame(master=self.__root)
        self.__section_content.pack(anchor="s")

        self.updateSection("Home")

    def updateMode(self):
        mode = self.__mode_switch_string_var.get()
        self.__selected_mode = mode
        self.__root._set_appearance_mode(mode)

    def startApp(self):
        self.__root.mainloop()

    def showConfirm(self, message=""):
        msg = CTkMessagebox(title="Exit?", message=message, icon="question", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
    
        if response=="Yes":
            return True
        else:
            return False
    
    def showInfo(self, message=""):
        CTkMessagebox(title="Info", message=message)

        
    def stopApp(self):
        if self.showConfirm("Would you like to close the program ?"):
            self.showInfo("Closing in 3 sec.")
            time.sleep(3)
            self.__root.destroy()
        else:
            return
    
    def setFileName(self):
        self.__fileConvObj.getFilename()
        return
    
    def callConverter(self, file_extension=""):
        if file_extension in self.__fileConvObj.IMAGE_FORMATS:
            runner_thread = threading.Thread(target=self.__fileConvObj.convertImgFile, kwargs={'extension': file_extension})
        elif file_extension in self.__fileConvObj.SPREADSHEET_FORMATS:
            runner_thread = threading.Thread(target=self.__fileConvObj.convertToSpreadSheet, kwargs={'extension': file_extension})
        runner_thread.start()
        runner_thread.join()
    
    def downloadVideo(self):
        ytVidLink = self.__yt_link_entry_field.get()
        runner_thread = threading.Thread(target=self.__netOpeObj.ytVideoDownload, kwargs={"url": ytVidLink, "saveLocation": fb.askdirectory()})
        runner_thread.start()
        runner_thread.join()
    
    def downloadAudio(self):
        ytVidLink = self.__yt_link_entry_field.get()
        runner_thread = threading.Thread(target=self.__netOpeObj.ytAudioDownload, kwargs={"url": ytVidLink, "saveLocation": fb.askdirectory()})
        runner_thread.start()
        runner_thread.join()


    def generate_speedtest_report(self):
        self.showInfo("Testing the network speed. This may take a few seconds.")
        returned_dict = self.__netOpeObj.speedTest()
        time.sleep(0.1)
        self.__ping_display_label.configure(text=round(returned_dict["Ping"]))
        self.__upload_display_label.configure(text=round(returned_dict["Upload"]))
        self.__download_display_label.configure(text=round(returned_dict["Download"]))

    def displayPassword(self):
        pwdLength = self.__pwdLenIntVar.get()
        pwd = self.__pwdObj.generatePassword(wordLength=pwdLength)
        self.__password_display_label.configure(text=pwd)
        self.__root.clipboard_append(pwd)
        self.showInfo("Password Copied to your clipboard !!!")
    
    def convertVidToAudio(self):
        runner_thread = threading.Thread(target=self.__fileConvObj.convertVideoToAudio, kwargs={"fileObject": fb.askopenfilenames()})
        runner_thread.start()
        runner_thread.join()
    
    def updateSection(self, section=""):
        def clearFrame():
            for widget in self.__section_content.winfo_children():
                widget.destroy()

        match section:
            case "Home":
                clearFrame()
                self.__sections_label = ctk.CTkLabel(master=self.__section_content, text="")

                self.__file_conversion_home_button = ctk.CTkButton(master=self.__sections_label, text="File Conversion", command=lambda: self.updateSection("File Conversion"))
                self.__file_conversion_home_button.grid(row=0, columnspan=2)

                self.__password_generation_home_button = ctk.CTkButton(master=self.__sections_label, text="Password Generation", command=lambda: self.updateSection("Password Generation"))
                self.__password_generation_home_button.grid(row=1, columnspan=2)

                self.__network_operations_speedtest_home_button = ctk.CTkButton(master=self.__sections_label, text="Speed Test", command=lambda: self.updateSection("Speedtest"))
                self.__network_operations_speedtest_home_button.grid(row=2, columnspan=2)

                self.__network_operations_yt_video_download_home_button = ctk.CTkButton(master=self.__sections_label, text="YT Video Download", command=lambda: self.updateSection("YT Video Download"))
                self.__network_operations_yt_video_download_home_button.grid(row=3, columnspan=2)

                self.__convert_video_to_audio_home_button = ctk.CTkButton(master=self.__sections_label, text="Convert To Audio", command=lambda: self.updateSection("Convert To Audio"))
                self.__convert_video_to_audio_home_button.grid(row=4, columnspan=2)

                self.__sections_label.grid(row=1, column=1, rowspan=4, columnspan=4)

            case "File Conversion":
                clearFrame()

                self.__img_conversion_label = ctk.CTkLabel(master=self.__section_content, text="")

                self.__img_conversion_name = ctk.CTkLabel(master=self.__img_conversion_label, text="Convert Image Files")
                self.__img_conversion_name.grid(row=0, columnspan=2)

                self.__img_choose_label = ctk.CTkLabel(master=self.__img_conversion_label, text="Choose your file")
                self.__img_choose_label.grid(row=1, column=0)

                self.__img_choose_button = ctk.CTkButton(master=self.__img_conversion_label, text="Choose File", command=self.setFileName)
                self.__img_choose_button.grid(row=1, column=1)

                self.__to_img_extension_label = ctk.CTkLabel(master=self.__img_conversion_label, text="To extension")
                self.__to_img_extension_label.grid(row=2, column=0)

                self.__to_img_extension_menu = ctk.CTkOptionMenu(master=self.__img_conversion_label, values=[".png", ".tiff", ".jpg", ".jpeg"], command=self.callConverter)
                self.__to_img_extension_menu.set("File Extension")
                self.__to_img_extension_menu.grid(row=2, column=1)

                self.__img_conversion_label.pack(side="left")


                self.__img_conversion_label = ctk.CTkLabel(master=self.__section_content, text="")

                self.__img_conversion_name = ctk.CTkLabel(master=self.__img_conversion_label, text="Convert Spreadsheet Files")
                self.__img_conversion_name.grid(row=0, columnspan=2)

                self.__img_choose_label = ctk.CTkLabel(master=self.__img_conversion_label, text="Choose your file")
                self.__img_choose_label.grid(row=1, column=0)

                self.__img_choose_button = ctk.CTkButton(master=self.__img_conversion_label, text="Choose File", command=lambda: self.setFileName)
                self.__img_choose_button.grid(row=1, column=1)

                self.__to_img_extension_label = ctk.CTkLabel(master=self.__img_conversion_label, text="To extension")
                self.__to_img_extension_label.grid(row=2, column=0)

                self.__to_img_extension_menu = ctk.CTkOptionMenu(master=self.__img_conversion_label, values=[".xlsx", ".csv"], command=lambda: self.callConverter)
                self.__to_img_extension_menu.set("File Extension")
                self.__to_img_extension_menu.grid(row=2, column=1)

                self.__img_conversion_label.pack(side="right")

            case "Password Generation":
                clearFrame()
                
                self.__password_generator_label = ctk.CTkLabel(master=self.__section_content, text="")

                self.__password_generation_length_entry = ctk.CTkEntry(master=self.__password_generator_label, textvariable=self.__pwdLenIntVar)
                self.__password_generation_length_entry.grid(row=0, column=0)

                self.__password_generation_generate_button = ctk.CTkButton(master=self.__password_generator_label, text="Generate", command=self.displayPassword)
                self.__password_generation_generate_button.grid(row=0, column=1)

                self.__password_display_label = ctk.CTkLabel(master=self.__password_generator_label, text="")
                self.__password_display_label.grid(row=1, columnspan=2)

                self.__password_generator_label.grid(row=1, column=1, rowspan=4, columnspan=4)

            case "Speedtest":
                clearFrame()
                
                self.__speed_test_title_label = ctk.CTkLabel(master=self.__section_content, text="Speedtest")
                self.__speed_test_title_label.grid(row=0, column=0, columnspan=2)

                self.__speed_test_contents = ctk.CTkLabel(master=self.__section_content, text="")

                self.__ping_parent_label = ctk.CTkLabel(master=self.__speed_test_contents, text="")
                self.__ping_child_label = ctk.CTkLabel(master=self.__ping_parent_label, text="Ping", padx=10)
                self.__ping_child_label.grid(row=0, column=0)

                self.__ping_display_label = ctk.CTkLabel(master=self.__ping_parent_label, text="0")
                self.__ping_display_label.grid(row=0, column=1)

                self.__ping_unit_display_label = ctk.CTkLabel(master=self.__ping_parent_label, text="ms", padx=10)
                self.__ping_unit_display_label.grid(row=0, column=2)
                self.__ping_parent_label.grid(row=0, columnspan=3)

                
                self.__upload_speed_parent_label = ctk.CTkLabel(master=self.__speed_test_contents, text="")
                self.__upload_child_label = ctk.CTkLabel(master=self.__upload_speed_parent_label, text="Upload", padx=10)
                self.__upload_child_label.grid(row=1, column=0)

                self.__upload_display_label = ctk.CTkLabel(master=self.__upload_speed_parent_label, text="0")
                self.__upload_display_label.grid(row=1, column=1)

                self.__upload_unit_display_label = ctk.CTkLabel(master=self.__upload_speed_parent_label, text="mbps", padx=10)
                self.__upload_unit_display_label.grid(row=1, column=2)
                self.__upload_speed_parent_label.grid(row=1, columnspan=3)

                
                self.__download_speed_parent_label = ctk.CTkLabel(master=self.__speed_test_contents, text="")
                self.__download_child_label = ctk.CTkLabel(master=self.__download_speed_parent_label, text="Download", padx=10)
                self.__download_child_label.grid(row=2, column=0)

                self.__download_display_label = ctk.CTkLabel(master=self.__download_speed_parent_label, text="0")
                self.__download_display_label.grid(row=2, column=1)

                self.__download_unit_display_label = ctk.CTkLabel(master=self.__download_speed_parent_label, text="mbps", padx=10)
                self.__download_unit_display_label.grid(row=2, column=2)
                self.__download_speed_parent_label.grid(row=2, columnspan=3)

                self.__speed_test_button = ctk.CTkButton(master=self.__speed_test_contents, text="Test", command=self.generate_speedtest_report)
                self.__speed_test_button.grid(row=3, columnspan=3)

                self.__speed_test_contents.grid(row=1, column=1, rowspan=4, columnspan=4)

            case "YT Video Download":
                clearFrame()
                
                self.__video_download_title_label = ctk.CTkLabel(master=self.__section_content, text="Youtube Video Download")

                self.__yt_link_paste_label = ctk.CTkLabel(master=self.__video_download_title_label, text="")

                self.__yt_link_entry_field = ctk.CTkEntry(master=self.__yt_link_paste_label, placeholder_text="Paste Link here")
                self.__yt_link_entry_field.grid(row=0, columnspan=3)

                self.__yt_link_video_download_button = ctk.CTkButton(master=self.__yt_link_paste_label, text="Download Video", command=self.downloadVideo)
                self.__yt_link_video_download_button.grid(row=0, column=3, columnspan=1)

                self.__yt_link_paste_label.grid(row=1, column=0, columnspan=4)

                self.__video_download_title_label.grid(row=1, column=1, rowspan=4, columnspan=4)
        
            case "Convert To Audio":
                clearFrame()
                self.__convert_video_to_audio_main_label = ctk.CTkLabel(master=self.__section_content, text="Convert Video To Audio")

                self.__choose_video_file_button = ctk.CTkButton(master=self.__convert_video_to_audio_main_label, text="Choose Video File", command=lambda: self.__fileConvObj.convertVideoToAudio())
                self.__choose_video_file_button.grid(row=0, column=0, rowspan=4)

                self.__convert_video_to_audio_main_label.grid(row=1, column=1, columnspan=4, rowspan=4)
                ...
            
            case _:              # Default Case
                clearFrame()
                self.updateSection(section="Home")
            
        self.__root.update()

mainThread = threading.Thread(target=Interface().startApp(), daemon=True)
mainThread.start()
mainThread.join()
