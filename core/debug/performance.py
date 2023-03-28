#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from tensorflow.config import list_physical_devices


class Performance:
    def __init__(self, tracker=None):
        """
        Performance debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'performance'

    def update(self):
        """Updates the performance debug window."""
        self.tracker.debug.begin(self.id)

        # fps
        self.tracker.debug.add(self.id, 'tracker.fps', str(self.tracker.current_fps))

        # display GPU info
        gpus = list_physical_devices('GPU')
        if len(gpus) > 0:
            for gpu in list_physical_devices('GPU'):
                self.tracker.debug.add(self.id, 'GPU/CPU', "[GPU] " + str(gpu.name) + ", Type:" + str(gpu.device_type))
        else:
            self.tracker.debug.add(self.id, 'GPU/CPU', "NO GPU, USING CPU")

        # ping
        self.tracker.debug.add(self.id, 'remote.ping_video (ms)', str(self.tracker.remote.ping_video))
        self.tracker.debug.add(self.id, 'remote.ping_data (ms)', str(self.tracker.remote.ping_data))
        self.tracker.debug.add(self.id, 'sockets.packets_wait', str(self.tracker.sockets.packets_wait))

        # remote clients
        for ip in self.tracker.remote.clients:
            prefix = '[HOST ' + str(ip) + '] '
            self.tracker.debug.add(self.id, prefix + 'ping_video (ms)', str(self.tracker.remote.clients[ip].ping_video))
            self.tracker.debug.add(self.id, prefix + 'ping_data (ms)', str(self.tracker.remote.clients[ip].ping_data))

        self.tracker.debug.end(self.id)
