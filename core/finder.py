#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Finder:
    def __init__(self, tracker=None):
        """
        Object find handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.match_type = None

    def find(self):
        """
        Find previously detected target

        :return: target index
        """
        self.match_type = None

        if self.tracker.targets.is_locked():  # if target is locked
            idx = self.tracker.targets.idx
            identifier = self.tracker.targets.identifier
            bounding = self.tracker.targets.box_lock
            center = self.tracker.targets.center_last
        else:  # if target is not locked
            idx = self.tracker.targets.idx
            identifier = self.tracker.targets.tmp_identifier
            bounding = self.tracker.targets.box_current
            center = self.tracker.targets.center_current

        current = self.tracker.matcher.match_exactly(bounding, idx, identifier, False)
        if current is not None:
            self.match_type = 'all_1'
            return current

        current = self.tracker.matcher.match_exactly(bounding, None, identifier, True)
        if current is not None:
            self.match_type = 'all_2'
            return current

        current = self.tracker.matcher.match_exactly(bounding, None, identifier, True)
        if current is not None:
            self.match_type = 'curr_id'
            return current

        current = self.tracker.matcher.match_closest(center, identifier)
        if current is not None:
            self.match_type = 'close_id'
            return current

        if (self.tracker.targets.is_search() or not self.tracker.targets.is_locked()
            and not self.tracker.targets.is_single()) or self.tracker.action.is_enabled():
            current = self.tracker.matcher.match_closest(center)
            if current is not None:
                self.match_type = 'close_search'
                return current

    def find_next(self):
        """
        Find next target in X coord

        :return: target index
        """
        current = self.tracker.targets.center_last
        next_idx = None
        idx = 0
        for obj in self.tracker.objects:
            if self.tracker.IDX_CENTER in obj:
                if obj[self.tracker.IDX_CENTER][0] >= current[0] \
                        and idx != self.tracker.targets.idx:
                    next_idx = idx
                    break
            idx += 1

        return next_idx

    def find_prev(self):
        """
        Find previous target in X coord

        :return: target index
        """
        current = self.tracker.targets.center_last
        prev_idx = None
        idx = 0
        for obj in self.tracker.objects:
            if self.tracker.IDX_CENTER in obj:
                if obj[self.tracker.IDX_CENTER][0] <= current[0] \
                        and idx != self.tracker.targets.idx:
                    prev_idx = idx
                    break
            idx += 1

        return prev_idx

    def find_first(self):
        """
        Find first target in X coord

        :return: target index
        """
        min = None
        tmp_idx = None
        idx = 0
        for obj in self.tracker.objects:
            if self.tracker.IDX_CENTER in obj:
                if min is None or obj[self.tracker.IDX_CENTER][0] < min:
                    min = obj[self.tracker.IDX_CENTER][0]
                    tmp_idx = idx
            idx += 1

        return tmp_idx

    def find_last(self):
        """
        Find last target in X coord

        :return: target index
        """
        max = None
        tmp_idx = None
        idx = 0
        for obj in self.tracker.objects:
            if self.tracker.IDX_CENTER in obj:
                if max is None or obj[self.tracker.IDX_CENTER][0] > max:
                    max = obj[self.tracker.IDX_CENTER][0]
                    tmp_idx = idx
            idx += 1

        return tmp_idx
