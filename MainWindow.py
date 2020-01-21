from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

import MenuBar
import RawDataPlot
import SpectrogramPlot
import FftPlot


from scipy import signal
import numpy as np
import os

import MainWindowPresenter

class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.presenter = MainWindowPresenter.MainWindowPresenter(self)

        self.root.title("SpectroAdele xD") 
        self.width = 1620
        self.height = 960
        self.root.geometry("{:d}x{:d}".format(self.width, self.height))

        # MenuBar config
        self.menuBar = MenuBar.MenuBar(self.root)
        self.menuBar.FileNew_Callback = self.MenuBarFileNew_Callback
        self.menuBar.FileOpen_Callback = self.MenuBarFileOpen_Callback
        self.menuBar.FileSave_Callback = self.MenuBarFileSave_Callback
        self.menuBar.Init()
        
        # RawDataPlot config
        self.rawDataPlot = RawDataPlot.RawDataPlot(self.root)
        self.rawDataPlot.width = self.width-310
        self.rawDataPlot.height = 300
        self.rawDataPlot.event_callback = self.RawDataPlotEventDispatch
        self.rawDataPlot.Init()

        # SpectrogramPlot config
        self.spectrogramPlot = SpectrogramPlot.SpectrogramPlot(self.root)
        self.spectrogramPlot.width = self.width-310
        self.spectrogramPlot.height = 600
        self.spectrogramPlot.progress_callback = self.SetProgress
        self.spectrogramPlot.event_callback = self.SpectrogramPlotEventDispatch
        self.spectrogramPlot.Init()

        self.fftPlot = FftPlot.FftPlot(self.root)
        self.fftPlot.width = 300
        self.fftPlot.height = 600
        self.fftPlot.progress_callback = self.SetProgress
        self.fftPlot.event_callback = self.FftPlotEventDispatch
        self.fftPlot.Init()

        #Progress config
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")

        # layout
        self.root.config(menu=self.menuBar.GetObject())
        self.rawDataPlot.GetObject().grid(row = 1, column = 0, sticky = W+E, padx = 5, pady = 5)
        self.spectrogramPlot.GetObject().grid(row = 0, column = 0, sticky = W+E, padx = 5, pady = 5)
        self.fftPlot.GetObject().grid(row = 0, column = 1, sticky = W, padx = 5, pady = 5)

        self.progress.grid(row = 2, column = 0, sticky = W+E, padx = 5, pady = 5)

    # MenuBar callbacks
    def MenuBarFileNew_Callback(self):
        pass

    def MenuBarFileOpen_Callback(self):
        filename = askopenfilename(initialdir = os.getcwd(), filetypes = [("WAV files","*.wav")] )
        self.presenter.OpenFile(filename)

    def MenuBarFileSave_Callback(self):
        filename = asksaveasfilename(defaultextension='.wav', filetypes=[('Wave files', '.wav')], initialdir = os.getcwd())
        if filename is not None:
            self.presenter.SaveFile(filename)

    def SetProgress(self, progress):
        self.progress['length'] = 100
        self.progress['value'] = progress
        self.root.update_idletasks()

    def SpectrogramPlotEventDispatch(self, event):
        if event == SpectrogramPlot.SpectrogramPlotEvent.CURSOR_CHANGE:
            self.rawDataPlot.cursor_x = self.spectrogramPlot.cursor_x
            self.rawDataPlot.Refresh()

            self.fftPlot.cursor_y = self.spectrogramPlot.cursor_y
            fft = self.spectrogramPlot.GetFft()
            self.fftPlot.Draw(fft)
            self.fftPlot.Refresh()

    def RawDataPlotEventDispatch(self, event):
        if event == RawDataPlot.RawDataPlotEvent.CURSOR_CHANGE:
            self.spectrogramPlot.cursor_x = self.rawDataPlot.cursor_x
            self.spectrogramPlot.Refresh()

            fft = self.spectrogramPlot.GetFft()
            self.fftPlot.Draw(fft)
            self.fftPlot.Refresh()

    def FftPlotEventDispatch(self, event):
        if event == FftPlot.FftPlotEvent.CURSOR_CHANGE:
            self.spectrogramPlot.cursor_y = self.fftPlot.cursor_y
            self.spectrogramPlot.Refresh()

            fft = self.spectrogramPlot.GetFft()
            self.fftPlot.Draw(fft)
            self.fftPlot.Refresh()
    
    def MainLoop(self):
        self.root.mainloop()