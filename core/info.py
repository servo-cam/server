#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Info:
    def __init__(self, tracker=None):
        self.tracker = tracker

        # prepare info ids
        self.ids = ['about', 'change_log']
        self.active = {}

        # prepare active
        for id in self.ids:
            self.active[id] = False
