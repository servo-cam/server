#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QVBoxLayout,
                               QWidget)
from core.utils import trans
from core.ui.style import Style
from core.ui.widgets import CoordsInput


class UIControlArea:
    def __init__(self, window=None):
        """
        Area control UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup area control

        :return: QWidget
        """
        self.window.control_area = {}

        # rows widgets
        target = self.setup_area_target(self.window.tracker.area.TYPE_TARGET)
        patrol = self.setup_area_target(self.window.tracker.area.TYPE_PATROL)
        action = self.setup_area_target(self.window.tracker.area.TYPE_ACTION)

        layout = QHBoxLayout()
        layout.addWidget(target)
        layout.addWidget(patrol)
        layout.addWidget(action)

        # container
        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_area_target(self, mode=None):
        """
        Setup area target control (left column)

        :param mode: area mode
        :return: QWidget
        """
        # tracking mode
        label = QLabel(trans("area." + mode + ".label"))
        label.setMaximumHeight(Style.LABEL_MAX_HEIGHT)
        label.setStyleSheet('font-weight: bold;')

        self.window.control_area[mode + '.select'] = QPushButton(trans("area.btn.select"))
        self.window.control_area[mode + '.select'].setCheckable(True)
        self.window.control_area[mode + '.select'].clicked.connect(
            lambda: self.window.tracker.controller.control_area.toggle_select(mode))

        self.window.control_area[mode + '.clear'] = QPushButton(trans("area.btn.clear"))
        self.window.control_area[mode + '.clear'].clicked.connect(
            lambda: self.window.tracker.controller.control_area.clear(mode))

        self.window.control_area[mode + '.enable'] = QPushButton(trans("area.btn.enable"))
        self.window.control_area[mode + '.enable'].setCheckable(True)
        self.window.control_area[mode + '.enable'].clicked.connect(
            lambda: self.window.tracker.controller.control_area.toggle_enable(mode))

        self.window.control_area[mode + '.world'] = QPushButton(trans("area.btn.world"))
        self.window.control_area[mode + '.world'].setCheckable(True)
        self.window.control_area[mode + '.world'].clicked.connect(
            lambda: self.window.tracker.controller.control_area.toggle_world(mode))

        self.window.control_area[mode + '.x'] = CoordsInput(self.window)
        self.window.control_area[mode + '.y'] = CoordsInput(self.window)
        self.window.control_area[mode + '.w'] = CoordsInput(self.window)
        self.window.control_area[mode + '.h'] = CoordsInput(self.window)

        self.window.control_area[mode + '.x'].id = mode
        self.window.control_area[mode + '.y'].id = mode
        self.window.control_area[mode + '.w'].id = mode
        self.window.control_area[mode + '.h'].id = mode

        self.window.control_area[mode + '.x'].setToolTip("X")
        self.window.control_area[mode + '.y'].setToolTip("Y")
        self.window.control_area[mode + '.w'].setToolTip("W")
        self.window.control_area[mode + '.h'].setToolTip("H")

        coords_x = QHBoxLayout()
        coords_x.addWidget(self.window.control_area[mode + '.x'])
        coords_x.addWidget(self.window.control_area[mode + '.w'])

        coords_y = QHBoxLayout()
        coords_y.addWidget(self.window.control_area[mode + '.y'])
        coords_y.addWidget(self.window.control_area[mode + '.h'])

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.window.control_area[mode + '.enable'])
        layout.addWidget(self.window.control_area[mode + '.select'])
        layout.addWidget(self.window.control_area[mode + '.clear'])
        layout.addWidget(self.window.control_area[mode + '.world'])
        layout.addLayout(coords_x)
        layout.addLayout(coords_y)

        widget = QWidget()
        widget.setLayout(layout)

        return widget
