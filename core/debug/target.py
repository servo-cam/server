#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Target:
    def __init__(self, tracker=None):
        """
        Target debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'target'

    def update(self):
        """Updates the target debug window."""
        self.tracker.debug.begin(self.id)

        # -- finder ---
        self.tracker.debug.add(self.id, 'finder.match_type',
                               str(self.tracker.finder.match_type))

        # -- targets ---

        # idx
        self.tracker.debug.add(self.id, 'targets.idx',
                               str(self.tracker.targets.idx))
        self.tracker.debug.add(self.id, 'targets.tmp_idx',
                               str(self.tracker.targets.tmp_idx))
        self.tracker.debug.add(self.id, 'targets.identifier',
                               str(self.tracker.targets.identifier))
        self.tracker.debug.add(self.id, 'targets.tmp_identifier',
                               str(self.tracker.targets.tmp_identifier))
        self.tracker.debug.add(self.id, 'targets.change_idx',
                               str(self.tracker.targets.change_idx))

        # states
        self.tracker.debug.add(self.id, 'targets.matched',
                               str(self.tracker.targets.matched))
        self.tracker.debug.add(self.id, 'targets.is_target',
                               str(self.tracker.targets.is_target))
        self.tracker.debug.add(self.id, 'targets.search',
                               str(self.tracker.targets.search))
        self.tracker.debug.add(self.id, 'targets.lost',
                               str(self.tracker.targets.lost))
        self.tracker.debug.add(self.id, 'targets.locked',
                               str(self.tracker.targets.locked))
        self.tracker.debug.add(self.id, 'targets.single',
                               str(self.tracker.targets.single))

        # center of target
        self.tracker.debug.add(self.id, 'targets.center_last',
                               str(self.tracker.targets.center_last))
        self.tracker.debug.add(self.id, 'targets.center_current',
                               str(self.tracker.targets.center_current))

        # bounding box of target
        self.tracker.debug.add(self.id, 'targets.box_current',
                               str(self.tracker.targets.box_current))
        self.tracker.debug.add(self.id, 'targets.box_lock',
                               str(self.tracker.targets.box_lock))
        self.tracker.debug.add(self.id, 'targets.box_last',
                               str(self.tracker.targets.box_last))

        # -- target ---

        # counters
        self.tracker.debug.add(self.id, 'target.counter_on',
                               str(self.tracker.target.counter_on))
        self.tracker.debug.add(self.id, 'target.counter_leave',
                               str(self.tracker.target.counter_leave))
        self.tracker.debug.add(self.id, 'target.interval_leave',
                               str(self.tracker.target.interval_leave))

        # timeouts
        self.tracker.debug.add(self.id, 'target.AS_TARGET_MIN_TIME',
                               str(self.tracker.target.AS_TARGET_MIN_TIME))
        self.tracker.debug.add(self.id, 'target.AS_LOST_MIN_TIME',
                               str(self.tracker.target.AS_LOST_MIN_TIME))
        self.tracker.debug.add(self.id, 'target.BEFORE_TARGET_MIN_TIME',
                               str(self.tracker.target.BEFORE_TARGET_MIN_TIME))
        self.tracker.debug.add(self.id, 'target.ON_TARGET_MAX_VALUE',
                               str(self.tracker.target.ON_TARGET_MAX_VALUE))
        self.tracker.debug.add(self.id, 'target.MIN_MATCH_SCORE',
                               str(self.tracker.target.MIN_MATCH_SCORE))
        self.tracker.debug.add(self.id, 'target.MIN_DETECT_SCORE',
                               str(self.tracker.target.MIN_DETECT_SCORE))

        self.tracker.debug.end(self.id)
