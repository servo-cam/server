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


class PredatorFilter:
    def __init__(self, tracker=None):
        """
        Predator filter

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.name = "Predator"

    def clear(self):
        """Clear filter"""
        pass

    def apply(self, frame):
        """
        Apply predator filter

        :param frame: frame to apply filter
        :return: frame with applied filter
        """
        if frame.shape[2] == 1:
            gray_mat = frame
        else:
            gray_mat = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.applyColorMap(gray_mat, cv2.COLORMAP_HSV)
