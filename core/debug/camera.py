#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Camera:
    def __init__(self, tracker=None):
        """
        Camera debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'camera'

    def update(self):
        """Updates the camera debug window."""
        self.tracker.debug.begin(self.id)

        self.tracker.debug.add(self.id, 'camera.idx.',
                               str(self.tracker.camera.idx))
        self.tracker.debug.add(self.id, 'camera.fov',
                               str(self.tracker.camera.fov))
        self.tracker.debug.add(self.id, 'camera.width',
                               str(self.tracker.camera.width))
        self.tracker.debug.add(self.id, 'camera.height',
                               str(self.tracker.camera.height))
        self.tracker.debug.add(self.id, 'camera.fps',
                               str(self.tracker.camera.fps))

        self.tracker.debug.end(self.id)
