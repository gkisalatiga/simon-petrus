"""
Simon Petrus
AGPL-3.0-licensed
Copyright (C) GKI Salatiga 2024
Written by Samarthya Lykamanuella (github.com/groaking)
"""

from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from ui import dialog_static_content


class DialogStaticContent(QtWidgets.QDialog, dialog_static_content.Ui_Dialog):
    def __init__(self, *args, obj=None, title='', **kwargs):
        super(DialogStaticContent, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Prevent resizing. [10]
        self.setFixedSize(self.size())

        # Input fields validation.
        self.field_title.textChanged.connect(self.validate_fields)
        self.field_subtitle.textChanged.connect(self.validate_fields)
        self.field_url.textChanged.connect(self.validate_fields)
        self.editor_main.textChanged.connect(self.on_editor_main_changed)
        self.chk_autorender.stateChanged.connect(self.on_chk_autorender_changed)

        # Enable JavaScript rendering.
        self.webview_main.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

    @pyqtSlot()
    def on_btn_render_clicked(self):
        self.render_html()

    @pyqtSlot()
    def on_chk_autorender_changed(self):
        autorender_on = self.findChild(QtWidgets.QCheckBox, 'chk_autorender').isChecked()
        if autorender_on:
            self.findChild(QtWidgets.QPushButton, 'btn_render').setEnabled(False)
        else:
            self.findChild(QtWidgets.QPushButton, 'btn_render').setEnabled(True)

    @pyqtSlot()
    def on_editor_main_changed(self):
        autorender_on = self.findChild(QtWidgets.QCheckBox, 'chk_autorender').isChecked()
        if autorender_on:
            self.render_html()

        # What is certain is that we always validate fields upon text change.
        self.validate_fields()

    @pyqtSlot()
    def render_html(self):
        html_content = self.findChild(QtWidgets.QPlainTextEdit, 'editor_main').toPlainText()
        self.webview_main.setHtml(html_content)

    def validate_fields(self):
        title = self.findChild(QtWidgets.QLineEdit, 'field_title').text().strip()
        subtitle = self.findChild(QtWidgets.QLineEdit, 'field_subtitle').text().strip()
        url = self.findChild(QtWidgets.QLineEdit, 'field_url').text().strip()
        html = self.findChild(QtWidgets.QPlainTextEdit, 'editor_main').toPlainText().strip()

        if title == '' or url == '' or html == '':
            self.findChild(QtWidgets.QLabel, 'label_status').setText('Anda harus memasukkan judul, tautan gambar, dan konten HTML!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        elif not url.startswith('http') or not url.__contains__('://'):
            self.findChild(QtWidgets.QLabel, 'label_status').setText('URL Anda harus dimulai dengan "http://" atau "https://"!')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(False)
        else:
            self.findChild(QtWidgets.QLabel, 'label_status').setText('-')
            self.findChild(QtWidgets.QDialogButtonBox, 'button_box').buttons()[0].setEnabled(True)
