# -*- mode: python ; coding: utf-8 -*-

import sys

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'], 
    binaries=[],
    datas=[
        ('assets/*', 'assets'),
    ],
    hiddenimports=['pandas', 'PySide6'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if sys.platform == 'darwin':
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name='lumber-jills-tip-calculator',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        icon='assets/lumberjillslogo.icns',
    )
    app = BUNDLE(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        name="Lumber Jill's Tip Calculator.app",
        icon='assets/lumberjillslogo.icns',
        bundle_identifier='com.yourname.lumber-jills-tip-calculator',
    )
else:
    try:
        exe = EXE(
            pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name='lumber-jills-tip-calculator',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=False,
            icon='assets/lumberjillslogo.png',
        )
    except:
        exe = EXE(
            pyz,
            a.scripts,
            [],
            exclude_binaries=True,
            name='lumber-jills-tip-calculator',
            debug=False,
            bootloader_ignore_signals=False,
            strip=False,
            upx=True,
            console=False,
            icon='assets/lumberjillslogo.png',
        )
    finally:
        coll = COLLECT(
            exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name='lumber-jills-tip-calculator',
        )