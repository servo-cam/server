#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6 import QtCore


class Keyboard:
    def __init__(self, tracker=None):
        """
        Keyboard handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

    def on_key_release(self, event):
        """
        Handle key release

        :param event: key event
        """
        if self.tracker.control_view == self.tracker.CONTROL_VIEW_MANUAL:
            # manual actions
            if self.tracker.action.manual_mode != self.tracker.ACTION_MODE_OFF:
                if self.tracker.action.manual_mode == self.tracker.ACTION_MODE_CONTINUOUS:
                    if event.key() == QtCore.Qt.Key_1:
                        self.tracker.controller.control_manual.action_end(self.tracker.ACTION_A1)
                    elif event.key() == QtCore.Qt.Key_2:
                        self.tracker.controller.control_manual.action_end(self.tracker.ACTION_A2)
                    elif event.key() == QtCore.Qt.Key_3:
                        self.tracker.controller.control_manual.action_end(self.tracker.ACTION_A3)
                    elif event.key() == QtCore.Qt.Key_4:
                        self.tracker.controller.control_manual.action_end(self.tracker.ACTION_A4)
                    elif event.key() == QtCore.Qt.Key_5:
                        self.tracker.controller.control_manual.action_end(self.tracker.ACTION_A5)
                    elif event.key() == QtCore.Qt.Key_6:
                        self.tracker.controller.control_manual.action_end(self.tracker.ACTION_A6)

    def on_key_press(self, event):
        """
        Handle key press

        :param event: key event
        """
        if self.tracker.control_view == self.tracker.CONTROL_VIEW_MANUAL:
            # movement
            if event.key() == QtCore.Qt.Key_W:
                self.tracker.manual.do_action(self.tracker.MOVEMENT_UP)
            elif event.key() == QtCore.Qt.Key_S:
                self.tracker.manual.do_action(self.tracker.MOVEMENT_DOWN)
            elif event.key() == QtCore.Qt.Key_D:
                self.tracker.manual.do_action(self.tracker.MOVEMENT_RIGHT)
            elif event.key() == QtCore.Qt.Key_A:
                self.tracker.manual.do_action(self.tracker.MOVEMENT_LEFT)

            # manual actions
            if self.tracker.action.manual_mode != self.tracker.ACTION_MODE_OFF:
                # actions
                if self.tracker.action.manual_mode == self.tracker.ACTION_MODE_SINGLE or self.tracker.action.manual_mode == self.tracker.ACTION_MODE_TOGGLE:
                    if event.key() == QtCore.Qt.Key_1:
                        self.tracker.controller.control_manual.action(self.tracker.ACTION_A1)
                        self.tracker.debug.log("SINGLE ACTION: " + self.tracker.ACTION_A1)
                    elif event.key() == QtCore.Qt.Key_2:
                        self.tracker.controller.control_manual.action(self.tracker.ACTION_A2)
                        self.tracker.debug.log("SINGLE ACTION: " + self.tracker.ACTION_A2)
                    elif event.key() == QtCore.Qt.Key_3:
                        self.tracker.controller.control_manual.action(self.tracker.ACTION_A3)
                        self.tracker.debug.log("SINGLE ACTION: " + self.tracker.ACTION_A3)
                    elif event.key() == QtCore.Qt.Key_4:
                        self.tracker.controller.control_manual.action(self.tracker.ACTION_B4)
                        self.tracker.debug.log("SINGLE ACTION: " + self.tracker.ACTION_B4)
                    elif event.key() == QtCore.Qt.Key_5:
                        self.tracker.controller.control_manual.action(self.tracker.ACTION_B5)
                        self.tracker.debug.log("SINGLE ACTION: " + self.tracker.ACTION_B5)
                    elif event.key() == QtCore.Qt.Key_6:
                        self.tracker.controller.control_manual.action(self.tracker.ACTION_B6)
                        self.tracker.debug.log("SINGLE ACTION: " + self.tracker.ACTION_B6)

                elif self.tracker.action.manual_mode == self.tracker.ACTION_MODE_CONTINUOUS:
                    if event.key() == QtCore.Qt.Key_1:
                        self.tracker.controller.control_manual.action_begin(self.tracker.ACTION_A1)
                    elif event.key() == QtCore.Qt.Key_2:
                        self.tracker.controller.control_manual.action_begin(self.tracker.ACTION_A2)
                    elif event.key() == QtCore.Qt.Key_3:
                        self.tracker.controller.control_manual.action_begin(self.tracker.ACTION_A3)
                    elif event.key() == QtCore.Qt.Key_4:
                        self.tracker.controller.control_manual.action_begin(self.tracker.ACTION_B4)
                    elif event.key() == QtCore.Qt.Key_5:
                        self.tracker.controller.control_manual.action_begin(self.tracker.ACTION_B5)
                    elif event.key() == QtCore.Qt.Key_6:
                        self.tracker.controller.control_manual.action_begin(self.tracker.ACTION_B6)

            # auto mode
            elif self.tracker.control_view == self.tracker.CONTROL_VIEW_AUTO:
                pass
                '''
                if event.key() == QtCore.Qt.Key_Escape:
                    self.tracker.action.stop()
                    self.tracker.action.clear()
                elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                    self.tracker.action.start()
                elif event.key() == QtCore.Qt.Key_Space:
                    self.tracker.action.toggle()

                # targets
                elif event.key() == QtCore.Qt.Key_PageUp:
                    self.tracker.targets.next()
                elif event.key() == QtCore.Qt.Key_PageDown:
                    self.tracker.targets.prev()
                elif event.key() == QtCore.Qt.Key_Tab:
                    self.tracker.targets.next()
                elif event.key() == QtCore.Qt.Key_Backtab:
                    self.tracker.targets.prev()
                '''
