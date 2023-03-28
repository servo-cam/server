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
from PySide6.QtGui import QStandardItemModel
from core.utils import trans
from core.ui.widgets import ClientsMenu


class UIRemoteClients:
    REMOTE_HOST, REMOTE_IP, REMOTE_TIME, REMOTE_STATUS, REMOTE_PING = range(5)  # list columns

    def __init__(self, window=None):
        """
        Remote clients UI setup

        :param window: main UI window object
        """
        self.window = window
        self.idx = 0
        self.model = None
        self.count = 0
        self.initialized = False

    def setup_list(self):
        """
        Setup remote clients list

        :return: QTreeView
        """
        # remote devices list
        self.window.clients = ClientsMenu(self.window)
        self.window.clients.setMinimumHeight(140)
        self.window.clients.setAlternatingRowColors(True)
        self.window.clients.setIndentation(0)
        # self.window.devices_list.setFont(FONT_CONSOLE)
        return self.window.clients

    def setup(self):
        """Setup remote clients model"""
        self.model = self.create_model(self.window)

    def create_model(self, parent):
        """
        Create clients list model
        :param parent: parent widget
        :return: QStandardItemModel
        """
        model = QStandardItemModel(0, 5, parent)
        model.setHeaderData(self.REMOTE_HOST, Qt.Horizontal, trans("list.clients.host"))
        model.setHeaderData(self.REMOTE_IP, Qt.Horizontal, trans("list.clients.ip"))
        model.setHeaderData(self.REMOTE_TIME, Qt.Horizontal, trans("list.clients.time"))
        model.setHeaderData(self.REMOTE_STATUS, Qt.Horizontal, trans("list.clients.status"))
        model.setHeaderData(self.REMOTE_PING, Qt.Horizontal, trans("list.clients.ping"))
        return model

    def update(self):
        """Update clients list"""
        self.idx = 0
        self.window.clients.setModel(self.model)
        if self.count != self.model.rowCount():
            self.model.removeRows(0, self.model.rowCount())
            self.initialized = False
            self.idx = 0

        i = 0
        for ip in self.window.tracker.remote.clients:
            if self.window.tracker.remote.clients[ip].removed:
                continue
            self.add_client(ip, self.window.tracker.remote.clients[ip])
            i += 1

        self.count = i
        self.initialized = True

    def add_client(self, ip, client):
        """
        Add/update client entry

        :param ip: client IP
        :param client: client object
        """
        is_current = (ip == self.window.tracker.remote_ip)
        name = client.hostname
        if client.name is not None:
            name = client.name
        if client.last_active_time is not None:
            state = client.last_active_time.strftime('%H:%M:%S')
        else:
            state = trans("list.clients.not_connected")

        # ping
        pings = "%d / %d" % (client.ping_video, client.ping_data)

        # if already active host, mark it
        if is_current:
            name = '>> ' + name

        if client.state is not None:
            state = client.state

        # get remote status
        remote_status = ''
        if ip in self.window.tracker.remote_status:
            remote_status = self.window.tracker.remote_status[ip]

        if self.initialized is False:
            idx = self.model.rowCount()
            self.model.insertRow(idx)
            self.model.setData(self.model.index(idx, self.REMOTE_HOST), name)
            self.model.setData(self.model.index(idx, self.REMOTE_IP), ip)
            self.model.setData(self.model.index(idx, self.REMOTE_TIME), state)
            self.model.setData(self.model.index(idx, self.REMOTE_STATUS), remote_status)
            self.model.setData(self.model.index(idx, self.REMOTE_PING), pings)
        else:
            for idx in range(0, self.model.rowCount()):
                if self.model.index(idx, self.REMOTE_IP).data() == ip:
                    self.model.setData(self.model.index(idx, self.REMOTE_HOST), name)
                    self.model.setData(self.model.index(idx, self.REMOTE_TIME), state)
                    self.model.setData(self.model.index(idx, self.REMOTE_STATUS), remote_status)
                    self.model.setData(self.model.index(idx, self.REMOTE_PING), pings)
                    return
        self.idx += 1
