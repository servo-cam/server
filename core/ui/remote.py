#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtWidgets import QTabWidget
from core.ui.remote_clients import UIRemoteClients
from core.ui.remote_streams import UIRemoteStreams


class UIRemote:
    def __init__(self, window=None):
        """
        Remote UI setup

        :param window: main UI window object
        """
        self.window = window
        self.clients = UIRemoteClients(self.window)
        self.streams = UIRemoteStreams(self.window)

    def setup(self):
        """Setup remote tab"""
        self.clients.setup()
        self.streams.setup()

    def update(self):
        """Update remote tab"""
        self.clients.update()
        self.streams.update()

    def setup_tabs(self):
        """
        Setup remote tabs

        :return: QTabWidget
        """
        self.window.remote_tabs = QTabWidget()
        self.window.remote = {}

        ip = self.clients.setup_list()
        stream = self.streams.setup_list()

        self.window.remote_tabs.addTab(ip, "IP")
        self.window.remote_tabs.addTab(stream, "Stream")

        return self.window.remote_tabs
