import os
from datetime import datetime
import multiprocessing
import cv2
from kivy.clock import Clock
from kivy.core.image import Texture
from kivymd.utils import asynckivy

from studio.view import AudioRecorder, VideoRecorder
from studio.view.CameraFrame import Camera


class CamCapture:
    # Initialiser l'enregistrement à False
    recording = False
    record_demarage = False
    # Liste pour stocker les images à enregistrer
    frames_to_record = []
    
    videoCamera = None
    audioCamera = None

    cameraVideo = Camera()
    
    def __init__(self, lien=None, screen_video=None, tab=None, **kwargs):
        super().__init__(**kwargs)
        self.tab = tab
        self.capture = 0
        self.lien = lien
        self.screen_video = screen_video


    def captureCamera(self):
        self.capture = 1

    def afert(self, delay, func):
        Clock.schedule_once(func, delay)
        # self.window.after(delay, func)

    def stop_record(self):
        self.recording = not self.recording
        self.frames_to_record = asynckivy.start(self.cameraVideo.stop_enregistrer(self.frames_to_record))
        self.frames_to_record = []
        self.record_demarage = False
    
    def stop_video(self, mix=False):
        try:
            self.videoCamera = None
            if mix:
                asynckivy.start(self.cameraVideo.stop(True))
            else:
                asynckivy.start(self.cameraVideo.stop(False))
            if self.recording:
                self.stop_record()
            self.videoCamera = None
        except Exception as e:
            self.videoCamera = None
            print(e)

    def enregistrer(self):
        self.recording = True
        print("Star record: " + str(self.recording))

    async def lancer(self, cam=None):
        await asynckivy.sleep(0.8)
        if not cam:
            if self.videoCamera is None:
                await self.cameraVideo.afficheCamara(self.lien)
                await asynckivy.sleep(1.5)
                self.videoCamera = self.cameraVideo.video_Camera
            print(f"lancer====>>>> {self.videoCamera}")
            self.update()
            return self.videoCamera
        else:
            await self.cameraVideo.afficheCamara(self.lien, cam)
            await asynckivy.sleep(0.6)
            self.videoCamera = self.cameraVideo.video_Camera
            print(f"lancer====>>>> {cam}")
            self.update()
            return cam

    def update(self, dt=None):

        if self.videoCamera:
            # Lire une image depuis le flux vidéo
            ret, frame = self.videoCamera.read()
            # Appeler récursivement la fonction update après un certain délai
            if ret:
                buf1 = cv2.flip(frame, 0)
                buf = buf1.tostring()
                image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.screen_video.ids.cardImage.image.texture = image_texture
                if self.capture == 1 or self.capture == 2:
                    name = str(self.capture) + "_" + datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S")
                    self.save_frame_camera_key("enregistrement/capture", 'capture', name, frame)
                    self.capture += 1
                    print(self.capture)
                if self.capture == 2:
                    self.capture = 0

                # Enregistrer la frame si l'enregistrement est activé
                if self.recording:
                    # print(self.frames_to_record)
                    self.frames_to_record.append(frame)
                    if not self.record_demarage:
                        self.record_demarage = not self.record_demarage
                        asynckivy.start(self.cameraVideo.record_demarage(self.frames_to_record))
                        # self.record_update()
                        self.frames_to_record = []
                    if self.frames_to_record:
                        asynckivy.start(self.cameraVideo.update_enregistrer(self.frames_to_record))                

            time = 1 / 30
            self.afert(time, self.update)

    def record_update(self, dt=None):
        async def record():
            if self.recording and self.frames_to_record:
                await self.cameraVideo.update_enregistrer(self.frames_to_record)
                self.frames_to_record = []
                # processus = multiprocessing.Process(target=self.afert, args=(10, self.record_update))
                # processus.start()
                # processus.join()
                # self.afert(20, self.record_update)
        asynckivy.start(record())

        # self.record_update()
    def stopCamera(self):
        self.recording = not self.recording
        self.frames_to_record = asynckivy.start(self.cameraVideo.enregistrer(self.frames_to_record))
        self.frames_to_record = []
        self.record_demarage = False

    def save_frame_camera_key(self, dir_path, basename, n, frame, ext='jpg'):
        base_path = os.path.join(dir_path, basename)

        cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)

        