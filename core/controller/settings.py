#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.30 17:00
# =============================================================================

class Settings:
    def __init__(self, tracker=None):
        """
        Settings handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self, id):
        """Initializes the settings."""

        if id == 'servo':
            # slider / input
            self.apply('servo.min.x', self.tracker.servo.ANGLE_MIN_X, '', False)
            self.apply('servo.max.x', self.tracker.servo.ANGLE_MAX_X, '', False)
            self.apply('servo.min.y', self.tracker.servo.ANGLE_MIN_Y, '', False)
            self.apply('servo.max.y', self.tracker.servo.ANGLE_MAX_Y, '', False)
            self.apply('servo.limit.min.x', self.tracker.servo.ANGLE_LIMIT_MIN_X, '', False)
            self.apply('servo.limit.max.x', self.tracker.servo.ANGLE_LIMIT_MAX_X, '', False)
            self.apply('servo.limit.min.y', self.tracker.servo.ANGLE_LIMIT_MIN_Y, '', False)
            self.apply('servo.limit.max.y', self.tracker.servo.ANGLE_LIMIT_MAX_Y, '', False)
            self.apply('servo.fov.x', self.tracker.camera.fov[0], '', False)
            self.apply('servo.fov.y', self.tracker.camera.fov[1], '', False)

    def update(self):
        """Updates the settings."""
        pass

    def toggle(self, id, value):
        """
        Toggles the checkbox.

        :param id: checkbox option id
        :param value: checkbox option value
        """
        if id == 'key':
            # update bool value here
            pass

        self.tracker.window.settings[id].box.setChecked(value)

    def change(self, id, value):
        """
        Changes the input value.

        :param id: input option id
        :param value: input option value
        """
        # update value
        if id == 'servo.min.x':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.servo.ANGLE_MIN_X = value
        elif id == 'servo.max.x':
            value = int(value)
            if value > 180:
                value = 180
            self.tracker.servo.ANGLE_MAX_X = value
        elif id == 'servo.min.y':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.servo.ANGLE_MIN_Y = value
        elif id == 'servo.max.y':
            value = int(value)
            if value > 180:
                value = 180
            self.tracker.servo.ANGLE_MAX_Y = value
        elif id == 'servo.limit.min.x':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.servo.ANGLE_LIMIT_MIN_X = value
        elif id == 'servo.limit.max.x':
            value = int(value)
            if value > 180:
                value = 180
            self.tracker.servo.ANGLE_LIMIT_MAX_X = value
        elif id == 'servo.limit.min.y':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.servo.ANGLE_LIMIT_MIN_Y = value
        elif id == 'servo.limit.max.y':
            value = int(value)
            if value > 180:
                value = 180
            self.tracker.servo.ANGLE_LIMIT_MAX_Y = value
        elif id == 'servo.fov.x':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.camera.fov[0] = value
        elif id == 'servo.fov.y':
            value = int(value)
            if value < 1:
                value = 1
            self.tracker.camera.fov[1] = value

        txt = '{}'.format(round(value))
        self.tracker.window.settings[id].setText(txt)

    def apply(self, id, value, type=None, as_float=True):
        """
        Applies the slider / input value.

        :param id: option id
        :param value: option value
        :param type: option type
        :param as_float: parse as float, otherwise as int, default: True
        """
        multiplier = 1

        if as_float:
            input_value = float(value)
        else:
            input_value = round(value, 0)

        # multiplier
        if id == 'servo.min.x':
            multiplier = 1
        elif id == 'servo.max.x':
            multiplier = 1
        elif id == 'servo.min.y':
            multiplier = 1
        elif id == 'servo.max.y':
            multiplier = 1
        elif id == 'servo.limit.min.x':
            multiplier = 1
        elif id == 'servo.limit.max.x':
            multiplier = 1
        elif id == 'servo.limit.min.y':
            multiplier = 1
        elif id == 'servo.limit.max.y':
            multiplier = 1
        elif id == 'servo.fov.x':
            multiplier = 1
        elif id == 'servo.fov.y':
            multiplier = 1

        # if from slider then convert to input
        if type == 'slider':
            if as_float:
                input_value = float(value / multiplier)

        # update value
        if id == 'servo.min.x':
            self.tracker.servo.ANGLE_MIN_X = int(input_value)
        elif id == 'servo.max.x':
            self.tracker.servo.ANGLE_MAX_X = int(input_value)
        elif id == 'servo.min.y':
            self.tracker.servo.ANGLE_MIN_Y = int(input_value)
        elif id == 'servo.max.y':
            self.tracker.servo.ANGLE_MAX_Y = int(input_value)
        elif id == 'servo.limit.min.x':
            self.tracker.servo.ANGLE_LIMIT_MIN_X = int(input_value)
        elif id == 'servo.limit.max.x':
            self.tracker.servo.ANGLE_LIMIT_MAX_X = int(input_value)
        elif id == 'servo.limit.min.y':
            self.tracker.servo.ANGLE_LIMIT_MIN_Y = int(input_value)
        elif id == 'servo.limit.max.y':
            self.tracker.servo.ANGLE_LIMIT_MAX_Y = int(input_value)
        elif id == 'servo.fov.x':
            self.tracker.camera.fov[0] = int(input_value)
        elif id == 'servo.fov.y':
            self.tracker.camera.fov[1] = int(input_value)

        # prepare slider value
        if as_float:
            slider_value = int(input_value * multiplier)
        else:
            slider_value = int(input_value)

        # update row
        if type == 'slider':
            txt = '{}'.format(round(input_value))
            self.tracker.window.settings[id].input.setText(txt)
        elif type == 'input':
            self.tracker.window.settings[id].slider.setValue(int(slider_value))
        else:
            txt = '{}'.format(round(input_value))
            self.tracker.window.settings[id].input.setText(txt)
            self.tracker.window.settings[id].slider.setValue(int(slider_value))
