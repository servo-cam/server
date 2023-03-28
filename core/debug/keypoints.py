#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Keypoints:
    def __init__(self, tracker=None):
        """
        Keypoints debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'keypoints'

    def update(self):
        """Updates the keypoints debug window."""
        self.tracker.debug.begin(self.id)

        # sorter
        self.tracker.debug.add(self.id, 'sorter.prev_boxes', str(self.tracker.sorter.prev_boxes))
        self.tracker.debug.add(self.id, 'sorter.mapping', str(self.tracker.sorter.mapping))
        self.tracker.debug.add(self.id, 'sorter.prev_mapping', str(self.tracker.sorter.prev_mapping))
        self.tracker.debug.add(self.id, 'sorter.max_id', str(self.tracker.sorter.max_id))

        # predictions
        for i, obj in enumerate(self.tracker.objects):
            prefix = '[' + str(i) + '] '
            if self.tracker.IDX_ID in obj:
                self.tracker.debug.add(self.id, prefix + 'id', str(obj[self.tracker.IDX_ID]))
            if self.tracker.IDX_CLASS in obj:
                self.tracker.debug.add(self.id, prefix + 'class', str(obj[self.tracker.IDX_CLASS]))
            if self.tracker.IDX_SCORE in obj:
                self.tracker.debug.add(self.id, prefix + 'score', str(obj[self.tracker.IDX_SCORE]))
            if self.tracker.IDX_BOX in obj:
                self.tracker.debug.add(self.id, prefix + 'box', str(obj[self.tracker.IDX_BOX]))
            if self.tracker.IDX_CENTER in obj:
                self.tracker.debug.add(self.id, prefix + 'center', str(obj[self.tracker.IDX_CENTER]))
            if self.tracker.IDX_KEYPOINTS in obj:
                for j, kp in enumerate(obj[self.tracker.IDX_KEYPOINTS]):
                    self.tracker.debug.add(self.id, prefix + ' kp ' + str(j), str(kp))

        self.tracker.debug.end(self.id)
