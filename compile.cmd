pyinstaller main.py ^
--clean ^
--log-level INFO ^
--onefile ^
--windowed ^
--paths src/simon_petrus/ ^
--add-data "src/simon_petrus/assets/loading_animation.gif;assets" ^
--name simon-petrus-v0.1.1-pyinstaller-windows
