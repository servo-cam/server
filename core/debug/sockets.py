#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Sockets:
    def __init__(self, tracker=None):
        """
        Sockets debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'sockets'

    def update(self):
        """Updates the sockets debug window."""
        self.tracker.debug.begin(self.id)

        self.tracker.debug.add(self.id, 'sockets.started', str(self.tracker.sockets.started))
        self.tracker.debug.add(self.id, 'sockets.is_send', str(self.tracker.sockets.is_send))
        self.tracker.debug.add(self.id, 'sockets.is_recv', str(self.tracker.sockets.is_recv))
        self.tracker.debug.add(self.id, 'sockets.last_reset', str(self.tracker.sockets.last_reset))
        self.tracker.debug.add(self.id, 'sockets.packets_wait', str(self.tracker.sockets.packets_wait))
        self.tracker.debug.add(self.id, 'sockets.PORT_DATA', str(self.tracker.sockets.PORT_DATA))
        self.tracker.debug.add(self.id, 'sockets.PORT_CONN', str(self.tracker.sockets.PORT_CONN))
        self.tracker.debug.add(self.id, 'sockets.PORT_STATUS', str(self.tracker.sockets.PORT_STATUS))

        self.tracker.debug.end(self.id)
