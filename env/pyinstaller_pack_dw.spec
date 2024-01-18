# -*- mode: python -*-

block_cipher = None


a = Analysis(['..\\src\\main.py',
              '..\\src\\win\\faTesterWin.py',
              '..\\src\\ui\\uicore.py',
              '..\\src\\ui\\uidef.py',
              '..\\src\\ui\\uilang.py',
              '..\\src\\ui\\uivar.py',],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MCU-FATestSuite',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MCU-FATestSuite')
