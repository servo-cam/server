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


class NightVision:
    def __init__(self, tracker=None):
        """
        Night vision filter

        :param tracker: tracker object
        """
        self.tracker = tracker

    def clear(self):
        """Clear filter"""
        pass

    def apply(self, image):
        """
        Apply night vision filter

        :param image: image to apply filter
        :return: image with applied filter
        """
        alpha = 1.3
        beta = 40
        h, w = image.shape[:2]
        new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        gray_img = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        blue_img = np.zeros((h, w, 3), dtype='uint8')
        blue_img[:, :, 1] = gray_img
        return blue_img
