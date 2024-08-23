#!/bin/sh
# Compile Simon Petrus into a Linux executable

# The compiled binary name.
target_bin_name="simon-petrus-v0.3.1-pyinstaller-linux"

# SPEC file generator.
pyinstaller src/simon_petrus/main.py \
--paths src/simon_petrus/ \
--add-data "src/simon_petrus/assets/loading_animation.gif:assets" \
--clean \
--log-level INFO \
--onefile \
--windowed \
--name "$target_bin_name"

# Using generated SPEC file.
# pyinstaller "$target_bin_name".spec
