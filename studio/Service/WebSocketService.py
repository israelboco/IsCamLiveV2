from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.network.urlrequest import UrlRequest
import socketio
from kivy.clock import Clock


class WebSocketService():

    def __init__(self) -> None:
        self.client_id = None
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:5000')

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('notification', self.on_notification)

        # layout = BoxLayout(orientation='vertical')
        # self.label = Label(text='CamLive - Client')
        # layout.add_widget(self.label)
        # self.button = MDRaisedButton(text='Envoyer Image', on_release=self.send_image)
        # layout.add_widget(self.button)
        # return layout

    def on_connect(self):
        self.client_id = self.sio.sid
        print('Connected to server with client ID:', self.client_id)

    def on_disconnect(self):
        print('Disconnected from server')

    def on_notification(self, data):
        # Schedule dialog creation on the main thread
        Clock.schedule_once(lambda dt: self.show_dialog(data['message']))

    def show_dialog(self, message):
        self.dialog = MDDialog(title='Notification', text=message)
        self.dialog.open()

    def send_image(self, instance):
        with open(r'C:\Users\issrael BOCO\Desktop\ISRAEL\Projet\CamliveWeb\static\images\image1.jpg', 'rb') as f:
            image_data = f.read()
        print('send')
        self.sio.emit('image', image_data)

    def send_image_facial(self, source_path, path):
        # Envoyer une image (à adapter selon votre source d'image)
        with open(path, 'rb') as f:
            image_data = f.read()
        print('send')
        self.sio.emit('image', image_data)
    
    def send_image_objet(self, path):
        # Envoyer une image (à adapter selon votre source d'image)
        with open(path, 'rb') as f:
            image_data = f.read()
        print('send')
        self.sio.emit('image', image_data)