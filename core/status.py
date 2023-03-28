#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Status:
    def __init__(self, tracker=None):
        """
        Device status handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

    def can_listen(self):
        """
        Check if can listen

        :return: True if can listen, False otherwise
        """
        if self.tracker.servo.local is not None:
            if self.tracker.serial.port is None:
                return False
            return True
        return False

    def listen(self):
        """
        Listen for messages from serial port

        :return: received message
        """
        if self.tracker.servo.local is not None:
            return self.tracker.serial.listen()

    def handle_thread(self, buff):
        """
        Handle thread

        :param buff: received data
        """
        if self.tracker.servo.local is not None:
            self.tracker.serial.handle_thread(buff)
