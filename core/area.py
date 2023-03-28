#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Area:
    def __init__(self, tracker=None):
        """
        Area handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

        self.TYPE_TARGET = 'TARGET'
        self.TYPE_ACTION = 'ACTION'
        self.TYPE_PATROL = 'PATROL'

        self.ids = [self.TYPE_TARGET, self.TYPE_ACTION, self.TYPE_PATROL]

        # world mapping
        self.world = {
            self.TYPE_TARGET: False,
            self.TYPE_ACTION: False,
            self.TYPE_PATROL: False,
        }
        self.enabled = {
            self.TYPE_TARGET: False,
            self.TYPE_ACTION: False,
            self.TYPE_PATROL: False,
        }
        self.areas = {
            self.TYPE_TARGET: [0, 0, 0, 0],
            self.TYPE_ACTION: [0, 0, 0, 0],
            self.TYPE_PATROL: [0, 0, 0, 0],
        }
        self.select = {
            self.TYPE_TARGET: False,
            self.TYPE_ACTION: False,
            self.TYPE_PATROL: False,
        }
        self.rgb = {
            self.TYPE_TARGET: [255, 255, 0],
            self.TYPE_ACTION: [255, 0, 0],
            self.TYPE_PATROL: [127, 0, 255],
        }

        self.draw = False

    def is_enabled(self, mode):
        """
        Check if area is enabled

        :param mode: area mode
        :return: True if enabled
        """
        if mode in self.enabled:
            return self.enabled[mode]
        return False

    def get_area(self, mode):
        """
        Get area bounds

        :param mode: area name
        :return: area bounds
        """
        if mode in self.areas:
            return self.areas[mode]

    def get_middle_y(self, mode):
        """
        Get middle height

        :param mode: area name
        :return: middle height
        """
        if mode in self.areas:
            box = self.areas[mode]
            min_y = box[1]  # y
            max_y = box[1] + box[3]  # y + h
            y1 = min_y + self.tracker.dy
            y2 = y1 + box[3]  # y + delta + h
            if not self.world[mode]:
                return (y1 + y2) / 2 - self.tracker.dy  # with delta
            else:
                return (max_y + min_y) / 2
        return 0.5

    def in_area(self, coords, mode):
        """
        Check if coords are in area

        :param coords: coords to check
        :param mode: area name
        :return: True if in area
        """
        if mode not in self.enabled:
            return True

        box = []
        box.append(self.areas[mode][0])
        box.append(self.areas[mode][1])
        box.append(self.areas[mode][2])
        box.append(self.areas[mode][3])

        # if NOT world position
        if mode not in self.world or not self.world[mode]:
            box[0] -= self.tracker.dx
            box[1] -= self.tracker.dy

        return self.tracker.keypoints.check_bounding(coords, box)

    def render(self):
        """Render areas boxes on screen"""
        for mode in self.ids:
            if self.enabled[mode]:
                box = []
                box.append(self.areas[mode][0])
                box.append(self.areas[mode][1])
                box.append(self.areas[mode][2])
                box.append(self.areas[mode][3])

                if self.tracker.render.simulator:
                    # if NOT world position then add delta transform
                    if not self.world[mode]:
                        box[0] -= self.tracker.dx
                        box[1] -= self.tracker.dy
                elif self.tracker.render.center_lock:
                    # if world position and center lock then add delta transform
                    if self.world[mode]:
                        box[0] -= self.tracker.dx
                        box[1] -= self.tracker.dy

                self.tracker.overlay.draw_area(box, self.rgb[mode], 3)

    def set_coord(self, axis, mode, value):
        """
        Set area coord

        :param axis: key to set
        :param mode: area name
        :param value: value to set
        """
        try:
            coord = float(value)
        except ValueError:
            coord = 0.0
        if mode in self.areas:
            self.areas[mode][axis] = coord

    def can_draw(self):
        """
        Check if can draw an area

        :return: True if can draw
        """
        for mode in self.ids:
            if self.select[mode]:
                return True
        return False

    def on_click(self, coords=None):
        """
        Enable area drawing

        :param coords: mouse coords
        """
        self.draw = self.can_draw()
        if self.draw:
            self.tracker.drawing.start('area')

    def on_release(self, coords=None):
        """
        Finish area drawing

        :param coords:
        """
        if self.draw:
            area = self.tracker.drawing.get_area()
            self.tracker.drawing.stop()

            for mode in self.ids:
                if self.select[mode]:
                    self.areas[mode] = area
                    self.enabled[mode] = True
                    self.select[mode] = False

            self.tracker.controller.control_area.update()
