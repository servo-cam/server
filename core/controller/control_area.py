#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class ControlArea:
    def __init__(self, tracker=None):
        """
        Area control handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the control area."""
        self.update_enable()
        self.update_world()
        self.update_inputs()

    def toggle_select(self, mode):
        """
        Toggles the area selection.
        :param mode: area to draw
        """
        if self.tracker.area.select[mode]:
            self.tracker.area.select[mode] = False
        else:
            self.tracker.area.select[mode] = True

        # update inputs
        self.update_inputs()

    def toggle_enable(self, mode):
        """
        Toggles the area enable.

        :param mode: area to toggle
        """
        if self.tracker.area.enabled[mode]:
            self.tracker.area.enabled[mode] = False
        else:
            self.tracker.area.enabled[mode] = True

        # update buttons
        self.update_enable()

    def clear(self, mode):
        """
        Clears the area.

        :param mode: area to clear
        """
        self.tracker.area.enabled[mode] = False
        self.tracker.area.world[mode] = False
        self.tracker.area.areas[mode] = [0, 0, 0, 0]

        # update buttons
        self.update_enable()
        self.update_world()

        # update inputs
        self.update_inputs()

    def toggle_world(self, mode):
        """
        Toggles the world mode.

        :param mode: area to toggle
        """
        if self.tracker.area.world[mode]:
            self.tracker.area.world[mode] = False
        else:
            self.tracker.area.world[mode] = True

        # update buttons
        self.update_world()

    def update(self):
        """Updates all."""
        self.update_enable()
        self.update_world()
        self.update_select()
        self.update_inputs()

    def update_enable(self):
        """Updates the area enable buttons."""
        for mode in self.tracker.area.ids:
            if self.tracker.area.enabled[mode]:
                self.tracker.window.control_area[mode + '.enable'].setChecked(True)
            else:
                self.tracker.window.control_area[mode + '.enable'].setChecked(False)

    def update_select(self):
        """Updates the area select buttons."""
        for mode in self.tracker.area.ids:
            if self.tracker.area.select[mode]:
                self.tracker.window.control_area[mode + '.select'].setChecked(True)
            else:
                self.tracker.window.control_area[mode + '.select'].setChecked(False)

    def update_world(self):
        """Updates the area world buttons."""
        for mode in self.tracker.area.ids:
            if self.tracker.area.world[mode]:
                self.tracker.window.control_area[mode + '.world'].setChecked(True)
            else:
                self.tracker.window.control_area[mode + '.world'].setChecked(False)

    def apply(self, id):
        """Applies the area from the inputs."""
        x = self.tracker.window.control_area[id + '.x'].text()
        y = self.tracker.window.control_area[id + '.y'].text()
        w = self.tracker.window.control_area[id + '.w'].text()
        h = self.tracker.window.control_area[id + '.h'].text()

        self.tracker.area.set_coord(0, id, x)
        self.tracker.area.set_coord(1, id, y)
        self.tracker.area.set_coord(2, id, w)
        self.tracker.area.set_coord(3, id, h)

        self.update_inputs()

    def update_inputs(self):
        """Updates the area inputs."""
        for mode in self.tracker.area.ids:
            # inputs
            self.tracker.window.control_area[mode + '.x'].setText(str(round(self.tracker.area.areas[mode][0], 2)))
            self.tracker.window.control_area[mode + '.y'].setText(str(round(self.tracker.area.areas[mode][1], 2)))
            self.tracker.window.control_area[mode + '.w'].setText(str(round(self.tracker.area.areas[mode][2], 2)))
            self.tracker.window.control_area[mode + '.h'].setText(str(round(self.tracker.area.areas[mode][3], 2)))
