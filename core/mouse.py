#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtGui import Qt


class Mouse:
    CURSOR_DEFAULT = "default"
    CURSOR_HOVER = "hover"
    CURSOR_MOVE = "move"
    CURSOR_CROSSHAIR = "crosshair"
    CURSOR_WAIT = "wait"
    CURSOR_FORBIDDEN = "forbidden"
    CURSOR_RESIZE = "resize"

    def __init__(self, tracker=None):
        """
        Mouse handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.coords = (0, 0)
        self.prevCoords = (0, 0)
        self.move = False
        self.is_mouse_control = False
        self.mouse_start_coords = [0, 0]
        self.mouse_stop_coords = [0, 0]
        self.mouse_delta = [0, 0]
        self.current_cursor = self.CURSOR_DEFAULT

        # buttons
        self.MOUSE_LEFT = 1
        self.MOUSE_RIGHT = 2
        self.MOUSE_MIDDLE = 3

        # pressed buttons
        self.pressed = {
            self.MOUSE_LEFT: False,
            self.MOUSE_RIGHT: False,
            self.MOUSE_MIDDLE: False
        }

    def click(self, btn):
        """
        On mouse click

        :param btn: button id
        """
        # store pressed button
        self.pressed[btn] = True

        # enable mouse control
        self.mouse_delta = [self.tracker.dx, self.tracker.dy]
        self.mouse_start_coords = self.coords
        self.is_mouse_control = True

        # if control view is auto then send event to targets
        if self.tracker.control_view == self.tracker.CONTROL_VIEW_AUTO:
            self.tracker.targets.on_click(self.coords)
        # if control view is area then send event to area
        elif self.tracker.control_view == self.tracker.CONTROL_VIEW_AREA:
            if self.tracker.area.can_draw():
                self.change_cursor(self.CURSOR_CROSSHAIR)  # update cursor
            self.tracker.area.on_click(self.coords)
        # if manual
        elif self.tracker.control_view == self.tracker.CONTROL_VIEW_MANUAL:
            self.change_cursor(self.CURSOR_MOVE)  # update cursor
            self.tracker.manual.on_click(self.coords)

    def dbl_click(self, btn):
        """
        On mouse double click

        :param btn: button id
        """
        pass

    def release(self, btn):
        """
        On mouse release

        :param btn: button id
        """
        # update cursor
        self.change_cursor(self.CURSOR_DEFAULT)

        # store pressed button
        self.pressed[btn] = False

        # disable mouse control
        self.is_mouse_control = False
        self.mouse_delta = [0, 0]
        self.mouse_start_coords = [0, 0]
        self.mouse_stop_coords = self.coords

        # if control view is area then send event to area
        if self.tracker.control_view == self.tracker.CONTROL_VIEW_AREA:
            self.change_cursor(self.CURSOR_DEFAULT)  # update cursor
            self.tracker.area.on_release(self.coords)
        # if manual
        elif self.tracker.control_view == self.tracker.CONTROL_VIEW_MANUAL:
            self.change_cursor(self.CURSOR_DEFAULT)  # update cursor
            self.tracker.manual.on_release(self.coords)

    def change_cursor(self, cursor):
        """
        Change cursor icon

        :param cursor: cursor name
        """
        if self.current_cursor != cursor:
            self.current_cursor = cursor
            current = None
            if cursor == self.CURSOR_DEFAULT:
                current = Qt.ArrowCursor
            elif cursor == self.CURSOR_MOVE:
                current = Qt.OpenHandCursor
            elif cursor == self.CURSOR_CROSSHAIR:
                current = Qt.CrossCursor
            elif cursor == self.CURSOR_WAIT:
                current = Qt.WaitCursor
            elif cursor == self.CURSOR_FORBIDDEN:
                current = Qt.ForbiddenCursor
            elif cursor == self.CURSOR_RESIZE:
                current = Qt.SizeAllCursor
            elif cursor == self.CURSOR_HOVER:
                current = Qt.PointingHandCursor

            if current is not None:
                self.tracker.window.output.setCursor(current)

    def update(self):
        """On update call"""
        # enable movement only if mouse coords changed
        if self.coords != self.prevCoords:
            self.move = True
            self.prevCoords = self.coords
        else:
            self.move = False

        # if no mouse control then return
        if not self.is_mouse_control or not self.move:
            return

        # if control view is manual then update servo angle
        if self.tracker.control_view == self.tracker.CONTROL_VIEW_MANUAL:

            # update cursor
            self.change_cursor(self.CURSOR_MOVE)

            mouse_delta = [0.5 - self.coords[0], 0.5 - self.coords[1]]
            min_delta = self.tracker.servo.get_min_delta()
            max_delta = self.tracker.servo.get_max_delta()

            # calc delta movement
            delta_movement = [self.coords[0] - self.mouse_start_coords[0],
                              self.coords[1] - self.mouse_start_coords[1]]

            # if simulator or center lock then add delta movement
            if self.tracker.render.simulator or self.tracker.render.center_lock:
                if max_delta[0] >= self.tracker.dx >= min_delta[0]:
                    self.tracker.dx = self.mouse_delta[0] + delta_movement[0]

                if max_delta[1] >= self.tracker.dy >= min_delta[1]:
                    self.tracker.dy = self.mouse_delta[1] + delta_movement[1]
            else:
                # if not then set delta mouse movement only
                if max_delta[0] >= self.tracker.dx >= min_delta[0]:
                    self.tracker.dx = mouse_delta[0]

                if max_delta[1] >= self.tracker.dy >= min_delta[1]:
                    self.tracker.dy = mouse_delta[1]

            # fix min / max
            if self.tracker.dx > max_delta[0]:
                self.tracker.dx = max_delta[0]
            elif self.tracker.dx < min_delta[0]:
                self.tracker.dx = min_delta[0]

            if self.tracker.dy > max_delta[1]:
                self.tracker.dy = max_delta[1]
            elif self.tracker.dy < min_delta[1]:
                self.tracker.dy = min_delta[1]
