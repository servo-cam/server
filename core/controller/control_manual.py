#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from core.ui.style import Style


class ControlManual:
    def __init__(self, tracker=None):
        """
        Manual mode control.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the manual mode control."""
        self.update_zoom()
        self.update_speed()
        self.update_action_mode()

    def handle(self):
        """Handles the manual mode control."""
        self.update_zoom()
        self.update_speed()

    def change_speed(self, val):
        """Changes the manual control speed."""
        self.tracker.manual.speed = val

    def change_zoom(self, val):
        """Changes the manual control zoom."""
        self.tracker.render.zoom = val

    def movement_begin(self, action):
        """Begins a movement action."""
        self.tracker.manual.start_action(action)
        self.update_zoom()
        self.update_speed()

    def movement_end(self, action):
        """Ends a movement action."""
        self.tracker.manual.stop_action(action)
        self.update_zoom()
        self.update_speed()

    def toggle_action_mode(self, mode):
        """
        Toggles the action mode.

        :param mode: action mode
        """
        checked = self.tracker.window.control_manual['mode'][mode].isChecked()
        if checked:
            self.tracker.action.manual_mode = mode

        # stop all if not toggled mode (?)
        # if mode != 'TOGGLE':
        # self.tracker.action.clear_all()

        # enable / disable action buttons
        self.update_actions()

    def action(self, action):
        """
        Execute an action.

        :param action: action name
        """
        if self.tracker.action.manual_mode == self.tracker.ACTION_MODE_SINGLE:
            self.tracker.action.single(action)
        elif self.tracker.action.manual_mode == self.tracker.ACTION_MODE_TOGGLE:
            self.tracker.action.toggle(action)

        self.update_actions()

    def action_begin(self, action):
        """
        Begin an action.

        :param action: action name
        """
        if self.tracker.action.manual_mode == self.tracker.ACTION_MODE_CONTINUOUS:
            self.tracker.action.begin(action)

    def action_end(self, action):
        """
        Stop an action.

        :param action: action name
        """
        if self.tracker.action.manual_mode == self.tracker.ACTION_MODE_CONTINUOUS:
            self.tracker.action.end(action)

    def update_action_mode(self):
        """Updates the action mode."""
        self.tracker.window.control_manual['mode'][self.tracker.ACTION_MODE_OFF].setChecked(False)
        self.tracker.window.control_manual['mode'][self.tracker.ACTION_MODE_SINGLE].setChecked(False)
        self.tracker.window.control_manual['mode'][self.tracker.ACTION_MODE_CONTINUOUS].setChecked(False)
        self.tracker.window.control_manual['mode'][self.tracker.action.manual_mode].setChecked(True)
        self.update_actions()

    def update_actions(self):
        """Updates the action buttons."""
        # enable / disable actions
        if self.tracker.action.manual_mode == self.tracker.ACTION_MODE_OFF:
            for k in self.tracker.action.actions:
                self.tracker.window.control_manual['action'][k].setDisabled(True)
        else:
            for k in self.tracker.action.actions:
                self.tracker.window.control_manual['action'][k].setDisabled(False)

        # toggled actions colors
        for k in self.tracker.action.actions:
            if (k in self.tracker.action.toggled and self.tracker.action.toggled[k]) \
                    or (k == self.tracker.action.auto_name and self.tracker.action.is_single_action):
                self.tracker.window.control_manual['action'][k].setStyleSheet(Style.BTN_DANGER)
            else:
                self.tracker.window.control_manual['action'][k].setStyleSheet(Style.BTN_DEFAULT)

    def update_speed(self):
        """Updates the manual control speed slider."""
        self.tracker.window.control_manual['speed'].setValue(self.tracker.manual.speed)

    def update_zoom(self):
        """Updates the manual control zoom slider."""
        self.tracker.window.control_manual['zoom'].setValue(self.tracker.render.zoom)
