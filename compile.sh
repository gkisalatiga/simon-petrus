#!/bin/sh
# Compile Simon Petrus into a Linux executable

# SPEC file generator.
# pyinstaller src/simon_petrus/main.py --paths src/simon_petrus/ --add-data "src/simon_petrus/assets/loading_animation.gif:assets" --clean --log-level INFO --onefile --windowed --name simon-petrus-v0.1.1-pyinstaller-linux

pyinstaller simon-petrus-v0.1.1-pyinstaller-linux.spec
