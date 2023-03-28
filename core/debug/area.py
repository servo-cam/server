#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Area:
    def __init__(self, tracker=None):
        """
        Area debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'area'

    def update(self):
        """Updates the area debug window."""
        self.tracker.debug.begin(self.id)

        self.tracker.debug.add(self.id, 'area.enabled',
                               str(self.tracker.area.enabled))
        self.tracker.debug.add(self.id, 'area.select',
                               str(self.tracker.area.select))
        self.tracker.debug.add(self.id, 'area.world',
                               str(self.tracker.area.world))
        self.tracker.debug.add(self.id, 'area.areas',
                               str(self.tracker.area.areas))
        self.tracker.debug.add(self.id, 'area.rgb',
                               str(self.tracker.area.rgb))

        self.tracker.debug.end(self.id)
