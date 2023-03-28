#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Command:
    def __init__(self, tracker=None):
        """
        Command handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.initialized = False
        self.current = None
        self.can_send = False

        # current angle
        self.angle = [0, 0]

        # cmd
        self.prev_cmd = [90, 90]
        self.next_cmd = [90, 90]
        self.send_cmd = [False, False]
        self.prev_rest = {}

    def init(self):
        """Initialize default values"""
        self.prev_cmd[0] = self.tracker.servo.ANGLE_START_X
        self.prev_cmd[1] = self.tracker.servo.ANGLE_START_Y
        self.next_cmd[0] = self.tracker.servo.ANGLE_START_X
        self.next_cmd[1] = self.tracker.servo.ANGLE_START_Y

    def prepare(self):
        """Prepare servo params"""
        # convert current delta to angle
        self.angle = self.tracker.servo.delta_to_angle()  # screen view = 100% real camera FOV

        if self.tracker.servo.x:
            self.next_cmd[0] = int(self.angle[0] + (self.tracker.servo.ANGLE_MAX_X / 2))

        if self.tracker.servo.y:
            self.next_cmd[1] = int(self.angle[1] + (self.tracker.servo.ANGLE_MAX_Y / 2))

        # fix min/max angle
        if self.next_cmd[0] < self.tracker.servo.ANGLE_MIN_X:
            self.next_cmd[0] = self.tracker.servo.ANGLE_MIN_X
        elif self.next_cmd[0] > self.tracker.servo.ANGLE_MAX_X:
            self.next_cmd[0] = self.tracker.servo.ANGLE_MAX_X

        if self.next_cmd[1] < self.tracker.servo.ANGLE_MIN_Y:
            self.next_cmd[1] = self.tracker.servo.ANGLE_MIN_Y
        elif self.next_cmd[1] > self.tracker.servo.ANGLE_MAX_Y:
            self.next_cmd[1] = self.tracker.servo.ANGLE_MAX_Y

        # check LIMIT
        if self.next_cmd[0] < self.tracker.servo.ANGLE_LIMIT_MIN_X:
            self.next_cmd[0] = self.tracker.servo.ANGLE_LIMIT_MIN_X
        elif self.next_cmd[0] > self.tracker.servo.ANGLE_LIMIT_MAX_X:
            self.next_cmd[0] = self.tracker.servo.ANGLE_LIMIT_MAX_X

        if self.next_cmd[1] < self.tracker.servo.ANGLE_LIMIT_MIN_Y:
            self.next_cmd[1] = self.tracker.servo.ANGLE_LIMIT_MIN_Y
        elif self.next_cmd[1] > self.tracker.servo.ANGLE_LIMIT_MAX_Y:
            self.next_cmd[1] = self.tracker.servo.ANGLE_LIMIT_MAX_Y

    def build(self):
        """Build command to servo"""
        self.send_cmd[0] = False
        self.send_cmd[1] = False

        # x axis
        if self.prev_cmd[0] != self.next_cmd[0]:
            if self.tracker.servo.ANGLE_STEP_X == 0 \
                    or (self.next_cmd[0] % self.tracker.servo.ANGLE_STEP_X == 0):
                self.send_cmd[0] = True

        # y axis
        if self.prev_cmd[1] != self.next_cmd[1]:
            if self.tracker.servo.ANGLE_STEP_Y == 0 \
                    or (self.next_cmd[1] % self.tracker.servo.ANGLE_STEP_Y == 0):
                self.send_cmd[1] = True

        # sending command
        self.can_send = False
        if self.tracker.servo.x or self.tracker.servo.y:
            if self.send_cmd[0] or self.send_cmd[1]:
                self.can_send = True

        self.prev_cmd[0] = self.next_cmd[0]
        self.prev_cmd[1] = self.next_cmd[1]

    def update(self, action=None):
        """
        Prepare and send command to servo

        :param action: force single action
        """
        # initialize variables
        if not self.initialized:
            self.init()
            self.initialized = True

        # prepare command
        self.prepare()
        self.build()

        # init empty command array
        cmd_ary = []
        prev = []

        # angle
        cmd_ary.append(str(self.prev_cmd[0]))  # x
        cmd_ary.append(str(self.prev_cmd[1]))  # y

        # detected objects count
        if self.tracker.objects is not None:
            c = str(len(self.tracker.objects))
            cmd_ary.append(c)
            prev.append(c)
        else:
            cmd_ary.append('0')
            prev.append('0')

        # actions
        for name in self.tracker.action.actions:
            # if force single action then send command now
            if action == name:
                cmd_ary.append('1')
                prev.append('1')
            else:
                # send state of action if toggled or continuous
                if name in self.tracker.action.toggled and self.tracker.action.toggled[name]:
                    cmd_ary.append('1')
                    prev.append('1')
                else:
                    cmd_ary.append('0')
                    prev.append('0')

        # check with prev and if send allowed
        if not self.can_send:
            if prev == self.prev_rest:
                return  # abort sending if not changed

        self.prev_rest = prev

        # send only if changed
        self.send(','.join(cmd_ary))

    def send(self, command):
        """
        Send command to servo

        :param command: command to send
        """
        # send only if whole command changed
        if command == self.current:
            return

        self.current = command

        if not self.tracker.servo.enable:
            return

        # remote servo TODO: if self.tracker.source == self.tracker.SOURCE_REMOTE and ...
        if self.tracker.servo.remote is not None:
            self.tracker.sockets.send(self.tracker.servo.remote, command)

        # local servo
        if self.tracker.servo.local is not None:
            self.tracker.serial.send(command)

        # stream servo
        if self.tracker.servo.stream is not None:
            self.tracker.stream.send_command(self.tracker.servo.stream, command)

    def reset(self, send=False):
        """
        Reset all values
        :param send: send reset command to servo
        """
        self.angle = [90, 90]

        # cmd
        self.init()
        self.send_cmd = [False, False]
        self.current = None
        self.can_send = False

        if send:
            self.send('90,90,0,0,0,0,0,0,0')
