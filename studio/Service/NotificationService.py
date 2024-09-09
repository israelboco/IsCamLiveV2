from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRectangleFlatButton
from studio.constants.GetNetworks import GetNetworks
from kivymd.toast import toast
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty
from tkinter import filedialog


class NotificationService:
    dialogConnectLiveBox = None
    dialogAddCamBox = None
    dialogOpenPramBox = None

    def start_connect_live(self):
        if not self.dialogConnectLiveBox:
            self.dialogConnectLiveBox = MDDialog(
                    title="[b][color=#5AA6FF]Live Partage[/color][/b]",
                    type="custom",
                    content_cls=ConnectLiveBox(),
                    md_bg_color="#262626",
                    buttons=[
                        MDRectangleFlatButton(
                            text="Annuler",
                            theme_text_color="Custom",
                            text_color="#4287f5",
                        ),
                        MDRectangleFlatButton(
                            text="Connexion",
                            theme_text_color="Custom",
                            text_color="#4287f5",
                        ),
                    ],
            )
        self.dialogConnectLiveBox.open()    

    def add_cam_box(self):
        if not self.dialogAddCamBox:
            self.dialogAddCamBox = MDDialog(
                    title="[b][color=#5AA6FF]Ajouter un nouveau cam vidéo[/color][/b]",
                    type="custom",
                    content_cls=AddCamBox(),
                    md_bg_color="#262626",
                    buttons=[
                        MDRectangleFlatButton(
                            text="Annuler",
                            theme_text_color="Custom",
                            text_color="#4287f5",
                            on_release= self.cencel_cam
                        ),
                        MDRectangleFlatButton(
                            text="Ouvrir",
                            theme_text_color="Custom",
                            text_color="#4287f5",
                            on_release= self.ouvrir_cam
                        ),
                    ],
            )
        self.dialogAddCamBox.open()

    def ouvrir_cam(self, dt):
        text = self.dialogAddCamBox.content_cls.lien.text
        if text == "":
            return toast("source vide")
        self.dialogAddCamBox.content_cls.open_cam()
        self.dialogAddCamBox.dismiss()
    
    def cencel_cam(self, dt):
        self.dialogAddCamBox.dismiss()
    
    def open_param(self):
        if not self.dialogOpenPramBox:
            self.dialogOpenPramBox = MDDialog(
                    title="[b][color=#5AA6FF]Parametre[/color][/b]",
                    type="custom",
                    content_cls=ParamBox(),
                    md_bg_color="#262626",
                    pos_hint={'center_x': .75,'center_y': .75},
                    size_hint_x=.3,
                    size_hint_y=.2,
                    buttons=[
                        MDRectangleFlatButton(
                            text="Enregistrer",
                            theme_text_color="Custom",
                            text_color="5AA6FF",
                            on_release=self.enregister
                        ),
                    ],
            )
        self.dialogOpenPramBox.open()
    
    def enregister(self, dt):
        text = self.dialogOpenPramBox.content_cls.ids.text_field.text
        if self.dialogOpenPramBox.content_cls.app.data.define_session:
            select_stockage_sql = "SELECT * FROM configs WHERE name=? AND fk_session=?"
            stockage = self.dialogOpenPramBox.content_cls.app.data.db_manager.fetch_data(select_stockage_sql, ("stockage", self.dialogOpenPramBox.content_cls.app.data.define_session[0]))
            if not stockage:
                insert_sql = "INSERT INTO configs (name, reference, fk_session) VALUES (?, ?, ?)"
                self.dialogOpenPramBox.content_cls.app.data.db_manager.insert_data(insert_sql, ("stockage", text, self.dialogOpenPramBox.content_cls.app.data.define_session[0]))
            else:
                update_sql = "UPDATE configs SET reference = ? WHERE name = ? AND fk_session = ?"
                self.dialogOpenPramBox.content_cls.app.data.db_manager.update_data(update_sql, (text, "stockage", self.dialogOpenPramBox.content_cls.app.data.define_session[0]))
        


class ConnectLiveBox(MDBoxLayout):
    
     def demarrer(self):
        if self.ids.demarrer.text == "Démarrer":
            self.ids.demarrer.text = "Allumer"
            self.ids.demarrer.md_bg_color = '#00FF40'
            # print(self.app.screenMain.ids)
            # self.app.screenMain.ids.connect.ids.Camlive.ids.bage_card.md_bg_color = '#00FF40'
            self.app.demarer_connect_live_box()
        else:
            self.ids.demarrer.text = "Démarrer"
            self.ids.demarrer.md_bg_color = '#676767'
            self.app.stop_connect_live_box()

class ParamBox(MDBoxLayout):
    
    def folder_manager_open(self):
        path = filedialog.askdirectory( )
        self.ids.text_field.text = path     


class AddCamBox(MDBoxLayout):
    menu_items_camera = None
    dropdown2 = None
    getnetworks = GetNetworks()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_camera, width_mult=3, caller=self.ids.list_camera)

    
    def open_cam(self):
        self.app.add_tab(self.lien.text)
    
    def affiche_camera(self):

        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index["interface"]),
                "trailing_icon": str(index["trailing_icon"]),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(md_bg_color="#bdc6b0",items=self.menu_items_camera, width_mult=3, caller=self.ids.list_camera)

    def listcamera(self):
        self.dropdown2.open()
    
    def selectDropdownNetwork(self, text):
        ip = text["ip_address"]
        if ip == 0:
            self.ids.lien.text = str(f"{ip}")
        else:
            self.ids.lien.text = str(f"https://{ip}")
        if self.dropdown2:
            self.dropdown2.dismiss()


class Connexion(MDBoxLayout):
    pass


class Compte(MDBoxLayout):
    pass


class TextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    
    def affiche_session(self):
        self.app.data.session_list(self.text_field)



    def selectDropdownNetwork(self, text):
        ip = text
        if ip == 0:
            self.screenMain.ids.lien.text = str(f"{ip}")
        else:
            self.screenMain.ids.lien.text = str(f"https:/{ip}")
            self.screenMain.ids.lien.focus = True
        if self.dropdown2:
            self.dropdown2.dismiss()