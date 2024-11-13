import cv2
from datetime import datetime
import math
from collections import namedtuple
from PIL import Image
import numpy as np
from kivy.graphics.texture import Texture
from kivymd.utils import asynckivy
from kivy.clock import Clock
import time
import os
from kivymd.toast import toast

class Traitement:
    
    def __init__(self):
        self.current_dir = os.getcwd()
        # Joindre un autre chemin
        self.traints = []
        self.gray_target = None
        self.encours = False
    
    async def person_detected(self, target):
        if not self.encours:
            toast('Personne trouvée')
            await asynckivy.sleep(1)
            toast('la cam est en cours de basculer')
            target.camController.on_switch()
            self.encours = not self.encours
            Clock.schedule_once(self.update_encour, 15)

    def update_encour(self, dt):
        self.encours = not self.encours
    
    def afert(self, delay, func, id):
        Clock.schedule_once(lambda dt: func(id, dt), delay)
    
    def start_traint(self, target):
        gry_target = self.profile_detection(target.detect_path)
        self.traints.append((target.id, target, gry_target))

    def stop_traints(self, target):
        self.traints.remove(target)
    
    def find_target(self, search_target):
        for id, target, gry_target in self.traints:
            if id == search_target:
                return (id, target, gry_target)
        return None
    
    def jsonDictDecoder(self, jsonDict):
        return namedtuple('X', jsonDict.keys())(*jsonDict.values())
        

    async def object_dectionz(self, path):
        try:
            
            image = path
            height, width = image.shape[:2]
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)

            layer_names = self.net.getLayerNames()
            output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
            outs = self.net.forward(output_layers)
            boxes = []
            class_ids = []
            confidences = []
            for out in outs:
                await asynckivy.sleep(0)
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                print(indices)
                if len(indices) > 0:
                    indices = indices.flatten() 
                    for i in indices:
                        await asynckivy.sleep(0)
                        box = boxes[i]
                        x, y, w, h = box[0], box[1], box[2], box[3]
                        label = str(self.classes[class_ids[i]])
                        cv2.rectangle(path, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(path, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Conversion de l'image OpenCV en texture Kivy
            buf1 = cv2.flip(path, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(path.shape[1], path.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.save_image(path)
            
            return image_texture

        except Exception as e:
            print("object_detectionz ===>")
            print(e)

        return None

    def start(self, id=None, dt=None):
        controle = self.find_target(id)
        if not controle:
            return
        asynckivy.start(self.start_controle(controle))
 
    async def start_controle(self, controle):
        id, target, gray_target = controle

        face = target.face
        profile = target.profile
        eye = target.eye

        if target.camController.videoCamera and target.type_personne:
            # Lire une image depuis le flux vidéo
            ret, frame = target.camController.videoCamera.read()
            # Appeler récursivement la fonction update après un certain délai
            if ret:
                # small_frame = cv2.resize(frame, (640, 480))
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.classCascadefacial.empty():
                    print("Erreur : Le classificateur facial n'a pas été chargé correctement.")
                    return
                # faces = self.classCascadefacial.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
                faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                profiles = self.profile_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                eyes = self.eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
                min_val_face, max_val_face, min_loc_face, max_loc_face = (0, 0, 0, 0)
                min_val_profile, max_val_profile, min_loc_profile, max_loc_profile = (0, 0, 0, 0)
                min_val_eyes, max_val_eyes, min_loc_eyes, max_loc_eyes = (0, 0, 0, 0)
                print(face)
                if face >= 0.6:
                    await self.face_dectect(frame, target)
                elif face > 0 and face < 0.6:
                    for (x, y, w, h) in faces:
                        roi = gray_frame[y:y+h, x:x+w]
                        result_face = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                        min_val_face, max_val_face, min_loc_face, max_loc_face = cv2.minMaxLoc(result_face)
                        if max_val_face > face:
                            await self.person_detected(target)
                            top_left = max_loc_face
                            h, w = gray_frame.shape
                            bottom_right = (top_left[0] + w, top_left[1] + h)
                            cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            buf1 = cv2.flip(frame, 0)
                            buf = buf1.tobytes()
                            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                            self.save_image(frame)
                            
                if profile > 0 and face > 0.8:
                    for (x, y, w, h) in profiles:
                        roi = gray_frame[y:y+h, x:x+w]
                        result_profile = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                        min_val_profile, max_val_profile, min_loc_profile, max_loc_profile = cv2.minMaxLoc(result_profile)
                        if max_val_profile > profile:
                            await self.person_detected(target)
                            top_left = max_loc_profile
                            h, w = gray_frame.shape
                            bottom_right = (top_left[0] + w, top_left[1] + h)
                            cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            buf1 = cv2.flip(frame, 0)
                            buf = buf1.tobytes()
                            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                            self.save_image(frame)

                if eye > 0 and face > 0.8:
                    for (x, y, w, h) in eyes:
                        roi = gray_frame[y:y+h, x:x+w]
                        result_eyes = cv2.matchTemplate(roi, gray_target, cv2.TM_CCOEFF_NORMED)
                        min_val_eyes, max_val_eyes, min_loc_eyes, max_loc_eyes = cv2.minMaxLoc(result_eyes)
                        if max_val_eyes > eye:
                            await self.person_detected(target)
                            top_left = max_loc_eyes
                            h, w = gray_frame.shape
                            bottom_right = (top_left[0] + w, top_left[1] + h)
                            cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                            buf1 = cv2.flip(frame, 0)
                            buf = buf1.tobytes()
                            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                            self.save_image(frame)

                self.afert(1, self.start, target.id)


    def facialDetectionAndMark(self, _image, _classCascade):
        imgreturn = _image.copy()
        gray = cv2.cvtColor(imgreturn, cv2.COLOR_BGR2GRAY)
        faces = _classCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(imgreturn, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return imgreturn

    def profile_detection(self, path):
        self.target_image = cv2.imread(path)
        self.gray_target = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2GRAY)
        return self.gray_target

    def save_image(self, image):
        name = "detectOject_" + datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S") + '.png'
        path = os.path.join(self.current_dir, "enregistrement", "capture", name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image)
        image_pil.save(path)
        return path
    
    async def face_dectect(self, frame, target):
        small_frame = cv2.resize(frame, (640, 480))
        path_small_frame = self.save_image(small_frame)
        detect_path = target.detect_path
        try:
            # frame_source = cv2.imread(target.detect_path)
            # result = DeepFace.verify(target.detect_path, path_small_frame)
            # if result["verified"]:
            #     facial_areas = self.jsonDictDecoder(result).facial_areas
            #     print(facial_areas)
            #     img1 = self.jsonDictDecoder(facial_areas).img1
            #     img1 = self.jsonDictDecoder(img1)
            #     img2 = self.jsonDictDecoder(facial_areas).img2
            #     img2 = self.jsonDictDecoder(img2)
            #     print(img2)
            #     x1, y1, w1, h1 = (img1.x, img1.y, img1.w, img1.h)  
            #     x, y, w, h = (img2.x, img2.y, img2.w, img2.h)  
            #     cv2.rectangle(frame_source, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
            #     cv2.rectangle(small_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #     self.save_image(small_frame)
            #     self.save_image(frame_source)
                await self.person_detected(target)
        except Exception as e:
            print("Erreur lors de la comparaison des visages:", e)