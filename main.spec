# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/issrael BOCO/Desktop/ISRAEL/Projet/camaraLive/main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/issrael BOCO/Desktop/ISRAEL/Projet/camaraLive/studio/view/kv/main.kv', 'studio/view/kv/main.kv')],
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
