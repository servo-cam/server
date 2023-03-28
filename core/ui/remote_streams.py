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
from core.ui.widgets import StreamsMenu


class UIRemoteStreams:
    STREAM_NAME, STREAM_HOST, STREAM_PORT, STREAM_STATUS = range(4)  # list columns

    def __init__(self, window=None):
        """
        Remote streams UI setup

        :param window: main UI window object
        """
        self.window = window
        self.idx = 0
        self.model = None
        self.count = 0
        self.initialized = False

    def setup_list(self):
        """
        Setup remote streams list

        :return: QTreeView
        """
        # remote devices list
        self.window.remote['stream'] = StreamsMenu(self.window)
        self.window.remote['stream'].setMinimumHeight(140)
        self.window.remote['stream'].setAlternatingRowColors(True)
        self.window.remote['stream'].setIndentation(0)
        # self.window.devices_list.setFont(FONT_CONSOLE)
        return self.window.remote['stream']

    def setup(self):
        """Setup remote streams model"""
        self.model = self.create_model(self.window)

    def create_model(self, parent):
        """
        Create streams list model

        :param parent: parent widget
        :return: QStandardItemModel
        """
        model = QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.STREAM_NAME, Qt.Horizontal, trans("list.streams.name"))
        model.setHeaderData(self.STREAM_HOST, Qt.Horizontal, trans("list.streams.host"))
        model.setHeaderData(self.STREAM_PORT, Qt.Horizontal, trans("list.streams.port"))
        model.setHeaderData(self.STREAM_STATUS, Qt.Horizontal, trans("list.streams.status"))
        return model

    def update(self):
        """Update streams list"""
        self.idx = 0
        self.window.remote['stream'].setModel(self.model)
        if self.count != self.model.rowCount():
            self.model.removeRows(0, self.model.rowCount())
            self.initialized = False
            self.idx = 0

        i = 0
        for unique_id in self.window.tracker.stream.streams:
            if self.window.tracker.stream.streams[unique_id].removed:
                continue
            self.add(self.window.tracker.stream.streams[unique_id])
            i += 1

        self.count = i
        self.initialized = True

    def add(self, stream):
        """
        Add stream to list

        :param stream:
        """
        curr_unique = self.window.tracker.stream.get_unique_id(self.window.tracker.stream_url)
        is_current = (stream.unique_id == curr_unique)
        name = stream.host
        if stream.name is not None:
            name = stream.name

        # if already active host, mark it
        if is_current:
            name = '>> ' + name

        # get remote status
        remote_status = None
        if is_current:
            if '-' in self.window.tracker.remote_status:
                remote_status = self.window.tracker.remote_status['-']

        if self.initialized is False:
            idx = self.model.rowCount()
            self.model.insertRow(idx)
            self.model.setData(self.model.index(idx, self.STREAM_NAME), name)
            self.model.setData(self.model.index(idx, self.STREAM_HOST), stream.host)
            self.model.setData(self.model.index(idx, self.STREAM_PORT), stream.port)
            self.model.setData(self.model.index(idx, self.STREAM_STATUS), remote_status)
        else:
            for idx in range(0, self.model.rowCount()):
                if self.model.index(idx, self.STREAM_HOST).data() == stream.host and \
                        self.model.index(idx, self.STREAM_PORT).data() == stream.port:
                    self.model.setData(self.model.index(idx, self.STREAM_NAME), name)
                    self.model.setData(self.model.index(idx, self.STREAM_HOST), stream.host)
                    self.model.setData(self.model.index(idx, self.STREAM_PORT), stream.port)
                    if remote_status is not None:
                        self.model.setData(self.model.index(idx, self.STREAM_STATUS), remote_status)
                    return
        self.idx += 1
