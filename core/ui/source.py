#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QWidget, QComboBox)
from core.utils import trans
from core.ui.style import Style
from core.ui.widgets import AddressInput


class UISource:
    def __init__(self, window=None):
        """
        Source UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup source selection

        :return: QWidget
        """
        buttons = self.setup_source_buttons()
        self.setup_camera_select()
        address = self.setup_address()

        # source layout
        layout = QHBoxLayout()
        layout.addWidget(buttons)
        layout.addLayout(address)

        self.window.source_widget = QWidget()
        self.window.source_widget.setLayout(layout)

        return self.window.source_widget

    def setup_source_buttons(self):
        """
        Setup source buttons

        :return: QWidget
        """
        self.window.source_btn = {}
        self.window.source_btn[self.window.tracker.SOURCE_LOCAL] = QPushButton(trans("btn.source.local"))
        self.window.source_btn[self.window.tracker.SOURCE_REMOTE] = QPushButton(trans("btn.source.remote"))
        self.window.source_btn[self.window.tracker.SOURCE_VIDEO] = QPushButton(trans("btn.source.video"))
        self.window.source_btn[self.window.tracker.SOURCE_STREAM] = QPushButton(trans("btn.source.stream"))

        self.window.source_btn[self.window.tracker.SOURCE_LOCAL].clicked.connect(
            lambda: self.window.tracker.controller.source.toggle(self.window.tracker.SOURCE_LOCAL))
        self.window.source_btn[self.window.tracker.SOURCE_REMOTE].clicked.connect(
            lambda: self.window.tracker.controller.source.toggle(self.window.tracker.SOURCE_REMOTE))
        self.window.source_btn[self.window.tracker.SOURCE_VIDEO].clicked.connect(
            lambda: self.window.tracker.controller.source.toggle(self.window.tracker.SOURCE_VIDEO))
        self.window.source_btn[self.window.tracker.SOURCE_STREAM].clicked.connect(
            lambda: self.window.tracker.controller.source.toggle(self.window.tracker.SOURCE_STREAM))

        layout = QHBoxLayout()
        layout.addWidget(self.window.source_btn[self.window.tracker.SOURCE_LOCAL])
        layout.addWidget(self.window.source_btn[self.window.tracker.SOURCE_REMOTE])
        layout.addWidget(self.window.source_btn[self.window.tracker.SOURCE_VIDEO])
        layout.addWidget(self.window.source_btn[self.window.tracker.SOURCE_STREAM])

        widget = QWidget()
        widget.setLayout(layout)
        widget.setMaximumWidth(Style.SOURCE_BUTTONS_MAX_WIDTH)

        return widget

    def setup_address(self):
        """
        Setup source address input

        :return: QHBoxLayout
        """
        self.window.source_address = AddressInput(self.window)
        self.window.source_address.setMinimumSize(Style.SOURCE_ADDRESS_MIN_WIDTH, 0)
        self.window.source_address.setText(self.window.tracker.video_url)
        self.window.source_browse_btn = QPushButton(trans("btn.source.address.browse"))
        self.window.source_browse_btn.clicked.connect(
            lambda: self.window.tracker.controller.source.browse())
        self.window.source_load_btn = QPushButton(trans("btn.source.address.load"))
        self.window.source_load_btn.clicked.connect(
            lambda: self.window.tracker.controller.source.load(self.window.source_address.text()))

        # resource label
        self.window.source_address_prefix = QLabel(trans("label.source.address"))
        self.window.source_address_prefix.setMaximumWidth(200)

        layout = QHBoxLayout()
        layout.addWidget(self.window.source_address_prefix)
        layout.addWidget(self.window.source_camera_local)
        layout.addWidget(self.window.source_address)
        layout.addWidget(self.window.source_browse_btn)
        layout.addWidget(self.window.source_load_btn)

        return layout

    def setup_camera_select(self):
        """Setup camera select"""
        self.window.source_camera_local = QComboBox()
        self.window.tracker.controller.camera.reload_indexes()

        self.window.source_camera_local.currentIndexChanged.connect(
            lambda: self.window.tracker.controller.camera.toggle(self.window.source_camera_local.currentIndex()))

        # hide camera select on startup
        self.window.source_camera_local.setHidden(True)
