# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['enter.py'],
             pathex=[
				 'D:\\Projects\\Python\\temp\\.pyenv\\Lib\\site-packages\\', 
				 'D:\\Projects\\Python\\temp\\main',
				 'D:\\Projects\\Python\\temp\\utils\\AiModel',
				 'D:\\Projects\\Python\\temp\\utils\\DataAugmentation',
				 'D:\\Projects\\Python\\temp\\utils\\EasyAuth',
				 'D:\\Projects\\Python\\temp\\utils\\Evaluation',
				 'D:\\Projects\\Python\\temp\\utils\\ModelService',
				 'D:\\Projects\\Python\\temp\\utils\\Others',
				 'D:\\Projects\\Python\\temp\\utils\\Postprocess',
				 'D:\\Projects\\Python\\temp\\utils\\Preprocess',
				 'D:\\Projects\\Python\\temp\\utils\\ProjectUtil',
				 'D:\\Projects\\Python\\temp\\utils\\ResultStorage',
			 ],
             binaries=[],
             datas=[
				('D:\\Projects\\Python\\temp\\sample', 'sample'),
				('D:\\Projects\\Python\\temp\\main\\run_queue.json', 'main'),
				('D:\\Projects\\Python\\temp\\utils\\Preprocess\\normalizeRecord.json', 'utils\\Preprocess'),
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
