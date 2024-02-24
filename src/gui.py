import ctypes
import asyncio
import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkCheckBox, CTkImage, ThemeManager
from course_info import CourseInfo
from scraping import LinkScraper
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

        self.tab_control = ttk.Notebook(self.master)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Download Course")

        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text="Content Selection")

        self.create_widgets()

        self.tab_control.pack(expand=1, fill="both")

        self.output_path = None
        self.scraper = None

    def create_widgets(self):
        self.canvas = tk.Canvas(self.tab1)
        self.canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.course_url_entry = CTkEntry(
            self.canvas,
            corner_radius=0,
            border_width=0,
            placeholder_text="Enter course URL here",
        )
        self.course_url_entry.pack(fill="both", expand=True)

        self.paste_button = CTkButton(
            self.canvas,
            text="Paste",
            # TODO: PIL image support
            # image=CTkImage(r"C:\Users\samo\dev\MOC_downloader\src\paste.png", size=(40, 40)),
            fg_color=ThemeManager.theme["CTkEntry"]["fg_color"],
            # bg_color="transparent",
            corner_radius=0,
            hover=False,
            width=30,
            command=self.paste_clipboard,
        )
        self.paste_button.place(relx=1.0, rely=0.0, anchor="ne")

        self.get_info_button = CTkButton(
            self.tab1, text="Get Course Info", command=self.course_info_callback
        )
        self.get_info_button.grid(row=1, column=0, padx=10, pady=10)

        self.output_button = CTkButton(
            self.tab1, text="Choose Output Folder", command=self.select_output
        )
        self.output_button.grid(row=2, column=0, padx=10, pady=10)

        self.download_button = CTkButton(
            self.tab1, text="Download", state="normal", command=self.download
        )
        self.download_button.grid(row=3, column=0, padx=10, pady=10)

        self.course_name_label = CTkLabel(self.tab1, text="",anchor="w", text_color="gray")
        self.course_name_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.total_size_label = CTkLabel(self.tab1, text="", anchor="w", text_color="gray")
        self.total_size_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.tab1.grid_columnconfigure(0, weight=1)

        self.checkbuttons = []
        self.var_list = []

        # for i, file_name in enumerate(self.scraper.get_file_names()):
        #     var = tk.IntVar()
        #     self.var_list.append(var)
        #     checkbutton = CTkCheckBox(self.tab2, text=file_name, variable=var, command=self.update_total_size)
        #     checkbutton.pack(anchor='w')
        #     self.checkbuttons.append(checkbutton)`

    def select_output(self):
        self.output_path = filedialog.askdirectory()

    def download(self):
        if self.download_button.cget("state") == "normal":
            self.download_button.configure(state="disabled")
            self.download_button.configure(text="Downloading...")
        downloader = Downloader(self.output_path, self.scraper, self.var_list)

    def update_total_size(self):
        pass
    
    def course_info_callback(self):
        asyncio.run(self.get_course_info())
        self.course_name_label.configure(text="Name: " + self.course_info.course_name)
        self.total_size_label.configure(text="Total Size: " + self.course_info.total_size)

    async def get_course_info(self):
        if self.link_scraper is None:
            self.link_scraper = LinkScraper(self.course_url_entry.get())
        self.course_info = await CourseInfo.create(self.link_scraper)


    def paste_clipboard(self): 
        clipboard_content = self.master.clipboard_get()
        self.course_url_entry.delete(0, "end")
        self.course_url_entry.insert(0, clipboard_content)


ctypes.windll.shcore.SetProcessDpiAwareness(True)
root = tk.Tk()
gui = MainGUI(root)
root.mainloop()
