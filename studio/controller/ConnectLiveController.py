from flask import Flask, Response
import cv2
import webbrowser
from studio.controller.CamController import CamController


class ConnectLiveController(CamController):
    app = Flask(__name__)
    CHUNK = 1024

    def generate_audio(self):
        
        while self.audioCamera:
            data = self.audioCamera.read(self.CHUNK)
            yield data

    def generate_frames(self):

        while self.videoCamera:
            success, frame = self.videoCamera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                

    def local_template(self):
        file_path = 'controller/template/index.html'
        webbrowser.open_new_tab(file_path)

    @app.route('/audio_feed')
    def audio_feed(self):
        return Response(self.generate_audio(),
                        mimetype='audio/x-wav')
    
    @app.route('/video_feed')
    def video_feed(self):
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        self.app.run(host='0.0.0.0', port=5000)
