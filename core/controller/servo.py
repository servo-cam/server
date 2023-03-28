#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtGui import QAction


class Servo:
    def __init__(self, tracker=None):
        """
        Servo handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the servo."""
        self.update_local_devices()

    def toggle(self, axis):
        """
        Toggles the servo.

        :param axis: axis to toggle
        """
        if axis == 'x':
            if self.tracker.servo.x:
                self.tracker.servo.x = False
            else:
                self.tracker.servo.x = True
        elif axis == 'y':
            if self.tracker.servo.y:
                self.tracker.servo.y = False
            else:
                self.tracker.servo.y = True

        # update menu
        self.update()

    def toggle_enable(self):
        """Toggles the servo enable state."""
        if self.tracker.servo.enable:
            self.tracker.servo.enable = False
            self.tracker.render.center_lock = False
            self.tracker.debug.log('[SERVO] Disabled')
            self.tracker.debug.log('[INFO] Center lock disabled')
        else:
            # reset targeting and command
            self.tracker.targeting.reset()
            self.tracker.command.reset()

            # enable servo
            self.tracker.servo.enable = True
            self.tracker.debug.log('[SERVO] Enabled')

            self.enable_required_params()

        # update render
        self.tracker.controller.render.update()

        # update menu
        self.update()

    def enable_required_params(self):
        """Enables required parameters."""
        # disable simulator if enabled and enable center if disabled
        if self.tracker.render.simulator:
            self.tracker.render.simulator = False
            self.tracker.debug.log('[INFO] Simulator disabled due to servo')
            self.tracker.controller.render.update()
        if not self.tracker.render.center_lock:
            if self.tracker.source == self.tracker.SOURCE_REMOTE \
                    or self.tracker.source == self.tracker.SOURCE_LOCAL \
                    or self.tracker.source == self.tracker.SOURCE_STREAM:
                self.tracker.render.center_lock = True
                self.tracker.debug.log('[INFO] Center lock enabled due to servo')
            self.tracker.controller.render.update()

    def toggle_local(self, port):
        """
        Toggles the local servo.
        :param port: port to toggle
        """
        if self.tracker.window.menu['servo.local'][port].isChecked():
            self.tracker.serial.clear()
            self.tracker.servo.local = port
            self.tracker.serial.port = port

            self.enable_required_params()
        else:
            self.tracker.serial.clear()
            self.tracker.servo.local = None
            self.tracker.serial.port = None

        # update menu
        self.update()

    def toggle_remote(self, ip):
        """
        Toggles the remote servo.

        :param ip: remote IP to toggle
        """
        if self.tracker.window.menu['servo.remote'][ip].isChecked():
            self.tracker.servo.remote = ip
            self.enable_required_params()
        else:
            self.tracker.servo.remote = None

        # update menu
        self.update()

    def toggle_stream(self, unique_id):
        """
        Toggles the stream servo.

        :param unique_id: unique ID to toggle
        """
        if self.tracker.window.menu['servo.stream'][unique_id].isChecked():
            self.tracker.servo.stream = unique_id
            self.enable_required_params()
        else:
            self.tracker.servo.stream = None

        # update menu
        self.update()

    def update_local_devices(self):
        """Updates the local devices."""
        # local serial ports
        ports = self.tracker.window.tracker.serial.get_ports()
        for port in ports:
            if port not in self.tracker.window.menu['servo.local']:
                self.tracker.window.menu['servo.local'][port] = QAction(port, self.tracker.window,
                                                                        checkable=True)
                self.tracker.window.menu['servo.local'][port].triggered.connect(
                    lambda checked=None, port=port: self.tracker.controller.servo.toggle_local(port))
                self.tracker.window.servo_local.addAction(self.tracker.window.menu['servo.local'][port])
                self.tracker.debug.log('[INFO] Serial port detected: {}'.format(port))

        for port in list(self.tracker.window.menu['servo.local']):
            if port not in ports:
                self.tracker.window.servo_local.removeAction(self.tracker.window.menu['servo.local'][port])
                self.tracker.window.menu['servo.local'][port].deleteLater()
                del self.tracker.window.menu['servo.local'][port]
                self.tracker.debug.log('[WARNING] Serial port disconnected: {}'.format(port))
                self.tracker.debug.log('[WARNING] Detaching port: {}'.format(port))
                if port == self.tracker.servo.local:
                    self.tracker.servo.local = None
                    self.tracker.serial.port = None
                    self.tracker.serial.serial = None

    def update_remote(self):
        """Updates the remote devices."""
        for ip in self.tracker.remote.clients:
            if ip not in self.tracker.window.menu['servo.remote']:
                self.tracker.window.menu['servo.remote'][ip] = QAction(ip,
                                                                       self.tracker.window,
                                                                       checkable=True)
                self.tracker.window.menu['servo.remote'][ip].triggered.connect(
                    lambda checked=None, ip=ip: self.toggle_remote(ip))
                self.tracker.window.servo_remote.addAction(self.tracker.window.menu['servo.remote'][ip])

        for ip in list(self.tracker.window.menu['servo.remote']):
            if ip not in self.tracker.remote.clients:
                self.tracker.window.servo_remote.removeAction(self.tracker.window.menu['servo.remote'][ip])
                self.tracker.window.menu['servo.remote'][ip].deleteLater()
                del self.tracker.window.menu['servo.remote'][ip]

        for ip in self.tracker.window.menu['servo.remote']:
            self.tracker.window.menu['servo.remote'][ip].setChecked(False)

        if self.tracker.servo.remote is not None and self.tracker.servo.remote in self.tracker.window.menu[
            'servo.remote']:
            self.tracker.window.menu['servo.remote'][self.tracker.servo.remote].setChecked(True)
            self.enable_required_params()

    def update_stream(self):
        """Updates the stream devices."""
        for unique_id in self.tracker.stream.streams:
            name = unique_id.replace('_', ':')
            if unique_id not in self.tracker.window.menu['servo.stream']:
                self.tracker.window.menu['servo.stream'][unique_id] = QAction(name,
                                                                              self.tracker.window,
                                                                              checkable=True)
                self.tracker.window.menu['servo.stream'][unique_id].triggered.connect(
                    lambda checked=None, unique_id=unique_id: self.toggle_stream(unique_id))
                self.tracker.window.servo_stream.addAction(self.tracker.window.menu['servo.stream'][unique_id])

        for unique_id in list(self.tracker.window.menu['servo.stream']):
            if unique_id not in self.tracker.stream.streams:
                self.tracker.window.servo_stream.removeAction(self.tracker.window.menu['servo.stream'][unique_id])
                self.tracker.window.menu['servo.stream'][unique_id].deleteLater()
                del self.tracker.window.menu['servo.stream'][unique_id]

        for unique_id in self.tracker.window.menu['servo.stream']:
            self.tracker.window.menu['servo.stream'][unique_id].setChecked(False)

        if self.tracker.servo.stream is not None \
                and self.tracker.servo.stream in self.tracker.window.menu['servo.stream']:
            self.tracker.window.menu['servo.stream'][self.tracker.servo.stream].setChecked(True)
            self.enable_required_params()

    def update_local(self):
        """Updates the local devices."""
        self.update_local_devices()

        # local / remote, reset all
        for port in self.tracker.window.menu['servo.local']:
            self.tracker.window.menu['servo.local'][port].setChecked(False)

        # enable by port
        if self.tracker.serial.port is not None and self.tracker.serial.port in self.tracker.window.menu['servo.local']:
            self.tracker.window.menu['servo.local'][self.tracker.serial.port].setChecked(True)
            self.tracker.servo.local = self.tracker.serial.port
            self.enable_required_params()
        else:
            self.tracker.servo.local = None

    def update(self):
        """Updates the menu: servo."""
        # enable on/off
        if self.tracker.servo.enable:
            self.tracker.window.menu['servo.enable'].setChecked(True)
        else:
            self.tracker.window.menu['servo.enable'].setChecked(False)

        # enable / disable axis x
        if self.tracker.servo.x:
            self.tracker.window.menu['servo.axis_x'].setChecked(True)
        else:
            self.tracker.window.menu['servo.axis_x'].setChecked(False)

        # enable / disable axis y
        if self.tracker.servo.y:
            self.tracker.window.menu['servo.axis_y'].setChecked(True)
        else:
            self.tracker.window.menu['servo.axis_y'].setChecked(False)

        self.update_local()
        self.update_remote()
        self.update_stream()
