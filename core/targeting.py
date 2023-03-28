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
    # multipliers
    DELAY_MULTIPLIER = 0.40
    SPEED_MULTIPLIER = 0.1
    SMOOTH_MULTIPLIER = 1.6

    # smoothing
    SMOOTH_FOLLOW = False
    SMOOTH_CAMERA = True
    BRAKE = True

    # mean
    MEAN_TARGET = True
    MEAN_STEP_TARGET = 0.005
    MEAN_DEPTH_TARGET = 2

    MEAN_NOW = True
    MEAN_STEP_NOW = 0.01
    MEAN_DEPTH_NOW = 2

    MEAN_CAM = False
    MEAN_STEP_CAM = 0.01
    MEAN_DEPTH_CAM = 2

    def __init__(self, tracker=None):
        """
        Targeting handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.started = False
        self.from_patrol = False
        self.is_control = True

        self.dist_nt = [0, 0]
        self.dist_cn = [0, 0]
        self.perc_nt = [0, 0]
        self.perc_cn = [0, 0]

        self.move = {
            'UP': False,
            'DOWN': False,
            'LEFT': False,
            'RIGHT': False
        }
        self.speed = [0, 0]
        self.threshold = [0.15, 0.15]
        self.power = [0, 0]

        # target
        self.target = None
        self.before_target = None

        self.cam = [0.5, 0.5]
        self.now = [0.5, 0.5]

        # prev
        self.prev_target = []
        self.prev_cam = []
        self.prev_now = []

    def update(self):
        """On frame update"""
        # prepare initial cam and now points
        self.prepare()

        # choose target object idx
        target_idx = self.tracker.targets.choose()

        # choose or change target point if target is matched
        if self.has_control():
            if self.tracker.targets.has_target():
                self.target = self.tracker.targets.get_target_point(self.tracker.target_point, target_idx)
            else:
                self.target = None

        # if no target then use previous current
        if self.target is None:
            self.target = self.before_target

        # prepare now to target distance and percent value
        if self.target is not None:
            # check allowed target area
            if not self.tracker.area.is_enabled(self.tracker.area.TYPE_TARGET) \
                    or self.tracker.area.in_area(self.target, self.tracker.area.TYPE_TARGET):
                self.before_target = self.target
                self.prepare_position()
            else:
                self.target = None
        else:
            # if no target or target leaved then stop servo - do not move to empty space
            if self.has_control() \
                    and self.tracker.target_mode == self.tracker.TARGET_MODE_FOLLOW \
                    and self.BRAKE \
                    and self.before_target is not None:

                # check allowed target area
                if not self.tracker.area.is_enabled(self.tracker.area.TYPE_TARGET) \
                        or self.tracker.area.in_area(self.cam, self.tracker.area.TYPE_TARGET):
                    self.now[0] = self.cam[0]  # stop servo movement immediately!
                    self.now[1] = self.cam[1]
            else:
                if self.target is not None:
                    self.target[0] = self.cam[0]  # stop servo movement immediately!
                    self.target[1] = self.cam[1]
                self.now[0] = self.cam[0]  # stop servo movement immediately!
                self.now[1] = self.cam[1]

        # prepare now movement power
        self.prepare_power()

        # move current target (now) towards destination target
        if self.target is not None:
            self.update_position()

        self.prepare_movement()  # prepare distance from now to center and delta movement speed and threshold
        self.init_movement()  # init/reset servo movement
        self.handle_prev()  # store previous coords
        self.smooth_coords()  # smooth current coords

        # target mode controller
        if self.tracker.target_mode == self.tracker.TARGET_MODE_PATROL:  # patrol mode
            self.set_control(False)  # disable control here
            self.tracker.patrol.handle()  # handle movement in patrol mode
            if not self.tracker.render.center_lock:
                self.set_movement()
        elif self.tracker.target_mode == self.tracker.TARGET_MODE_FOLLOW:  # follow mode
            self.set_control(True)  # enable control here
            self.set_movement()
            if self.tracker.patrol.is_paused():  # if patrol was activated and it's only paused
                if not self.tracker.targets.has_target():
                    self.tracker.patrol.resume()  # if no target then resume patrol
                    self.tracker.patrol.check()  # check if no need to activate patrol
                else:
                    self.tracker.patrol.cancel()  # if target then cancel patrol

        # if controlled here then handle target detection
        if self.has_control():
            self.tracker.target.update()
        else:
            # if no control here then stop action now!
            if self.tracker.action.is_active():
                self.tracker.action.stop()  # stop action execute

        self.transform_movement()  # move delta

        # if enabled render targeting
        if self.tracker.render.targeting:
            self.render()  # render overlay

    def prepare(self):
        """Prepare initial cam and now points"""
        # locked central point
        if self.tracker.render.center_lock:
            if not self.tracker.render.simulator:
                self.cam = [0.5, 0.5]
            else:
                self.cam = [0.5 - self.tracker.dx, 0.5 - self.tracker.dy]
        else:
            # free look
            self.cam = [0.5 - self.tracker.dx, 0.5 - self.tracker.dy]

        # init now at center
        if not self.started:
            self.now = [0.5, 0.5]
            self.started = True

    def prepare_position(self):
        """Prepare now to target distance and percent value"""
        # distance now <> target
        self.dist_nt = [abs(self.now[0] - self.target[0]),
                        abs(self.now[1] - self.target[1])]

        # percentage distance now <> target
        self.perc_nt = [self.dist_nt[0] * 100,
                        self.dist_nt[1] * 100]

    def prepare_power(self):
        """Prepare now movement power"""
        self.power = [(self.perc_nt[0] * self.DELAY_MULTIPLIER) / 100,
                      (self.perc_nt[1] * self.DELAY_MULTIPLIER) / 100]

    def update_position(self):
        """Move current target (now) towards destination target"""
        if self.SMOOTH_FOLLOW:
            # x axis
            if self.target[0] > self.now[0]:
                self.now[0] += self.power[0]
            elif self.target[0] < self.now[0]:
                self.now[0] -= self.power[0]

            # y axis
            if self.target[1] > self.now[1]:
                self.now[1] += self.power[1]
            elif self.target[1] < self.now[1]:
                self.now[1] -= self.power[1]
        else:
            # direct movement
            self.now = self.target  # TODO: not assign?

        # get min and max coords
        max = self.tracker.servo.get_max_coords(True)  # TODO: maybe real here?
        min = self.tracker.servo.get_min_coords(True)

        # fix only if target is controlled here, without this check patrol will be blocked when bounds reached
        if self.has_control():
            # x axis
            if self.now[0] > max[0]:
                self.now[0] = max[0]
            elif self.now[0] < min[0]:
                self.now[0] = min[0]

            # y axis
            if self.now[1] > max[1]:
                self.now[1] = max[1]
            elif self.now[1] < min[1]:
                self.now[1] = min[1]

    def prepare_movement(self):
        """Prepare distance from now to center and delta movement speed and threshold"""

        # distance cam center <> now
        self.dist_cn = [abs(self.cam[0] - self.now[0]),
                        abs(self.cam[1] - self.now[1])]

        # percentage distance cam center <> now
        self.perc_cn = [self.dist_cn[0] * 100,
                        self.dist_cn[1] * 100]

        # delta movement speed
        self.speed = [(self.perc_cn[0] * self.SPEED_MULTIPLIER) / 100,
                      (self.perc_cn[1] * self.SPEED_MULTIPLIER) / 100]

        # delta movement threshold
        self.threshold = [self.speed[0] * self.SMOOTH_MULTIPLIER,
                          self.speed[1] * self.SMOOTH_MULTIPLIER]

    def init_movement(self):
        """Init servo movement"""
        # reset movement
        self.move = {
            'UP': False,
            'DOWN': False,
            'LEFT': False,
            'RIGHT': False
        }

    def set_movement(self):
        """Enable or disable movement"""
        # x axis
        if self.now[0] < (self.cam[0] - self.threshold[0]):
            self.move['LEFT'] = True
        elif self.now[0] > (self.cam[0] + self.threshold[0]):
            self.move['RIGHT'] = True

        # y axis
        if self.now[1] < (self.cam[1] - self.threshold[1]):
            self.move['UP'] = True
        elif self.now[1] > (self.cam[1] + self.threshold[1]):
            self.move['DOWN'] = True

    def transform_movement(self):
        """Transform movement to servo delta"""
        if self.has_control():
            if not self.tracker.targets.has_target():
                return

        # get min and max delta
        min = self.tracker.servo.get_min_delta(True)
        max = self.tracker.servo.get_max_delta(True)

        # if smooth movement
        if self.SMOOTH_CAMERA:
            if self.move['LEFT']:
                if self.tracker.dx < max[0]:
                    self.tracker.dx += self.speed[0]
            elif self.move['RIGHT']:
                if self.tracker.dx > min[0]:
                    self.tracker.dx -= self.speed[0]
            if self.move['UP']:
                if self.tracker.dy < max[1]:
                    self.tracker.dy += self.speed[1]
            elif self.move['DOWN']:
                if self.tracker.dy > min[1]:
                    self.tracker.dy -= self.speed[1]

        # else if direct movement
        else:
            if self.move['LEFT']:
                if self.tracker.dx < max[0]:
                    self.tracker.dx = 0.5 - self.now[0]
            elif self.move['RIGHT']:
                if self.tracker.dx > min[0]:
                    self.tracker.dx = 0.5 - self.now[0]

            if self.move['UP']:
                if self.tracker.dy < max[1]:
                    self.tracker.dy = 0.5 - self.now[1]
            elif self.move['DOWN']:
                if self.tracker.dy > min[1]:
                    self.tracker.dy = 0.5 - self.now[1]

    def has_target_point(self):
        """
        Check if has target point

        :return: True if has target point
        """
        return self.target is not None

    def has_control(self):
        """
        Check if targeting has control

        :return: True if has control
        """
        return self.is_control

    def set_control(self, state=True):
        """
        Enable or disable control

        :param state: True to enable control
        """
        self.is_control = state

    def set_target_point(self, point):
        """
        Set current target point

        :param point: target point
        """
        self.target = point

    def smooth_coords(self):
        """Smooth with previous coords"""
        # only if has control
        if self.has_control() and self.MEAN_TARGET and self.target is not None:
            self.target = self.tracker.keypoints.get_mean_point(self.prev_target)
        if self.has_control() and self.MEAN_NOW and self.now is not None:
            self.now = self.tracker.keypoints.get_mean_point(self.prev_now)

        # if simulator then disable smooth cam
        if self.has_control() and not self.tracker.render.simulator and self.MEAN_CAM and self.cam is not None:
            self.cam = self.tracker.keypoints.get_mean_point(self.prev_cam)

    def handle_prev(self):
        """Update previous coords"""
        if self.target is not None:
            self.prev_target = self.store_prev(self.target, self.prev_target, self.MEAN_STEP_TARGET,
                                               self.MEAN_DEPTH_TARGET)
        if self.now is not None:
            self.prev_now = self.store_prev(self.now, self.prev_now, self.MEAN_STEP_NOW, self.MEAN_DEPTH_NOW)
        if self.cam is not None:
            self.prev_cam = self.store_prev(self.cam, self.prev_cam, self.MEAN_STEP_CAM, self.MEAN_DEPTH_CAM)

    def store_prev(self, element, ary, tolerance, depth):
        """
        Store previous coord

        :param element: element to store
        :param ary: list to store in
        :param tolerance: tolerance
        :param depth: depth
        :return: list
        """
        if ary is not None and len(ary) > 0:
            if self.tracker.keypoints.get_coord_distance(ary[0], element) < tolerance:
                return ary

        if ary is None:
            return

        ary.insert(0, element)
        if len(ary) > depth:
            ary.pop()
        return ary

    def render(self):
        """Render overlays"""
        if self.tracker.output is None:
            return

        # now
        self.tracker.overlay.draw_circle(self.now[0], self.now[1], 255, 0, 0)

        # now to target
        if self.target is not None:
            self.tracker.overlay.draw_line(self.cam[0], self.cam[1], self.target[0], self.target[1], 255, 0, 0)

        # crosshair
        self.tracker.overlay.draw_crosshair(self.now[0], self.now[1], 255, 0, 0, 3)

        # target
        if self.target is not None:
            self.tracker.overlay.draw_circle(self.target[0], self.target[1], 255, 255, 255)

        # cam
        self.tracker.overlay.draw_circle(self.cam[0], self.cam[1], 255, 255, 0)

        # lock box
        if self.tracker.targets.is_locked():
            if self.tracker.targets.box_lock is not None and self.tracker.targets.box_lock != [0, 0, 0, 0]:
                x, y, width, height = self.tracker.targets.box_lock
                self.tracker.overlay.draw_rectangle(x, y, width, height, 255, 0, 0, 6)

        # area
        self.tracker.area.render()

        # text status
        self.tracker.overlay.draw_status()

    def center(self):
        """Center target"""
        self.reset()

    def reset(self):
        """Reset all values"""
        self.speed = [0, 0]
        self.power = [0, 0]

        # target
        self.target = None
        self.before_target = None

        self.cam = [0.5, 0.5]
        self.now = [0.5, 0.5]

        # prev
        self.prev_target = []
        self.prev_cam = []
        self.prev_now = []

        # delta
        self.tracker.dx = 0
        self.tracker.dy = 0
