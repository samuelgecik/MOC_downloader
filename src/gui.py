import ctypes
import tkinter as tk
from tkinter import ttk, filedialog
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkCheckBox, ThemeManager
from scraping import LinkScraper


class MainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Course Downloader")
        self.master.geometry("800x800")
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
            fg_color=ThemeManager.theme["CTkEntry"]["fg_color"],
            # bg_color="transparent",
            corner_radius=0,
            hover=False,
            width=30,
            command=self.paste_clipboard,
        )
        self.paste_button.place(relx=1.0, rely=0.0, anchor="ne")

        self.output_button = CTkButton(
            self.tab1, text="Choose Output Folder", command=self.select_output
        )
        self.output_button.grid(row=1, column=0, padx=10, pady=10)

        self.download_button = CTkButton(
            self.tab1, text="Check Course Info", state="normal", command=self.download
        )
        self.download_button.grid(row=2, column=0, padx=10, pady=10)

        self.course_name_label = CTkLabel(self.tab1, text="")
        self.course_name_label.grid(row=3, column=0, padx=10, pady=10)

        self.file_size_label = CTkLabel(self.tab1, text="")
        self.file_size_label.grid(row=4, column=0, padx=10, pady=10)

        self.total_size_label_tab2 = CTkLabel(self.tab2, text="")
        self.total_size_label_tab2.pack(pady=10)

        self.tab1.grid_columnconfigure(0, weight=1)

        self.checkbuttons = []
        self.var_list = []

        # for i, file_name in enumerate(self.scraper.get_file_names()):
        #     var = tk.IntVar()
        #     self.var_list.append(var)
        #     checkbutton = CTkCheckBox(self.tab2, text=file_name, variable=var, command=self.update_total_size)
        #     checkbutton.pack(anchor='w')
        #     self.checkbuttons.append(checkbutton)

    def select_output(self):
        self.output_path = filedialog.askdirectory()

    def download(self):
        if self.download_button.cget("state") == "normal":
            self.download_button.configure(state="active"),
            self.download_button.configure(text="Download")
            return
        if self.download_button.cget("state") == "active":
            self.download_button.configure(state="disabled")
            self.download_button.configure(text="Downloading...")
            return

    def update_total_size(self):
        pass

    def get_course_info(self):
        pass

    def paste_clipboard(self):
        clipboard_content = self.master.clipboard_get()
        self.course_url_entry.delete(0, "end")
        self.course_url_entry.insert(0, clipboard_content)


ctypes.windll.shcore.SetProcessDpiAwareness(True)
root = tk.Tk()
gui = MainGUI(root)
root.mainloop()
