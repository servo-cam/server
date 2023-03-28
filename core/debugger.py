#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from tensorflow.config import list_physical_devices
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QStandardItemModel
from core.debug.main import Main
from core.debug.render import Render
from core.debug.keypoints import Keypoints
from core.debug.network import Network
from core.debug.manual import Manual
from core.debug.servo import Servo
from core.debug.targeting import Targeting
from core.debug.target import Target
from core.debug.action import Action
from core.debug.patrol import Patrol
from core.debug.area import Area
from core.debug.command import Command
from core.debug.sockets import Sockets
from core.debug.camera import Camera
from core.debug.filter import Filter
from core.debug.performance import Performance


class Debug:
    DBG_KEY, DBG_VALUE = range(2)

    def __init__(self, tracker=None):
        """
        Debug handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.logs = []

        # setup workers
        self.workers = {}
        self.workers['tracker'] = Main(self.tracker)
        self.workers['render'] = Render(self.tracker)
        self.workers['keypoints'] = Keypoints(self.tracker)
        self.workers['network'] = Network(self.tracker)
        self.workers['manual'] = Manual(self.tracker)
        self.workers['targeting'] = Targeting(self.tracker)
        self.workers['target'] = Target(self.tracker)
        self.workers['action'] = Action(self.tracker)
        self.workers['patrol'] = Patrol(self.tracker)
        self.workers['servo'] = Servo(self.tracker)
        self.workers['area'] = Area(self.tracker)
        self.workers['command'] = Command(self.tracker)
        self.workers['sockets'] = Sockets(self.tracker)
        self.workers['camera'] = Camera(self.tracker)
        self.workers['filter'] = Filter(self.tracker)
        self.workers['performance'] = Performance(self.tracker)

        # prepare debug ids
        self.ids = self.workers.keys()

        self.models = {}
        self.initialized = {}
        self.active = {}
        self.idx = {}
        self.counters = {}

        # prepare debug workers data
        for id in self.ids:
            self.models[id] = self.create_model(self.tracker.window)
            self.initialized[id] = False
            self.active[id] = False
            self.idx[id] = 0

        # display GPU info
        gpus = list_physical_devices('GPU')
        if len(gpus) > 0:
            for gpu in list_physical_devices('GPU'):
                self.log("[GPU] " + gpu.name + ", Type:" + gpu.device_type)
        else:
            self.log("[GPU] NOT DETECTED, USING CPU MODE")

    def update(self):
        """Update debug windows"""
        for id in self.workers:
            if id in self.active and self.active[id]:
                self.workers[id].update()

    def begin(self, id):
        """
        Begin debug data add

        :param id: debug id
        """
        self.tracker.window.debug[id].setModel(self.models[id])
        if id not in self.counters or self.counters[id] != self.models[id].rowCount():
            self.models[id].removeRows(0, self.models[id].rowCount())
            self.initialized[id] = False
        self.idx[id] = 0

    def end(self, id):
        """
        End debug data add

        :param id: debug id
        """
        self.counters[id] = self.idx[id]
        self.initialized[id] = True

    def add(self, id, k, v):
        """
        Add debug entry

        :param id: debug id
        :param k: key
        :param v: value
        """
        if self.initialized[id] is False:
            idx = self.models[id].rowCount()
            self.models[id].insertRow(idx)
            self.models[id].setData(self.models[id].index(idx, self.DBG_KEY), k)
            self.models[id].setData(self.models[id].index(idx, self.DBG_VALUE), v)
        else:
            for idx in range(0, self.models[id].rowCount()):
                if self.models[id].index(idx, self.DBG_KEY).data() == k:
                    self.models[id].setData(self.models[id].index(idx, self.DBG_VALUE), v)
                    self.idx[id] += 1
                    return
        self.idx[id] += 1

    def log(self, text, app=True):
        """
        Add log entry

        At first, add entry to list
        It is required for threading, logs will be printed later - without this it will cause crash!

        :param text: log message
        :param app: append to app window log
        """
        print(text)
        if not app:
            return

        self.logs.append(text)

    def append_logs(self):
        """Append logs to console"""
        for text in self.logs:
            cur = self.tracker.window.console.textCursor()  # Move cursor to end of text
            cur.movePosition(QTextCursor.End)
            s = str(text) + "\n"
            while s:
                head, sep, s = s.partition("\n")  # Split line at LF
                cur.insertText(head)  # Insert text at cursor
                if sep:  # New line if LF
                    cur.insertBlock()
            self.tracker.window.console.setTextCursor(cur)  # Update visible cursor
        self.logs = []

    def create_model(self, parent):
        """
        Create list model

        :param parent: parent widget
        :return: model instance
        """
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.DBG_KEY, Qt.Horizontal, "Key")
        model.setHeaderData(self.DBG_VALUE, Qt.Horizontal, "Value")
        return model
