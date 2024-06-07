import os
import pyaudio
import wave
import threading
from kivymd.utils import asynckivy


class AudioRecorder:

    # Audio class based on pyAudio and Wave
    def __init__(self, filename=None, lien=None):

        self.open = False
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        user_home = os.path.expanduser('~')
        downloads_folder = os.path.join(user_home, 'Downloads')
        self.audio_filename = "CamLive/enregistrement/{}.wav".format(filename)
        self.video_filename = os.path.join(downloads_folder, self.audio_filename)
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
        try:
            if self.open:
                self.open = not self.open
                print("start audio " + str(self.open))
                self.stream.stop_stream()
                self.stream.close()
                self.audio.terminate()

                if self.audio_frames:
                    waveFile = wave.open(self.audio_filename, 'wb')
                    waveFile.setnchannels(self.channels)
                    waveFile.setsampwidth(self.audio.get_sample_size(self.format))
                    waveFile.setframerate(self.rate)
                    waveFile.writeframes(b''.join(self.audio_frames))
                    waveFile.close()
                    self.audio_frames = []
        except Exception as e:
            self.audio = None
            self.stream = None
            self.audio_frames = []
            print(e)

    # Launches the audio recording function using a thread
    async def start_record(self):
        await asynckivy.sleep(0)
        print("start audio")
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

    def start(self):
        # audio_thread.start()
        pass
