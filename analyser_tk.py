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

#Initial page user will interact with
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="It Works!").pack()

        button = tk.Button(self, text="Dummy Page", command=lambda: controller.resolve(DummyPage)).pack()

#Just a demo page
class DummyPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

#Calls app
mainrun = AnalysisApp()
mainrun.mainloop()