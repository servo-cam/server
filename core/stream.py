#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Stream:
    def __init__(self):
        """
        Stream host object
        """
        self.unique_id = None
        self.addr = None
        self.host = None
        self.protocol = None
        self.port = None
        self.name = None
        self.query = None
        self.password = None
        self.disconnected = False
        self.removed = False
        self.state = None
        self.ping_video = 0
        self.ping_data = 0
