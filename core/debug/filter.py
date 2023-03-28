#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Filter:
    def __init__(self, tracker=None):
        """
        Filter debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'filter'

    def update(self):
        """Updates the filter debug window."""
        self.tracker.debug.begin(self.id)

        self.tracker.debug.add(self.id, 'filter.filters',
                               str(self.tracker.filter.filters))

        self.tracker.debug.end(self.id)
