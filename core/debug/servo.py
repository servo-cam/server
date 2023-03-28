#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Servo:
    def __init__(self, tracker=None):
        """
        Servo debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'servo'

    def update(self):
        """Updates the servo debug window."""
        self.tracker.debug.begin(self.id)

        # command
        self.tracker.debug.add(self.id, 'command.current', str(self.tracker.command.current))

        # servo
        self.tracker.debug.add(self.id, 'servo.local', str(self.tracker.servo.local))
        self.tracker.debug.add(self.id, 'servo.remote', str(self.tracker.servo.remote))
        self.tracker.debug.add(self.id, 'servo.stream', str(self.tracker.servo.stream))
        self.tracker.debug.add(self.id, 'servo.map_fov', str(self.tracker.servo.map_fov))
        self.tracker.debug.add(self.id, 'servo.use_limit', str(self.tracker.servo.use_limit))
        self.tracker.debug.add(self.id, 'servo.enable', str(self.tracker.servo.enable))
        self.tracker.debug.add(self.id, 'servo.x', str(self.tracker.servo.x))
        self.tracker.debug.add(self.id, 'servo.y', str(self.tracker.servo.y))

        self.tracker.debug.add(self.id, 'servo.ANGLE_START_X', str(self.tracker.servo.ANGLE_START_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_START_Y', str(self.tracker.servo.ANGLE_START_Y))

        self.tracker.debug.add(self.id, 'servo.ANGLE_MIN_X', str(self.tracker.servo.ANGLE_MIN_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_MAX_X', str(self.tracker.servo.ANGLE_MAX_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_MIN_Y', str(self.tracker.servo.ANGLE_MIN_Y))
        self.tracker.debug.add(self.id, 'servo.ANGLE_MAX_Y', str(self.tracker.servo.ANGLE_MAX_Y))

        self.tracker.debug.add(self.id, 'servo.ANGLE_STEP_X', str(self.tracker.servo.ANGLE_STEP_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_STEP_Y', str(self.tracker.servo.ANGLE_STEP_Y))

        self.tracker.debug.add(self.id, 'servo.ANGLE_MULTIPLIER_X', str(self.tracker.servo.ANGLE_MULTIPLIER_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_MULTIPLIER_Y', str(self.tracker.servo.ANGLE_MULTIPLIER_Y))

        self.tracker.debug.add(self.id, 'servo.ANGLE_LIMIT_MIN_X', str(self.tracker.servo.ANGLE_LIMIT_MIN_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_LIMIT_MAX_X', str(self.tracker.servo.ANGLE_LIMIT_MAX_X))
        self.tracker.debug.add(self.id, 'servo.ANGLE_LIMIT_MIN_Y', str(self.tracker.servo.ANGLE_LIMIT_MIN_Y))
        self.tracker.debug.add(self.id, 'servo.ANGLE_LIMIT_MAX_Y', str(self.tracker.servo.ANGLE_LIMIT_MAX_Y))

        # serial
        self.tracker.debug.add(self.id, 'serial.port', str(self.tracker.serial.port))
        self.tracker.debug.add(self.id, 'serial.BAUD_RATE', str(self.tracker.serial.BAUD_RATE))
        self.tracker.debug.add(self.id, 'serial.is_send', str(self.tracker.serial.is_send))
        self.tracker.debug.add(self.id, 'serial.is_recv', str(self.tracker.serial.is_recv))
        self.tracker.debug.add(self.id, 'serial.last_reset', str(self.tracker.serial.last_reset))
        self.tracker.debug.add(self.id, 'serial.is_device_sending', str(self.tracker.serial.sending))
        self.tracker.debug.add(self.id, 'serial.last_status_check', str(self.tracker.serial.last_status_check))
        self.tracker.debug.add(self.id, 'serial.STATUS_CHECK_INTERVAL', str(self.tracker.serial.STATUS_CHECK_INTERVAL))
        self.tracker.debug.add(self.id, 'serial.check_status', str(self.tracker.serial.check_status))
        self.tracker.debug.add(self.id, 'serial.data_format', str(self.tracker.serial.data_format))
        self.tracker.debug.add(self.id, 'serial.END_CHAR', str(self.tracker.serial.END_CHAR))

        self.tracker.debug.end(self.id)
