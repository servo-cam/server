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


class Console:
    def __init__(self, tracker=None):
        """
        Console handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

    def handle(self, args):
        """
        Handle console

        :param args: console arguments (dict)
        """
        while True:
            frame = self.tracker.render.handle()
            self.tracker.render.cv_render(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.tracker.release()
        cv2.destroyAllWindows()
