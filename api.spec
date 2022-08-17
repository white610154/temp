# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['enter.py'],
             pathex=[
				 'C:\\Users\\LEADTEK\\anaconda3\\envs\\sala\\Lib\\site-packages\\', 
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\main',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\AiModel',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\DataAugmentation',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\EasyAuth',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\Evaluation',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\ModelService',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\Others',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\Postprocess',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\Preprocess',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\ProjectUtil',
				 'C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\ResultStorage',
			 ],
             binaries=[],
             datas=[
				('C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\sample', 'sample'),
				('C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\main\\run_queue.json', 'main'),
				('C:\\Users\\LEADTEK\\Desktop\\SALA\\temp\\utils\\Preprocess\\normalizeRecord.json', 'utils\\Preprocess'),
			 ],
             hiddenimports=['intel-openmp'],
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
          name='api',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          icon='AULOGO.ico', 
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='api')
