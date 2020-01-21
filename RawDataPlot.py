from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
from enum import Enum

class RawDataPlotEvent(Enum):
    CURSOR_CHANGE = 1

class RawDataPlot:
    def __init__(self, root):
        self.root = root
        self.width = 1600
        self.height = 300

        self.cursor_x = 0
        self.cursor_y = 0

        self.event_callback = self.__DoNothing

    def Init(self):
        self.__plot_offset_h=25
        self.__plot_offset_w=50
        self.__height_plot = self.height - self.__plot_offset_h
        self.__width_plot = self.width - self.__plot_offset_w

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.font = ImageFont.truetype('arial.ttf', 15)

        self.plotImage = Image.new('RGB', (self.width, self.height))
        self.plotImageDrawer = ImageDraw.Draw(self.plotImage)

        self.displayedImage = Image.new('RGB', (self.width, self.height))
        self.displayedImageDrawer = ImageDraw.Draw(self.displayedImage)
        
        self.canvas.bind("<Button-1>", self.__MouseClick)

        self.__DrawBackground()

        self.Refresh()

    def GetObject(self):
        return self.canvas

    def __MouseClick(self, event):
        if event.x > 50 and event.y > self.__plot_offset_h and event.y < self.height-self.__plot_offset_h:
            self.cursor_x = event.x
            self.cursor_y = event.y
            self.__DrawCursor()

            self.Refresh()
        
        self.event_callback(RawDataPlotEvent.CURSOR_CHANGE)

    def Draw(self, data, sampleRate=44100):
        self.__DrawBackground(sampleRate, len(data))
        self.__DrawData(data)
        self.__DrawCursor()
        self.Refresh()

    def __DrawData(self, data):
        length = len(data)
        span = length/self.__width_plot
        max_val = 65535

        last = (self.__plot_offset_w, data[0]*(self.__height_plot) / max_val + (self.__height_plot)/2)
        for x in range(1, self.__width_plot):
            if(span*x >length ):
                break
            amp = data[int(span*x)]*(self.__height_plot) / max_val + (self.__height_plot)/2 + self.__plot_offset_h
            self.plotImageDrawer.line((last[0], last[1], x+self.__plot_offset_w, amp), fill=(0,0,0,0))
            last = (x+self.__plot_offset_w, amp)

    def __DrawCursor(self):
        self.displayedImage.paste(self.plotImage, (0, 0))
        self.displayedImageDrawer.line((self.cursor_x, self.__plot_offset_h, self.cursor_x, self.height), fill=(55,70,50,50))

    def Refresh(self):
        self.__DrawCursor()
        self.image = ImageTk.PhotoImage(self.displayedImage)
        self.canvas.create_image((0,0), image=self.image, anchor="nw")

    def __DrawBackground(self, sampleRate = None, data_len = None):
        self.plotImageDrawer.rectangle((0, 0, self.width, self.height), fill=(255,255,255,0))
        self.plotImageDrawer.rectangle((self.__plot_offset_w, self.__plot_offset_h-1, self.width-1, self.height-1), fill =(198,234,190,0),  outline=(115,142,109,0))
        # zero line
        self.plotImageDrawer.line((self.__plot_offset_w, self.__height_plot/2+self.__plot_offset_h, self.width, self.__height_plot/2+self.__plot_offset_h), fill=(115,142,109,0))
        self.plotImageDrawer.text((self.__plot_offset_w-15,self.__height_plot/2+self.__plot_offset_h-4) , "0" , fill=(0,0,0,0), font=self.font)

        if sampleRate is None:
             return

        seconds_total = data_len/sampleRate

        #draw time
        for i in range(0, 20):
            self.plotImageDrawer.line((i*self.__width_plot/20 + self.__plot_offset_w, self.__plot_offset_h, i*self.__width_plot/20 + self.__plot_offset_w, self.height), fill=(115,142,109,0))
            self.plotImageDrawer.text((i*self.__width_plot/20-18 + self.__plot_offset_w, 4), "{:.2f}s".format(i*seconds_total/20) , fill=(0,0,0,0), font=self.font)

        self.plotImageDrawer.text((self.width-37, 4), "{:.2f}s".format(seconds_total) , fill=(0,0,0,0), font=self.font)

    def __DoNothing(self, event = None):
        pass

        




        