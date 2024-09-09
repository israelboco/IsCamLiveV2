import hashlib
import os
import re
from studio.Service.DBCamlive import DatabaseManager
from studio.Service.NotificationService import Compte, Connexion
from studio.Service.Traitement import Traitement # type: ignore
from studio.controller.CamController import CamController
from studio.model.ThreadClass import ThreadManager
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.uix.button import MDRectangleFlatButton
from studio.controller.ExpansionPanel import ExpansionPanelVid
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineAvatarListItem


class Data:
    index = 1
    listProces = []
    listCam = []
    connectLiveController = None
    menu_items_format = []
    menu_items_camera = []
    resource_cam_thread = None
    manager = ThreadManager()
    expansion = ExpansionPanelVid()
    expand_two = False
    expand_one = False
    app = None
    dialogConnexionBox = None
    dialogCompteBox = None
    username = None
    email = None
    list_sessions = None
    dialogSessionBox = None
    define_session = None

    def __init__(self, app) -> None:
        self.camController = CamController()
        self.app = app
        self.camController.app = app
        self.db_manager = DatabaseManager("camlive.db")
        self.traitement = Traitement()
    
    def connexion_sessions(self, dt):
        self.dialogCompteBox.dismiss()
        if self.dialogCompteBox:
            self.dialogCompteBox = None
        self.sessions()

    def sessions(self):
        if not self.dialogConnexionBox:
            self.dialogConnexionBox = MDDialog(
                    title="[b][color=#5AA6FF]Connexion[/color][/b]",
                    type="custom",
                    content_cls=Connexion(),
                    md_bg_color="#262626",
                    buttons=[
                        MDRectangleFlatButton(
                            text="Continuer sans connexion",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.continuer
                        ),
                        MDRectangleFlatButton(
                            text="Connexion",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.connexion
                        ),
                        MDRectangleFlatButton(
                            text="Créer un compte",
                            theme_text_color="Custom",
                            text_color=self.app.theme_cls.primary_color,
                            on_release=self.creer_compte
                        ),
                    ],
            )
        self.dialogConnexionBox.open()

    def continuer(self, dt):
        self.app.main_view.transition.direction = "left"
        self.app.main_view.current = "screen main"
        self.dialogConnexionBox.dismiss()

    def creer_compte(self, dt):
        name = self.dialogConnexionBox.content_cls.text_username.text
        password = self.dialogConnexionBox.content_cls.text_password.text
        email = self.dialogConnexionBox.content_cls.text_email.text
        if name == "" or password == "" or not self.is_valid_email(email):
            return toast("Entrer invalide")
        try:
            select_user_sql = "SELECT * FROM users WHERE email = ?;"
            user = self.db_manager.fetch_data(select_user_sql, (email,))
            if not user:
                password_hash = self.hash_password(password)
                insert_sql = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
                self.db_manager.insert_data(insert_sql, (name, email, password_hash))
            else:
                return toast("L'utilisateur exist déjà, veiller vous connectez!")
            select_user_sql = "SELECT * FROM users WHERE email = ?"
            user = self.db_manager.fetch_data(select_user_sql, (email,))[0]
            if not user:
                return toast("Probleme de connexion, Veillez réessayer !")
            self.username = user[1]
            self.email = user[2]
            select_session_sql = "SELECT * FROM sessions WHERE fk_user=? ORDER BY id DESC"
            self.list_sessions = self.db_manager.fetch_data(select_session_sql, (user[0],))
            if not self.list_sessions:
                insert_sql = "INSERT INTO sessions (name, fk_user) VALUES (?, ?)"
                self.db_manager.insert_data(insert_sql, ("session 1", user[0]))
                self.list_sessions = self.db_manager.fetch_data(select_session_sql, (user[0],))
                self.define_session = self.list_sessions[0]
            else:
                self.define_session = self.list_sessions[0]
            self.dialogConnexionBox.dismiss()
            self.app.main_view.transition.direction = "left"
            self.app.main_view.current = "screen main"
            self.app.demarer_session()
            if self.dialogCompteBox:
                self.dialogCompteBox = None
        except Exception as e:
            print(e)
            return toast("Une erreur est survenue veillez réessayé")
    
    def connexion(self, dt):
        name = self.dialogConnexionBox.content_cls.text_username.text
        password = self.dialogConnexionBox.content_cls.text_password.text
        email = self.dialogConnexionBox.content_cls.text_email.text
        if name == "" or password == "" or not self.is_valid_email(email):
            return toast("Entrer invalide")
        try:
            select_user_sql = "SELECT * FROM users WHERE email=?"
            user = self.db_manager.fetch_data(select_user_sql, (email,))
            if not user:
                return toast("Utilisateur n'exist pas, Veillez creer un Compte")
            user = user[0]
            if not self.verify_password(user[3], password):
                return toast("Mot de passe invalide")
            self.username = user[1]
            self.email = user[2]
            select_session_sql = "SELECT * FROM sessions WHERE fk_user=? ORDER BY id DESC"
            self.list_sessions = self.db_manager.fetch_data(select_session_sql , (user[0],))
            if not self.list_sessions:
                insert_sql = "INSERT INTO sessions (name, fk_user) VALUES (?, ?)"
                self.db_manager.insert_data(insert_sql, ("session 1", user[0]))
                self.list_sessions = self.db_manager.fetch_data(select_session_sql, (user[0],))
                self.define_session = self.list_sessions[0]
            else:
                self.define_session = self.list_sessions[0]
            self.dialogConnexionBox.dismiss()
            self.app.main_view.transition.direction = "left"
            self.app.main_view.current = "screen main"
            self.app.demarer_session()
            if self.dialogCompteBox:
                self.dialogCompteBox = None
        except Exception as e:
            print(e)
            return toast("Une erreur est survenue veillez réessayé")


    def hash_password(self, password):
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt + hashed

    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:16]
        stored_hash = stored_password[16:]
        hashed = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
        return hashed == stored_hash

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    def compte(self):
        if not self.dialogCompteBox:
            if self.email:
                self.dialogCompteBox = MDDialog(
                        title="[b][color=#5AA6FF]Compte[/color][/b]",
                        type="custom",
                        content_cls=Compte(),
                        md_bg_color="#262626",
                        buttons=[
                            MDRectangleFlatButton(
                                text="Modifier",
                                theme_text_color="Custom",
                                text_color=self.app.theme_cls.primary_color,
                                on_release=self.modifier
                            ),
                            MDRectangleFlatButton(
                                text="Deconnexion",
                                theme_text_color="Custom",
                                text_color=self.app.theme_cls.primary_color,
                                on_release=self.deconnexion
                            ),
                        ],
                )
            else:
                self.dialogCompteBox = MDDialog(
                        title="[b][color=#5AA6FF]Compte[/color][/b]",
                        md_bg_color="#262626",
                        buttons=[
                            MDRectangleFlatButton(
                                text="Connexion",
                                theme_text_color="Custom",
                                text_color=self.app.theme_cls.primary_color,
                                on_release=self.connexion_sessions
                            ),
                        ],
                )
        if self.email:
            self.dialogCompteBox.content_cls.text_username.text = self.username
            self.dialogCompteBox.content_cls.text_email.text = self.email
            self.dialogCompteBox.content_cls.sessions.text = self.define_session[1]
        self.dialogCompteBox.open()

    def modifier(self, dt):
        email = self.email
        text = str(self.dialogCompteBox.content_cls.sessions.text_field.text)
        print(text)
        if text == "":
            return toast("Entrer invalide")
        select_user_sql = "SELECT * FROM users WHERE email = ?;"
        user = self.db_manager.fetch_data(select_user_sql, (email,))
        user = user[0]
        if user:
            select_session_sql = "SELECT * FROM sessions WHERE fk_user=? AND name=?"
            sessions = self.db_manager.fetch_data(select_session_sql , (user[0], text))
            if not sessions:
                insert_sql = "INSERT INTO sessions (name, fk_user) VALUES (?, ?)"
                self.db_manager.insert_data(insert_sql, (text, user[0]))
                select_session_sql = "SELECT * FROM sessions WHERE fk_user=? AND name = ?"
                list_sessions = self.db_manager.fetch_data(select_session_sql, (user[0], text))
                if list_sessions:
                    self.define_session = list_sessions[0]
            select_session_sql = "SELECT * FROM sessions WHERE fk_user=? ORDER BY id DESC"
            self.list_sessions = self.db_manager.fetch_data(select_session_sql, (user[0],))
            if self.dialogSessionBox:
                self.dialogSessionBox = None

        self.dialogCompteBox.dismiss()
    
    def deconnexion(self, dt):
        self.email = None
        self.dialogCompteBox.dismiss()
        if self.dialogCompteBox:
            self.dialogCompteBox = None
    
    def session_list(self, text=None):
        items_sessions = []
        for index in self.list_sessions:
            items_sessions.append(
                Item(
                    text=f"[b][color=#5AA6FF]{index[1]}[/color][/b]", 
                    source="content-save-outline", 
                    on_release=lambda x: self.select_sesssion(index, text)
                )
            )
        if not self.dialogSessionBox:
            self.dialogSessionBox = MDDialog(
                    title="[b][color=#5AA6FF]Select Sessions[/color][/b]",
                    type="simple",
                    md_bg_color="#262626",
                    items=items_sessions   
            )
        self.dialogSessionBox.open()

    def select_sesssion(self, session=None, text=None, dt=None):
        self.define_session = session
        if text:
            text.text = session[1]
        self.dialogSessionBox.dismiss()
        if self.dialogSessionBox:
            self.dialogSessionBox = None


class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()