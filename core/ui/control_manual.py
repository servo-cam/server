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
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QGridLayout, QVBoxLayout, QWidget, QSlider,
                               QRadioButton)
from core.utils import trans
from core.ui.style import Style


class UIControlManual:
    def __init__(self, window=None):
        """
        Manual control UI setup

        :param window: main UI window object
        """
        self.window = window

        self.FONT_BTN_BOLD = QFont()
        self.FONT_BTN_BOLD.setBold(True)

    def setup(self):
        """
        Setup manual control

        :return: QWidget
        """
        self.window.control_manual = {}

        # setup
        self.setup_movement()
        self.setup_actions()
        self.setup_extra()

        movement = self.setup_grid()
        mode = self.setup_mode()
        sliders = self.setup_sliders()

        layout = QVBoxLayout()
        layout.addLayout(sliders)
        layout.addWidget(movement, Qt.AlignCenter)
        layout.addWidget(mode, Qt.AlignCenter)

        # container
        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_movement(self):
        """Setup movement buttons"""
        self.window.control_manual['move'] = {}
        self.window.control_manual['move'][self.window.tracker.MOVEMENT_LEFT] = QPushButton(trans("btn.move.LEFT"))
        self.window.control_manual['move'][self.window.tracker.MOVEMENT_RIGHT] = QPushButton(trans("btn.move.RIGHT"))
        self.window.control_manual['move'][self.window.tracker.MOVEMENT_UP] = QPushButton(trans("btn.move.UP"))
        self.window.control_manual['move'][self.window.tracker.MOVEMENT_DOWN] = QPushButton(trans("btn.move.DOWN"))
        self.window.control_manual['move'][self.window.tracker.MOVEMENT_CENTER] = QPushButton(trans("btn.move.CENTER"))

        for k in self.window.control_manual['move']:
            self.window.control_manual['move'][k].setFont(self.FONT_BTN_BOLD)
            self.window.control_manual['move'][k].setFixedSize(Style.CONTROL_GRID_BTN_WIDTH,
                                                               Style.CONTROL_GRID_BTN_HEIGHT)
            self.window.control_manual['move'][k].pressed.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.movement_begin(arg))
            self.window.control_manual['move'][k].released.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.movement_end(arg))

    def setup_actions(self):
        """Setup action buttons"""
        self.window.control_manual['action'] = {}
        self.window.control_manual['action'][self.window.tracker.ACTION_A1] = QPushButton(trans("btn.action.A1"))
        self.window.control_manual['action'][self.window.tracker.ACTION_A2] = QPushButton(trans("btn.action.A2"))
        self.window.control_manual['action'][self.window.tracker.ACTION_A3] = QPushButton(trans("btn.action.A3"))
        self.window.control_manual['action'][self.window.tracker.ACTION_B4] = QPushButton(trans("btn.action.B4"))
        self.window.control_manual['action'][self.window.tracker.ACTION_B5] = QPushButton(trans("btn.action.B5"))
        self.window.control_manual['action'][self.window.tracker.ACTION_B6] = QPushButton(trans("btn.action.B6"))

        for k in self.window.control_manual['action']:
            self.window.control_manual['action'][k].setFixedSize(Style.CONTROL_GRID_BTN_WIDTH,
                                                                 Style.CONTROL_GRID_BTN_HEIGHT)
            self.window.control_manual['action'][k].clicked.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.action(arg))
            self.window.control_manual['action'][k].pressed.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.action_begin(arg))
            self.window.control_manual['action'][k].released.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.action_end(arg))

    def setup_extra(self):
        """Setup extra buttons"""
        self.window.control_manual['extra'] = {}
        self.window.control_manual['extra'][self.window.tracker.MOVEMENT_ZOOM_IN] = QPushButton(
            trans("btn.move.ZOOM_IN"))
        self.window.control_manual['extra'][self.window.tracker.MOVEMENT_ZOOM_OUT] = QPushButton(
            trans("btn.move.ZOOM_OUT"))
        self.window.control_manual['extra'][self.window.tracker.MOVEMENT_SPEED_UP] = QPushButton(
            trans("btn.move.SPEED_UP"))
        self.window.control_manual['extra'][self.window.tracker.MOVEMENT_SPEED_DOWN] = QPushButton(
            trans("btn.move.SPEED_DOWN"))

        for k in self.window.control_manual['extra']:
            self.window.control_manual['extra'][k].setFixedSize(Style.CONTROL_GRID_BTN_WIDTH,
                                                                Style.CONTROL_GRID_BTN_HEIGHT)
            self.window.control_manual['extra'][k].pressed.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.movement_begin(arg))
            self.window.control_manual['extra'][k].released.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.movement_end(arg))

    def setup_grid(self):
        """
        Setup grid layout

        :return: QWidget
        """
        grid = QGridLayout()

        grid.addWidget(self.window.control_manual['action'][self.window.tracker.ACTION_A1], 0, 0)
        grid.addWidget(self.window.control_manual['action'][self.window.tracker.ACTION_A2], 1, 0)
        grid.addWidget(self.window.control_manual['action'][self.window.tracker.ACTION_A3], 2, 0)

        grid.addWidget(self.window.control_manual['action'][self.window.tracker.ACTION_B4], 0, 4)
        grid.addWidget(self.window.control_manual['action'][self.window.tracker.ACTION_B5], 1, 4)
        grid.addWidget(self.window.control_manual['action'][self.window.tracker.ACTION_B6], 2, 4)

        grid.addWidget(self.window.control_manual['extra'][self.window.tracker.MOVEMENT_ZOOM_IN], 0, 1)
        grid.addWidget(self.window.control_manual['extra'][self.window.tracker.MOVEMENT_ZOOM_OUT], 2, 1)
        grid.addWidget(self.window.control_manual['move'][self.window.tracker.MOVEMENT_UP], 0, 2)
        grid.addWidget(self.window.control_manual['move'][self.window.tracker.MOVEMENT_LEFT], 1, 1)
        grid.addWidget(self.window.control_manual['move'][self.window.tracker.MOVEMENT_CENTER], 1, 2)
        grid.addWidget(self.window.control_manual['move'][self.window.tracker.MOVEMENT_RIGHT], 1, 3)
        grid.addWidget(self.window.control_manual['move'][self.window.tracker.MOVEMENT_DOWN], 2, 2)
        grid.addWidget(self.window.control_manual['extra'][self.window.tracker.MOVEMENT_SPEED_UP], 0, 3)
        grid.addWidget(self.window.control_manual['extra'][self.window.tracker.MOVEMENT_SPEED_DOWN], 2, 3)

        grid.setAlignment(Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(grid)

        return widget

    def setup_mode(self):
        """
        Setup mode buttons

        :return: QWidget
        """
        self.window.control_manual['mode'] = {}
        self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_OFF] = QRadioButton(
            trans("manual.action.mode.OFF"))
        self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_SINGLE] = QRadioButton(
            trans("manual.action.mode.SINGLE"))
        self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_CONTINUOUS] = QRadioButton(
            trans("manual.action.mode.CONTINUOUS"))
        self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_TOGGLE] = QRadioButton(
            trans("manual.action.mode.TOGGLE"))

        for k in self.window.control_manual['mode']:
            self.window.control_manual['mode'][k].toggled.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_manual.toggle_action_mode(arg))

        layout = QHBoxLayout()
        layout.addWidget(self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_OFF])
        layout.addWidget(self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_SINGLE])
        layout.addWidget(self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_CONTINUOUS])
        layout.addWidget(self.window.control_manual['mode'][self.window.tracker.ACTION_MODE_TOGGLE])

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_sliders(self):
        """
        Setup sliders

        :return: QWidget
        """
        self.window.control_manual['speed'] = QSlider(Qt.Horizontal)
        self.window.control_manual['speed'].valueChanged.connect(
            lambda: self.window.tracker.controller.control_manual.change_speed(
                self.window.control_manual['speed'].value()))

        self.window.control_manual['zoom'] = QSlider(Qt.Horizontal)
        self.window.control_manual['zoom'].valueChanged.connect(
            lambda: self.window.tracker.controller.control_manual.change_zoom(
                self.window.control_manual['zoom'].value()))

        # slider: zoom
        zoom_layout = QVBoxLayout()
        zoom_layout.addWidget(QLabel(trans('manual.zoom')))
        zoom_layout.addWidget(self.window.control_manual['zoom'])
        zoom = QWidget()
        zoom.setLayout(zoom_layout)

        # slider: speed
        speed_layout = QVBoxLayout()
        speed_layout.addWidget(QLabel(trans('manual.speed')))
        speed_layout.addWidget(self.window.control_manual['speed'])
        speed = QWidget()
        speed.setLayout(speed_layout)

        sliders = QHBoxLayout()
        sliders.addWidget(zoom)
        sliders.addWidget(speed)

        return sliders
