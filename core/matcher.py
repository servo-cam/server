#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Matcher:
    def __init__(self, tracker=None):
        """
        Object matching main class

        :param tracker: tracker object
        """
        self.tracker = tracker

    def match_exactly(self, bounding=None, idx=None, identifier=None, check_bounds=False):
        """
        Match exactly params

        :param bounding: count only objects in bounding box
        :param idx: count only object with index
        :param identifier: count only object with identifier
        :param check_bounds: check if object is in bounding box
        :return: object index
        """
        tmp_idx = None
        n = 0
        if self.tracker.objects is None:
            return tmp_idx

        for obj in self.tracker.objects:
            # check score and rest of filters (min score is defined in filter)
            if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_TARGET):
                n += 1
                continue

            if self.tracker.IDX_CENTER not in obj:
                n += 1
                continue

            if idx is None or (idx is not None and n == idx):
                if self.tracker.IDX_ID in obj and (
                        identifier is None or obj[self.tracker.IDX_ID] == identifier):
                    if (not check_bounds or self.tracker.keypoints.in_bounding(
                            obj[self.tracker.IDX_CENTER], bounding)) and self.is_closest(n):
                        tmp_idx = n
                        break
            n += 1
        return tmp_idx

    def match_closest(self, center=None, identifier=None):
        """
        Match closest object

        :param center: match closest object to this center
        :param identifier: match closest object with this identifier
        :return: object index
        """
        if center is None:
            return None

        tmp_idx = None
        if self.tracker.objects is None:
            return tmp_idx

        centers = []
        n = 0
        for obj in self.tracker.objects:

            # check score and rest of filters (min score is defined in filter)
            if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_TARGET):
                n += 1
                continue

            if self.tracker.IDX_CENTER not in obj:
                n += 1
                continue

            if identifier is not None:
                if self.tracker.IDX_ID in obj \
                        and obj[self.tracker.IDX_ID] != identifier:
                    n += 1
                    continue
            centers.insert(n, obj[self.tracker.IDX_CENTER])
            n += 1

        if len(centers) == 0:
            return None

        scores = self.tracker.keypoints.get_center_scores(center, centers)
        idx = self.find_best_score(scores)
        if idx is not None:
            if idx < len(self.tracker.objects):
                tmp_idx = idx

        return tmp_idx

    def is_closest(self, idx):
        """
        Check if object is closest

        :param idx: object index
        :return: True if object is closest
        """
        if self.tracker.objects is None:
            return True

        centers = []
        current = None
        n = 0
        for obj in self.tracker.objects:
            if self.tracker.IDX_CENTER not in obj:
                n += 1
                continue

            # check score and rest of filters (min score is defined in filter)
            if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_TARGET):
                n += 1
                continue

            if n == idx:
                current = obj[self.tracker.IDX_CENTER]

            centers.insert(n, obj[self.tracker.IDX_CENTER])
            n += 1

        if len(centers) == 0:
            return False

        scores = self.tracker.keypoints.get_center_scores(current, centers)
        best_idx = self.find_best_score(scores)
        if best_idx is not None and best_idx == idx:
            return True

        return False

    def find_best_score(self, scores):
        """
        Find best score

        :param scores: scores
        :return: object index with best score
        """
        min = None
        idx = None
        for i in scores:
            if scores[i] is None:
                continue
            if min is None or scores[i] < min:
                min = scores[i]
                idx = i
        return idx
