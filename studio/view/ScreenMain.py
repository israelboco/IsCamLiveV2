from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.behaviors.focus_behavior import FocusBehavior


class ScreenMain(MDScreen):
        pass

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


class CardImage(MDCard):
        pass


class CardReducteImage(MDCard, FocusBehavior):
        def __init__(self, unfocus_color=None, **kwargs):
                super().__init__(**kwargs)
                self.focus_color = "#DCE8F8"
                if not unfocus_color:
                        self.unfocus_color = "#676767"
                else:
                        self.unfocus_color = unfocus_color
                        self.opposite_colors: True


class MainScreenView(MDScreenManager):
        pass


class AProposBox(MDBoxLayout):
        pass