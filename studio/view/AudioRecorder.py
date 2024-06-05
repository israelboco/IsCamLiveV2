import pyaudio
import wave
import threading


class AudioRecorder:

    # Audio class based on pyAudio and Wave
    def __init__(self, filename=None, lien=None):

        self.open = False
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "enregistrement/output_{}.wav".format(filename)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        if lien:
            device_index = lien + "/audio"
            self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer,
                                      input_device_index = device_index)
        if self.stream:
            self.open = True

        self.audio_frames = []

    # Audio starts being recorded
    def record(self):

        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break

    # Finishes the audio recording therefore the thread too
    def stop(self):

        if self.open:
            self.open = not self.open
            print("start audio " + str(self.open))
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()
            self.audio_frames = []

    # Launches the audio recording function using a thread
    def start(self):
        print("start audio")
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
