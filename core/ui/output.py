#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTabWidget
from core.utils import trans
from core.ui.widgets import VideoLabel, VideoContainer


class UIOutput:

    def __init__(self, window=None):
        """
        Output UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup output video tab

        :return: QTabWidget
        """
        self.window.tabs = QTabWidget()

        # video output
        self.window.output = VideoLabel("", self.window)
        self.window.output.setAlignment(Qt.AlignCenter)
        self.window.output.setStyleSheet("background-color: #000000;")

        self.window.montage = VideoLabel("", self.window)
        self.window.montage.setAlignment(Qt.AlignCenter)
        self.window.montage.setStyleSheet("background-color: #000000;")

        self.window.container_video = VideoContainer(self.window)
        self.window.container_video.setWidget(self.window.output)

        self.window.container_montage = VideoContainer(self.window)
        self.window.container_montage.setWidget(self.window.montage)

        self.window.tabs.addTab(self.window.container_video, trans("tab.output.title"))
        self.window.tabs.addTab(self.window.container_montage, trans("tab.output.montage"))
        # self.window.tabs.setBackgroundRole(QPalette.Dark)
        return self.window.tabs
