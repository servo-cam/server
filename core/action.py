#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Action:
    def __init__(self, tracker=None):
        """
        Action handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.enabled = False  # is auto action enabled
        self.active = False  # is auto action active
        self.is_single_action = False  # tmp flag for single action state
        self.manual_mode = self.tracker.ACTION_MODE_OFF
        self.auto_name = self.tracker.ACTION_A1
        self.auto_mode = self.tracker.ACTION_MODE_SINGLE
        self.switch_value = 20  # next target interval
        self.length_value = 10  # action length
        self.action_counter = 0  # current action counter
        self.target_counter = 0  # current target time counter
        self.toggled = {}  # toggled actions
        self.stopped = False  # tmp stop for single action

        # actions list
        self.actions = [
            self.tracker.ACTION_A1,
            self.tracker.ACTION_A2,
            self.tracker.ACTION_A3,
            self.tracker.ACTION_B4,
            self.tracker.ACTION_B5,
            self.tracker.ACTION_B6,
        ]

        # modes list
        self.modes = [
            self.tracker.ACTION_MODE_SINGLE,
            self.tracker.ACTION_MODE_SERIES,
            self.tracker.ACTION_MODE_CONTINUOUS,
            self.tracker.ACTION_MODE_TOGGLE
        ]

    def begin(self, name):
        """
        Start continuous action

        :param name: action name
        """
        # self.tracker.debug.log("MANUAL CONTINUOUS ACTION (START): " + name)
        self.toggled[name] = True

    def end(self, name):
        """
        Stop continuous action

        :param name: action name
        """
        # self.tracker.debug.log("MANUAL CONTINUOUS ACTION (STOP): " + name)
        self.toggled[name] = False

    def single(self, name, clear=True):
        """
        Start single action

        :param name: action name
        :param clear: if False, do not clear toggled actions
        """
        if not clear:
            self.is_single_action = True
        self.tracker.command.update(name)  # send command now!
        # self.tracker.debug.log("MANUAL SINGLE ACTION: " + name)

    def clear(self):
        """Clear all toggled actions"""
        self.target_counter = 0
        self.is_single_action = False
        self.toggled = {}

    def reset(self):
        """Reset all"""
        self.stop()
        self.clear()

    def start(self):
        """Start auto action"""
        self.active = True
        self.stopped = False  # tmp stop for single action

        if self.auto_mode == self.tracker.ACTION_MODE_SINGLE:
            self.single(self.auto_name, False)  # store state of single action
            self.action_counter = self.length_value - 1  # show monit only for a while
        elif self.auto_mode == self.tracker.ACTION_MODE_CONTINUOUS:
            self.begin(self.auto_name)  # begin continuous action
            self.action_counter = 0
        elif self.auto_mode == self.tracker.ACTION_MODE_TOGGLE:
            self.toggled[self.auto_name] = True  # toggle action
            self.action_counter = 0
        elif self.auto_mode == self.tracker.ACTION_MODE_SERIES:
            self.single(self.auto_name, False)  # store state of single action
            self.action_counter = self.length_value - 1  # needed for show monit for a while

        self.target_counter = 0  # init target counter

        # update actions in manual view
        self.tracker.controller.control_manual.update_actions()

        self.show()

    def stop(self):
        """Stop auto action"""
        if self.auto_mode == self.tracker.ACTION_MODE_CONTINUOUS or self.auto_mode == self.tracker.ACTION_MODE_TOGGLE:
            self.end(self.auto_name)  # end continuous action

        self.active = False
        self.stopped = False  # tmp stop for single action
        self.is_single_action = False  # clear tmp single action state
        self.action_counter = 0
        self.target_counter = 0
        self.hide()
        self.clear()

        # update actions in manual view
        self.tracker.controller.control_manual.update_actions()

    def is_toggled(self, name):
        """
        Check if action is toggled

        :param name: action name
        :return: True if toggled
        """
        return name in self.toggled and self.toggled[name]

    def toggle(self, name):
        """
        Toggle action (manual)
        :param name: action name
        """
        if self.is_toggled(name):
            self.toggled[name] = False
            # self.tracker.debug.log("MANUAL TOGGLED ACTION (STOP): " + name)
        else:
            self.toggled[name] = True
            # self.tracker.debug.log("MANUAL TOGGLED ACTION (START): " + name)

    def enable(self):
        """Enable auto action"""
        self.enabled = True
        if not self.tracker.targets.is_locked():
            self.tracker.targets.locked = True
        self.tracker.debug.log("AUTO ACTION ENABLED")

    def disable(self):
        """Disable auto action"""
        self.enabled = False
        self.is_single_action = False
        self.tracker.debug.log("AUTO ACTION DISABLED")

    def is_active(self):
        """
        Check if action is active (auto)

        :return: True if active
        """
        return self.active

    def is_enabled(self):
        """
        Check if action is enabled (auto)

        :return: True if enabled
        """
        return self.enabled

    def show(self):
        """Show action monit"""
        self.tracker.set_state(self.tracker.STATE_ACTION, True)

    def hide(self):
        """Hide action monit"""
        self.tracker.set_state(self.tracker.STATE_ACTION, False)

    def update(self):
        """Update auto action on frame update"""
        if self.action_counter > self.length_value:
            if self.auto_mode == self.tracker.ACTION_MODE_SINGLE:
                self.action_counter = 0
                self.stopped = True  # tmp stop for single action
                self.is_single_action = False
                self.hide()
            elif self.auto_mode == self.tracker.ACTION_MODE_CONTINUOUS:
                self.action_counter = 0
                self.end(self.auto_name)  # end continuous action
                self.stopped = True  # tmp stop for single action
                self.hide()
                self.tracker.targets.next()  # TODO: check if this is needed
            elif self.auto_mode == self.tracker.ACTION_MODE_SERIES:
                self.hide()
                self.single(self.auto_name, False)  # store state of single action
                self.action_counter = 0

            # update actions in manual view
            self.tracker.controller.control_manual.update_actions()

            # if toggle then do not stop and increment counter to infinity (for monit)
            if self.auto_mode != self.tracker.ACTION_MODE_TOGGLE:
                return

        # increment target counter
        self.target_counter += 1

        # check next target (switch) counter
        if not self.tracker.targets.is_single() and 0 < self.switch_value <= self.target_counter:
            # self.tracker.debug.log("[ACTION] NEXT TARGET")
            self.target_counter = 0
            self.tracker.targets.next()  # next target >>>

        if not self.stopped:
            self.action_counter += 1
            self.show()
