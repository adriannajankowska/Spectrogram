from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
from enum import Enum

class SpectrogramPlotEvent(Enum):
    CURSOR_CHANGE = 1


class SpectrogramPlot:
    def __init__(self, root):
        self.root = root
        self.width = 1600
        self.height = 600

        self.cursor_x = 0
        self.cursor_y = 0

        self.progress_callback = None
        self.event_callback = self.__DoNothing

        self.__last_progress = 0

    def Init(self):
        self.__plot_padding_h=10
        self.__plot_offset_w=50
        self.__height_plot = self.height - 2*self.__plot_padding_h
        self.__width_plot = self.width - self.__plot_offset_w

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.font = ImageFont.truetype('arial.ttf', 15)

        self.backgroundImage = Image.new('RGB', (self.width, self.height), color = 'white')
        self.backgroundImageDrawer = ImageDraw.Draw(self.backgroundImage)

        self.spectrogramImage = Image.new('RGB', (self.__width_plot, self.__height_plot), color = '#7F7F7F')
        self.spectrogramImageDrawer = ImageDraw.Draw(self.spectrogramImage)

        self.plotImage = Image.new('RGB', (self.width, self.height), color = 'white')
        self.plotImageDrawer = ImageDraw.Draw(self.plotImage)

        self.__DrawBackground()
        self.Refresh()

        self.canvas.bind("<Button-1>", self.__MouseClick)

    def __MouseClick(self, event):
        if event.x > 50 and event.y > self.__plot_padding_h and event.y < self.height-self.__plot_padding_h:
            self.cursor_x = event.x
            self.cursor_y = event.y
            self.Refresh()
        
        self.event_callback(SpectrogramPlotEvent.CURSOR_CHANGE)

    def GetObject(self):
        return self.canvas

    def GetFft(self):
        line = []
        for i in range(0, self.__height_plot):
            r,g,b = self.spectrogramImage.getpixel((self.cursor_x-self.__plot_offset_w, i))
            line.append((r,g,b))
        return line

    def Draw(self, data):
        self.__DrawBackground()
        self.__DrawSpectrogram(data)
        self.Refresh()

    def __DrawBackground(self):
        self.backgroundImageDrawer.rectangle((0, 0, self.width, self.height), fill=(255,255,255,0))

        for i in range(0, 20):
            self.backgroundImageDrawer.line((47, self.height-i*30-self.__plot_padding_h-1, 50, self.height-i*30-self.__plot_padding_h-1), fill=(0,0,0,0))
            self.backgroundImageDrawer.text((7, self.height-i*30-self.__plot_padding_h-8), "{:d}".format(i*1000) , fill=(0,0,0,0), font=self.font)

    def __DrawSpectrogram(self, data):
        self.__SetProgress(len(data), 0)
        data = np.log(data)
        data = data/data.max()
        spectrogramImage = Image.new('RGB', (len(data[0]), len(data)), color = '#7F7F7F')
        spectrogramDrawer = ImageDraw.Draw(spectrogramImage)
        for x in range(0, len(data)):
            for y in range(0, len(data[0])):
                spectrogramDrawer.point((y, len(data)-x), fill=self.ValueToColor(data[x,y]))
            self.__SetProgress(len(data), x)

        self.spectrogramImage = spectrogramImage.resize((self.__width_plot, self.__height_plot), Image.ANTIALIAS)
        self.__SetProgress(len(data), len(data))

    def __DrawCursor(self, x, y):
        self.plotImageDrawer.line((50, y, self.width, y), fill=(0,255,0,50))
        self.plotImageDrawer.line((x, self.__plot_padding_h, x, self.height-self.__plot_padding_h), fill=(0,255,0,50))

    def Refresh(self):
        self.plotImage.paste(self.backgroundImage, (0, 0))
        self.plotImage.paste(self.spectrogramImage, (self.__plot_offset_w, self.__plot_padding_h))
        self.__DrawCursor(self.cursor_x, self.cursor_y)
        self.image = ImageTk.PhotoImage(self.plotImage)
        self.canvas.create_image((0,0), image=self.image, anchor="nw")

    def __SetProgress(self, total, progress):
        percentage = int(100.0*progress/total)
        if self.progress_callback is not None and self.__last_progress != percentage:
            self.__last_progress = percentage
            self.progress_callback(percentage)

    def ValueToColor(self, value):
        if value < 0:
            return 0

        val_int = int(value*1280)

        if val_int < 256:
            return (0,
                    0,
                    val_int%256,
                    0) #blue
        elif val_int < 512:
            return (val_int%256,
                    0,
                    255,
                    0) #purple
        elif val_int < 768:
            return (255,
                    0,
                    255-val_int%256,
                    0) #red
        elif val_int < 1024:
            return (255,
                    val_int%256,
                    0,
                    0) #yellow
        elif val_int < 1280:
            return (255,
                    255,
                    val_int%256,
                    0) #white
        else:
            return (255,
                    255,
                    255,
                    0) #white

    def __DoNothing(self, event = None):
        pass

        