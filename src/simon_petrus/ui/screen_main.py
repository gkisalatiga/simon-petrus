# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/ssynthesia/ghostcity/git-collab/gkisalatiga/simon-petrus/qtdesigner-ui/screen_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(847, 713)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(10, 120, 231, 561))
        self.toolBox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 231, 501))
        self.page.setObjectName("page")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.page)
        self.scrollArea_2.setGeometry(QtCore.QRect(0, 0, 231, 501))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 229, 499))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.cmd_warta = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents_2)
        self.cmd_warta.setGeometry(QtCore.QRect(9, 9, 211, 36))
        self.cmd_warta.setObjectName("cmd_warta")
        self.cmd_liturgi = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents_2)
        self.cmd_liturgi.setGeometry(QtCore.QRect(9, 51, 211, 36))
        self.cmd_liturgi.setObjectName("cmd_liturgi")
        self.cmd_wp_home = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents_2)
        self.cmd_wp_home.setGeometry(QtCore.QRect(9, 93, 211, 36))
        self.cmd_wp_home.setObjectName("cmd_wp_home")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setEnabled(True)
        self.page_2.setGeometry(QtCore.QRect(0, 0, 231, 501))
        self.page_2.setObjectName("page_2")
        self.scrollArea = QtWidgets.QScrollArea(self.page_2)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 231, 501))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -21, 215, 520))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.cmd_carousel = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_carousel.setEnabled(True)
        self.cmd_carousel.setObjectName("cmd_carousel")
        self.verticalLayout.addWidget(self.cmd_carousel)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.commandLinkButton_8 = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton_8.setEnabled(False)
        self.commandLinkButton_8.setObjectName("commandLinkButton_8")
        self.verticalLayout.addWidget(self.commandLinkButton_8)
        self.cmd_agenda = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_agenda.setEnabled(True)
        self.cmd_agenda.setObjectName("cmd_agenda")
        self.verticalLayout.addWidget(self.cmd_agenda)
        self.cmd_persembahan = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_persembahan.setEnabled(True)
        self.cmd_persembahan.setObjectName("cmd_persembahan")
        self.verticalLayout.addWidget(self.cmd_persembahan)
        self.cmd_renungan = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_renungan.setObjectName("cmd_renungan")
        self.verticalLayout.addWidget(self.cmd_renungan)
        self.cmd_formulir = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_formulir.setEnabled(True)
        self.cmd_formulir.setObjectName("cmd_formulir")
        self.verticalLayout.addWidget(self.cmd_formulir)
        self.cmd_gallery = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_gallery.setEnabled(True)
        self.cmd_gallery.setObjectName("cmd_gallery")
        self.verticalLayout.addWidget(self.cmd_gallery)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.commandLinkButton_11 = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton_11.setEnabled(False)
        self.commandLinkButton_11.setObjectName("commandLinkButton_11")
        self.verticalLayout.addWidget(self.commandLinkButton_11)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.commandLinkButton_4 = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.commandLinkButton_4.setEnabled(False)
        self.commandLinkButton_4.setObjectName("commandLinkButton_4")
        self.verticalLayout.addWidget(self.commandLinkButton_4)
        self.cmd_social_media = QtWidgets.QCommandLinkButton(self.scrollAreaWidgetContents)
        self.cmd_social_media.setAutoRepeatDelay(300)
        self.cmd_social_media.setAutoRepeatInterval(100)
        self.cmd_social_media.setAutoDefault(False)
        self.cmd_social_media.setDefault(True)
        self.cmd_social_media.setObjectName("cmd_social_media")
        self.verticalLayout.addWidget(self.cmd_social_media)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.toolBox.addItem(self.page_2, "")
        self.app_title = QtWidgets.QLabel(self.centralwidget)
        self.app_title.setGeometry(QtCore.QRect(10, 10, 591, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.app_title.setFont(font)
        self.app_title.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.app_title.setObjectName("app_title")
        self.app_subtitle = QtWidgets.QLabel(self.centralwidget)
        self.app_subtitle.setGeometry(QtCore.QRect(10, 80, 591, 21))
        font = QtGui.QFont()
        font.setItalic(True)
        self.app_subtitle.setFont(font)
        self.app_subtitle.setObjectName("app_subtitle")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 10, 61, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.btn_sync = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sync.setGeometry(QtCore.QRect(620, 10, 201, 31))
        self.btn_sync.setObjectName("btn_sync")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(250, 120, 581, 561))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.fragment_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.fragment_layout.setContentsMargins(0, 0, 0, 0)
        self.fragment_layout.setObjectName("fragment_layout")
        self.btn_push = QtWidgets.QPushButton(self.centralwidget)
        self.btn_push.setEnabled(True)
        self.btn_push.setGeometry(QtCore.QRect(620, 40, 201, 31))
        self.btn_push.setObjectName("btn_push")
        self.app_subtitle_2 = QtWidgets.QLabel(self.centralwidget)
        self.app_subtitle_2.setGeometry(QtCore.QRect(10, 50, 591, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.app_subtitle_2.setFont(font)
        self.app_subtitle_2.setObjectName("app_subtitle_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName("menubar")
        self.menuBerkas = QtWidgets.QMenu(self.menubar)
        self.menuBerkas.setEnabled(False)
        self.menuBerkas.setObjectName("menuBerkas")
        self.menuAkun = QtWidgets.QMenu(self.menubar)
        self.menuAkun.setObjectName("menuAkun")
        MainWindow.setMenuBar(self.menubar)
        self.actionTentang = QtWidgets.QAction(MainWindow)
        self.actionTentang.setEnabled(True)
        self.actionTentang.setObjectName("actionTentang")
        self.actionBantuan = QtWidgets.QAction(MainWindow)
        self.actionBantuan.setObjectName("actionBantuan")
        self.actionLisensi = QtWidgets.QAction(MainWindow)
        self.actionLisensi.setObjectName("actionLisensi")
        self.actionLog_Masuk = QtWidgets.QAction(MainWindow)
        self.actionLog_Masuk.setObjectName("actionLog_Masuk")
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setObjectName("action_settings")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.actionLog_Pembaruan = QtWidgets.QAction(MainWindow)
        self.actionLog_Pembaruan.setObjectName("actionLog_Pembaruan")
        self.actionGenerate_Secure_Credential = QtWidgets.QAction(MainWindow)
        self.actionGenerate_Secure_Credential.setObjectName("actionGenerate_Secure_Credential")
        self.menuBerkas.addAction(self.actionTentang)
        self.menuBerkas.addAction(self.actionBantuan)
        self.menuBerkas.addAction(self.actionLisensi)
        self.menuBerkas.addAction(self.actionLog_Pembaruan)
        self.menuAkun.addAction(self.action_settings)
        self.menuAkun.addAction(self.action_exit)
        self.menubar.addAction(self.menuAkun.menuAction())
        self.menubar.addAction(self.menuBerkas.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simon Petrus"))
        self.cmd_warta.setText(_translate("MainWindow", "Unggah Warta Jemaat ..."))
        self.cmd_liturgi.setText(_translate("MainWindow", "Unggah Tata Ibadah ..."))
        self.cmd_wp_home.setText(_translate("MainWindow", "Perbarui Halaman Utama ..."))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "GKISalatiga.org (Website)"))
        self.label_2.setText(_translate("MainWindow", "Komedi Putar"))
        self.cmd_carousel.setText(_translate("MainWindow", "Tampilkan Poster ..."))
        self.label_3.setText(_translate("MainWindow", "Menu Utama"))
        self.commandLinkButton_8.setText(_translate("MainWindow", "Warta dan Tata Ibadah"))
        self.cmd_agenda.setText(_translate("MainWindow", "Agenda Sepekan"))
        self.cmd_persembahan.setText(_translate("MainWindow", "Persembahan"))
        self.cmd_renungan.setText(_translate("MainWindow", "Renungan YKB"))
        self.cmd_formulir.setText(_translate("MainWindow", "Formulir"))
        self.cmd_gallery.setText(_translate("MainWindow", "Galeri"))
        self.label_4.setText(_translate("MainWindow", "Layanan YouTube"))
        self.commandLinkButton_11.setText(_translate("MainWindow", "Tampilkan Daftar Putar ..."))
        self.label_5.setText(_translate("MainWindow", "Profil Gereja"))
        self.commandLinkButton_4.setText(_translate("MainWindow", "Konten Profil Gereja"))
        self.cmd_social_media.setText(_translate("MainWindow", "Tautan Sosial Media"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "GKI Salatiga+ (Mobile App)"))
        self.app_title.setText(_translate("MainWindow", "Simon Petrus"))
        self.app_subtitle.setText(_translate("MainWindow", "Komisi Multimedia dan Sarana Prasarana GKI Salatiga"))
        self.label.setText(_translate("MainWindow", "v0.1.7"))
        self.btn_sync.setText(_translate("MainWindow", "🔁    SINKRONISASI DATA"))
        self.btn_push.setText(_translate("MainWindow", "✅    UNGGAH PEMBARUAN"))
        self.app_subtitle_2.setText(_translate("MainWindow", "SISTEM MONITORING DAN PENGELOLAAN DATA TERPADU GKI SALATIGA"))
        self.menuBerkas.setTitle(_translate("MainWindow", "Info"))
        self.menuAkun.setTitle(_translate("MainWindow", "Aplikasi"))
        self.actionTentang.setText(_translate("MainWindow", "Tentang"))
        self.actionBantuan.setText(_translate("MainWindow", "Bantuan"))
        self.actionLisensi.setText(_translate("MainWindow", "Lisensi"))
        self.actionLog_Masuk.setText(_translate("MainWindow", "Log Masuk"))
        self.action_settings.setText(_translate("MainWindow", "Pengaturan"))
        self.action_exit.setText(_translate("MainWindow", "Keluar Aplikasi"))
        self.actionLog_Pembaruan.setText(_translate("MainWindow", "Log Pembaruan"))
        self.actionGenerate_Secure_Credential.setText(_translate("MainWindow", "Generate Secure Credential ..."))
