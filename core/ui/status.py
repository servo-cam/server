#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtWidgets import (QLabel, QVBoxLayout, QTreeView)
from core.utils import trans


class UIStatus:
    REMOTE_IP, REMOTE_HOST, REMOTE_TIME = range(3)

    def __init__(self, window=None):
        """
        Status UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup status

        :return: QTreeView
        """
        self.window.status_text = QTreeView()
        self.window.status_text.setRootIsDecorated(False)
        self.window.status_text.setAlternatingRowColors(True)
        self.window.status_text.setMinimumSize(200, 100)
        self.window.status_text.setMaximumHeight(100)

        status_box = QVBoxLayout()
        status_box.addWidget(QLabel(trans("label.status")))
        status_box.addWidget(self.window.status_text)

        return status_box

    def show_message(self, message):
        """
        Show message in status bar

        :param message: message to show
        """
        self.window.statusBar().showMessage(message, 5000)
