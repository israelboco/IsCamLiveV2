from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.magic_behavior import MagicBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivymd.uix.behaviors.focus_behavior import FocusBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine, MDExpansionPanelTwoLine


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
            icon="studio\\asset\holo.png",
            content=ContentExpandOne(),  # content of panel
            panel_cls=MDExpansionPanelTwoLine(  # content of header
                text="Connect to an online network",
                secondary_text="Live connection",
            )
        )
    
    def start_expand_two(self):
        self.expand_two = MDExpansionPanel(
            icon="studio\\asset\holo.png",
            content=ContentExpandTwo(),  # content of panel
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