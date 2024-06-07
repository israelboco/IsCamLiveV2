import kivymd
from kivy.lang import Builder
from kivymd.app import MDApp # type: ignore
from kivymd.font_definitions import fonts
from kivymd.uix.screen import MDScreen
from kivy.uix.button import Button
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDIconButton
# from kivy.uix.dropdown import DropDown
from kivymd.uix.menu import MDDropdownMenu
from kivymd.utils import asynckivy # type: ignore
from kivymd.toast import toast
from threading import Thread

from studio.Service.NotificationService import NotificationService
from studio.constants.GetNetworks import GetNetworks
from studio.controller.ConnectLiveController import ConnectLiveController
from studio.controller.CamController import CamController
from studio.controller.ExpansionPanel import ExpansionPanelVid, FocusButton, IconButtonAction
from kivymd.uix.expansionpanel import MDExpansionPanel # type: ignore
from studio.enum.FormatEnum import FormatEnum
from studio.view.CamCapture import CamCapture
from studio.view.CameraFrame import Camera
from studio.view.CardAudio import CardAudio
from studio.view.MyProcess import  MyProcess
from studio.view.ScreenMain import MainScreenView, ScreenMain
from studio.view.TabVideos import TabVideo
from kivymd.icon_definitions import md_icons

# Builder.load_file("studio/view/kv/main.kv")


class AppCameraLive(MDApp):
    index = 1
    listProces = []
    listCam = []
    camController = CamController()
    connectLiveController = None
    menu_items_format = []
    menu_items_camera = []
    resource_cam_thread = None
    # items = [f"{index}" for index in list(FormatEnum)]
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        # self.dropdown = MDDropdownMenu()
        self.main_view = MainScreenView()
        self.getnetworks = GetNetworks()
        self.notificationService = NotificationService()
        self.screenMain = self.main_view.screen_main

    def build(self) -> MDScreen:
        self.title = "Camera Live"
        return self.main_view

    def on_start(self):
        tab = TabVideo(id='1', title="CamLive 1")
        self.screenMain.ids.tab_videos.add_widget(tab)
        self.affiche_format()
        self.affiche_camera()
        self.affiche_audio()
        expansion = ExpansionPanelVid()
        expansion.start_expand_one()
        expansion.start_expand_two()
        self.screenMain.ids.one_widget.add_widget(expansion.expand_one)
        # self.screenMain.ids.two_widget.add_widget(expansion.expand_two)


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
            self.screenMain.ids.tab_videos.add_widget(
                tab
            )
        except Exception as e:
            print(e)
        self.affiche_audio()

    def remove_tab(self):
        if self.index > 1:
            self.index -= 1
        self.screenMain.ids.tab_videos.remove_widget(
            self.screenMain.ids.tab_videos.get_tab_list()[-1]
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

    async def on_start_video(self):
        self.screenMain.ids.spinner.active = True
        await asynckivy.sleep(2)
        if self.camController.videoCamera:
            self.screenMain.ids.spinner.active = False
            return toast("stopper d'abord la camera en cours.")
        self.resource_cam_thread = None
        await self.async_cam_thread()
        self.screenMain.ids.spinner.active = False
    
    async def async_cam_thread(self):
        self.resource_cam_thread = Thread(target=self.cam_thread)
        self.resource_cam_thread.start()

    def cam_thread(self):
        text = self.screenMain.ids.lien.text
        if text:
            asynckivy.start(self.start_source(text))
    
    async def start_source(self, text):
        cam = None
        for content in self.listCam:
            listText= content[0]
            if text == listText:
                cam = content[1]
                break
        lancer = await self.camController.add_start_video(text, self.screenMain, cam)
        if not self.connectLiveController:
            print('===============>>>>>>> connectLiveController')
            self.connectLiveController = ConnectLiveController(self.camController)
        if lancer:
            print(f"start_source====>>>> {lancer}")
            if not cam:
                self.listCam.append((text, lancer))

    def affiche_format(self):
       
        self.menu_items_format = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index.name),
                "on_release": lambda x=index: self.selectDropdown(x),
            } for index in list(FormatEnum)
        ]

        self.dropdown1 = MDDropdownMenu(items=self.menu_items_format, width_mult=4, caller=self.screenMain.ids.shape)

    def listDropdown(self):
        print('listDropdown')
        self.dropdown1.open()

    def affiche_camera(self):

        self.menu_items_camera = [
            {
                "viewclass": "OneLineListItem",
                "text": str(index['interface']),
                "on_release": lambda x=index: self.selectDropdownNetwork(x),
            } for index in self.getnetworks.get_networks()
        ]

        self.dropdown2 = MDDropdownMenu(items=self.menu_items_camera, width_mult=3, caller=self.screenMain.ids.list_camera)


    def affiche_audio(self):

        self.menu_items_audio = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Audio Cam {str(index + 1)}",
                "on_release": lambda x=f"Audio Cam {str(index + 1)}": self.selectDropdownAudio(x),
            } for index in range(0, self.index)
        ]

        self.dropdown3 = MDDropdownMenu(items=self.menu_items_audio, width_mult=3, caller=self.screenMain.ids.microphone)

    def listaudio(self):
        self.dropdown3.open()

    def listcamera(self):
        self.dropdown2.open()

    # @staticmethod
    def selectDropdown(self, text):
        self.screenMain.ids.label_format.text = "[color=#4287f5]format :" + str(text.value) + "[/color]"
        self.camController.select_format(text.value)
        if self.dropdown1:
            self.dropdown1.dismiss()
    
    def selectDropdownNetwork(self, text):
        self.screenMain.ids.lien.text = str(text['interface'])
        # self.camController.start_source(text)
        if self.dropdown2:
            self.dropdown2.dismiss()
    
    def selectDropdownAudio(self, text):
        self.screenMain.ids.audio.text = str('[color=#4287f5]' + text + '[/color]')
        # self.camController.start_source(text)
        if self.dropdown3:
            self.dropdown3.dismiss()
    
    def start_connect_live(self):
        if not self.camController.videoCamera:
            return toast('connectez vous a un camera')
        self.notificationService.start_connect_live()
    
    def demarer_connect_live_box(self):
        self.connectLiveController.start()
    
    def stop_connect_live_box(self):
        self.connectLiveController.stop()

    # def tap_expansion_chevron(
    #     self, panel: MDExpansionPanel, chevron: MDIconButton
    # ):
    #     panel.open() if not panel.is_open else panel.close()
    #     panel.set_chevron_down(
    #         chevron
    #     ) if not panel.is_open else panel.set_chevron_up(chevron)


app = AppCameraLive()
app.run()