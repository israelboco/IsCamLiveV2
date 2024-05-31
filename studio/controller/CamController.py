from studio.view.CamCapture import CamCapture


class CamController:
    camView = None
    # pass
    
    def __init__(self, camView=None, **kwargs):
        super().__init__(**kwargs)
        self.camView = camView

    def add_start_video(self, camView):
        self.camView = camView
    
    def on_break(self):
        print('on_break')

    def on_play(self):
        print('on_play')

    def on_stop(self):
        print('on_stop')

    def on_record(self):
        print('on_record')

    def select_format(self):
        print('select_format')

    def on_switch(self):
        print('on_switch')

    
