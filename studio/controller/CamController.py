from studio.view.CamCapture import CamCapture
from kivymd.toast import toast


class CamController(CamCapture):
    camView = None
    # pass
    
    def __init__(self, camView=None, **kwargs):
        super().__init__(**kwargs)
        self.camView = camView

    def add_start_video(self, camView):
        self.camView = camView
    
    def on_break(self):
        if not self.camView:
            return toast('entrer url de la source')

    def on_play(self):
        if not self.camView:
            return toast('entrer url de la source')

    def on_stop(self):
        if not self.camView:
            return toast('aucun camera en cours de lecture')

    def on_record(self):
        if not self.camView:
            return toast('aucun camera en cours de lecture')

    def select_format(self):
        if not self.camView:
            return toast('aucun camera en cours de lecture')

    def on_switch(self):
        if not self.camView:
            return toast('La cam principe ne peux pas basculer sur ce camera')


    
