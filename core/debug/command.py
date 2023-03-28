#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Command:
    def __init__(self, tracker=None):
        """
        Command debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'command'

    def update(self):
        """Updates the command debug window."""
        self.tracker.debug.begin(self.id)

        self.tracker.debug.add(self.id, 'command.initialized', str(self.tracker.command.initialized))
        self.tracker.debug.add(self.id, 'command.current', str(self.tracker.command.current))
        self.tracker.debug.add(self.id, 'command.angle', str(self.tracker.command.angle))
        self.tracker.debug.add(self.id, 'command.prev_cmd', str(self.tracker.command.prev_cmd))
        self.tracker.debug.add(self.id, 'command.next_cmd', str(self.tracker.command.next_cmd))
        self.tracker.debug.add(self.id, 'command.send_cmd', str(self.tracker.command.send_cmd))
        self.tracker.debug.add(self.id, 'command.prev_rest', str(self.tracker.command.prev_rest))
        self.tracker.debug.add(self.id, 'command.can_send', str(self.tracker.command.can_send))

        self.tracker.debug.end(self.id)
