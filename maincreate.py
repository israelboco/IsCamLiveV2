import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onedir',
    '--windowed',
    '-n Camlive',
])

# pyinstaller --noconfirm --onefile --windowed -n "Camlive" --icon "C:/Users/issrael BOCO/Desktop/ISRAEL/Projet/camaraLive/studio/asset/Logo.ico" --add-data "C:/Users/issrael BOCO/Desktop/ISRAEL/Projet/camaraLive/studio;studio/"  "main.py"