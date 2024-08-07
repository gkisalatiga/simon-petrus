#!/bin/sh
# AGPL-3.0-licensed
# Copyright (C) GKI Salatiga 2024
# Written by Samarthya Lykamanuella (github.com/groaking)
# ---
# This script automatically converts each UI file (created using QtDesigner)
# under the folder ./qtdesigner-ui into python files.

# Please change the "base" folder to the folder path wherein you clone this repo.
base="/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus"
base_ui="$base/qtdesigner-ui"
base_exported="$base/src/simon_petrus/ui"

# Export the UI files (main app)
ls $base_ui | while read -r l; do
    exported_python_name=$(echo $l | sed -e 's/\.ui$/\.py/g')
    echo "Converting $l --> $exported_python_name"
    /bin/pyuic5 "$base_ui/$l" -o "$base_exported/$exported_python_name"
done
