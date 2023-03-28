#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Manual:
    def __init__(self, tracker=None):
        """
        Manual control handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.speed = 10
        self.current = {}

    def start_action(self, action):
        """
        Start continuous action

        :param action: action name
        """
        self.current[action] = True

    def stop_action(self, action):
        """
        Stop continuous action

        :param action: action name
        """
        self.current[action] = False

    def stop_all(self):
        """Stop all continuous actions"""
        self.current = {}

    def update(self):
        """Update manual movement"""
        for action in self.current:
            if self.current[action]:
                self.do_action(action)

    def do_action(self, action):
        """
        Handle manual action

        :param action: action name
        """
        # self.tracker.debug.log("MANUAL CONTROL: " + action)
        if action == self.tracker.MOVEMENT_LEFT:
            self.tracker.dx = self.tracker.dx + (self.speed / 1000)
        elif action == self.tracker.MOVEMENT_RIGHT:
            self.tracker.dx = self.tracker.dx - (self.speed / 1000)
        elif action == self.tracker.MOVEMENT_UP:
            self.tracker.dy = self.tracker.dy + (self.speed / 1000)
        elif action == self.tracker.MOVEMENT_DOWN:
            self.tracker.dy = self.tracker.dy - (self.speed / 1000)
        elif action == self.tracker.MOVEMENT_CENTER:
            self.tracker.targeting.center()
        elif action == self.tracker.MOVEMENT_ZOOM_IN:
            self.tracker.render.zoom += 1
        elif action == self.tracker.MOVEMENT_ZOOM_OUT:
            self.tracker.render.zoom -= 1
        elif action == self.tracker.MOVEMENT_SPEED_UP:
            self.speed += 1
        elif action == self.tracker.MOVEMENT_SPEED_DOWN:
            self.speed -= 1

        # fix min / max
        min_delta = self.tracker.servo.get_min_delta()
        max_delta = self.tracker.servo.get_max_delta()

        if self.tracker.render.zoom >= 100:
            self.tracker.render.zoom = 99
        elif self.tracker.render.zoom < 0:
            self.tracker.render.zoom = 0
        if self.speed >= 100:
            self.speed = 99
        elif self.speed < 1:
            self.speed = 1

        if self.tracker.dx > max_delta[0]:
            self.tracker.dx = max_delta[0]
        elif self.tracker.dx < min_delta[0]:
            self.tracker.dx = min_delta[0]

        if self.tracker.dy > max_delta[1]:
            self.tracker.dy = max_delta[1]
        elif self.tracker.dy < min_delta[1]:
            self.tracker.dy = min_delta[1]

    def on_click(self, coords=None):
        """
        Handle mouse click

        :param coords: mouse coords
        """
        pass

    def on_release(self, coords=None):
        """
        Handle mouse release

        :param coords: mouse coords
        """
        pass
