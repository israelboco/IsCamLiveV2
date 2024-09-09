from deepface import DeepFace
import cv2
from datetime import datetime
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
import os
from PIL import Image as PILImage
# DeepFace.build_model('VGG-Face', weights_path='path/to/vgg_face_weights.h5')

class CameraApp(MDApp):
    def build(self):
        self.image = Image()
        layout = BoxLayout()
        layout.add_widget(self.image)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/10.0)  # Augmentez l'intervalle pour réduire la fréquence de mise à jour
        return layout

    def save_image(self, image):
        current_dir = os.getcwd()
        name = "detectObject_" + datetime.now().strftime("%Y%m%d_%H%M%S") + '.png'  # Réduit la longueur du nom du fichier
        path = os.path.join(current_dir, "enregistrement", "capture", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = PILImage.fromarray(image)
        image_pil.save(path)

    def update(self, dt):
        ret, frame = self.capture.read()
        if not ret:
            return

        # Redimensionner le cadre pour améliorer la performance
        small_frame = cv2.resize(frame, (640, 480))  # Modifiez la taille en fonction de vos besoins
        # rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # frame_path = os.path.join("temp_frame.jpg")
        # cv2.imwrite(frame_path, rgb_frame)

        # Comparer les visages
        try:
            result = DeepFace.verify(source_image_path, small_frame)
            if result["verified"]:
                print(result)
                top, right, bottom, left = (50, 50, 200, 200)  # Dummy coordinates; update with actual face location if needed
                    # cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    # self.save_image(small_frame)
        except Exception as e:
            print("Erreur lors de la comparaison des visages:", e)

        buf1 = cv2.flip(small_frame, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(size=(small_frame.shape[1], small_frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = image_texture

    def on_stop(self):
        self.capture.release()

if __name__ == '__main__':
    # Charger l'image source
    source_image_path = r"C:\Users\issrael BOCO\Desktop\ISRAEL\Projet\camaraLive\studio\Service\image.jpeg"
    CameraApp().run()




















# import face_recognition
# import dlib
# import cv2
# from datetime import datetime
# from kivy.graphics.texture import Texture
# from kivy.uix.image import Image
# from kivymd.app import MDApp
# from kivy.clock import Clock
# from kivy.uix.boxlayout import BoxLayout
# import os
# from PIL import Image as PILImage

# class CameraApp(MDApp):
#     def build(self):
#         self.image = Image()
#         layout = BoxLayout()
#         layout.add_widget(self.image)
#         self.capture = cv2.VideoCapture(0)
#         Clock.schedule_interval(self.update, 1.0/10.0)  # Augmentez l'intervalle pour réduire la fréquence de mise à jour
#         return layout

#     def save_image(self, image):
#         current_dir = os.getcwd()
#         name = "detectObject_" + datetime.now().strftime("%Y%m%d_%H%M%S") + '.png'  # Réduit la longueur du nom du fichier
#         path = os.path.join(current_dir, "enregistrement", "capture", name)
#         os.makedirs(os.path.dirname(path), exist_ok=True)
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         image_pil = PILImage.fromarray(image)
#         image_pil.save(path)

#     def update(self, dt):
#         ret, frame = self.capture.read()
#         if not ret:
#             return

#         # Redimensionner le cadre pour améliorer la performance
#         small_frame = cv2.resize(frame, (640, 480))  # Modifiez la taille en fonction de vos besoins
#         rgb_frame = small_frame[:, :, ::-1]

#         # Trouver les emplacements et les encodages des visages
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations)

#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             matches = face_recognition.compare_faces([source_encoding], face_encoding)
#             if True in matches:
#                 top, right, bottom, left = face_location
#                 cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 self.save_image(small_frame)

#         buf1 = cv2.flip(small_frame, 0)
#         buf = buf1.tobytes()
#         image_texture = Texture.create(size=(small_frame.shape[1], small_frame.shape[0]), colorfmt='bgr')
#         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         self.image.texture = image_texture

#     def on_stop(self):
#         self.capture.release()

# if __name__ == '__main__':
#     # Charger l'image source
#     source_image = face_recognition.load_image_file(r"C:\Users\issrael BOCO\Desktop\ISRAEL\Projet\camaraLive\enregistrement\capture\detectOject_Monday_12_August_2024_06_10_37.png")
#     source_image = cv2.resize(source_image, (640, 480))  # Redimensionner l'image source
#     face_encodings = face_recognition.face_encodings(source_image)
#     print(face_encodings)
#     if len(face_encodings) > 0:
#         source_encoding = face_encodings[0]
#         CameraApp().run()
#     else:
#         print("Aucun visage détecté dans l'image source.")

# # distances = face_recognition.face_distance([source_encoding], face_encoding)
# # match = distances[0] <= 0.6











# {'verified': True, 'distance': 0.6268175575213742, 'threshold': 0.68, 'model': 'VGG-Face', 'detector_backend': 'opencv', 'similarity_metric': 'cosine', 'facial_areas': {'img1': {'x': 181, 'y': 234, 'w': 472, 'h': 472, 'left_eye': None, 'right_eye': None}, 'img2': {'x': 190, 'y': 138, 'w': 223, 'h': 223, 'left_eye': None, 'right_eye': None}}, 'time': 4.15}