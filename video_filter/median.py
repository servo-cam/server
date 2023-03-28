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
import numpy as np


class MedianFilter:
    def __init__(self, tracker=None):
        """
        Median filter

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.name = "Median"
        self.minFrames = 5
        self.frames = []

    def clear(self):
        """Clear filter"""
        self.frames = []

    def apply(self, frame):
        """
        Apply median filter

        :param frame: frame to apply filter
        :return: frame with applied filter
        """
        if len(self.frames) < self.minFrames:
            self.frames.append(frame)
            return frame
        else:
            self.frames.pop(0)
            self.frames.append(frame)
            median = np.median(self.frames, axis=0).astype(dtype=np.uint8)
            grayMedianFrame = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dframe = cv2.absdiff(frame, grayMedianFrame)
            th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
            dframe = cv2.cvtColor(dframe, cv2.COLOR_GRAY2BGR)
            return dframe
