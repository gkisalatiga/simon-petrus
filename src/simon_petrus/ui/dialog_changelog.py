# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/dialog_changelog.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(650, 531)
        self.app_title = QtWidgets.QLabel(Dialog)
        self.app_title.setGeometry(QtCore.QRect(10, 10, 391, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title.setObjectName("app_title")
        self.app_title_2 = QtWidgets.QLabel(Dialog)
        self.app_title_2.setGeometry(QtCore.QRect(10, 40, 391, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.app_title_2.setFont(font)
        self.app_title_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title_2.setObjectName("app_title_2")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 631, 411))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 615, 1237))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.app_caption = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.app_caption.setFont(font)
        self.app_caption.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.app_caption.setWordWrap(True)
        self.app_caption.setObjectName("app_caption")
        self.horizontalLayout.addWidget(self.app_caption)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.btn_close = QtWidgets.QPushButton(Dialog)
        self.btn_close.setGeometry(QtCore.QRect(10, 490, 111, 31))
        self.btn_close.setObjectName("btn_close")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Simon Petrus Changelog"))
        self.app_title.setText(_translate("Dialog", "CHANGELOG"))
        self.app_title_2.setText(_translate("Dialog", "Simon Petrus v0.3.2 build 15 - August 2024"))
        self.app_caption.setText(_translate("Dialog", "# Simon Petrus Changelog\n"
"\n"
"## v0.3.2 (15) --- 2024-09-13\n"
"\n"
"- Fix: Fixed cannot parse unicode characters in the JSON files\n"
"\n"
"## v0.3.1 (14) --- 2024-08-23\n"
"\n"
"- New: Added \"static content\" (church profile content) editor\n"
"\n"
"## v0.3.0 (13) --- 2024-08-20\n"
"\n"
"- New: Added the dashboard menu to add and manage YouTube playlists of GKI Salatiga+\n"
"- New: Added the flag to fetch more than 100 Google Drive photos in GKI Salatiga+ gallery menu\n"
"- New: Added license and changelog info dialog\n"
"- Improved: You can now decrypt credentials by pressing the \"enter/return\" key\n"
"- Fix: Uploading the JSON data does not commit the latest update on first launch\n"
"- Fix: Fixed Google Drive OAUTH2.0 token expires after 50 API calls\n"
"- Fix: Fixed loading animation screen does not close during sync and fetch due to lost internet\n"
"\n"
"## v0.2.0 (12) --- 2024-08-17\n"
"\n"
"- Info: Switched dependency from \"pyargon2\" to \"argon2-cffi\"\n"
"- Info: Switched dependency from \"python-magic\" to \"filetype\"\n"
"- New: Introduced the `global_schema` file that handles all app-wide global variable assignments and storage\n"
"- Improved: Splitted screen, frame, and dialog classes in `main.py` to individual class files under `handler` folder\n"
"- Fix: Fixed module dependency so that the source is pyinstaller-compilable on Windows without Visual C++ 14.0 requirement\n"
"- Fix: Fixed API key error not detected when attempting to git-push the change\n"
"\n"
"## v0.1.7 (11) --- 2024-08-15\n"
"\n"
"- New: Added the gallery interface for uploading photo albums\n"
"- Fix: Fixed typos on the use of hypens\n"
"\n"
"## v0.1.6 (10) --- 2024-08-14\n"
"\n"
"- New: Added carousel poster banner uploader and editor\n"
"- New: Added the interface to update agenda data\n"
"- Fix: Fixed carousel not preserving banner order\n"
"\n"
"## v0.1.5 (9) --- 2024-08-13\n"
"\n"
"- New: Added QRIS code image updater\n"
"- New: Added offertories bank transfer destination updater\n"
"\n"
"## v0.1.4 (8) --- 2024-08-12\n"
"\n"
"- New: Added forms data editor\n"
"\n"
"## v0.1.3 (7) --- 2024-08-11\n"
"\n"
"- Improved: Now using CalendarWidget instead of date line input when uploading Warta and Liturgi\n"
"\n"
"## v0.1.2 (6) --- 2024-08-11\n"
"\n"
"- New: Added configuration and common settings window\n"
"- New: Composed the GitHub pusher for GKI Salatiga+ JSON schema\n"
"- Fix: (Minor) Disabled window/screen resizing\n"
"\n"
"## v0.1.1 (5) --- 2024-08-10\n"
"\n"
"- Info: Changed PDF thumbnail generator dependency from \"pdf2image\" to \"fitz\" (PyMuPDF) to allow PDF rasterization without external binary install\n"
"\n"
"## v0.1.0 (4) --- 2024-08-10\n"
"\n"
"- Info: This is the first compilation attempt of the app into executable binaries\n"
"- New: Added the WordPress homepage updater of GKISalatiga.org\n"
"- Fix: Fixed segmentation fault when updating the loading progress bar\n"
"\n"
"## v0.0.3 (3) --- 2024-08-09\n"
"\n"
"- New: Added loading window during uploads and most other operations\n"
"- Improved: The Qt main window no longer freezes during operations\n"
"\n"
"## v0.0.2 (2) --- 2024-08-09\n"
"\n"
"- New: Added \"Warta Jemaat\" and \"Tata Ibadah\" automatic uploader\n"
"\n"
"## v0.0.1 (1) --- 2024-08-07\n"
"\n"
"- New: Added the app\'s credential generator\n"
"- New: Added the backend to save preferences and JSON schema\n"
"- New: Created the mechanism to read the encrypted credential\n"
"- New: Created screens: Renungan YKB and Social Media\n"
""))
        self.btn_close.setText(_translate("Dialog", "CLOSE"))
