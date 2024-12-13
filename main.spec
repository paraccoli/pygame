# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('config.py', '.'),
        ('dialogue_manager.py', '.'),
        ('episode0.py', '.'),
        ('episode0_0.py', '.'),
        ('episode1.py', '.'),
        ('field_create.py', '.'),
        ('field_create_view.py', '.'),
        ('game_logic.py', '.'),
        ('open_world.py', '.'),
        ('player_data.py', '.'),
        ('save_manager.py', '.'),
        ('settings.py', '.'),
        ('variables.py', '.'),
        ('save/*', 'save'),
        ('characters/icons/*', 'characters/icons'),
        ('maps/*', 'maps'),
        ('music/*', 'music'),
        ('Texture/*', 'Texture'),
        ('font/*', 'font'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
