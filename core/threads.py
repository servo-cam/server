#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import time
import numpy as np
from PySide6.QtCore import QThread, Signal


# remote video thread
class RemoteVideoThread(QThread):
    def __init__(self, window):
        """
        Remote video thread
        :param window: main window object
        """
        super(RemoteVideoThread, self).__init__()
        self.exiting = False
        self.window = window

    started_signal = Signal()
    finished_signal = Signal()
    handle_video_signal = Signal(np.ndarray)

    def run(self):
        """Run thread"""
        self.started_signal.emit()  # send signal on thread start
        while not self.exiting:
            if self.isInterruptionRequested():
                break

            # handle only in remote mode and if remote is active
            if self.window.tracker.source != self.window.tracker.SOURCE_REMOTE:
                time.sleep(0.01)
                continue

            if self.window.tracker.remote.active:
                self.window.tracker.capture = self.window.tracker.handle(self.window.tracker.SOURCE_REMOTE)
                for ip in self.window.tracker.capture:
                    # single view only, show only current. montages are handled in separate way
                    if ip == self.window.tracker.remote_ip:
                        frame = self.window.tracker.capture[ip]
                        self.handle_video_signal.emit(frame)  # signal to handle video frame

        self.finished_signal.emit()  # send signal on thread exit


# socket thread
class SocketThread(QThread):
    def __init__(self, window):
        """
        Socket thread
        :param window: main window object
        """
        super(SocketThread, self).__init__()
        self.exiting = False
        self.window = window

    started_signal = Signal()
    finished_signal = Signal()
    handle_socket_signal = Signal(str, str)

    def run(self):
        """Run thread"""
        self.started_signal.emit()  # send signal on thread start
        while not self.exiting:
            if self.isInterruptionRequested():
                break

            # handle only in remote mode
            if self.window.tracker.source != self.window.tracker.SOURCE_REMOTE:
                time.sleep(0.01)
                continue
            if self.window.tracker.remote_ip is not None:
                buff = self.window.tracker.sockets.listen()
                if buff is not None:
                    self.handle_socket_signal.emit(buff.decode('utf-8'),
                                                   self.window.tracker.remote_ip)  # signal to handle socket message
            else:
                time.sleep(0.01)
                continue

        self.finished_signal.emit()  # send signal on thread exit


# status check thread
class StatusThread(QThread):
    def __init__(self, window):
        """
        Status thread
        :param window: main window object
        """
        super(StatusThread, self).__init__()
        self.exiting = False
        self.window = window

    started_signal = Signal()
    finished_signal = Signal()
    handle_status_signal = Signal(str)

    def run(self):
        """Run thread"""
        self.started_signal.emit()  # send signal on thread start
        while not self.exiting:
            if self.isInterruptionRequested():
                break

            if not self.window.tracker.status.can_listen():
                time.sleep(0.01)
                continue

            buff = self.window.tracker.status.listen()
            if buff is not None:
                self.handle_status_signal.emit(buff)  # signal to handle serial message

        self.finished_signal.emit()  # send signal on thread exit
