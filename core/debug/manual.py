#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Manual:
    def __init__(self, tracker=None):
        """
        Manual debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'manual'

    def update(self):
        """Updates the manual debug window."""
        self.tracker.debug.begin(self.id)

        # pointer
        self.tracker.debug.add(self.id, 'mouse.coords.x', str(self.tracker.mouse.coords[0]))
        self.tracker.debug.add(self.id, 'mouse.coords.y', str(self.tracker.mouse.coords[1]))

        # movement
        self.tracker.debug.add(self.id, 'mouse.move', str(self.tracker.mouse.move))

        # pressed
        self.tracker.debug.add(self.id, 'mouse.pressed.LEFT',
                               str(self.tracker.mouse.pressed[self.tracker.mouse.MOUSE_LEFT]))
        self.tracker.debug.add(self.id, 'mouse.pressed.RIGHT',
                               str(self.tracker.mouse.pressed[self.tracker.mouse.MOUSE_RIGHT]))
        self.tracker.debug.add(self.id, 'mouse.pressed.MIDDLE',
                               str(self.tracker.mouse.pressed[self.tracker.mouse.MOUSE_MIDDLE]))

        # manual
        self.tracker.debug.add(self.id, 'manual.speed', str(self.tracker.manual.speed))
        self.tracker.debug.add(self.id, 'manual.current', str(self.tracker.manual.current))

        self.tracker.debug.end(self.id)
