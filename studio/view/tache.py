# # comment on peut diffuser une video de opencv depuis un programme python sur un projecteur connecter au reseau wifi
# from flask import Flask, Response
# import cv2

# app = Flask(__name__)
# cap = cv2.VideoCapture(0)  # Capture vidéo depuis la webcam, remplacez 0 par le chemin de votre fichier vidéo si nécessaire

# def generate_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)




# import os

# Obtenez le chemin vers le répertoire DCIM
# dcim_path = os.path.join(os.path.expanduser("~"), "DCIM")

# Utilisez dcim_path pour enregistrer votre image


# #comment publier une instance d'opencv video sur le reseau avec un lien depuis un programme python

# import cv2
# from flask import Flask, Response

# app = Flask(__name__)
# cap = cv2.VideoCapture(0)  # Capture vidéo à partir de la webcam (changez le numéro pour utiliser une autre source)

# def generate_frames():
#     while True:
#         success, frame = cap.read()  # Lire le cadre de la vidéo
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)  # Convertir le cadre en format JPEG
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Générer les trames

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')  # Diffuser le flux vidéo

# if __name__ == "__main__":
#     app.run(debug=True)  # Démarrer le serveur Flask en mode debug



# from openai_whisper import transcribe

# # Transcription d'un fichier audio
# text = transcribe('chemin_vers_le_fichier_audio.wav')
# print(text)