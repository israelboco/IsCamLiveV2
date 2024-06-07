from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog


class NotificationService:
    dialogConnectLiveBox = None

    def start_connect_live(self):
        if not self.dialogConnectLiveBox:
            self.dialogConnectLiveBox = MDDialog(
                    title="[b][color=#5AA6FF]A propos[/color][/b]",
                    type="custom",
                    content_cls=ConnectLiveBox(),
                    md_bg_color="#262626",
            )
        self.dialogConnectLiveBox.open()    


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
