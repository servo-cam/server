#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Patrol:
    def __init__(self, tracker=None):
        """
        Patrol debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'patrol'

    def update(self):
        """Updates the patrol debug window."""
        self.tracker.debug.begin(self.id)

        # state
        self.tracker.debug.add(self.id, 'patrol.active',
                               str(self.tracker.patrol.active))
        self.tracker.debug.add(self.id, 'patrol.paused',
                               str(self.tracker.patrol.paused))
        self.tracker.debug.add(self.id, 'patrol.direction',
                               str(self.tracker.patrol.direction))

        # timers
        self.tracker.debug.add(self.id, 'patrol.interval',
                               str(self.tracker.patrol.interval))
        self.tracker.debug.add(self.id, 'patrol.resume_timer',
                               str(self.tracker.patrol.resume_timer))
        self.tracker.debug.add(self.id, 'patrol.resume_start',
                               str(self.tracker.patrol.resume_start))

        # config
        self.tracker.debug.add(self.id, 'patrol.STEP',
                               str(self.tracker.patrol.STEP))
        self.tracker.debug.add(self.id, 'patrol.TIMEOUT',
                               str(self.tracker.patrol.TIMEOUT))
        self.tracker.debug.add(self.id, 'patrol.INTERVAL_TIME',
                               str(self.tracker.patrol.INTERVAL_TIME))

        self.tracker.debug.end(self.id)
