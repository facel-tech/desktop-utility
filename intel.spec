# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
import PyInstaller.config

PyInstaller.config.CONF['distpath'] = "./dist/dmg"

block_cipher = None
hidden_total = collect_submodules('PyQT6.sip') + ['PyQT6.sip']

a = Analysis(
    ['main.py'],
    pathex=['venv/lib/python3.8/site-packages'],
    binaries=[],
    datas=[('favicon_sad.icns', '.')],
    hiddenimports=hidden_total,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Facel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Facel',
)
app = BUNDLE(
    coll,
    name='Facel.app',
    icon="favicon_happy.icns",
    bundle_identifier="tech.facel.desktop",
    info_plist={
        'LSUIElement': True
    }
)
