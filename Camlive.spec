# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/issrael BOCO/Desktop/ISRAEL/Projet/camaraLive/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/issrael BOCO/Desktop/ISRAEL/Projet/camaraLive/studio', 'studio/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Camlive',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\issrael BOCO\\Downloads\\Logo-500x500-px-_1_.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Camlive',
)
