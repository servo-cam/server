# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['app.py'],
    pathex=[
        '.'
    ],
    binaries=[],
    datas=[
        ('model/movenet_multi_pose_lightning_1', 'model/movenet_multi_pose_lightning_1'),
        ('model/movenet_single_pose_lightning_4', 'model/movenet_single_pose_lightning_4'),
        ('model/movenet_single_pose_thunder_4', 'model/movenet_single_pose_thunder_4'),
        ('model/ssd_mobilenet_2', 'model/ssd_mobilenet_2'),
        ('assets/logo.png', 'assets'), 
        ('assets/icon.ico', 'assets'),
        ('assets/servo_axes.png', 'assets'),
        ('assets/defaults/*', 'assets/defaults'),
        ('locale/*', 'locale'), 
        ('config.ini', '.'),
        ('hosts.txt', '.'),
        ('streams.txt', '.'),
        ('CHANGELOG.txt', '.'),
        ('__init__.py', '.')
    ],
    hiddenimports=['core', 'video_filter', 'wrapper'],
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
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='./assets/icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Linux',
)
