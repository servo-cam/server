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
from PySide6.QtWidgets import (QSplitter, QVBoxLayout, QWidget)
from core.ui.source import UISource
from core.ui.menu import UIMenu
from core.ui.footer import UIFooter
from core.ui.dialogs import UIDialogs
from core.ui.output import UIOutput
from core.ui.toolbox import UIToolbox


class UI:
    def __init__(self, window):
        """
        Main UI setup

        :param window: main UI window object
        """
        self.window = window
        self.source = UISource(window)
        self.menu = UIMenu(window)
        self.footer = UIFooter(window)
        self.dialogs = UIDialogs(window)
        self.output = UIOutput(window)
        self.toolbox = UIToolbox(window)

    def setup(self):
        """Setup main UI"""
        # layout elements
        self.window.layout_top = self.source.setup()
        self.window.layout_toolbox = self.toolbox.setup()
        self.window.layout_output = self.output.setup()
        self.window.layout_bottom = self.footer.setup()

        # middle container
        self.window.layout_center = QWidget()

        self.window.layout_center = QSplitter()
        self.window.layout_center.addWidget(self.window.layout_toolbox)
        self.window.layout_center.addWidget(self.window.layout_output)
        self.window.layout_center.setStyleSheet("QSplitter::handle{background-color: #ccc;}")
        self.window.layout_center.setHandleWidth(1)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.window.layout_top)
        splitter.addWidget(self.window.layout_center)
        splitter.addWidget(self.window.layout_bottom)
        splitter.setStyleSheet("QSplitter::handle{background-color: #ccc;}")
        splitter.setHandleWidth(1)

        # main layout
        self.window.layout = QVBoxLayout()
        self.window.layout.addWidget(splitter)

        # clients list
        self.toolbox.remote.setup()

        # dialogs
        self.dialogs.setup()

        # main container
        self.window.main_widget = QWidget()
        self.window.main_widget.setLayout(self.window.layout)
        self.window.setCentralWidget(self.window.main_widget)

        # main menu
        self.menu.setup()
