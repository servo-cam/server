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
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QVBoxLayout,
                               QWidget, QScrollArea)
from core.utils import trans
from core.ui.widgets import FilterInput


class UIControlFilter:
    def __init__(self, window=None):
        """
        Filter control UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup filter control

        :return: QWidget
        """
        self.window.control_filter = {}

        bold = "font-weight: bold;"

        # rows widgets
        detect_label = QLabel(trans("filter.detect.label"))
        detect_label.setStyleSheet(bold)
        detect_classes = self.setup_input_filter('classes', 'detect.classes')
        detect_min_score = self.setup_input_filter('min_score', 'detect.min_score')

        target_label = QLabel(trans("filter.target.label"))
        target_label.setStyleSheet(bold)
        target_classes = self.setup_input_filter('classes', 'target.classes')
        target_min_score = self.setup_input_filter('min_score', 'target.min_score')

        action_label = QLabel(trans("filter.action.label"))
        action_label.setStyleSheet(bold)
        action_classes = self.setup_input_filter('classes', 'action.classes')
        action_min_score = self.setup_input_filter('min_score', 'action.min_score')

        layout = QVBoxLayout()

        layout.addWidget(detect_label)
        layout.addWidget(detect_classes)
        layout.addWidget(detect_min_score)

        layout.addWidget(target_label)
        layout.addWidget(target_classes)
        layout.addWidget(target_min_score)

        layout.addWidget(action_label)
        layout.addWidget(action_classes)
        layout.addWidget(action_min_score)

        # container
        widget = QWidget()
        widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setAlignment(Qt.AlignCenter)
        scroll.setWidget(widget)

        return scroll

    def setup_input_filter(self, name, mode):
        """
        Setup filter input

        :param name: filter name
        :param mode: filter mode
        :return: QWidget
        """
        label = QLabel(trans("filter." + name + ".label"))

        self.window.control_filter[mode] = FilterInput(self.window)

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.window.control_filter[mode])

        widget = QWidget()
        widget.setLayout(layout)

        return widget
