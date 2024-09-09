# source_image = face_recognition.load_image_file(target.detect_path)
#         small_frame = cv2.resize(frame, (640, 480))
#         try:
#             result = DeepFace.verify(source_image_path, small_frame)
#             if result["verified"]:
#                 print(result)
#                 top, right, bottom, left = (50, 50, 200, 200)  # Dummy coordinates; update with actual face location if needed
#                     # cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                     # self.save_image(small_frame)
#         except Exception as e:
#             print("Erreur lors de la comparaison des visages:", e)

#         buf1 = cv2.flip(small_frame, 0)
#         buf = buf1.tobytes()
#         image_texture = Texture.create(size=(small_frame.shape[1], small_frame.shape[0]), colorfmt='bgr')
#         image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         self.image.texture = image_texture

        
#         source_encoding = face_recognition.face_encodings(source_image)[0]

#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Detect faces in the current frame
#         faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#         for (x, y, w, h) in faces:
#             await asynckivy.sleep(0)
#             # Extract the face region from the RGB frame for accurate comparison
#             roi_rgb = rgb_frame[y:y+h, x:x+w]
#             face_encodings = face_recognition.face_encodings(roi_rgb)
            
#             if face_encodings:
#                 face_encoding = face_encodings[0]
                
#                 # Compare the detected face with the source image encoding
#                 matches = face_recognition.compare_faces([source_encoding], face_encoding, tolerance=0.6)
#                 face_distances = face_recognition.face_distance([source_encoding], face_encoding)
#                 best_match_index = np.argmin(face_distances)
                
#                 if matches[best_match_index]:
#                     await self.person_detected(target)
#                     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#                     buf1 = cv2.flip(frame, 0)
#                     buf = buf1.tobytes()
#                     image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
#                     image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#                     self.save_image(frame)

# # import cv2
# # import numpy as np

# # # Chemins vers les fichiers YOLO
# # config_path = 'yolov3.cfg'
# # weights_path = 'yolov3.weights'
# # names_path = 'coco.names'

# # # Charger le modèle YOLO
# # net = cv2.dnn.readNet(weights_path, config_path)
# # layer_names = net.getLayerNames()
# # output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# # def detect_objects(image_path):
# #     image = cv2.imread(image_path)
# #     height, width, channels = image.shape

# #     # Prétraitement de l'image
# #     blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
# #     net.setInput(blob)
# #     outputs = net.forward(output_layers)

# #     class_ids = []
# #     confidences = []
# #     boxes = []

# #     # Traitement des résultats
# #     for output in outputs:
# #         for detection in output:
# #             for obj in detection:
# #                 scores = obj[5:]
# #                 class_id = np.argmax(scores)
# #                 confidence = scores[class_id]
# #                 if confidence > 0.5:
# #                     center_x = int(obj[0] * width)
# #                     center_y = int(obj[1] * height)
# #                     w = int(obj[2] * width)
# #                     h = int(obj[3] * height)
# #                     x = int(center_x - w / 2)
# #                     y = int(center_y - h / 2)
# #                     boxes.append([x, y, w, h])
# #                     confidences.append(float(confidence))
# #                     class_ids.append(class_id)

# #     indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# #     detected_objects = []
# #     for i in indices:
# #         i = i[0]
# #         box = boxes[i]
# #         detected_objects.append(box)

# #     return detected_objects

# # cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break

# #     # Détection dans le flux vidéo
# #     detected_objects = detect_objects(frame)
    
# #     # Affichage des objets détectés
# #     for box in detected_objects:
# #         x, y, w, h = box
# #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

# #     cv2.imshow('Video', frame)

# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()









# ################################""
# # import dlib

# # # Initialize dlib's face detector and face recognition model
# # detector = dlib.get_frontal_face_detector()
# # sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# # facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# # def get_face_encoding(image):
# #     faces = detector(image, 1)
# #     face_descriptors = []
# #     for k, d in enumerate(faces):
# #         shape = sp(image, d)
# #         face_descriptor = facerec.compute_face_descriptor(image, shape)
# #         face_descriptors.append(face_descriptor)
# #     return face_descriptors

# # # Replace this part of your code
# # face_encodings = get_face_encoding(rgb_frame)
# # if face_encodings:
# #     matches = dlib.compare_faces([source_encoding], face_encodings[0])
# #     if matches:
# #         # Do something, e.g., draw rectangle, save image, etc.
