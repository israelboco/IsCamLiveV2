from kivy.properties import ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivymd.utils import asynckivy
from studio.controller.CamController import CamController
from studio.controller.ExpansionPanel import FocusButton
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture


class TabVideo(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.''' 
    dropdown = None
    camController = CamController()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on_start_video(self):
        text = self.ids.source.text
        if text:
            self.ids.spinner.active = True
            asynckivy.start(self.start_source(text))
        else:
            self.ids.spinner.active = False
    
    async def start_source(self, text):
        cam = None
        await asynckivy.sleep(1)
        for content in self.app.listCam:
            listText= content[0]
            if text == listText:
                cam = content[1]
                break
        self.ids.spinner.active = False
        lancer = await self.camController.add_start_video(text, self, cam)
        if lancer:
            print(f"start_source====>>>> {lancer}")
            if not self.app.camController.videoCamera:
                asynckivy.start(self.app.start_source(text))
            if not cam:
                self.app.listCam.append((text, lancer))

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