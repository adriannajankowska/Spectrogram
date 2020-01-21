import MainWindow

import Interactor
# import SoundData
# import matplotlib.pyplot as plot


# sd = SoundData.SoundData()

# sd.Load("chirp.wav")
mainwindow = MainWindow.MainWindow()

# mainwindow.rawData = sd.data[:]


# Plot the signal read from wav file
# plot.subplot(211)
# plot.title('Spectrogram of a wav file with piano music')
# plot.plot(mainwindow.rawData)
# plot.xlabel('Sample')
# plot.ylabel('Amplitude')


# plot.subplot(212)
# plot.specgram(mainwindow.rawData, Fs=1, NFFT=1600, noverlap=1500)
# plot.xlabel('Time')
# plot.ylabel('Frequency')

 

# plot.show()
mainwindow.MainLoop()

