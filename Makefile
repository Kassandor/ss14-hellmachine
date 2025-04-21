build_win64:
	pyinstaller --name hellmachine_win64 --onefile --windowed --add-data "static/maps:static/maps" main.py

build_linux:
	pyinstaller --name hellmachine_linux_amd64 --onefile --add-data "static/maps:static/maps" main.py