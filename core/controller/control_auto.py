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
from core.utils import trans


class ControlAuto:
    def __init__(self, tracker=None):
        """
        Auto mode control.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the auto mode control."""
        self.update_target_mode()
        self.update_target_point()
        self.update_action_enable()
        self.update_action_name()
        self.update_action_mode()
        self.update_single_target()
        self.update_target_lock()
        self.update_action_length()
        self.update_action_next_target()

    def toggle_target_mode(self, mode):
        """
        Toggles the target mode.

        :param mode: target mode
        """
        self.tracker.target_mode = mode

        # reset patrol if not patrol mode (requires)
        if mode != self.tracker.TARGET_MODE_PATROL:
            self.tracker.patrol.active = False
            self.tracker.patrol.paused = False

        if mode == self.tracker.TARGET_MODE_OFF:
            # reset all
            self.tracker.action.disable()
            self.tracker.action.stop()
            self.tracker.targeting.reset()

        # update buttons
        self.update_target_mode()

    def toggle_target_point(self, point):
        """
        Toggles the target point.

        :param point: target point
        """
        self.tracker.target_point = point

        # update buttons
        self.update_target_point()

    def toggle_action_enable(self):
        """Toggle the action enable."""
        if self.tracker.action.enabled:
            self.tracker.action.stop()
            self.tracker.action.disable()
        else:
            self.tracker.action.enable()

        # update buttons
        self.update_action_enable()
        self.update_target_lock()

    def toggle_action_name(self, idx):
        """
        Toggle the action name.

        :param idx: action index
        """
        n = 0
        for action in self.tracker.action.actions:
            if n == idx:
                self.tracker.action.auto_name = action
                break
            n += 1
        self.update_action_name()

    def toggle_action_mode(self, idx):
        """
        Toggle the action mode.

        :param idx: action mode index
        """
        n = 0
        for action in self.tracker.action.modes:
            if n == idx:
                self.tracker.action.auto_mode = action
                break
            n += 1
        self.update_action_mode()

    def toggle_single_target(self):
        """Toggle the single target mode."""
        self.tracker.targets.single = not self.tracker.targets.single

        # update buttons
        self.update_single_target()

    def toggle_target_lock(self):
        """Toggle the target lock."""
        self.tracker.targets.locked = not self.tracker.targets.locked

        if self.tracker.targets.locked:
            self.tracker.targets.lock()
        else:
            self.tracker.targets.unlock()

        # update buttons
        self.update_target_lock()

    def change_action_length(self, val):
        """
        Change the action length.

        :param val: action length
        """
        self.tracker.action.length_value = val

    def change_action_next_target(self, val):
        """
        Change the action next target time.

        :param val: action next target time
        """
        self.tracker.action.switch_value = val

    def update_target_mode(self):
        """Update the auto target mode select."""
        for k in self.tracker.window.control_auto['mode']:
            self.tracker.window.control_auto['mode'][k].setChecked(False)
        self.tracker.window.control_auto['mode'][self.tracker.target_mode].setChecked(True)

    def update_target_point(self):
        """Update the auto target point select."""
        for k in self.tracker.window.control_auto['target_point']:
            self.tracker.window.control_auto['target_point'][k].setChecked(False)
        self.tracker.window.control_auto['target_point'][self.tracker.target_point].setChecked(True)

    def update_action_enable(self):
        """Update the auto action enable select."""
        if self.tracker.action.enabled:
            self.tracker.window.control_auto['action_enable'].setChecked(True)
            self.tracker.window.control_auto['action_enable'].setStyleSheet(Style.BTN_DANGER_IMPORTANT)
        else:
            self.tracker.window.control_auto['action_enable'].setChecked(False)
            self.tracker.window.control_auto['action_enable'].setStyleSheet(Style.BTN_DEFAULT)

    def update_action_name(self):
        """Update the auto action name list."""
        self.tracker.window.control_auto['action_name'].setCurrentText(self.tracker.action.auto_name)

    def update_action_mode(self):
        """Update the auto action mode select."""
        n = 0
        for action in self.tracker.action.modes:
            if action == self.tracker.action.auto_mode:
                str = trans('auto.action.mode.' + action)
                self.tracker.window.control_auto['action_mode'].setCurrentText(str)
                break
            n += 1

    # update menu: auto single enable
    def update_single_target(self):
        """Update the auto single target button."""
        if self.tracker.targets.single:
            self.tracker.window.control_auto['single_target'].setChecked(True)
            self.tracker.window.control_auto['single_target'].setStyleSheet(Style.BTN_ACTIVE)
        else:
            self.tracker.window.control_auto['single_target'].setChecked(False)
            self.tracker.window.control_auto['single_target'].setStyleSheet(Style.BTN_DEFAULT)

    # update menu: auto locked enable
    def update_target_lock(self):
        """Update the auto target lock button."""
        if self.tracker.targets.locked:
            self.tracker.window.control_auto['target_lock'].setChecked(True)
        else:
            self.tracker.window.control_auto['target_lock'].setChecked(False)

    def update_action_length(self):
        """Update the auto action length slider."""
        self.tracker.window.control_auto['action_length'].setValue(self.tracker.action.length_value)

    def update_action_next_target(self):
        """Update the auto action next target slider."""
        self.tracker.window.control_auto['action_next_target'].setValue(self.tracker.action.switch_value)
