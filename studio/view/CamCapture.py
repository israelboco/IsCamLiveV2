import os
from datetime import datetime
import multiprocessing   
import time
import cv2
from kivy.clock import Clock
from kivy.core.image import Texture
from kivymd.utils import asynckivy
from threading import Thread
from studio.view import AudioRecorder, VideoRecorder
from studio.view.CameraFrame import Camera


class CamCapture:

    def __init__(self, lien=None, screen_video=None, tab=None, **kwargs):
        super().__init__(**kwargs)
        self.tab = tab
        self.capture = 0
        self.lien = lien
        self.screen_video = screen_video
        # Initialiser l'enregistrement à False
        self.recording = False
        self.record_demarage = False
        # Liste pour stocker les images à enregistrer
        self.frames_to_record = []
        
        self.videoCamera = None
        self.audioCamera = None
        self.app = None

        self.cameraVideo = Camera()


    def captureCamera(self):
        self.capture = 1

    def afert(self, delay, func):
        Clock.schedule_once(func, delay)

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

    async def lancer(self, cam=None, app=None):
        self.app = app
        await asynckivy.sleep(0.8)
        if not cam:
            if self.videoCamera is None:
                print(self.lien)
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
    
    def recordUpdate(self):
        if self.videoCamera:
            # Lire une image depuis le flux vidéo
            self.resource_record_cam_thread = self.app.data.manager.start_thread(self.record_cam_thread)
            # self.resource_record_cam_thread = Thread(target=self.record_cam_thread)
            # self.resource_record_cam_thread.start()

    def record_cam_thread(self):
        # Enregistrer la frame si l'enregistrement est activé
        while self.recording:
            ret, frame = self.videoCamera.read()
            if ret:
                self.frames_to_record.append(frame)
                if not self.record_demarage:
                    self.record_demarage = not self.record_demarage
                    asynckivy.start(self.cameraVideo.record_demarage(self.frames_to_record))
                    self.frames_to_record = []
                if self.frames_to_record:
                    asynckivy.start(self.cameraVideo.update_enregistrer(self.frames_to_record))  
            time.sleep(1 / 5)            

    def traitement_update(self):
        if self.videoCamera:
            # Lire une image depuis le flux vidéo
            self.resource_traitement_cam_thread = self.app.data.manager.start_thread(self.traitement_cam_thread)
            # self.resource_traitement_cam_thread.start()
    
    def traitement_cam_thread(self):
        pass

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
                try:
                    self.screen_video.ids.cardImage.image.texture = image_texture
                except Exception as e:
                    self.screen_video.ids.image.texture = image_texture
                    #print(e)
                if self.capture == 1 or self.capture == 2:
                    name = str(self.capture) + "_" + datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S")
                    self.save_frame_camera_key("enregistrement/capture", 'capture', name, frame)
                    self.capture += 1
                if self.capture == 2:
                    self.capture = 0

            time = 1 / 30
            self.afert(time, self.update)

    def record_update(self, dt=None):
        async def record():
            if self.recording and self.frames_to_record:
                await self.cameraVideo.update_enregistrer(self.frames_to_record)
                self.frames_to_record = []
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

        