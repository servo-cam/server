#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import json
from serial.tools import list_ports  # pip install pyserial
import serial
from datetime import datetime
from core.utils import to_json


class Serial:
    FORMAT_RAW = 'RAW'
    FORMAT_JSON = 'JSON'
    DATA_TYPE_CMD = 'cmd'
    CMD_STATUS = '0'
    END_CHAR = "\n"
    STATUS_CHECK_INTERVAL = 3
    BAUD_RATE = 9600

    def __init__(self, tracker=None):
        """
        Serial port handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.port = None
        self.serial = None
        self.is_send = False
        self.is_recv = False
        self.last_reset = datetime.now()
        self.sending = False
        self.last_status_check = datetime.now()
        self.last_update_list = datetime.now()
        self.check_status = True

        # data format
        self.data_format = self.FORMAT_RAW

    def clear(self):
        """Close serial port and clear data"""
        if self.serial is not None:
            if self.serial.is_open:
                self.serial.close()
                if self.tracker is not None:
                    self.tracker.debug.log('[SERIAL] Serial port closed: ' + str(self.port))
                else:
                    print('[SERIAL] Serial port closed: ' + str(self.port))

        self.port = None
        self.serial = None

    def get_ports(self):
        """
        Get list of available serial ports

        :return: list of ports
        """
        ports = []
        for port in list_ports.comports():
            ports.append(port.device)
        return ports

    def init(self):
        """Initialize serial port"""
        if self.serial is None and self.port is not None:
            try:
                self.serial = serial.Serial(self.port, self.BAUD_RATE)
                # self.serial.timeout = 0.4
                if self.tracker is not None:
                    self.tracker.debug.log('[SERIAL] Serial port opened: ' + str(self.port))
                else:
                    print('[SERIAL] Serial port opened: ' + str(self.port))
            except:
                if self.tracker is not None:
                    self.tracker.debug.log('[ERROR] Serial: init error (opened by other application?)')
                else:
                    print('[ERROR] Serial: init error (opened by other application?)')
                self.serial = None

    def send(self, command):
        """
        Send data to serial port (bytes)

        :param command: data to send
        """
        if self.port is None:
            return

        self.init()
        if self.serial is None:
            return

        if not self.serial.is_open:
            return
        try:
            # convert to json if needed
            if self.data_format == self.FORMAT_JSON:
                command = to_json(command, self.DATA_TYPE_CMD)

            # add end of command termination character
            command += self.END_CHAR
            self.sending = True
            self.serial.write(bytes(command, 'UTF-8'))
            self.sending = False
            self.is_send = True
        except:
            if self.tracker is not None:
                self.tracker.debug.log('[ERROR] Serial: error sending data')
            else:
                print('[ERROR] Serial: error sending data')

    def send_status_check(self):
        """Send status check command"""
        if self.sending:
            return

        # check only in specified seconds period
        if (datetime.now() - self.last_status_check).seconds > self.STATUS_CHECK_INTERVAL:
            self.send(self.CMD_STATUS)
            self.last_status_check = datetime.now()

    def update(self):
        """Update serial ports list and send status check"""
        # update devices menu list
        if (datetime.now() - self.last_update_list).seconds > 5:
            self.tracker.controller.servo.update_local_devices()
            self.last_update_list = datetime.now()

        if self.port is None or self.serial is None or not self.serial.is_open:
            return

        if self.check_status:
            self.send_status_check()

    def listen(self):
        """
        Listen for messages from serial port

        :return: received message
        """
        if self.port is None:
            return

        self.init()
        if self.serial is None:
            return

        if not self.serial.is_open:
            return

        try:
            buff = self.serial.readline().decode('utf-8')[:-2]
            self.is_recv = True
            return buff
        except:
            pass
            # if self.tracker is not None:
            # self.tracker.debug.log('[ERROR] Serial: listening error')
            # else:
            # print('[ERROR] Serial: listening error')

    def handle_thread(self, buff):
        """
        Handle received data from serial port

        :param buff: received data
        """
        if buff is None and buff != '':
            return

        if self.tracker is not None:
            # parse data if json
            if self.data_format == self.FORMAT_JSON:
                try:
                    buff = json.loads(buff)[self.DATA_TYPE_CMD]  # buff is already a decoded UTF-8 string
                except:
                    if self.tracker is not None:
                        self.tracker.debug.log("[SERIAL] Received invalid JSON from " + self.port)
                    else:
                        print("[SERIAL] Received invalid JSON from " + self.port)

            self.tracker.remote_status['-'] = buff

    def reset_state(self):
        """Reset recv/send states"""
        # wait a little before reset
        if (datetime.now() - self.last_reset).microseconds < 100000:
            return

        self.is_send = False
        self.is_recv = False
        self.last_reset = datetime.now()
