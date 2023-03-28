#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from datetime import datetime


class Patrol:
    DIR_LEFT = 'LEFT'
    DIR_RIGHT = 'RIGHT'
    INITIAL_COORDS = [0.5, 0.5]
    STEP = 0.02
    TIMEOUT = 500  # resume timeout in ms
    INTERVAL_TIME = 600

    def __init__(self, tracker=None):
        """
        Patrol mode handling class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.active = False
        self.paused = False
        self.interval = False
        self.resume_timer = False
        self.resume_start = None
        self.direction = self.DIR_RIGHT
        self.prev_y = None

    def handle(self):
        """Handle patrol mode"""
        if not self.interval:
            self.start()
        else:
            self.update()

    def cancel(self):
        """Cancel patrol resuming"""
        if self.resume_timer:
            self.pause()
            self.resume_timer = False
            self.resume_start = None

    def resume(self):
        """Resume patrol automatically after timeout (paused after target found)"""
        if not self.resume_timer:
            self.resume_start = datetime.now()
            self.resume_timer = True

    def check(self):
        """Check if patrol is active"""
        if self.resume_timer:
            if (datetime.now() - self.resume_start).seconds > 0:
                self.start()
                self.resume_timer = None

    def update(self):
        """Update patrol mode (every frame)"""
        # if target found then send control to targeting (stop patrolling and start tracking)
        if self.tracker.targets.has_target():
            self.pause()
            self.stop()
            self.tracker.target_mode = self.tracker.TARGET_MODE_FOLLOW
            self.tracker.targeting.is_control = True
            self.tracker.targeting.prev_target = []
            self.tracker.targeting.prev_now = []
            self.tracker.targeting.prev_cam = []
            return
        else:
            # else take control here if no target found (continue patrolling)
            self.unpause()
            self.start()
            self.tracker.targeting.is_control = False
            self.tracker.target_mode = self.tracker.TARGET_MODE_PATROL

        # if paused outside then deactivate here
        if self.is_paused():
            self.deactivate()
            return

        self.activate()

        # check if target is initialized in targeting, if not then create empty one and center it in X and Y axis
        if self.tracker.targeting.target is None:
            self.tracker.targeting.set_target_point(self.INITIAL_COORDS)

        # get max left and right positions
        min_delta = self.tracker.servo.get_min_delta(True)
        max_delta = self.tracker.servo.get_max_delta(True)
        min_coords = self.tracker.servo.get_min_coords(True)
        max_coords = self.tracker.servo.get_max_coords(True)
        max_delta_left = max_delta[0]
        max_delta_right = min_delta[0]

        # check for area limit bounds
        if self.tracker.area.is_enabled(self.tracker.area.TYPE_PATROL):
            # max left and right positions
            area = self.tracker.area.get_area(self.tracker.area.TYPE_PATROL)

            # get y coordinate
            mid = self.tracker.area.get_middle_y(self.tracker.area.TYPE_PATROL)
            if mid is None or mid > max_coords[1] or mid < min_coords[1]:
                mid = 0.5
            self.tracker.targeting.target[1] = mid

            if self.prev_y != self.tracker.targeting.target[1]:
                if self.tracker.area.TYPE_PATROL not in self.tracker.area.world \
                        or not self.tracker.area.world[self.tracker.area.TYPE_PATROL]:
                    self.tracker.dy = 0.5 - self.tracker.targeting.target[1] + 0.001
                else:
                    self.tracker.targeting.target[1] = mid
                    self.tracker.dy = 0.5 - self.tracker.targeting.target[1]
                self.prev_y = self.tracker.targeting.target[1]

            # create tmp box
            a = [area[0], area[1], area[0] + area[2], area[1] + area[3]]
            box_delta = [
                0.5 - a[0],  # x1
                0.5 - a[1],  # y1
                0.5 - a[2],  # x2
                0.5 - a[2]  # y2
            ]

            # add delta if NOT world position
            if self.tracker.area.TYPE_PATROL not in self.tracker.area.world \
                    or not self.tracker.area.world[self.tracker.area.TYPE_PATROL]:
                a[0] = (box_delta[0] * 2) - self.tracker.dx  # required multiply * 2
                a[2] = (box_delta[2] * 2) - self.tracker.dx  # required multiply * 2
                max_delta_left = a[0]
                max_delta_right = a[2]
            else:
                max_delta_left = 0.5 - a[0]
                max_delta_right = 0.5 - a[2]

            # fix min/ max delta
            if max_delta_left > max_delta[0]:
                max_delta_left = max_delta[0]
            elif max_delta_left < min_delta[0]:
                max_delta_left = min_delta[0]

            if max_delta_right > max_delta[0]:
                max_delta_right = max_delta[0]
            elif max_delta_right < min_delta[0]:
                max_delta_right = min_delta[0]

            # switch positions if reversed, max_delta_right should be always negative
            if max_delta_right > max_delta_left:
                tmp_left = max_delta_right
                tmp_right = max_delta_left
                max_delta_left = tmp_left
                max_delta_right = tmp_right

        else:
            self.tracker.targeting.target[1] = 0.5  # center current target in Y axis

        # if direction = right - real angle starts from 90, 90 (center), screen angle starts from 0
        if self.direction == self.DIR_RIGHT:  # real angle from 180 to 0
            # movement from left to right on screen (from right to left in real)
            if self.tracker.dx >= max_delta_right:  # >= -90
                self.tracker.targeting.target[0] += self.STEP  # target x++
                self.tracker.dx -= self.STEP

            # change direction if bound reached
            if self.tracker.dx <= max_delta_right:
                self.tracker.targeting.prev_target = []
                # self.tracker.targeting.target[0] = 0.5  # jump to max x (-90)
                self.tracker.dx = max_delta_right
                self.change_direction()  # switch to left

        # if direction = left - real angle starts from 90, 90 (center), screen angle starts from 0
        elif self.direction == self.DIR_LEFT:  # real angle from 0 to 180
            # movement from right to left on screen (from left to right in real)
            if self.tracker.dx <= max_delta_left:  # <= 90
                self.tracker.targeting.target[0] -= self.STEP  # target x--
                self.tracker.dx += self.STEP

            # change direction if bound reached
            if self.tracker.dx >= max_delta_left:
                self.tracker.targeting.prev_target = []
                # self.tracker.targeting.target[0] = 0.5  # jump to min x (90)
                self.tracker.dx = max_delta_left
                self.change_direction()  # switch to right

    def change_direction(self):
        """Switch direction left <> right"""
        if self.direction == self.DIR_RIGHT:
            self.direction = self.DIR_LEFT
        elif self.direction == self.DIR_LEFT:
            self.direction = self.DIR_RIGHT

    def start(self):
        """Start patrol interval"""
        if not self.interval:
            self.tracker.targeting.cam = self.INITIAL_COORDS  # center camera in X and Y axis
            self.interval = True
            self.resume_timer = False
            self.update()

    def activate(self):
        """Activate patrol"""
        self.active = True

    def deactivate(self):
        """Deactivate patrol"""
        self.active = False

    def pause(self):
        """Pause patrol"""
        self.paused = True

    def unpause(self):
        """Unpause patrol"""
        self.paused = False

    def stop(self):
        """Stop patrol"""
        self.interval = False

    def is_paused(self):
        """
        Return paused status

        :return: True if paused, False otherwise
        """
        return self.paused

    def is_active(self):
        """
        Return activated status

        :return: True if activated, False otherwise
        """
        return self.active
