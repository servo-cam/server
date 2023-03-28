#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================


import sys
import numpy as np
from PySide6.QtCore import QTimer, Slot
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (QApplication, QMainWindow)
from core.tracker import Tracker
from core.ui.main import UI
from core.threads import RemoteVideoThread, SocketThread, StatusThread


class MainWindow(QMainWindow):

    def __init__(self):
        """App main window"""
        super().__init__()
        self.tracker = Tracker(self)
        self.timer = None

        # setup UI
        self.ui = UI(self)
        self.ui.setup()

        # load model
        self.tracker.controller.internals.toggle_model(self.tracker.model_name)

        # init app
        self.setup()

        self.setWindowTitle('SERVO CAM v{} | build {} | servocam.org'.format(self.tracker.version, self.tracker.build))

        # create remote video capture thread
        self.video_thread = RemoteVideoThread(self)
        self.video_thread.handle_video_signal.connect(self.handle_video)
        self.video_thread.started_signal.connect(lambda: self.tracker.debug.log('[THREAD: VIDEO] Started'))
        self.video_thread.finished_signal.connect(lambda: self.tracker.debug.log('[THREAD: VIDEO] Exited'))
        self.video_thread.start()

        # create socket connection thread
        self.socket_thread = SocketThread(self)
        self.socket_thread.handle_socket_signal.connect(self.handle_socket)
        self.socket_thread.started_signal.connect(lambda: self.tracker.debug.log('[THREAD: SOCKET] Started'))
        self.socket_thread.finished_signal.connect(lambda: self.tracker.debug.log('[THREAD: SOCKET] Exited'))
        self.socket_thread.start()

        # create serial listen thread
        self.status_thread = StatusThread(self)
        self.status_thread.handle_status_signal.connect(self.handle_status)
        self.status_thread.started_signal.connect(lambda: self.tracker.debug.log('[THREAD: STATUS] Started'))
        self.status_thread.finished_signal.connect(lambda: self.tracker.debug.log('[THREAD: STATUS] Exited'))
        self.status_thread.start()

        # show info about encryption
        if self.tracker.encrypt.enabled_data:
            self.tracker.debug.log("[AES ENCRYPTION] Data encryption is enabled")
        if self.tracker.encrypt.enabled_video:
            self.tracker.debug.log("[AES ENCRYPTION] Video stream encryption is enabled")

    def setup(self):
        """Setup app"""
        self.tracker.controller.init(self.tracker.source)  # init tracker with default source
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.tracker.fps)

    def update(self):
        """On frame update"""
        self.tracker.update()

    @Slot(np.ndarray)
    def handle_video(self, frame):
        """
        Handle remote video thread signal

        :param frame: video frame
        """
        self.tracker.render.handle_thread(frame)  # handle remote video

    @Slot(str, str)
    def handle_socket(self, buff, ip):
        """
        Handle socket thread signal

        :param buff: received data
        :param ip: ip address
        """
        self.tracker.sockets.handle_thread(buff, ip)  # handle socket

    @Slot(str)
    def handle_status(self, buff):
        """
        Handle status thread signal

        :param buff: received data
        """
        self.tracker.status.handle_thread(buff)  # handle status

    def keyPressEvent(self, event):
        """
        Handle key press event

        :param event: key event
        """
        super(MainWindow, self).keyPressEvent(event)
        self.tracker.keyboard.on_key_press(event)

    def keyReleaseEvent(self, event):
        """
        Handle key release event

        :param event: key event
        """
        super(MainWindow, self).keyReleaseEvent(event)
        self.tracker.keyboard.on_key_release(event)

    # on close event
    def closeEvent(self, event):
        """
        Handle close event

        :param event: close event
        """
        self.tracker.debug.log("Closing...")
        if self.video_thread is not None:
            self.tracker.debug.log("Waiting for video thread to exit...")
            self.video_thread.exiting = True

        if self.socket_thread is not None:
            self.tracker.debug.log("Waiting for socket thread to exit...")
            self.socket_thread.exiting = True

        if self.status_thread is not None:
            self.tracker.debug.log("Waiting for status thread to exit...")
            self.status_thread.exiting = True

        self.tracker.debug.log("Exiting...")
        event.accept()  # let the window close


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    available_geometry = main_win.screen().availableGeometry()
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center() / 2
    topLeftPoint = QScreen.availableGeometry(QApplication.primaryScreen()).topLeft()
    main_win.resize(available_geometry.width() / 2, available_geometry.height() / 2)
    main_win.show()
    main_win.move(topLeftPoint)

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing...")
