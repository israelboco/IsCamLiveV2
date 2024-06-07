import cv2
from kivy.core.image import Texture


class CamReductController:

    def __init__(self) -> None:
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
                self.screen_video.ids.cardImage.image.texture = image_texture

            time = 1 / 30
            # self.afert(time, self.update)

        
        