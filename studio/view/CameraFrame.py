import os
import threading
import time
import subprocess
import shutil
from datetime import datetime
from studio.view.AudioRecorder import AudioRecorder
from studio.view.MyProcess import MyProcess
from studio.view.VideoRecorder import VideoRecorder
from kivymd.utils import asynckivy


class Camera():
    listProces = []
    video_Camera = None
    video_thread = None
    audio_thread = None

    def __int__(self, lien=None):
        self.lien = lien
        self.filename = None
        self.filename_video = None
        self.filename_audio = None
        self.filename_video_2 = None
        self.filename_video_final = None
        self.audioCamera = None

    async def afficheCamara(self, lien=None, cam=None):
        print(lien)
        if len(lien) == 1 and lien == "0":
            self.lien = int(lien)
            lien = int(lien)
        else:
            self.lien = lien
            lien = lien + "/video"
        print(lien)
        self.filename = datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S")
        self.filename_video = "{}/video.mp4".format(self.filename)
        self.filename_audio = "{}/audio".format(self.filename)
        if not cam:
            await self.start_AVrecording(lien, self.filename_video)
        else:
            await self.start_AVrecording(lien, self.filename_video, cam)

    async def start_AVrecording(self, lien=None, filename=None, cam=None):
        self.filename = filename
        self.video_thread =  VideoRecorder(lien, filename)
        await asynckivy.sleep(0)
        try:
            # int(self.lien)
            self.audio_thread = AudioRecorder(self.filename_audio, self.lien)
        except Exception as e:  # noqa: E722
            print(e)
            self.audio_thread = AudioRecorder(self.filename_audio)
        self.audioCamera = self.audio_thread
        try:
            if not cam:
                await self.video_thread.demarage(lien, filename)
            else:
                await self.video_thread.demarage(lien, filename, cam)
            self.video_Camera = self.video_thread.video_cap
            print(f"start_Av=======>  {self.video_Camera}")
        except Exception as e:
            print(f"start_Av=======>  {e}")
            self.video_Camera = None
            

    async def record_demarage(self, frames_to_record):
        if self.video_thread is not None:
            print("record_demarage True")
            await self.video_thread.record_demarage(frames_to_record)
            asynckivy.start(self.audio_thread.start_record())

    async def stop_enregistrer(self, frames_to_record):
        await asynckivy.sleep(0.2)
        if self.video_thread is not None:
            print("self.video_thread stop")
            video_frame = asynckivy.start(self.video_thread.stop_record(frames_to_record))
            # await self.stop()
            return video_frame

    async def update_enregistrer(self, frames_to_record):
        await asynckivy.sleep(0.2)
        if self.video_thread is not None:
            print("self.video_thread update")
            return self.video_thread.update_record(frames_to_record)

    async def stop(self, mix=False):
        try:
            await asynckivy.sleep(0)
            if mix:
                asynckivy.start(self.stop_enregistrement())
            else:
                self.video_thread.stop()
                self.audio_thread.stop()
            self.video_thread = None
            self.audio_thread = None
        except Exception as e:
            self.video_thread = None
            self.audio_thread = None
            print(e)

    async def stop_enregistrement(self):
        await asynckivy.sleep(0)
        local_path = os.getcwd()
        self.audio_thread.stop()
        frame_counts = self.video_thread.frame_counts
        elapsed_time = time.time() - self.video_thread.start_time
        recorded_fps = frame_counts / elapsed_time
        print("total frames " + str(frame_counts))
        print("elapsed time " + str(elapsed_time))
        print("recorded fps " + str(recorded_fps))
        self.video_thread.stop()
        try:
            self.filename_video_final = str(local_path) + "/enregistrement/final_" + self.filename_video
            self.filename_audio = str(local_path) + "/enregistrement/output_{}.wav".format(self.filename_audio)
            out_audio = shutil.copy(self.filename_audio, str(os.getcwd()) + "/temp_audio.wav")
            print(out_audio)
            out_video = shutil.copy(str(local_path) + "/enregistrement/" + self.filename_video, str(os.getcwd()) + "/temp_video.mp4")
            print(out_video)

            # Makes sure the threads have finished
            while threading.active_count() > 1:
                await asynckivy.sleep(0)
                time.sleep(1)

            #    Merging audio and video signal
            print(str(abs(recorded_fps - 6)))
            if abs(recorded_fps - 6) >= 0.01:  # If the fps rate was higher/lower than expected, re-encode it to the expected

                print("Re-encoding")
                cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.mp4 -pix_fmt yuv420p -r 6 temp_video2.mp4"
                subprocess.call(cmd, shell=True)

                print("Muxing")
                cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.mp4 -pix_fmt yuv420p filename.mp4"
                subprocess.call(cmd, shell=True)

            else:

                print("Normal recording\nMuxing")
                cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.mp4 -pix_fmt yuv420p filename.mp4"
                subprocess.call(cmd, shell=True)

                print("..")

            asynckivy.start(self.file_manager(self.filename))

        except Exception as e:
            print(str(e))

    # Required and wanted processing of final files
    async def file_manager(self, filename):
        await asynckivy.sleep(0)

        local_path = os.getcwd()

        if os.path.exists(str(local_path) + "/temp_audio.wav"):
            os.remove(str(local_path) + "/temp_audio.wav")

        if os.path.exists(str(local_path) + "/temp_video.mp4"):
            os.remove(str(local_path) + "/temp_video.mp4")

        if os.path.exists(str(local_path) + "/temp_video2.mp4"):
            os.remove(str(local_path) + "/temp_video2.mp4")

        if os.path.exists(str(local_path) + "/filename.mp4"):
            out_video = shutil.copy(str(os.getcwd()) + "/filename.mp4", self.filename_video_final)
            print(out_video)
            os.remove(str(local_path) + "/filename.mp4")
