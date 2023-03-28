#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import cv2


class Camera:
    def __init__(self, tracker=None):
        """
        Camera handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.idx = 0
        self.tmp_idx = None
        self.csi = False
        self.serial = False
        self.fov = [100, 68]
        self.width = 640
        self.height = 480
        self.fps = 30
        self.max_local_idx = -1

    def is_csi(self, index):
        """
        Check if camera is CSI camera

        :param index: camera index
        :return: True if CSI camera
        """
        return index == self.max_local_idx + 1

    def is_serial(self, index):
        """
        Check if camera is serial camera

        :param index: camera index
        :return: True if serial camera
        """
        return index == self.max_local_idx + 2

    def get_indexes(self):
        """
        Get camera indexes

        :return: list of camera indexes
        """

        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 10
        try:
            while i > 0:
                cap = cv2.VideoCapture(index)
                if cap.read()[0]:
                    arr.append(index)
                    cap.release()
                index += 1
                i -= 1
        except:
            pass

        self.max_local_idx = len(arr) - 1  # save max local index, if no camera is found, this will be -1

        return arr

    def handle(self, idx=0):
        """
        Handle camera stream

        :param idx: camera index
        :return: camera stream
        """
        capture = cv2.VideoCapture(idx)
        if self.width is not None and self.height is not None and self.width > 0 and self.height > 0:
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if self.fps is not None and self.fps > 0:
            capture.set(cv2.CAP_PROP_FPS, self.fps)
        return capture
