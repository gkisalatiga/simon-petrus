#!/bin/sh
# Compile Simon Petrus into a Linux executable
pyinstaller src/simon_petrus/main.py --paths src/simon_petrus/ --add-data "src/simon_petrus/assets/loading_animation.gif:assets" --clean --log-level INFO --onefile --windowed --name simon-petrus-v0.1.0-pyinstaller-linux
