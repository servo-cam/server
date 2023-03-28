#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Servo:
    ANGLE_START_X = 90
    ANGLE_START_Y = 90
    ANGLE_MIN_X = 0
    ANGLE_MAX_X = 180
    ANGLE_MIN_Y = 0
    ANGLE_MAX_Y = 180
    ANGLE_STEP_X = 2
    ANGLE_STEP_Y = 2
    ANGLE_MULTIPLIER_X = 1
    ANGLE_MULTIPLIER_Y = 1
    ANGLE_LIMIT_MIN_X = 0
    ANGLE_LIMIT_MAX_X = 180
    ANGLE_LIMIT_MIN_Y = 0
    ANGLE_LIMIT_MAX_Y = 180

    def __init__(self, tracker=None):
        """
        Servo handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.is_client = False
        self.map_fov = False
        self.use_limit = False
        self.enable = True
        self.local = None
        self.remote = None
        self.stream = None
        self.x = True
        self.y = True

    def get_min_coords(self, real=False):
        """
        Get min allowed coords

        :param real: use real camera params
        :return: min allowed coords
        """
        # video file, for video FOV is always 100%, from 0 to 1
        if self.tracker.source == self.tracker.SOURCE_VIDEO or not self.map_fov:
            return [0, 0]

        # camera, real camera params
        if self.use_limit or real:
            return [
                0 - ((self.ANGLE_LIMIT_MAX_X / self.tracker.camera.fov[0] - 1) / 2),
                0 - ((self.ANGLE_LIMIT_MAX_Y / self.tracker.camera.fov[1] - 1) / 2)
            ]
        else:
            return [
                0 - ((self.ANGLE_MAX_X / self.tracker.camera.fov[0] - 1) / 2),
                0 - ((self.ANGLE_MAX_Y / self.tracker.camera.fov[1] - 1) / 2)  # TODO: maybe x
            ]

    def get_max_coords(self, real=False):
        """
        Get max allowed coords

        :param real: use real camera params
        :return: max allowed coords
        """
        # video file, for video FOV is always 100%, from 0 to 1
        if self.tracker.source == self.tracker.SOURCE_VIDEO or not self.map_fov:
            return [1, 1]

        # camera, real camera params
        if self.use_limit or real:
            return [
                1 + ((self.ANGLE_LIMIT_MAX_X / self.tracker.camera.fov[0] - 1) / 2),
                1 + ((self.ANGLE_LIMIT_MAX_Y / self.tracker.camera.fov[1] - 1) / 2)
            ]
        else:
            return [
                1 + ((self.ANGLE_MAX_X / self.tracker.camera.fov[0] - 1) / 2),
                1 + ((self.ANGLE_MAX_Y / self.tracker.camera.fov[1] - 1) / 2)  # TODO: maybe x
            ]

    def get_min_delta(self, real=False):
        """
        Get min allowed delta

        :param real: use real camera params
        :return: min allowed delta
        """
        # video file, for video FOV is always 100%, from 0 to 1
        if self.tracker.source == self.tracker.SOURCE_VIDEO or not self.map_fov:
            return [-0.5, -0.5]

        # camera, real camera params
        if self.use_limit or real:  # TODO: add REAL flag to patrol (?)
            return [
                (-self.ANGLE_LIMIT_MAX_X / self.tracker.camera.fov[0]) / 2,
                (-self.ANGLE_LIMIT_MAX_Y / self.tracker.camera.fov[1]) / 2
            ]
        else:
            return [
                (-self.ANGLE_MAX_X / self.tracker.camera.fov[0]) / 2,
                (-self.ANGLE_MAX_Y / self.tracker.camera.fov[1]) / 2
            ]

    def get_max_delta(self, real=False):
        """
        Get max allowed delta

        :param real: use real camera params
        :return: max allowed delta
        """
        # video file, for video FOV is always 100%, from 0 to 1
        if self.tracker.source == self.tracker.SOURCE_VIDEO or not self.map_fov:
            return [0.5, 0.5]

        # camera, real camera params
        if self.use_limit or real:
            return [
                (self.ANGLE_LIMIT_MAX_X / self.tracker.camera.fov[0]) / 2 - (
                        self.ANGLE_LIMIT_MIN_X / self.tracker.camera.fov[0]),
                (self.ANGLE_LIMIT_MAX_Y / self.tracker.camera.fov[1]) / 2 - (
                        self.ANGLE_LIMIT_MIN_Y / self.tracker.camera.fov[1])
            ]
        else:
            return [
                (self.ANGLE_MAX_X / self.tracker.camera.fov[0]) / 2,
                (self.ANGLE_MAX_Y / self.tracker.camera.fov[1]) / 2
            ]

    def delta_to_angle(self, delta=None, real=False):
        """
        Convert delta to servo angle

        :param delta: initial delta
        :param real: use real camera params
        :return: servo angle
        """
        if delta is None:
            delta = [self.tracker.dx, self.tracker.dy]

        # video file, for video FOV is always 100%, from 0 to 1
        if self.tracker.source == self.tracker.SOURCE_VIDEO or not self.map_fov:
            if self.use_limit or real:
                return [
                    round(float(delta[0] * self.ANGLE_LIMIT_MAX_X)),
                    round(float(delta[1] * self.ANGLE_LIMIT_MAX_Y))
                ]
            else:
                return [
                    round(float(delta[0] * self.ANGLE_MAX_X)),
                    round(float(delta[1] * self.ANGLE_MAX_Y))
                ]

        # camera, real camera params
        return [
            round(float(delta[0] * self.tracker.camera.fov[0]) * self.ANGLE_MULTIPLIER_X),
            round(float(delta[1] * self.tracker.camera.fov[1]) * self.ANGLE_MULTIPLIER_Y)
        ]

    def point_to_angle(self, coords, real=False):
        """
        Convert point coords to servo angle

        :param coords: initial coords
        :param real: use real camera params
        :return: servo angle
        """
        # video file, for video FOV is always 100%, from 0 to 1
        if self.tracker.source == self.tracker.SOURCE_VIDEO or not self.map_fov:
            if self.use_limit or real:
                return [
                    round(float((0.5 - coords[0]) * self.ANGLE_LIMIT_MAX_X)),
                    -round(float((0.5 - coords[1]) * self.ANGLE_LIMIT_MAX_Y))
                ]
            else:
                return [
                    round(float((0.5 - coords[0]) * self.ANGLE_MAX_X)),
                    -round(float((0.5 - coords[1]) * self.ANGLE_MAX_Y))
                ]

        # camera, real camera params
        return [
            round(float((0.5 - coords[0]) * self.tracker.camera.fov[0] * self.ANGLE_MULTIPLIER_X)),
            -round(float((0.5 - coords[1]) * self.tracker.camera.fov[1] * self.ANGLE_MULTIPLIER_Y))
        ]
