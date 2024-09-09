from studio.view.CamCapture import CamCapture
from kivymd.toast import toast
import time
from kivy.clock import Clock


class CamController(CamCapture):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.format = None
        self.timer = False
        self.seconds = 0
        self.hour = 0
        self.app = None

    async def add_start_video(self, text, screen, cam, app):
        self.app = app
        try:
            self.lien = text
            self.screen_video = screen
            print(self.lien)
            return await self.on_play(cam)
        except Exception as e:
            print(e)
    
    def on_break(self):
        try:
            if not self.videoCamera:
                return toast('entrer url de la source')
            self.screen_video.ids.play.icon = 'play'
            self.screen_video.ids.bage_image.md_bg_color = '#fff000'
            # self.videoCamera.on_break()
            self.timer = False
        except Exception as e:
            print(e)

    async def on_play(self, cam=None):
        try:
            if not self.screen_video:
                return toast('entrer url de la source')
            print(self.lien)
            lancer = await self.lancer(cam, self.app)
            ret, frame = self.videoCamera.read()
            if not ret:
                self.videoCamera = None
                return toast('Lien source invalide, verifier et rééssayer')
            self.screen_video.ids.play.icon = 'pause'
            self.screen_video.ids.bage_image.md_bg_color = '#00FF40'
            self.timer = True
            self.countdown()
            return lancer
        except Exception as e:
            print(e)

    def on_stop(self, mix=False):
        try:
            if not self.videoCamera:
                return toast('aucun camera en cours de lecture')
            try:
                self.app.data.listCam.remove((self.lien, self.videoCamera))
            except Exception as e:
                print(e)
            self.screen_video.ids.bage_image.md_bg_color = '#FF0000'
            if mix:
                self.stop_video(True)
            else:
                self.stop_video(False)
            self.timer = False
            self.seconds = 0
            self.hour = 0
        except Exception as e:
            print(e)

    def on_record(self):
        try:
            if not self.videoCamera:
                return toast('aucun camera en cours de lecture')
            if not self.recording:
                self.enregistrer()
                self.screen_video.ids.save.unfocus_color = '#00FF40'
            else:
                self.on_stop_record()
        except Exception as e:
            print(e)
    
    def on_stop_record(self):
        try:
            if not self.videoCamera:
                return toast('aucun camera en cours de lecture')
            if self.recording:
                self.stop_record()
            self.screen_video.ids.save.unfocus_color = '#676767'
        except Exception as e:
            print(e)

    def select_format(self, format):
        try:
            if not self.videoCamera:
                return toast('aucun camera en cours de lecture')
            self.format = format
        except Exception as e:
            print(e)

    def on_switch(self):
        try:
            if not self.videoCamera:
                return toast('La cam principe ne peux pas basculer sur ce camera')
            cam = self.app.data.camController.init_on_switch(self.videoCamera)
            print(cam)
        except Exception as e:
            print(e)

    def countdown(self, dt=None):
        if self.timer:
            mins, secs = divmod(self.seconds, 60)
            timer = '{:02d}:{:02d}:{:02d}'.format(self.hour, mins, secs)
            self.screen_video.lecture.text = "[color=#ffffff]" + str(timer) + "[/color]" 
            self.seconds += 1
            if self.seconds == 3600:
                self.seconds = 0
                self.hour += 1
            Clock.schedule_once(self.countdown, 1)
    
    def init_on_switch(self, cam):
        self.videoCamera = cam
        return self.videoCamera