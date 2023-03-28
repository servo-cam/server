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
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QVBoxLayout,
                               QWidget, QSlider)
from core.utils import trans


class UIControlVideo:
    def __init__(self, window=None):
        """
        Video control UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup video control

        :return: QWidget
        """
        controls = self.setup_video()

        layout = QHBoxLayout()
        layout.addWidget(controls)

        # container
        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_video(self):
        """
        Setup video control

        :return: QWidget
        """
        self.window.control_video = {}

        self.window.control_video['label_time'] = QLabel('00:00:00')
        self.window.control_video['label_frame'] = QLabel('0')
        self.window.control_video['label_fps'] = QLabel('0')
        self.window.control_video['label_resolution'] = QLabel('')

        self.window.control_video['seek'] = QSlider(Qt.Horizontal)
        self.window.control_video['seek'].sliderPressed.connect(
            lambda: self.window.tracker.controller.video.start_seek())
        self.window.control_video['seek'].sliderReleased.connect(
            lambda: self.window.tracker.controller.video.stop_seek())

        btns = {}
        btns['pause'] = QPushButton(trans('video.control.pause'))
        btns['pause'].clicked.connect(
            lambda: self.window.tracker.controller.video.pause())
        btns['play'] = QPushButton(trans('video.control.play'))
        btns['play'].clicked.connect(
            lambda: self.window.tracker.controller.video.play())

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(btns['play'])
        btns_layout.addWidget(btns['pause'])

        layout = QVBoxLayout()
        layout.addWidget(self.window.control_video['label_resolution'])
        layout.addWidget(self.window.control_video['label_fps'])
        layout.addWidget(self.window.control_video['label_frame'])
        layout.addWidget(self.window.control_video['label_time'])
        layout.addWidget(self.window.control_video['seek'])
        layout.addLayout(btns_layout)

        widget = QWidget()
        widget.setLayout(layout)

        return widget
