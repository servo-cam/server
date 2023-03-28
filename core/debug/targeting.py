#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Targeting:
    def __init__(self, tracker=None):
        """
        Targeting debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'targeting'

    def update(self):
        """Updates the targeting debug window."""
        self.tracker.debug.begin(self.id)

        # delta
        self.tracker.debug.add(self.id, 'tracker.dx',
                               str(self.tracker.dx))
        self.tracker.debug.add(self.id, 'tracker.dy',
                               str(self.tracker.dy))

        # coords
        self.tracker.debug.add(self.id, 'targeting.cam',
                               str(self.tracker.targeting.cam))
        self.tracker.debug.add(self.id, 'targeting.now',
                               str(self.tracker.targeting.now))
        # coords[] prev
        self.tracker.debug.add(self.id, 'targeting.prev_cam',
                               str(self.tracker.targeting.prev_cam))
        self.tracker.debug.add(self.id, 'targeting.prev_now',
                               str(self.tracker.targeting.prev_now))

        # current values
        self.tracker.debug.add(self.id, 'targeting.dist_nt',
                               str(self.tracker.targeting.dist_nt))
        self.tracker.debug.add(self.id, 'targeting.perc_nt',
                               str(self.tracker.targeting.perc_nt))
        self.tracker.debug.add(self.id, 'targeting.dist_cn',
                               str(self.tracker.targeting.dist_cn))
        self.tracker.debug.add(self.id, 'targeting.perc_cn',
                               str(self.tracker.targeting.perc_cn))
        self.tracker.debug.add(self.id, 'targeting.move',
                               str(self.tracker.targeting.move))
        self.tracker.debug.add(self.id, 'targeting.speed',
                               str(self.tracker.targeting.speed))
        self.tracker.debug.add(self.id, 'targeting.threshold',
                               str(self.tracker.targeting.threshold))
        self.tracker.debug.add(self.id, 'targeting.power',
                               str(self.tracker.targeting.power))

        # target
        self.tracker.debug.add(self.id, 'targeting.target',
                               str(self.tracker.targeting.target))
        self.tracker.debug.add(self.id, 'targeting.prev_target',
                               str(self.tracker.targeting.prev_target))
        self.tracker.debug.add(self.id, 'targeting.before_target',
                               str(self.tracker.targeting.before_target))

        # state
        self.tracker.debug.add(self.id, 'targeting.started',
                               str(self.tracker.targeting.started))
        self.tracker.debug.add(self.id, 'targeting.is_control',
                               str(self.tracker.targeting.is_control))
        self.tracker.debug.add(self.id, 'targeting.from_patrol',
                               str(self.tracker.targeting.from_patrol))

        # smooth
        self.tracker.debug.add(self.id, 'targeting.SMOOTH_FOLLOW',
                               str(self.tracker.targeting.SMOOTH_FOLLOW))
        self.tracker.debug.add(self.id, 'targeting.SMOOTH_CAMERA',
                               str(self.tracker.targeting.SMOOTH_CAMERA))
        self.tracker.debug.add(self.id, 'targeting.BRAKE',
                               str(self.tracker.targeting.BRAKE))

        # multipliers
        self.tracker.debug.add(self.id, 'targeting.DELAY_MULTIPLIER',
                               str(self.tracker.targeting.DELAY_MULTIPLIER))
        self.tracker.debug.add(self.id, 'targeting.SPEED_MULTIPLIER',
                               str(self.tracker.targeting.SPEED_MULTIPLIER))
        self.tracker.debug.add(self.id, 'targeting.SMOOTH_MULTIPLIER',
                               str(self.tracker.targeting.SMOOTH_MULTIPLIER))

        # mean
        self.tracker.debug.add(self.id, 'targeting.MEAN_TARGET',
                               str(self.tracker.targeting.MEAN_TARGET))
        self.tracker.debug.add(self.id, 'targeting.MEAN_STEP_TARGET',
                               str(self.tracker.targeting.MEAN_STEP_TARGET))
        self.tracker.debug.add(self.id, 'targeting.MEAN_DEPTH_TARGET',
                               str(self.tracker.targeting.MEAN_DEPTH_TARGET))

        self.tracker.debug.add(self.id, 'targeting.MEAN_NOW',
                               str(self.tracker.targeting.MEAN_NOW))
        self.tracker.debug.add(self.id, 'targeting.MEAN_STEP_NOW',
                               str(self.tracker.targeting.MEAN_STEP_NOW))
        self.tracker.debug.add(self.id, 'targeting.MEAN_DEPTH_NOW',
                               str(self.tracker.targeting.MEAN_DEPTH_NOW))

        self.tracker.debug.add(self.id, 'targeting.MEAN_CAM',
                               str(self.tracker.targeting.MEAN_CAM))
        self.tracker.debug.add(self.id, 'targeting.MEAN_STEP_CAM',
                               str(self.tracker.targeting.MEAN_STEP_CAM))
        self.tracker.debug.add(self.id, 'targeting.MEAN_DEPTH_CAM',
                               str(self.tracker.targeting.MEAN_DEPTH_CAM))

        self.tracker.debug.end(self.id)
