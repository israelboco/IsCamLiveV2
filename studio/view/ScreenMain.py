from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from studio.Service.NotificationService import NotificationService
from tkinter import filedialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivymd.utils import asynckivy

from studio.constants.GetNetworks import GetNetworks


class ScreenMain(MDScreen):
    notificationService = NotificationService()

    def callWelcome(self):
        self.main_view.transition.direction = "left"
        self.main_view.current = "screen welcome"
    
    def dialog_box_cam(self):
        self.notificationService.add_cam_box()

class ScreenWelcome(MDScreen):
    dialog = None
    
    def apropos(self):
        text = '[i][color=#5AA6FF]Meilleure application pour optimiser la capture et la diffusion multi-sources en temps réel lors d\'événements : une solution rentable avec Cam Live.[/i][/color]'
        if not self.dialog:
                self.dialog = MDDialog(
                    title='[b][color=#5AA6FF]A propos[/color][/b]',
                    type="custom",
                    content_cls=AProposBox(),
                    md_bg_color="#262626",
                )
                self.dialog.content_cls.label_propos.text = text
                self.dialog.open()


class CardViewImage(MDCard):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
               

class CardReducteImage(MDCard, FocusBehavior):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controle = None
        self.dialogTraiteBox = None
        self.ids.check_person.active = True
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        self.getnetworks = GetNetworks()
        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "trailing_icon": str(index["trailing_icon"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_camera, width_mult=3, caller=self.ids.list_camera)


    def start(self):
        self.ids.lien.text = self.controle.text
        if self.controle.detect_path:
            self.ids.i_source.source = self.controle.detect_path
            self.ids.check_person.active = True
    
    def listcamera(self):
       self.dropdown2.open()

    def on_start_video(self):
        asynckivy.start(self.controle.on_start_video(self.ids.lien.text))

    def on_checkbox_active(self, type, active):
        if self.controle:
            if type == "Objet":
                self.controle.type_objet = True
                self.controle.type_personne = False
                if self.app.data.define_session:
                    select_traite_sql = "SELECT * FROM traitements WHERE fk_cam=? AND fk_session=?"
                    traite = self.app.data.db_manager.fetch_data(select_traite_sql, (self.controle.id, self.app.data.define_session[0]))
                    if traite:
                        update_sql = "UPDATE traitements SET type_objet = ? WHERE fk_cam = ? AND fk_session = ?"
                        self.app.data.db_manager.update_data(update_sql, ("object", self.controle.id, self.app.data.define_session[0]))
                self.ids.check_person.active = False
            elif type == "Personne":
                self.controle.type_objet = False
                self.controle.type_personne = True
                self.ids.check_objet.active = False
                self.dialog_profile()

    def dialog_profile(self):
        if not self.dialogTraiteBox:
            self.dialogTraiteBox = MDDialog(
                    title="[b][color=#5AA6FF]Config detection Personne[/color][/b]",
                    type="custom",
                    content_cls=DetectPerson(),
                    md_bg_color="#262626",
                    buttons=[
                        MDRectangleFlatButton(
                            text="Annuler",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.cancel
                        ),
                        MDRectangleFlatButton(
                            text="Enregistrer",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.save_config
                        ),
                    ],
            )

        self.dialogTraiteBox.open()
        self.dialogTraiteBox.content_cls.ids.face.text = str(self.controle.face * 100)
        self.dialogTraiteBox.content_cls.ids.profile.text = str(self.controle.profile * 100)
        self.dialogTraiteBox.content_cls.ids.eye.text = str(self.controle.eye * 100)
    
    def cancel(self, dt):
        self.dialogTraiteBox.dismiss()

    def save_config(self, dt):
        face = float(self.dialogTraiteBox.content_cls.ids.face.text) / 100
        profile = float(self.dialogTraiteBox.content_cls.ids.profile.text) / 100
        eye = float(self.dialogTraiteBox.content_cls.ids.eye.text) / 100
        if self.app.data.define_session:
            select_traite_sql = "SELECT * FROM traitements WHERE fk_cam=? AND fk_session=?"
            traite = self.app.data.db_manager.fetch_data(select_traite_sql, (self.controle.id, self.app.data.define_session[0]))
            if traite:
                update_sql = "UPDATE traitements SET type_objet = ? WHERE fk_cam = ? AND fk_session = ?"
                self.app.data.db_manager.update_data(update_sql, ("personne", self.controle.id, self.app.data.define_session[0]))
                update_sql = "UPDATE traitements SET face = ? WHERE fk_cam = ? AND fk_session = ?"
                self.app.data.db_manager.update_data(update_sql, (face, self.controle.id, self.app.data.define_session[0]))
                update_sql = "UPDATE traitements SET profile = ? WHERE fk_cam = ? AND fk_session = ?"
                self.app.data.db_manager.update_data(update_sql, (profile, self.controle.id, self.app.data.define_session[0]))
                update_sql = "UPDATE traitements SET eye = ? WHERE fk_cam = ? AND fk_session = ?"
                self.app.data.db_manager.update_data(update_sql, (eye, self.controle.id, self.app.data.define_session[0]))
                select_traite_sql = "SELECT * FROM traitements WHERE fk_cam=? AND fk_session=?"
                traite = self.app.data.db_manager.fetch_data(select_traite_sql, (self.controle.id, self.app.data.define_session[0]))
                data = traite[0]
                self.controle.init_config((data[1], data[2], data[3], data[4], data[5]))
        else:
            data = ("personne", self.controle.detect_path, face, profile, eye)
            self.controle.init_config(data)
        self.dialogTraiteBox.dismiss()

    def file_manager_open(self):
        if not self.controle.type_personne:
            return toast("Select Personne")
        
        path = filedialog.askopenfilename( 
            title="Ouvrir",
            defaultextension=".jpg",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp"), ("All files", "*.*"))
        )
        self.ids.i_source.source = path
        self.controle.detect_path = path
        if self.app.data.define_session:
            select_traite_sql = "SELECT * FROM traitements WHERE fk_cam=? AND fk_session=?"
            traite = self.app.data.db_manager.fetch_data(select_traite_sql, (self.controle.id, self.app.data.define_session[0]))
            if traite:
                update_sql = "UPDATE traitements SET detect_path = ? WHERE fk_cam = ? AND fk_session = ?"
                self.app.data.db_manager.update_data(update_sql, (path, self.controle.id, self.app.data.define_session[0]))

    def detect_object(self, dt=None):
        asynckivy.start(self.detect_object_async())
    
    async def detect_object_async(self):
        # self.ids.image.source = path
        if self.controle.camController.videoCamera:
            # Lire une image depuis le flux vidéo
            ret, frame = self.controle.camController.videoCamera.read()
            # Appeler récursivement la fonction update après un certain délai
            if ret:
                source = await self.app.data.traitement.object_dectionz(frame)
                try:
                    if not source:
                        self.ids.i_source.source = frame
                        return toast("Echec du traitement")
                    self.ids.i_source.texture = source
                except Exception as e:
                    print("file_manager_open ===>")
                    print(e)
            if self.controle.start_traint:
                self.afert(5, self.detect_object)
    
    def lancerTraitement(self):
        if self.controle.type_objet and self.ids.lancer.text == "Lancer":
            self.controle.start_traint = True
            self.detect_object()
        if self.controle.type_personne and self.ids.lancer.text == "Lancer":
            self.controle.start_traint = True
            self.app.data.traitement.start_traint(self.controle)
            self.app.data.traitement.start(self.controle.id)   
        if self.ids.lancer.text == "Lancer":
            self.ids.lancer.text = "Annuler"
        else:
            self.ids.lancer.text = "Lancer"
            self.controle.type_personne = False
            self.controle.type_objet = False
            self.controle.start_traint = False


    def afert(self, delay, func):
        Clock.schedule_once(func, delay)

    def select_path(self, path):
        self.exit_manager()
        print(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


class MainScreenView(MDScreenManager):
    pass


class AProposBox(MDBoxLayout):
          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DetectPerson(MDBoxLayout):
    
    def validate_float(self, instance):
        try:
            float(instance.text)
            instance.error = False
        except ValueError:
            instance.error = True
