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


class Render:
    def __init__(self, tracker=None):
        """
        Render debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'render'

    def update(self):
        """Updates the render debug window."""
        self.tracker.debug.begin(self.id)

        # fps
        self.tracker.debug.add(self.id, 'tracker.fps', str(self.tracker.current_fps))
        self.tracker.debug.add(self.id, 'tracker.ts', str(self.tracker.current_ts))

        # original frame
        if self.tracker.render.orig_frame is not None:
            self.tracker.debug.add(self.id, 'render.orig_frame',
                                   "W: " + str(self.tracker.render.orig_frame.shape[1]) + ", H: " + str(
                                       self.tracker.render.orig_frame.shape[0]))
        else:
            self.tracker.debug.add(self.id, 'render.orig_frame', '-')

        # current frame
        if self.tracker.render.frame is not None:
            self.tracker.debug.add(self.id, 'render.frame',
                                   "W: " + str(self.tracker.render.frame.shape[1]) + ", H: " + str(
                                       self.tracker.render.frame.shape[0]))
        else:
            self.tracker.debug.add(self.id, 'render.frame', '-')

        # states
        self.tracker.debug.add(self.id, 'render.montage_frames',
                               len(self.tracker.render.montage_frames) if self.tracker.render.montage_frames is not None else 0)
        self.tracker.debug.add(self.id, 'render.tracking', str(self.tracker.render.tracking))
        self.tracker.debug.add(self.id, 'render.targeting', str(self.tracker.render.targeting))
        self.tracker.debug.add(self.id, 'render.bounds', str(self.tracker.render.bounds))
        self.tracker.debug.add(self.id, 'render.labels', str(self.tracker.render.labels))
        self.tracker.debug.add(self.id, 'render.text', str(self.tracker.render.text))
        self.tracker.debug.add(self.id, 'render.center_lock', str(self.tracker.render.center_lock))
        self.tracker.debug.add(self.id, 'render.simulator', str(self.tracker.render.simulator))
        self.tracker.debug.add(self.id, 'render.zoom', str(self.tracker.render.zoom))
        self.tracker.debug.add(self.id, 'render.fit', str(self.tracker.render.fit))
        self.tracker.debug.add(self.id, 'render.full_screen', str(self.tracker.render.full_screen))
        self.tracker.debug.add(self.id, 'render.minimized', str(self.tracker.render.minimized))
        self.tracker.debug.add(self.id, 'render.maximized', str(self.tracker.render.maximized))
        self.tracker.debug.add(self.id, 'render.montage', str(self.tracker.render.montage))

        # capture
        if self.tracker.capture is not None and len(self.tracker.capture) > 0:
            for host in self.tracker.capture:
                if type(self.tracker.capture[host]) is not cv2.VideoCapture:
                    continue

                prefix = '# capture[' + host + ']: '
                self.tracker.debug.add(self.id, prefix + 'CAP_PROP_FRAME_WIDTH',
                                       self.tracker.capture[host].get(cv2.CAP_PROP_FRAME_WIDTH))
                self.tracker.debug.add(self.id, prefix + 'CAP_PROP_FRAME_HEIGHT',
                                       self.tracker.capture[host].get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.tracker.debug.add(self.id, prefix + 'CAP_PROP_FPS',
                                       self.tracker.capture[host].get(cv2.CAP_PROP_FPS))
                self.tracker.debug.add(self.id, prefix + 'CAP_PROP_FRAME_COUNT',
                                       self.tracker.capture[host].get(cv2.CAP_PROP_FRAME_COUNT))

        self.tracker.debug.end(self.id)
