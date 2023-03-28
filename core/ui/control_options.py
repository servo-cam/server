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
from core.ui.widgets import OptionSlider, OptionCheckbox, OptionInput
from core.utils import trans


class UIControlOptions:
    def __init__(self, window=None):
        """
        Options control UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """
        Setup options control

        :return: QWidget
        """
        controls = self.setup_options()

        layout = QHBoxLayout()
        layout.addWidget(controls)

        # container
        widget = QWidget()
        widget.setLayout(layout)

        return widget

    def setup_options(self):
        """
        Setup options control

        :return: QWidget
        """
        self.window.control_options = {}

        bold = "font-weight: bold;"

        # groups labels
        targeting_label = QLabel(trans("option.targeting"))
        targeting_label.setStyleSheet(bold)
        targeting_mean_label = QLabel(trans("option.targeting.mean"))
        targeting_mean_label.setStyleSheet(bold)
        targeting_smooth_label = QLabel(trans("option.targeting.smooth"))
        targeting_smooth_label.setStyleSheet(bold)
        patrol_label = QLabel(trans("option.patrol"))
        patrol_label.setStyleSheet(bold)
        servo_label = QLabel(trans("option.servo"))
        servo_label.setStyleSheet(bold)

        # targeting / multipliers
        self.window.control_options['targeting_speed'] = OptionSlider(self.window, 'targeting_speed',
                                                                      trans('option.targeting.multiplier.speed'), 1, 10,
                                                                      1, 1)
        self.window.control_options['targeting_delay'] = OptionSlider(self.window, 'targeting_delay',
                                                                      trans('option.targeting.multiplier.delay'), 1,
                                                                      100, 1, 4)
        self.window.control_options['targeting_smooth'] = OptionSlider(self.window, 'targeting_smooth',
                                                                       trans('option.targeting.multiplier.smooth'), 1,
                                                                       100, 1, 16)

        # rows widgets
        layout = QVBoxLayout()
        layout.addWidget(targeting_label)
        layout.addWidget(self.window.control_options['targeting_speed'])
        layout.addWidget(self.window.control_options['targeting_delay'])
        layout.addWidget(self.window.control_options['targeting_smooth'])

        # targeting / mean
        self.window.control_options['targeting_mean_target'] = OptionCheckbox(self.window, 'targeting_mean_target',
                                                                              trans('option.targeting.mean.target'),
                                                                              True)
        self.window.control_options['targeting_mean_now'] = OptionCheckbox(self.window, 'targeting_mean_now',
                                                                           trans('option.targeting.mean.now'), True)
        self.window.control_options['targeting_mean_cam'] = OptionCheckbox(self.window, 'targeting_mean_cam',
                                                                           trans('option.targeting.mean.cam'), True)
        self.window.control_options['targeting_mean_target_depth'] = OptionInput(self.window,
                                                                                 'targeting_mean_target_depth')
        self.window.control_options['targeting_mean_now_depth'] = OptionInput(self.window,
                                                                              'targeting_mean_now_depth')
        self.window.control_options['targeting_mean_cam_depth'] = OptionInput(self.window,
                                                                              'targeting_mean_cam_depth')

        # horizontal columns
        mean_layout = QHBoxLayout()
        mean_layout.addWidget(self.window.control_options['targeting_mean_target'])
        mean_layout.addWidget(self.window.control_options['targeting_mean_now'])
        mean_layout.addWidget(self.window.control_options['targeting_mean_cam'])

        mean_depth_layout = QHBoxLayout()
        mean_depth_layout.addWidget(self.window.control_options['targeting_mean_target_depth'])
        mean_depth_layout.addWidget(self.window.control_options['targeting_mean_now_depth'])
        mean_depth_layout.addWidget(self.window.control_options['targeting_mean_cam_depth'])

        layout.addWidget(targeting_mean_label)
        layout.addLayout(mean_layout)
        layout.addLayout(mean_depth_layout)

        # targeting / smooth
        self.window.control_options['targeting_smooth_follow'] = OptionCheckbox(self.window, 'targeting_smooth_follow',
                                                                                trans('option.targeting.smooth.follow'),
                                                                                True)
        self.window.control_options['targeting_smooth_camera'] = OptionCheckbox(self.window, 'targeting_smooth_camera',
                                                                                trans('option.targeting.smooth.camera'),
                                                                                True)
        self.window.control_options['targeting_brake'] = OptionCheckbox(self.window, 'targeting_brake',
                                                                        trans('option.targeting.brake'),
                                                                        True)

        smooth_layout = QHBoxLayout()
        smooth_layout.addWidget(self.window.control_options['targeting_smooth_follow'])
        smooth_layout.addWidget(self.window.control_options['targeting_smooth_camera'])
        smooth_layout.addWidget(self.window.control_options['targeting_brake'])

        layout.addWidget(targeting_smooth_label)
        layout.addLayout(smooth_layout)

        # patrol
        self.window.control_options['patrol_step'] = OptionSlider(self.window, 'patrol_step',
                                                                  trans('option.patrol.step'), 1, 100,
                                                                  1, 20)
        self.window.control_options['patrol_resume'] = OptionSlider(self.window, 'patrol_resume',
                                                                    trans('option.patrol.resume'), 1, 10000,
                                                                    1, 2000)

        layout.addWidget(patrol_label)
        layout.addWidget(self.window.control_options['patrol_step'])
        layout.addWidget(self.window.control_options['patrol_resume'])

        # servo step and multiplier
        self.window.control_options['servo_step_x'] = OptionSlider(self.window, 'servo_step_x',
                                                                   trans('option.servo.step.x'), 1, 10,
                                                                   1, 1)
        self.window.control_options['servo_step_y'] = OptionSlider(self.window, 'servo_step_y',
                                                                   trans('option.servo.step.y'), 1, 10,
                                                                   1, 1)
        self.window.control_options['servo_multiplier_x'] = OptionSlider(self.window, 'servo_multiplier_x',
                                                                         trans('option.servo.multiplier.x'), 1, 10,
                                                                         1, 1)
        self.window.control_options['servo_multiplier_y'] = OptionSlider(self.window, 'servo_multiplier_y',
                                                                         trans('option.servo.multiplier.y'), 1, 10,
                                                                         1, 1)

        layout.addWidget(servo_label)
        layout.addWidget(self.window.control_options['servo_step_x'])
        layout.addWidget(self.window.control_options['servo_step_y'])
        layout.addWidget(self.window.control_options['servo_multiplier_x'])
        layout.addWidget(self.window.control_options['servo_multiplier_y'])

        # container
        widget = QWidget()
        widget.setLayout(layout)

        scroll = QScrollArea()
        scroll.setAlignment(Qt.AlignCenter)
        scroll.setWidget(widget)

        return scroll
