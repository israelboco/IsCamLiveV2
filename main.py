import kivymd
from kivy.lang import Builder
from kivymd.app import MDApp # type: ignore
from kivymd.font_definitions import fonts
from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivymd.uix.button import MDIconButton
from kivy.uix.dropdown import DropDown
from kivymd.utils import asynckivy # type: ignore

from studio.controller.CamController import CamController
from studio.controller.ExpansionPanel import ExpansionPanelVid, FocusButton, IconButtonAction
from kivymd.uix.expansionpanel import MDExpansionPanel # type: ignore
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture
from studio.view.CameraFrame import Camera
from studio.view.CardAudio import CardAudio
from studio.view.MenuFrame import MenuBar
from studio.view.MyProcess import MyProcess
from studio.view.ScreenMain import ScreenMain
from studio.view.TabVideos import TabVideo
from kivymd.icon_definitions import md_icons

# Builder.load_file("studio/view/kv/main.kv")


class AppCameraLive(MDApp):
    index = 1
    listProces = []
    listCam = []
    camController = CamController()
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.dropdown = DropDown()
        self.screenMain = ScreenMain()

    def build(self) -> MDScreen:
        self.title = "Camera Live"
        return self.screenMain

    def on_start(self):
        tab = TabVideo(id='1', title="CamLive 1")
        self.root.ids.tab_videos.add_widget(tab)
        self.affiche_format()
        expansion = ExpansionPanelVid()
        expansion.start_expand_one()
        expansion.start_expand_two()
        self.screenMain.ids.one_widget.add_widget(expansion.expand_one)
        self.screenMain.ids.two_widget.add_widget(expansion.expand_two)

    def on_stop(self):
        pass

    def add_tab(self):
        try:
            self.index += 1
            name_tab = f"CamLive {self.index}"
            tab = TabVideo(
                id=str(self.index),
                tab_label_text=f"[ref={name_tab}][font={fonts[-1]['fn_regular']}]{md_icons['close']}[/font][/ref]{name_tab}",
            )
            self.root.ids.tab_videos.add_widget(
                tab
            )
        except Exception as e:
            print(e)

    def remove_tab(self):
        if self.index > 1:
            self.index -= 1
        self.root.ids.tab_videos.remove_widget(
            self.root.ids.tab_videos.get_tab_list()[-1]
        )

    def on_ref_press(
            self,
            instance_tab_videos,
            instance_tab_label,
            instance_tab,
            instance_tab_bar,
            instance_carousel,
    ):
        for instance_tab in instance_carousel.slides:
            if instance_tab.tab_label_text == instance_tab_label.text:
                instance_tab_videos.remove_widget(instance_tab_label)
                self.index -= 1
                break

    def on_start_video(self):
        text = self.screenMain.ids.lien.text
        if text:
            self.screenMain.ids.spinner.active = True
            asynckivy.start(self.start_source(text))
        else:
            self.screenMain.ids.spinner.active = False
    
    async def start_source(self, text):
        cam = None
        for content in self.listCam:
            print(content)
            listText= content[0]
            if text == listText:
                cam = content[1]
                break
        if not cam:
            await asynckivy.sleep(0.5)
            start_video = CamCapture(text, self.screenMain)
            lancer = await start_video.lancer()
            if lancer:
                print(f"start_source====>>>> {lancer}")
                self.listCam.append((text, lancer))
        else:
            await asynckivy.sleep(0.5)
            start_video = CamCapture(text, self.screenMain)
            lancer = await start_video.lancer(cam)
        self.screenMain.ids.spinner.active = False
        print(f"add_start_video ====>>>> {self.camController}")
        self.camController.add_start_video(start_video)
    
    def on_start_audio(self):
        pass

    def affiche_format(self):
        for index in list(FormatEnum):

            btn = FocusButton(text=str(index.value), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.selectDropdown(btn.text))
            self.dropdown.add_widget(btn)
    
    def listDropdown(self):
        self.dropdown.open(self.screenMain.ids.label_format)
    
    def selectDropdown(self, text):
        self.dropdown.select(text)
        self.screenMain.ids.label_format.text = "format :" + str(text)

    # def tap_expansion_chevron(
    #     self, panel: MDExpansionPanel, chevron: MDIconButton
    # ):
    #     panel.open() if not panel.is_open else panel.close()
    #     panel.set_chevron_down(
    #         chevron
    #     ) if not panel.is_open else panel.set_chevron_up(chevron)


app = AppCameraLive()
app.run()