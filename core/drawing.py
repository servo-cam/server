#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Drawing:
    def __init__(self, tracker=None):
        """
        Drawing handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.enabled = False
        self.id = None
        self.area = [0, 0, 0, 0]

    def start(self, id):
        """
        Start drawing

        :param id: drawing id
        """
        self.id = id
        self.enabled = True
        x = self.tracker.mouse.coords[0]
        y = self.tracker.mouse.coords[1]

        # fix coords if simulator
        if self.tracker.render.simulator:
            x -= self.tracker.dx
            y -= self.tracker.dy

        self.area = [x, y, 0, 0]

    def clear(self):
        """Clear drawing"""
        self.enabled = False
        self.id = None
        self.area = [0, 0, 0, 0]

    def stop(self):
        """Stop drawing"""
        self.enabled = False
        self.id = None

    def update(self):
        """Update drawing area (on mouse release))"""
        x = self.tracker.mouse.coords[0]
        y = self.tracker.mouse.coords[1]

        # TODO: fix zoomed coords on zoom

        # fix coords if simulator
        if self.tracker.render.simulator:
            x -= self.tracker.dx
            y -= self.tracker.dy

        self.area[2] = x - self.area[0]
        self.area[3] = y - self.area[1]
        self.render()

    def get_area(self):
        """
        Get current drawing area coords

        :return: area coords
        """
        area = self.area
        if area[2] < 0:
            area[0] += area[2]
            area[2] = abs(area[2])
        if area[3] < 0:
            area[1] += area[3]
            area[3] = abs(area[3])

        # fix area if simulator
        if self.tracker.render.simulator:
            area[0] += self.tracker.dx
            area[1] += self.tracker.dy
        return area

    def render(self):
        """Render drawing"""
        if self.enabled:
            self.tracker.overlay.draw_rectangle(self.area[0], self.area[1], self.area[2], self.area[3], 0, 255, 0, 3)
