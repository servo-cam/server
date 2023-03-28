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


class Status:
    def __init__(self, tracker=None):
        """
        Status handling.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.state = None
        self.counter = 0
        self.angle = None
        self.cmd = None
        self.video = False
        self.cmd_send = False
        self.cmd_recv = False
        self.ser_send = False
        self.ser_recv = False

    def handle(self):
        """Handle status update"""
        if self.tracker.window.layout_bottom.isVisible():
            self.update_indicators()

    def update_indicators(self):
        """Updates the status indicators."""
        tmp_state = ''
        if self.tracker.state[self.tracker.STATE_LOCKED]:
            tmp_state = trans('state.' + self.tracker.STATE_LOCKED)
            if self.tracker.state[self.tracker.STATE_TARGET]:
                tmp_state = trans('state.' + self.tracker.STATE_TARGET)
            if self.tracker.state[self.tracker.STATE_ACTION]:
                tmp_state = trans('state.' + self.tracker.STATE_ACTION)
        elif self.tracker.state[self.tracker.STATE_SEARCHING]:
            tmp_state = trans('state.' + self.tracker.STATE_SEARCHING)
        elif self.tracker.state[self.tracker.STATE_LOST]:
            tmp_state = trans('state.' + self.tracker.STATE_LOST)

        if self.state != tmp_state:
            self.tracker.window.status_label['state'].setText(str(tmp_state))

        if self.counter != self.tracker.count_detected():
            self.tracker.window.status_label['counter'].setText(str(self.tracker.count_detected()))

        # cmd
        cmd = self.tracker.command.current

        # angle
        angle = "a: " + str(self.tracker.command.angle[0]) + ',' + str(self.tracker.command.angle[1]) + ' d: ' + str(
            round(self.tracker.dx, 2)) + ',' + str(round(self.tracker.dy, 2)) + ''

        if self.angle != angle:
            self.tracker.window.status_label['angle'].setText(str(angle))

        if self.cmd != cmd:
            self.tracker.window.status_label['cmd'].setText(str(cmd))

        self.state = tmp_state
        self.counter = self.tracker.count_detected()
        self.angle = angle
        self.cmd = cmd

        # video
        if self.tracker.render.orig_frame is not None:
            if self.video is not True:
                self.tracker.window.status_indicator['video'].setStyleSheet(Style.BADGE_ACTIVE)
            self.video = True
        else:
            if self.video is not False:
                self.tracker.window.status_indicator['video'].setStyleSheet(Style.BADGE_DEFAULT)
            self.video = False

        # cmd send
        if self.tracker.sockets.is_send:
            if self.cmd_send is not True:
                self.tracker.window.status_indicator['cmd_send'].setStyleSheet(Style.BADGE_ACTIVE)
            self.cmd_send = True
        else:
            if self.cmd_send is not False:
                self.tracker.window.status_indicator['cmd_send'].setStyleSheet(Style.BADGE_DEFAULT)
            self.cmd_send = False

        # cmd recv
        if self.tracker.sockets.is_recv:
            if self.cmd_recv is not True:
                self.tracker.window.status_indicator['cmd_recv'].setStyleSheet(Style.BADGE_ACTIVE)
            self.cmd_recv = True
        else:
            if self.cmd_recv is not False:
                self.tracker.window.status_indicator['cmd_recv'].setStyleSheet(Style.BADGE_DEFAULT)
            self.cmd_recv = False

        # serial send
        if self.tracker.serial.is_send:
            if self.ser_send is not True:
                self.tracker.window.status_indicator['ser_send'].setStyleSheet(Style.BADGE_ACTIVE)
            self.ser_send = True
        else:
            if self.ser_send is not False:
                self.tracker.window.status_indicator['ser_send'].setStyleSheet(Style.BADGE_DEFAULT)
            self.ser_send = False

        # serial recv
        if self.tracker.serial.is_recv:
            if self.ser_recv is not True:
                self.tracker.window.status_indicator['ser_recv'].setStyleSheet(Style.BADGE_ACTIVE)
            self.ser_recv = True
        else:
            if self.ser_recv is not False:
                self.tracker.window.status_indicator['ser_recv'].setStyleSheet(Style.BADGE_DEFAULT)
            self.ser_recv = False
