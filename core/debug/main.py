#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Main:
    def __init__(self, tracker=None):
        """
        Main debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'tracker'

    def update(self):
        """Updates the main debug window."""
        self.tracker.debug.begin(self.id)

        self.tracker.debug.add(self.id, 'tracker.dx', str(self.tracker.dx))
        self.tracker.debug.add(self.id, 'tracker.dy', str(self.tracker.dy))
        self.tracker.debug.add(self.id, 'len(objects)',
                               len(self.tracker.objects) if self.tracker.objects is not None else 0)
        self.tracker.debug.add(self.id, 'tracker.remote_status',
                               str(self.tracker.remote_status))
        self.tracker.debug.add(self.id, 'tracker.video_dim', str(self.tracker.video_dim))

        self.tracker.debug.add(self.id, 'tracker.state', str(self.tracker.state))
        self.tracker.debug.add(self.id, 'tracker.model_name', str(self.tracker.model_name))

        self.tracker.debug.add(self.id, 'tracker.target_mode', str(self.tracker.target_mode))
        self.tracker.debug.add(self.id, 'tracker.target_point', str(self.tracker.target_point))
        self.tracker.debug.add(self.id, 'tracker.control_view', str(self.tracker.control_view))

        self.tracker.debug.add(self.id, 'tracker.window.width()', str(self.tracker.window.width()))
        self.tracker.debug.add(self.id, 'tracker.window.height()', str(self.tracker.window.height()))

        self.tracker.debug.add(self.id, 'tracker.w', str(self.tracker.w))
        self.tracker.debug.add(self.id, 'tracker.h', str(self.tracker.h))
        self.tracker.debug.add(self.id, 'tracker.fps', str(self.tracker.fps))

        self.tracker.debug.add(self.id, 'tracker.window.output.width()', str(self.tracker.window.output.height()))
        self.tracker.debug.add(self.id, 'tracker.window.output.height()', str(self.tracker.window.output.width()))

        self.tracker.debug.add(self.id, 'tracker.remote_ip', str(self.tracker.remote_ip))
        self.tracker.debug.add(self.id, 'tracker.remote_host', str(self.tracker.remote_host))
        self.tracker.debug.add(self.id, 'tracker.video_url', str(self.tracker.video_url))
        self.tracker.debug.add(self.id, 'tracker.stream_url', str(self.tracker.stream_url))

        self.tracker.debug.add(self.id, 'tracker.disabled', str(self.tracker.disabled))
        self.tracker.debug.add(self.id, 'tracker.paused', str(self.tracker.paused))
        self.tracker.debug.add(self.id, 'tracker.processing', str(self.tracker.processing))
        self.tracker.debug.add(self.id, 'tracker.ai_enabled', str(self.tracker.ai_enabled))
        self.tracker.debug.add(self.id, 'tracker.is_debug', str(self.tracker.is_debug))

        self.tracker.debug.end(self.id)
