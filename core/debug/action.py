#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Action:
    def __init__(self, tracker=None):
        """
        Action debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'action'

    def update(self):
        """Updates the action debug window."""
        self.tracker.debug.begin(self.id)

        # modes
        self.tracker.debug.add(self.id, 'action.name',
                               str(self.tracker.action.name))
        self.tracker.debug.add(self.id, 'action.manual_mode',
                               str(self.tracker.action.manual_mode))
        self.tracker.debug.add(self.id, 'action.auto_mode',
                               str(self.tracker.action.auto_mode))

        # sliders
        self.tracker.debug.add(self.id, 'action.switch_value',
                               str(self.tracker.action.switch_value))
        self.tracker.debug.add(self.id, 'action.length_value',
                               str(self.tracker.action.length_value))

        # state
        self.tracker.debug.add(self.id, 'action.enabled',
                               str(self.tracker.action.enabled))
        self.tracker.debug.add(self.id, 'action.active',
                               str(self.tracker.action.active))
        self.tracker.debug.add(self.id, 'action.toggled',
                               str(self.tracker.action.toggled))
        self.tracker.debug.add(self.id, 'action.is_single_action',
                               str(self.tracker.action.is_single_action))
        self.tracker.debug.add(self.id, 'action.stopped',
                               str(self.tracker.action.stopped))

        # counters
        self.tracker.debug.add(self.id, 'action.action_counter',
                               str(self.tracker.action_counter))
        self.tracker.debug.add(self.id, 'action.target_counter',
                               str(self.tracker.action.target_counter))

        self.tracker.debug.end(self.id)
