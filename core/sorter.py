#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from datetime import datetime


class Sorter:
    def __init__(self, tracker=None):
        """
        Object sorting handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.prev_boxes = {}
        self.mapping = {}
        self.prev_mapping = {}
        self.max_id = 1
        self.box_max_age = 10

    def add_prev_box(self, idx):
        """
        Add previous bounding box

        :param idx: index of object
        """
        id = self.max_id + 1
        # if ID is already in boxes, but this ID was not in prev box then create new
        while id in self.prev_boxes:
            id += 1

        if self.tracker.objects[idx][self.tracker.IDX_CENTER] is not None:
            self.prev_boxes[id] = {
                'box': self.tracker.objects[idx][self.tracker.IDX_BOX],
                'dt': datetime.now(),
                'c': 0
            }
            self.map_box(id, idx)
            self.max_id = id

    def map_box(self, id, idx):
        """
        Map bound to ID

        :param id: id of mapped object
        :param idx: index of object
        """
        self.mapping[id] = idx
        if id > self.max_id:
            self.max_id = id

    def get_closest_bound(self, idx):
        """
        Find the closest bound

        :param idx: index of object
        :return: id of closest bound
        """
        id = None
        scores = self.tracker.keypoints.get_bounding_scores_dict(self.tracker.objects[idx][self.tracker.IDX_CENTER],
                                                                 self.prev_boxes)
        if len(scores) > 0:
            id = min(scores, key=scores.get)
        if id is not None and id < 0:
            id = None
        return id

    def update_prev_bound(self, idx):
        """
        Update previous bound

        :param idx: index of object
        """
        id = self.get_closest_bound(idx)
        if id is not None:
            c = self.prev_boxes[id]['c'] + 1
            self.prev_boxes[id] = {
                'box': self.tracker.objects[idx][self.tracker.IDX_BOX],
                'dt': datetime.now(),
                'c': c
            }
            self.map_box(id, idx)
        else:
            self.add_prev_box(idx)

    def sort_by_bounds(self):
        """Sort objects by bounds"""
        for idx in range(len(self.tracker.objects)):
            if self.tracker.objects[idx][self.tracker.IDX_SCORE] is not None \
                    and self.tracker.objects[idx][self.tracker.IDX_SCORE] < 0.2:
                continue
            if self.tracker.objects[idx][self.tracker.IDX_CENTER] is not None:
                self.update_prev_bound(idx)

    def clean_prev_boxes(self):
        """Clean unused objects"""
        for idx in range(len(self.tracker.objects)):
            id = self.tracker.objects[idx][self.tracker.IDX_ID]

            if id in self.prev_boxes:
                for tmp_id in self.mapping:
                    old_idx = self.mapping[tmp_id]
                    if old_idx != idx:
                        continue
                    if tmp_id != id:
                        del self.mapping[tmp_id]

    def clear(self):
        """Clear expired objects"""
        for id in list(self.prev_boxes):
            if (datetime.now() - self.prev_boxes[id]['dt']).total_seconds() > self.box_max_age:
                if id in self.prev_boxes:
                    self.prev_boxes[id] = None
                    del self.prev_boxes[id]

    def reset(self):
        """Reset all"""
        self.prev_boxes = {}
        self.mapping = {}
        self.prev_mapping = {}
        self.max_id = 0

    def append_by_bounds(self):
        """Append sorting and ID mapping"""
        self.max_id = 0

        # append sorted initial ID's
        for idx in range(len(self.tracker.objects)):
            self.tracker.objects[idx][self.tracker.IDX_ID] = idx

        self.sort_by_bounds()

        for id in self.mapping:
            idx = self.mapping[id]
            if len(self.tracker.objects) > idx:
                self.tracker.objects[idx][self.tracker.IDX_ID] = id

        self.prev_mapping = self.mapping

        # clean / reset if too many objects
        if self.max_id > 100 or len(self.prev_boxes) > 100 or len(self.mapping) > 100:
            self.prev_boxes = {}
            self.mapping = {}
            self.prev_mapping = {}
            self.max_id = 0

    def sort_by_x(self):
        """Sort objects by X"""
        self.tracker.objects = sorted(self.tracker.objects, key=lambda x: x[self.tracker.IDX_CENTER][0])

    def sort_by_y(self):
        """Sort objects by Y"""
        self.tracker.objects = sorted(self.tracker.objects, key=lambda x: x[self.tracker.IDX_CENTER][1])

    def apply(self):
        """Apply sorting"""
        self.sort_by_x()
        self.append_by_bounds()
        self.clear()
        # objects = self.sort_by_y(objects)
