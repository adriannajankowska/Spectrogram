from scipy import signal
import numpy as np
import RawDataPlot
import SoundData

class MainWindowPresenter:
    def __init__(self, view):
        self.view = view
        self.rawData = None


    def OpenFile(self, filename):
        sd = SoundData.SoundData()
        sd.Load(filename)
        if len(sd.data.shape) == 2:
            self.rawData = sd.data[:,0]
        else:
            self.rawData = sd.data

        self.view.rawDataPlot.Draw(self.rawData)

        nfft = 2*700
        padded = np.pad(self.rawData, (0, nfft), 'constant', constant_values=(0, 0))

        overlap = int((1600*nfft - len(self.rawData))/(1600))+1

        f, t, Sxx = signal.spectrogram(padded, nfft=nfft, nperseg=nfft, noverlap=overlap, mode='psd', scaling='spectrum')
        self.view.spectrogramPlot.Draw(Sxx)
        fft = self.view.spectrogramPlot.GetFft()
        self.view.fftPlot.Draw(fft)

    
    def SaveFile(self, filename):
        pass
        # data = self.model.GetData()
        