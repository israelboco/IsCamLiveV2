# from tkinter import *


# class MenuBar(Frame):
#     """Barre de menus déroulants"""

#     def __init__(self, boss=None, window=None):
#         Frame.__init__(self, borderwidth=2, relief=GROOVE)
#         self.window = window
#         ##### Menu <Fichier> #####
#         fileMenu = Menubutton(self, text='Fichier')
#         fileMenu.pack(side=LEFT, padx=5)
#         me1 = Menu(fileMenu)
#         me1.add_command(label='Options', underline=0)
#         me1.add_command(label='Restart', underline=0)
#         fileMenu.configure(menu=me1)
#         ##### Menu <Aide> #####
#         helpMenu = Menubutton(self, text='Aide')
#         helpMenu.pack(side=LEFT, padx=5)
#         me1 = Menu(helpMenu)
#         me1.add_command(label='Principe de L\'application', underline=0)
#         me1.add_command(label='A propos ...', underline=0)
#         helpMenu.configure(menu=me1)
#         ##### Menu <play> #####
#         playMenu = Menubutton(self, text='Video')
#         playMenu.pack(side=LEFT, padx=5)
#         me2 = Menu(playMenu)
#         me2.add_command(label='Demarrer', underline=0, command=self.window.lancer)
#         me2.add_command(label='Enregistrer', underline=0, command=self.window.enregistrer)
#         me2.add_command(label='Stop', underline=0, command=self.window.stop)
#         me2.add_command(label='Pause', underline=0)
#         playMenu.configure(menu=me2)
