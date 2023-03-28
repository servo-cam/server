#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QVBoxLayout, QTextEdit, QPlainTextEdit, QWidget)
from core.utils import trans
from core.ui.style import Style


class UIFooter:
    def __init__(self, window=None):
        """
        Footer UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup footer

        :return: QWidget
        """
        console = self.setup_console()
        status = self.setup_remote_status()
        summary = self.setup_summary()
        indicators = self.setup_indicators()

        layout = QHBoxLayout()
        layout.addWidget(summary)
        layout.addLayout(console)
        layout.addLayout(indicators)

        self.window.footer_widget = QWidget()
        self.window.footer_widget.setLayout(layout)
        self.window.footer_widget.setMinimumSize(Style.FOOTER_MIN_WIDTH, Style.FOOTER_HEIGHT)
        self.window.footer_widget.setMaximumHeight(Style.FOOTER_HEIGHT)

        return self.window.footer_widget

    def setup_console(self):
        """
        Setup bottom console

        :return: QVBoxLayout
        """
        font = QFont()
        font.setPointSize(8)
        self.window.console = QPlainTextEdit()
        self.window.console.setFont(font)
        self.window.console.setReadOnly(True)
        self.window.console.setMaximumBlockCount(100)

        layout = QVBoxLayout()
        layout.addWidget(self.window.console)

        return layout

    def setup_remote_status(self):
        """
        Setup remote status

        :return: QVBoxLayout
        """
        self.window.remote_status = QTextEdit()
        self.window.remote_status.setFont(Style.FONT_CONSOLE)
        self.window.remote_status.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(trans("label.remote_status")))
        layout.addWidget(self.window.remote_status)

        return layout

    def setup_summary(self):
        """
        Setup bottom summary

        :return: QVBoxLayout
        """
        self.window.status_label = {}

        # status
        self.window.status_label['state'] = QLabel("SEARCHING")
        self.window.status_label['counter'] = QLabel("0")
        self.window.status_label['angle'] = QLabel("-")
        self.window.status_label['cmd'] = QLabel("-")

        self.window.status_label['state'].setFont(Style.FONT_CONSOLE)
        self.window.status_label['counter'].setFont(Style.FONT_CONSOLE)
        self.window.status_label['angle'].setFont(Style.FONT_CONSOLE)
        self.window.status_label['cmd'].setFont(Style.FONT_CONSOLE)

        self.window.status_label['state'].setMinimumWidth(Style.FOOTER_STATUS_MIN_WIDTH)
        self.window.status_label['counter'].setMinimumWidth(Style.FOOTER_STATUS_MIN_WIDTH)
        self.window.status_label['cmd'].setMinimumWidth(Style.FOOTER_STATUS_MIN_WIDTH)

        # summary, cmd, objects
        layout = QVBoxLayout()
        layout.addWidget(self.window.status_label['state'])
        layout.addWidget(self.window.status_label['counter'])
        layout.addWidget(self.window.status_label['angle'])
        layout.addWidget(self.window.status_label['cmd'])

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_indicators(self):
        """
        Setup bottom indicators

        :return: QVBoxLayout
        """
        self.window.status_indicator = {}

        # indicators
        self.window.status_indicator['video'] = QPushButton("VIDEO")
        self.window.status_indicator['cmd_send'] = QPushButton("SCK SEND")
        self.window.status_indicator['cmd_recv'] = QPushButton("SCK RECV")
        self.window.status_indicator['ser_send'] = QPushButton("SER SEND")
        self.window.status_indicator['ser_recv'] = QPushButton("SER RECV")

        self.window.status_indicator['video'].setStyleSheet(Style.BADGE_DEFAULT)
        self.window.status_indicator['cmd_send'].setStyleSheet(Style.BADGE_DEFAULT)
        self.window.status_indicator['cmd_recv'].setStyleSheet(Style.BADGE_DEFAULT)
        self.window.status_indicator['ser_send'].setStyleSheet(Style.BADGE_DEFAULT)
        self.window.status_indicator['ser_recv'].setStyleSheet(Style.BADGE_DEFAULT)

        self.window.status_indicator['video'].setFont(Style.FONT_CONSOLE)
        self.window.status_indicator['cmd_send'].setFont(Style.FONT_CONSOLE)
        self.window.status_indicator['cmd_recv'].setFont(Style.FONT_CONSOLE)
        self.window.status_indicator['ser_send'].setFont(Style.FONT_CONSOLE)
        self.window.status_indicator['ser_recv'].setFont(Style.FONT_CONSOLE)

        layout = QVBoxLayout()
        layout.addWidget(self.window.status_indicator['video'])
        layout.addWidget(self.window.status_indicator['cmd_send'])
        layout.addWidget(self.window.status_indicator['cmd_recv'])
        layout.addWidget(self.window.status_indicator['ser_send'])
        layout.addWidget(self.window.status_indicator['ser_recv'])

        return layout
