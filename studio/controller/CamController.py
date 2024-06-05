from studio.view.CamCapture import CamCapture
from kivymd.toast import toast
import time
from kivy.clock import Clock


class CamController(CamCapture):
    format = None
    timer = False
    seconds = 0
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def add_start_video(self, text, screen, cam):
        self.lien = text
        self.screen_video = screen
        return await self.on_play(cam)
    
    def on_break(self):
        if not self.videoCamera:
            return toast('entrer url de la source')
        self.screen_video.ids.cardImage.ids.play.icon = 'play'
        self.screen_video.ids.cardImage.ids.bage_image.md_bg_color = '#fff000'
        self.videoCamera.on_break()
        self.timer = False

    async def on_play(self, cam=None):
        if not self.screen_video:
            return toast('entrer url de la source')
        lancer = await self.lancer(cam)
        self.screen_video.ids.cardImage.ids.play.icon = 'pause'
        self.screen_video.ids.cardImage.ids.bage_image.md_bg_color = '#00FF40'
        self.timer = True
        self.countdown()
        return lancer

    def on_stop(self, mix=False):
        if not self.videoCamera:
            return toast('aucun camera en cours de lecture')
        self.screen_video.ids.cardImage.ids.bage_image.md_bg_color = '#FF0000'
        if mix:
            self.stop_video(True)
        else:
            self.stop_video(False)
        self.timer = False
        self.seconds = 0

    def on_record(self):
        if not self.videoCamera:
            return toast('aucun camera en cours de lecture')
        self.enregistrer()

    def select_format(self, format):
        if not self.videoCamera:
            return toast('aucun camera en cours de lecture')
        self.format = format

    def on_switch(self):
        if not self.videoCamera:
            return toast('La cam principe ne peux pas basculer sur ce camera')
        self.screen_video.app.camController.videoCamera = self.videoCamera


    def countdown(self, dt=None):
        if self.timer:
            mins, secs = divmod(self.seconds, 60)
            timer = '{:02d}:{:02d}:{:02d}'.format(0, mins, secs)
            self.screen_video.ids.cardImage.lecture.text = "[color=#ffffff]" + str(timer) + "[/color]" 
            self.seconds += 1
            Clock.schedule_once(self.countdown, 1)