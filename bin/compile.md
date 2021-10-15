## compile with pyinstaller
```shell
python -m PyInstaller --onefile --noconfirm --noconsole --uac-admin --specpath bin\spec --distpath bin\dist --workpath bin\build --name fix_windows_file_explorer fix_windows_file_explorer.py
```