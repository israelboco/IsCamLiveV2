import cv2
import imageio

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

# Créer un fichier vidéo
writer = imageio.get_writer('output_video.mp4', fps=30)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Écrire l'image dans le fichier vidéo
    writer.append_data(frame)

    # Afficher l'image
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
writer.close()
cv2.destroyAllWindows()


import cv2
import subprocess
import os

# Ouvrir la caméra
cap = cv2.VideoCapture(0)
frame_count = 0

# Dossier temporaire pour les images
temp_dir = 'temp_frames'
os.makedirs(temp_dir, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Sauvegarder l'image temporairement
    cv2.imwrite(os.path.join(temp_dir, f'frame_{frame_count:04d}.png'), frame)
    frame_count += 1

    # Afficher l'image
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()

# Convertir les images en vidéo avec ffmpeg
subprocess.run([
    'ffmpeg',
    '-framerate', '30',  # Cadence de la vidéo
    '-i', os.path.join(temp_dir, 'frame_%04d.png'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    'output_video.mp4'
])

# Supprimer les fichiers temporaires
for file in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file))
os.rmdir(temp_dir)



import cv2
import av

# Ouvrir la caméra
cap = cv2.VideoCapture(0)

# Créer un fichier vidéo
container = av.open('output_video.mp4', mode='w')
stream = container.add_stream('libx264', rate=30)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir l'image BGR à RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Ajouter la frame au conteneur
    packet = stream.encode(av.VideoFrame.from_ndarray(frame_rgb, format='rgb24'))
    container.mux(packet)

    # Afficher l'image
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
container.close()

