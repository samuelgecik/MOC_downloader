import tkinter as tk
from tkinter import ttk, filedialog
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkCheckBox
from scraping import LinkScraper

class MainGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Course Downloader")
        self.master.geometry("500x200")

        self.tab_control = ttk.Notebook(self.master)

        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Tab 1')

        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Tab 2')

        self.create_widgets()

        self.tab_control.pack(expand=1, fill='both')

        self.output_path = None
        self.scraper = None

    def create_widgets(self):
        self.course_url_entry = CTkEntry(self.tab1, placeholder_text="Enter course URL here")
        self.course_url_entry.pack(pady=10)

        self.output_button = CTkButton(self.tab1, text="Choose Output Folder", command=self.select_output)
        self.output_button.pack(pady=10)

        self.download_button = CTkButton(self.tab1, text="Download", command=self.download)
        self.download_button.pack(pady=10)

        self.course_name_label = CTkLabel(self.tab1, text="")
        self.course_name_label.pack(pady=10)

        self.file_size_label = CTkLabel(self.tab1, text="")
        self.file_size_label.pack(pady=10)

        self.total_size_label_tab2 = CTkLabel(self.tab2, text="")
        self.total_size_label_tab2.pack(pady=10)

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
        pass
 
    def update_total_size(self):
        pass

root = tk.Tk()
gui = MainGUI(root)
root.mainloop()