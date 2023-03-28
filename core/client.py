#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Client:
    def __init__(self):
        """
        Client object
        """
        self.ip = None
        self.hostname = None
        self.name = None
        self.last_active_time = None
        self.hang_time = None
        self.disconnected = False
        self.removed = False
        self.state = None
        self.ping_video = 0
        self.ping_data = 0
