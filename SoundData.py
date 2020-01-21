from scipy.io import wavfile

class SoundData:
    def __init__(self):
        pass

    def Load(self, filename):
        self.fs, self.data = wavfile.read(filename)