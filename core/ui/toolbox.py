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
from PySide6.QtWidgets import QSplitter
from core.ui.remote import UIRemote
from core.ui.controls import UIControls
from core.ui.status import UIStatus
from core.ui.style import Style


class UIToolbox:
    def __init__(self, window=None):
        """
        Toolbox UI setup

        :param window: main UI window object
        """
        self.window = window
        self.ui_controls = UIControls(window)
        self.ui_status = UIStatus(window)
        self.remote = UIRemote(window)

    def setup(self):
        """
        Setup left toolbox with tabs

        :return: QWidget
        """
        remote = self.remote.setup_tabs()
        controls = self.ui_controls.setup()

        remote.setMaximumWidth(Style.TOOLBOX_WIDTH)
        controls.setMaximumWidth(Style.TOOLBOX_WIDTH)

        widget = QSplitter(Qt.Vertical)
        widget.addWidget(remote)
        widget.addWidget(controls)
        widget.setStyleSheet("QSplitter::handle{background-color: #ccc;}")
        widget.setHandleWidth(1)

        return widget
