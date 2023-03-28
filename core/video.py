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


class Video:
    def __init__(self, tracker=None):
        """
        Video capture handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.loop = 1

    def handle(self, src):
        """
        Handle video source

        :param src: video source
        :return: video capture
        """
        return cv2.VideoCapture(src, cv2.CAP_FFMPEG)
