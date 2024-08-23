# Simon Petrus Changelog

## v0.3.1 (14) --- 2024-08-23

- New: Added "static content" (church profile content) editor

## v0.3.0 (13) --- 2024-08-20

- New: Added the dashboard menu to add and manage YouTube playlists of GKI Salatiga+
- New: Added the flag to fetch more than 100 Google Drive photos in GKI Salatiga+ gallery menu
- New: Added license and changelog info dialog
- Improved: You can now decrypt credentials by pressing the "enter/return" key
- Fix: Uploading the JSON data does not commit the latest update on first launch
- Fix: Fixed Google Drive OAUTH2.0 token expires after 50 API calls
- Fix: Fixed loading animation screen does not close during sync and fetch due to lost internet

## v0.2.0 (12) --- 2024-08-17

- Info: Switched dependency from "pyargon2" to "argon2-cffi"
- Info: Switched dependency from "python-magic" to "filetype"
- New: Introduced the `global_schema` file that handles all app-wide global variable assignments and storage
- Improved: Splitted screen, frame, and dialog classes in `main.py` to individual class files under `handler` folder
- Fix: Fixed module dependency so that the source is pyinstaller-compilable on Windows without Visual C++ 14.0 requirement
- Fix: Fixed API key error not detected when attempting to git-push the change

## v0.1.7 (11) --- 2024-08-15

- New: Added the gallery interface for uploading photo albums
- Fix: Fixed typos on the use of hypens

## v0.1.6 (10) --- 2024-08-14

- New: Added carousel poster banner uploader and editor
- New: Added the interface to update agenda data
- Fix: Fixed carousel not preserving banner order

## v0.1.5 (9) --- 2024-08-13

- New: Added QRIS code image updater
- New: Added offertories bank transfer destination updater

## v0.1.4 (8) --- 2024-08-12

- New: Added forms data editor

## v0.1.3 (7) --- 2024-08-11

- Improved: Now using CalendarWidget instead of date line input when uploading Warta and Liturgi

## v0.1.2 (6) --- 2024-08-11

- New: Added configuration and common settings window
- New: Composed the GitHub pusher for GKI Salatiga+ JSON schema
- Fix: (Minor) Disabled window/screen resizing

## v0.1.1 (5) --- 2024-08-10

- Info: Changed PDF thumbnail generator dependency from "pdf2image" to "fitz" (PyMuPDF) to allow PDF rasterization without external binary install

## v0.1.0 (4) --- 2024-08-10

- Info: This is the first compilation attempt of the app into executable binaries
- New: Added the WordPress homepage updater of GKISalatiga.org
- Fix: Fixed segmentation fault when updating the loading progress bar

## v0.0.3 (3) --- 2024-08-09

- New: Added loading window during uploads and most other operations
- Improved: The Qt main window no longer freezes during operations

## v0.0.2 (2) --- 2024-08-09

- New: Added "Warta Jemaat" and "Tata Ibadah" automatic uploader

## v0.0.1 (1) --- 2024-08-07

- New: Added the app's credential generator
- New: Added the backend to save preferences and JSON schema
- New: Created the mechanism to read the encrypted credential
- New: Created screens: Renungan YKB and Social Media
