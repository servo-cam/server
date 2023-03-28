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


class GrayscaleFilter:
    def __init__(self, tracker=None):
        """
        Grayscale filter

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.name = "Grayscale"

    def clear(self):
        """Clear filter"""
        pass

    def apply(self, frame):
        """
        Apply grayscale filter

        :param frame: frame to apply filter
        :return: frame with applied filter
        """
        bg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)
