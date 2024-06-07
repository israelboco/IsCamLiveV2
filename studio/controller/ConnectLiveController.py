from flask import Flask, Response, request, redirect, render_template, send_from_directory, url_for
import cv2
import os
import signal
import webbrowser
from threading import Thread
from studio.controller.CamController import CamController


class ConnectLiveController:
    app = Flask(__name__, template_folder='templates', static_folder='templates/static')
    CHUNK = 1024
    client_ip = None
    flask_thread = None
    # file_path = os.path.abspath("index.html")
    file_path = "index.html"

    def __init__(self, camController: CamController, **kwargs):
        super().__init__(**kwargs)
        self.camController = camController

        @self.app.route('/camlive')
        def home():
            script_path = url_for('static', filename='client.js')
            return render_template(self.file_path, client_ip=request.remote_addr, script_path=script_path) #, message=message

        @self.app.route('/camlive/audio_feed')
        def audio_feed():
            return Response(self.generate_audio(),
                            mimetype='audio/x-wav')
        
        @self.app.route('/camlive/video_feed')
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/camlive/old-api')
        def old_api():
            return redirect("https://new-domain.com/new-api", code=302)
        
        @self.app.route('/camlive/shutdown', methods=['POST'])
        def shutdown(self):
            self.stop()
            return 'Server shutting down...'

    def serve_static_client_js(self):
        return send_from_directory(os.path.join(self.app.root_path, 'static'), 'client.js')

    def generate_audio(self):
        
        while self.camController.audioCamera:
            data = self.camController.audioCamera.read(self.CHUNK)
            yield data

    def generate_frames(self):

        while self.camController.videoCamera:
            success, frame = self.camController.videoCamera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def local_template(self):
        file_path = self.file_path
        webbrowser.open_new_tab(file_path)

    def start(self):
        try:
            self.flask_thread = Thread(target=self.on_demare)
            self.flask_thread.start()
            # flask_thread.join()
        except Exception as e:
            print(e)
    
    def stop(self):
        try:
            # func = request.environ.get('werkzeug.server.shutdown')
            # if func is None:
            #     raise RuntimeError('Not running with the Werkzeug Server')
            # func()
            # self.app = None
            os.kill(os.getpid(), signal.SIGINT)
            self.flask_thread = None
        except Exception as e:
            # self.app = None
            print(e)

    def on_demare(self):
        # if not self.app:
        #     self.app = Flask(__name__, template_folder='templates', static_folder='templates/static')
        self.app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        self.client_ip = request.remote_addr

# , debug=True