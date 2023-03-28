#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Options:
    def __init__(self, tracker=None):
        """
        Options handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the options."""
        # slider / input
        self.apply('targeting_speed', self.tracker.targeting.SPEED_MULTIPLIER)
        self.apply('targeting_delay', self.tracker.targeting.DELAY_MULTIPLIER)
        self.apply('targeting_smooth', self.tracker.targeting.SMOOTH_MULTIPLIER)

        self.apply('patrol_step', self.tracker.patrol.STEP)
        self.apply('patrol_resume', self.tracker.patrol.TIMEOUT)
        self.apply('servo_step_x', self.tracker.servo.ANGLE_STEP_X)
        self.apply('servo_step_y', self.tracker.servo.ANGLE_STEP_Y)
        self.apply('servo_multiplier_x', self.tracker.servo.ANGLE_MULTIPLIER_X)
        self.apply('servo_multiplier_y', self.tracker.servo.ANGLE_MULTIPLIER_Y)

        # boolean / checkbox
        self.toggle('targeting_mean_target', self.tracker.targeting.MEAN_TARGET)
        self.toggle('targeting_mean_now', self.tracker.targeting.MEAN_NOW)
        self.toggle('targeting_mean_cam', self.tracker.targeting.MEAN_CAM)

        self.toggle('targeting_smooth_follow', self.tracker.targeting.SMOOTH_FOLLOW)
        self.toggle('targeting_smooth_camera', self.tracker.targeting.SMOOTH_CAMERA)
        self.toggle('targeting_brake', self.tracker.targeting.BRAKE)

        # input
        self.change('targeting_mean_target_depth', self.tracker.targeting.MEAN_DEPTH_TARGET)
        self.change('targeting_mean_now_depth', self.tracker.targeting.MEAN_DEPTH_NOW)
        self.change('targeting_mean_cam_depth', self.tracker.targeting.MEAN_DEPTH_CAM)

    def update(self):
        """Updates the options."""
        pass

    def toggle(self, id, value):
        """
        Toggles the checkbox.

        :param id: checkbox option id
        :param value: checkbox option value
        """
        if id == 'targeting_mean_target':
            self.tracker.targeting.MEAN_TARGET = value
        elif id == 'targeting_mean_now':
            self.tracker.targeting.MEAN_NOW = value
        elif id == 'targeting_mean_cam':
            self.tracker.targeting.MEAN_CAM = value
        elif id == 'targeting_smooth_follow':
            self.tracker.targeting.SMOOTH_FOLLOW = value
        elif id == 'targeting_smooth_camera':
            self.tracker.targeting.SMOOTH_CAMERA = value
        elif id == 'targeting_brake':
            self.tracker.targeting.BRAKE = value

        self.tracker.window.control_options[id].box.setChecked(value)

    def change(self, id, value):
        """
        Changes the input value.

        :param id: input option id
        :param value: input option value
        """
        if id == 'targeting_mean_target_depth':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.targeting.MEAN_DEPTH_TARGET = value
        elif id == 'targeting_mean_now_depth':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.targeting.MEAN_DEPTH_NOW = value
        elif id == 'targeting_mean_cam_depth':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.targeting.MEAN_DEPTH_CAM = value

        self.tracker.window.control_options[id].setText(str(value))

    def apply(self, id, value, type=None):
        """
        Applies the slider / input value.

        :param id: option id
        :param value: option value
        :param type: option type
        """
        multiplier = 10
        input_value = float(value)

        # multiplier
        if id == 'targeting_speed':
            multiplier = 10
        elif id == 'targeting_delay':
            multiplier = 10
        elif id == 'targeting_smooth':
            multiplier = 10
        elif id == 'patrol_step':
            multiplier = 1000
        elif id == 'patrol_resume':
            multiplier = 1
        elif id == 'servo_step_x':
            multiplier = 1
        elif id == 'servo_step_y':
            multiplier = 1
        elif id == 'servo_multiplier_x':
            multiplier = 1
        elif id == 'servo_multiplier_y':
            multiplier = 1

        # if from slider then convert to input
        if type == 'slider':
            input_value = float(int(value) / multiplier)

        if id == 'targeting_speed':
            self.tracker.targeting.SPEED_MULTIPLIER = input_value

            # required minimum to prevent stop
            if self.tracker.targeting.SPEED_MULTIPLIER >= 0.4:
                self.tracker.targeting.SMOOTH_MULTIPLIER = 0.1
                self.tracker.window.control_options['targeting_smooth'].slider.setValue(1)
                self.tracker.window.control_options['targeting_smooth'].input.setText('0.1')

        elif id == 'targeting_delay':
            self.tracker.targeting.DELAY_MULTIPLIER = input_value
        elif id == 'targeting_smooth':
            self.tracker.targeting.SMOOTH_MULTIPLIER = input_value
        elif id == 'patrol_step':
            self.tracker.patrol.STEP = input_value
        elif id == 'patrol_resume':
            self.tracker.patrol.TIMEOUT = input_value
        elif id == 'servo_step_x':
            self.tracker.servo.ANGLE_STEP_X = input_value
        elif id == 'servo_step_y':
            self.tracker.servo.ANGLE_STEP_Y = input_value
        elif id == 'servo_multiplier_x':
            self.tracker.servo.ANGLE_MULTIPLIER_X = input_value
        elif id == 'servo_multiplier_y':
            self.tracker.servo.ANGLE_MULTIPLIER_Y = input_value

        slider_value = int(input_value * multiplier)

        # update row
        if type == 'slider':
            self.tracker.window.control_options[id].input.setText(str(input_value))
        elif type == 'input':
            self.tracker.window.control_options[id].slider.setValue(int(slider_value))
        else:
            self.tracker.window.control_options[id].input.setText(str(input_value))
            self.tracker.window.control_options[id].slider.setValue(int(slider_value))
