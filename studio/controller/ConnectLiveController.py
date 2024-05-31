from flask import Flask, Response
import cv2


class ConnectLiveController:
    app = Flask(__name__)
    
    def __init__(self, cap=None) -> None:
        self.cap = cap

    def generate_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    @app.route('/video_feed')
    def video_feed(self):
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        self.app.run(host='0.0.0.0', port=5000)
