#!/usr/bin/python

'''
This project is licensed under the GPL V2.0

This app is intended to be a GUI-driven, user-friendly, scientific analysis
application, with a machine learning backend driving intelligent data cleaning,
analysis and results presentation.
'''

import numpy as np
import pandas as pd

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

#Parent class for the GUI
class AnalysisApp(tk.Tk):

    #Initialising the frontend
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        #Any pages added need to be added into the tuple in the for loop
        for page in (HomePage, DummyPage):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Calls the HomePage to be displayed
        self.resolve(HomePage)

    #Takes a page as an argument and displays it
    def resolve(self, page_container):
        frame = self.frames[page_container]
        frame.tkraise()

    #Displays a popup message to notify user of an error
    def warning_popup(self, text):
        popup = tk.Toplevel(self)

        popup.geometry("200x100")

        label = tk.Label(popup, text=text).pack(pady=10)
        dismiss_button = tk.Button(popup, text="Dismiss", command=lambda: popup.destroy()).pack()

#Initial page user will interact with
class HomePage(tk.Frame):

    def __init__(self, parent, controller):

        self.controller = controller

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Enter the filename (and path) in the textbox below").pack()

        #Initialising entry box and associated dependencies
        self.filename = tk.StringVar()
        filename_entry = tk.Entry(self, textvariable=self.filename).pack()

        submit_button = tk.Button(self, text="Submit data for Viewing", command=self.submit_button_command).pack()

        or_label = tk.Label(self, text="OR").pack(pady=10)

        browse_button = tk.Button(self, text="Browse", command=lambda: self.file_browser()).pack()

    #Currently primitive function that will expand as app becomes more complex
    #Will decide which analysis function to use etc, will become far more relevant
    #with inclusion of .FITS files
    def submit_button_command(self):
        self.filehandler()

    #Graphical filesystem browser that allows the user to choose a file using a GUI
    def file_browser(self):
        self.filename = askopenfilename(initialdir="mikie/home/Programming",
                                filetypes =(("All Files","*.*"),("Text File", "*.txt"),("CSV File", "*.csv"),("Excel File", "*.xlsx")),
                                title = "Choose a file."
                            )
        #Allowing for mistakes in file specification
        try:
            self.submit_button_command()
        except:
            self.controller.warning_popup("No file exists")

    #Branching function that allows relevant analysis functions to be called
    def filehandler(self):

        #Allowing for user-input text from textbox
        if type(self.filename) == tk.StringVar:
            self.filename_str = self.filename.get()

        #Handling File Browser input
        else:
            self.filename_str = self.filename

        #Identifying file extension
        try:
            self.file_ext = self.filename_str[self.filename_str.index("."):]

            #List of currently supported file types
            self.supported_types = [".csv", ".txt", ".xlsx"]

            if self.file_ext not in self.supported_types:
                self.controller.warning_popup("Unsupported File Type")

            #If file type is supported, will call relevant analysis function
            else:
                if self.file_ext == ".csv":
                    self.csv_handler()

                elif self.file_ext == ".txt":
                    self.txt_handler()

                elif self.file_ext == ".xlsx":
                    self.xlsx_handler()

        except ValueError:
            self.controller.warning_popup("Not a file")

    def csv_handler(self):
        data = pd.read_csv(self.filename_str)
        print(data)

    def txt_handler(self):
        data = pd.read_csv(self.filename_str, sep="\t")
        print(data)

    def xlsx_handler(self):
        data = pd.read_excel(self.filename_str)

#Just a demo page
class DummyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Dummy").pack()

        button = tk.Button(self, text="Go Home", command=lambda: controller.resolve(HomePage)).pack()

#Calls app
mainrun = AnalysisApp()
mainrun.geometry("400x300")
mainrun.mainloop()
