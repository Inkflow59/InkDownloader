# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('resources/icon.ico', 'resources')],  # Inclure l'icône dans le build
    hiddenimports=['packaging.version', 'packaging.specifiers', 'packaging.requirements'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='InkDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico',
    # Ajout des métadonnées de l'application
    version='file_version_info.txt',
    file_description='InkDownloader - A YouTube Video Downloader',
    company_name='InkFlow59',
    product_name='InkDownloader',
    copyright='MIT License',
    trademarks='InkDownloader'
)