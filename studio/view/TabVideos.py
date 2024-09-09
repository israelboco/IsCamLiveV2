from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivymd.utils import asynckivy
from studio.controller.CamController import CamController
from studio.controller.ExpansionPanel import FocusButton
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture
from kivymd.toast import toast
from threading import Thread
from studio.view.CamViewImage import CamViewImage


class CardScrollImage(MDCard):
    
    def __init__(self, app, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.app = app
        self.dropdown = None
        self.camController = CamController()
        self.detect_path = None
        self.type_objet = False
        self.type_personne = True
        self.start_traint = False
        self.face = 0
        self.profile = 0
        self.eye = 0

    def on_start(self):

        asynckivy.start(self.on_start_video(self.text))
    
    async def on_start_video(self, text):
        await asynckivy.sleep(2)
        if self.camController.videoCamera:
            return toast("stopper d'abord la camera en cours.")
        await self.start_source(text)
    
    async def start_source(self, text):
        cam = None
        await asynckivy.sleep(2)
        for content in self.app.data.listCam:
            listText= content[0]
            if text == listText:
                cam = content[1]
                break
        lancer = await self.camController.add_start_video(text, self, cam, self.app)
        if lancer:
            print(f"start_source====>>>> {lancer}")
            if not self.app.data.camController.videoCamera:
                asynckivy.start(self.app.start_source(text))
            if not cam:
                self.app.data.listCam.append((text, lancer))
            if self.app.data.define_session:
                select_cam_sql = "SELECT * FROM camlists WHERE tab_id=? AND fk_session=?"
                cam = self.app.data.db_manager.fetch_data(select_cam_sql, (self.id, self.app.data.define_session[0]))
                if not cam:
                    insert_sql = "INSERT INTO camlists (tab_id, cam_label, save, format, fk_session) VALUES (?, ?, ?, ?, ?)"
                    self.app.data.db_manager.insert_data(insert_sql, (self.id, text, True, "", self.app.data.define_session[0]))
                else:
                    update_sql = "UPDATE camlists SET cam_label = ? WHERE tab_id = ? AND fk_session = ?"
                    self.app.data.db_manager.update_data(update_sql, (text, self.id, self.app.data.define_session[0]))
                select_traite_sql = "SELECT * FROM traitements WHERE fk_cam=? AND fk_session=?"
                traite = self.app.data.db_manager.fetch_data(select_traite_sql, (self.id, self.app.data.define_session[0]))
                if not traite:
                    insert_sql = "INSERT INTO traitements (type_objet, detect_path, face, profile, eye, fk_cam, fk_session) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    self.app.data.db_manager.insert_data(insert_sql, ('personne', "", 0.2, 0.2, 0.2, self.id, self.app.data.define_session[0]))
                    traite = self.app.data.db_manager.fetch_data(select_traite_sql, (self.id, self.app.data.define_session[0]))
                    if traite:
                        data = traite[0]
                        self.init_config((data[1], data[2], data[3], data[4], data[5]))
                else:
                    data = traite[0]
                    self.init_config((data[1], data[2], data[3], data[4], data[5]))
                

    def on_audio(self):
        pass

    def affiche_format(self):
        if not self.dropdown:
            self.dropdown = DropDown()
            for index in list(FormatEnum):

                btn = FocusButton(text=str(index.value), size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.selectDropdown(btn.text))
                self.dropdown.add_widget(btn)
        self.dropdown.open(self.ids.label_format)
    
    def selectDropdown(self, text):
        self.dropdown.select(text)
        self.ids.label_format.text = "[color=#4287f5]format :" + str(text) + "[/color]"
        self.camController.select_format(text)
    
    def init_config(self, data):
        type_objet, self.detect_path, self.face, self.profile, self.eye = data
        if type_objet == "personne":
            self.type_objet = False
            self.type_personne = True
        else:
            self.type_objet = True
            self.type_personne = False

