from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors.magic_behavior import MagicBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelTwoLine
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar
from tkinter import filedialog

from studio.view.ScreenMain import CardReducteImage


class IconButtonAction(FocusBehavior, MagicBehavior, RotateBehavior, MDIconButton):
    
    def __init__(self, unfocus_color=None, **kwargs):
        super().__init__(**kwargs)
        self.focus_color = "#DCE8F8"
        if not unfocus_color:
            self.unfocus_color = "#676767"
        else:
            self.unfocus_color = unfocus_color
        self.opposite_colors: True
# DCE8F8

# class TextFieldFocus(FocusBehavior, MDTextField):
    
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.focus_color = "#DCE8F8"
#         self.unfocus_color = "#676767"
#         self.opposite_colors: True

class ExpansionPanelVid:
    expand_one = None
    expand_two = None

    def start_expand_one(self):
        self.expand_one = MDExpansionPanel(
            icon="studio/asset/holo.png",
            content=ContentExpandOne(id='connect'),  # content of panel
            panel_cls=MDExpansionPanelTwoLine(  # content of header
                text="Connect to an online network",
                secondary_text="Live connection",
            )
        )
    
    def start_expand_two(self):
        self.expand_two = MDExpansionPanel(
            icon="studio/asset/holo.png",
            content=CardReducteImage(),  # content of panel
            panel_cls=MDExpansionPanelOneLine(  # content of header
                text="Listes des cameras connecté",
            )
        )


class ContentExpandOne(MDBoxLayout):
    pass


class ContentExpandTwo(MDBoxLayout):
    pass


class FocusButton(FocusBehavior, Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.focus_color = "#DCE8F8"
        self.unfocus_color = "#676767"
        self.opposite_colors: True


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

class ClickableTextFieldRoundRedute(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ClickableTextFieldRoundCam(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )

    def file_manager_open(self):
        # self.file_manager.show('/')  # Ou spécifiez le chemin de départ
        # self.manager_open = True
        self.ids.text_field.text = filedialog.askopenfilename( 
            title="Ouvrir",
            defaultextension=".mp4",
            filetypes=(("Media files", "*.mp4"), ("All files", "*.*"))
        )

    def select_path(self, path):
        self.exit_manager()
        print(path)
        # Snackbar(text=f"Selected: {path}").open()
        # self.root.ids.video_player.source = path
        #  self.root.ids.video_player.state = 'play'

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()