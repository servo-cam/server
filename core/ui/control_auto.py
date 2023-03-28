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
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLabel, QVBoxLayout,
                               QWidget, QSlider, QSizePolicy, QSpacerItem, QComboBox)
from core.utils import trans
from core.ui.style import Style


class UIControlAuto:
    def __init__(self, window=None):
        """
        Auto control UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup auto control

        :return: QWidget
        """
        self.window.control_auto = {}

        # setup
        self.setup_target_mode()
        self.setup_target_point()
        self.setup_action_buttons()
        self.setup_sliders()
        self.setup_action_name()
        self.setup_action_mode()

        # columns widgets
        left = self.setup_left()
        right = self.setup_right()

        layout = QHBoxLayout()
        layout.addWidget(left)
        layout.addWidget(right)

        # container
        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_left(self):
        """
        Setup left column

        :return: QWidget
        """
        # tracking mode
        label = QLabel(trans("auto.label.tracking"))
        label.setMaximumHeight(Style.LABEL_MAX_HEIGHT)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_OFF])
        layout.addWidget(self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_IDLE])
        layout.addWidget(self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_FOLLOW])
        layout.addWidget(self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_PATROL])

        layout.addItem(QSpacerItem(40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # actions
        label = QLabel(trans("auto.label.action"))
        label.setMaximumHeight(Style.LABEL_MAX_HEIGHT)

        layout.addWidget(label)
        layout.addWidget(self.window.control_auto['action_enable'])
        layout.addWidget(self.window.control_auto['action_length'])
        layout.addWidget(self.window.control_auto['action_next_target'])
        layout.addWidget(self.window.control_auto['action_name'])
        layout.addWidget(self.window.control_auto['action_mode'])

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_right(self):
        """
        Setup right column

        :return: QWidget
        """
        # target point
        label = QLabel(trans("auto.label.target"))
        label.setMaximumHeight(Style.LABEL_MAX_HEIGHT)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_AUTO])
        layout.addWidget(self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_HEAD])
        layout.addWidget(self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_NECK])
        layout.addWidget(self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_BODY])
        layout.addWidget(self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_LEGS])

        # lock / single
        label = QLabel(trans("auto.label.locking"))
        label.setMaximumHeight(Style.LABEL_MAX_HEIGHT)

        btn_prev = QPushButton(trans("auto.target.prev"))
        btn_prev.clicked.connect(
            lambda: self.window.tracker.targets.prev())
        btn_next = QPushButton(trans("auto.target.next"))
        btn_next.clicked.connect(
            lambda: self.window.tracker.targets.next())

        persons = QHBoxLayout()
        persons.addWidget(btn_prev)
        persons.addWidget(btn_next)

        layout.addWidget(label)
        layout.addWidget(self.window.control_auto['target_lock'])
        layout.addWidget(self.window.control_auto['single_target'])
        layout.addLayout(persons)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_target_mode(self):
        """Setup target mode buttons"""
        self.window.control_auto['mode'] = {}
        self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_OFF] = QPushButton(
            trans("auto.target.mode.OFF"))
        self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_IDLE] = QPushButton(
            trans("auto.target.mode.IDLE"))
        self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_FOLLOW] = QPushButton(
            trans("auto.target.mode.FOLLOW"))
        self.window.control_auto['mode'][self.window.tracker.TARGET_MODE_PATROL] = QPushButton(
            trans("auto.target.mode.PATROL"))

        for k in self.window.control_auto['mode']:
            self.window.control_auto['mode'][k].setCheckable(True)
            self.window.control_auto['mode'][k].clicked.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_auto.toggle_target_mode(arg))

    def setup_target_point(self):
        """Setup target point buttons"""
        self.window.control_auto['target_point'] = {}
        self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_AUTO] = QPushButton(
            trans("auto.target.point.AUTO"))
        self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_HEAD] = QPushButton(
            trans("auto.target.point.HEAD"))
        self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_NECK] = QPushButton(
            trans("auto.target.point.NECK"))
        self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_BODY] = QPushButton(
            trans("auto.target.point.BODY"))
        self.window.control_auto['target_point'][self.window.tracker.TARGET_POINT_LEGS] = QPushButton(
            trans("auto.target.point.LEGS"))

        for k in self.window.control_auto['target_point']:
            self.window.control_auto['target_point'][k].setCheckable(True)
            self.window.control_auto['target_point'][k].clicked.connect(
                lambda checked=None, arg=k: self.window.tracker.controller.control_auto.toggle_target_point(arg))

    def setup_action_buttons(self):
        """Setup action buttons"""
        self.window.control_auto['action_enable'] = QPushButton(trans("auto.action.enable"))
        self.window.control_auto['target_lock'] = QPushButton(trans("auto.target.lock"))
        self.window.control_auto['single_target'] = QPushButton(trans("auto.target.single"))
        self.window.control_auto['action_enable'].setCheckable(True)
        self.window.control_auto['target_lock'].setCheckable(True)
        self.window.control_auto['single_target'].setCheckable(True)

        self.window.control_auto['action_enable'].clicked.connect(
            lambda: self.window.tracker.controller.control_auto.toggle_action_enable())
        self.window.control_auto['target_lock'].clicked.connect(
            lambda: self.window.tracker.controller.control_auto.toggle_target_lock())
        self.window.control_auto['single_target'].clicked.connect(
            lambda: self.window.tracker.controller.control_auto.toggle_single_target())

    def setup_sliders(self):
        """Setup sliders"""
        self.window.control_auto['action_length'] = QSlider(Qt.Horizontal)
        self.window.control_auto['action_next_target'] = QSlider(Qt.Horizontal)

        self.window.control_auto['action_length'].setToolTip(trans("auto.action.length.slider.tooltip"))
        self.window.control_auto['action_next_target'].setToolTip(trans("auto.action.switch.slider.tooltip"))

        self.window.control_auto['action_length'].valueChanged.connect(
            lambda: self.window.tracker.controller.control_auto.change_action_length(
                self.window.control_auto['action_length'].value()))
        self.window.control_auto['action_next_target'].valueChanged.connect(
            lambda: self.window.tracker.controller.control_auto.change_action_next_target(
                self.window.control_auto['action_next_target'].value()))

    def setup_action_name(self):
        """Setup action name select list"""
        self.window.control_auto['action_name'] = QComboBox()
        for action in self.window.tracker.action.actions:
            self.window.control_auto['action_name'].addItem(action)

        self.window.control_auto['action_name'].currentIndexChanged.connect(
            lambda: self.window.tracker.controller.control_auto.toggle_action_name(
                self.window.control_auto['action_name'].currentIndex()))

    def setup_action_mode(self):
        """Setup action mode select list"""
        self.window.control_auto['action_mode'] = QComboBox()
        for action in self.window.tracker.action.modes:
            str = trans('auto.action.mode.' + action)
            self.window.control_auto['action_mode'].addItem(str)

        self.window.control_auto['action_mode'].currentIndexChanged.connect(
            lambda: self.window.tracker.controller.control_auto.toggle_action_mode(
                self.window.control_auto['action_mode'].currentIndex()))
