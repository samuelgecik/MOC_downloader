import ctypes
import asyncio
import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkCheckBox, CTkImage, ThemeManager, CTkTabview
from course_info import CourseInfo
from scraping import LinkScraper
from downloading import Downloader
from PIL import Image, ImageTk
# from .downloading import Downloader

class MainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Course Downloader")
        self.master.geometry("800x800")
        self.link_scraper = None
        self.course_info = None
        #  Set the scaling factor
        # self.master.tk.call("tk", "scaling", 2.0)

        # self.tab_control = ttk.Notebook(self.master)

        # self.tab1 = ttk.Frame(self.tab_control)
        # self.tab_control.add(self.tab1, text="Download Course")

        # self.tab2 = ttk.Frame(self.tab_control)
        # self.tab_control.add(self.tab2, text="Content Selection")

        self.tab_control = CTkTabview(self.master, corner_radius=0, border_width=0)
        self.tab1 = self.tab_control.add("Download Course")
        self.tab2 = self.tab_control.add("Content Selection")
        

        self.create_widgets()

        self.tab_control.pack(expand=1, fill="both")

        self.output_path = None
        self.scraper = None

    def create_widgets(self):
        self.canvas = tk.Canvas(self.tab1)
        self.canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        entry_var = tk.StringVar()
        entry_var.set("Enter course URL here")
        entry_var.trace_add("write", self.entry_write_callback)
        self.course_url_entry = CTkEntry(
            self.canvas,
            corner_radius=0,
            border_width=0,
            placeholder_text_color=ThemeManager.theme["CTkEntry"]["placeholder_text_color"],

            textvariable=entry_var,
        )
        self.course_url_entry.pack(fill="both", expand=True, padx=(0, 30))
        
        self.paste_button = CTkButton(
            self.canvas,
            text="",
            # TODO: PIL image support
            image=CTkImage(Image.open(r"C:\Users\samo\dev\MOC_downloader\src\paste_blue.png"), size=(25, 25)),
            fg_color=ThemeManager.theme["CTkEntry"]["fg_color"],
            # bg_color="transparent",
            corner_radius=0,
            hover=False,
            width=30,
            command=self.paste_clipboard_callback,
        )
        self.paste_button.place(relx=1.0, rely=0.5, anchor="e")

        self.get_info_button = CTkButton(
            self.tab1, text="Get Course Info", state="disabled", command=self.course_info_callback
        )
        self.get_info_button.grid(row=1, column=0, padx=10, pady=10)

        self.output_button = CTkButton(
            self.tab1, text="Choose Output Folder", state="disabled", command=self.select_output_callback
        )
        self.output_button.grid(row=2, column=0, padx=10, pady=10)

        self.download_button = CTkButton(
            self.tab1, text="Download", state="disabled", command=self.download
        )
        self.download_button.grid(row=3, column=0, padx=10, pady=10)

        self.course_name_label = CTkLabel(self.tab1, text="", anchor="w", text_color="gray")
        self.course_name_label.grid(row=4, column=0, sticky="w")

        self.total_size_label = CTkLabel(self.tab1, text="", anchor="w", text_color="gray")
        self.total_size_label.grid(row=5, column=0, sticky="w")

        self.tab1.grid_columnconfigure(0, weight=1)

        self.checkbuttons = []
        self.var_list = []

        for i, video in enumerate(self.course_info.videos):
            var = tk.IntVar()
            self.var_list.append(var)
            self.checkbuttons.append(CTkCheckBox(self.tab2, text=video.title, var=var))
            self.checkbuttons[i].grid(row=i, column=0, sticky="w")
    
##########################################
##### Callbacks and async functions ######
##########################################

    def paste_clipboard_callback(self): 
        clipboard_content = self.master.clipboard_get()
        self.course_url_entry.delete(0, "end")
        self.course_url_entry.insert(0, clipboard_content)

    def entry_write_callback(self, *args):
        if self.course_url_entry.get() == "":
            raise ValueError("URL cannot be empty")
        # self.scraper = LinkScraper(self.course_url_entry.get())
        self.get_info_button.configure(state="normal")
        self.output_button.configure(state="normal")
        self.download_button.configure(state="normal")

    def select_output_callback(self):
        self.output_path = filedialog.askdirectory()

    def download_callback(self):
        if self.download_button.cget("state") == "normal":
            self.download_button.configure(state="disabled")
            self.download_button.configure(text="Downloading...")

    async def download(self):
        if self.output_path is None:
            return
        download_links = self.scraper.get_download_links()
        downloader = Downloader(download_links, self.output_path)
        await downloader.download([i for i, var in enumerate(self.var_list) if var.get() == 1])
        self.download_button.configure(state="normal")
        self.download_button.configure(text="Download")

    def course_info_callback(self):
        asyncio.run(self.get_course_info())
        self.course_name_label.configure(text="Name: " + self.course_info.course_name)
        self.total_size_label.configure(text="Total Size: " + self.course_info.total_size)
        # TODO: Add number of files (videos, pdfs, etc.)

    async def get_course_info(self):
        if self.link_scraper is None:
            self.link_scraper = LinkScraper(self.course_url_entry.get())
        self.course_info = await CourseInfo.create(self.link_scraper)



ctypes.windll.shcore.SetProcessDpiAwareness(True)
root = tk.Tk()
gui = MainGUI(root)
root.mainloop()
