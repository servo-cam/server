#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import math


class Keypoints:
    def __init__(self, tracker=None):
        """
        Keypoints handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

    def build_bounding(self, keypoints):
        """
        Build bounding box for object

        :param keypoints: object keypoints
        :return: bounding box
        """
        # build bounding box
        box = [None, None, None, None]
        for point in keypoints:
            tmp = point[self.tracker.IDX_X]
            if box[0] is None or tmp < box[0]:
                box[0] = tmp
            if box[2] is None or tmp > box[2]:
                box[2] = tmp

            tmp = point[self.tracker.IDX_Y]
            if box[1] is None or tmp < box[1]:
                box[1] = tmp
            if box[3] is None or tmp > box[3]:
                box[3] = tmp

        box[2] = box[2] - box[0]  # make width
        box[3] = box[3] - box[1]  # make height
        return box

    def build_center_point(self, idx):
        """
        Build center point for object

        :param idx: predicted object index
        :return: center point
        """
        if self.tracker.IDX_BOX in self.tracker.objects[idx]:
            box = self.tracker.objects[idx][self.tracker.IDX_BOX]
        else:
            box = self.build_bounding(self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS])
        return [
            box[0] + (box[2] / 2),
            box[1] + (box[3] / 2)
        ]

    def in_bounding(self, coords, box, idx=None):
        """
        Check if object center is in bounding box

        :param coords: object center
        :param box: bounding box
        :param idx: predicted object index
        :return: True if object center is in bounding box
        """
        if idx is None:
            return self.check_bounding(coords, box)

        # if multiple boxes passed
        if idx != '*':
            if idx in box:
                return self.check_bounding(coords, box[idx])
        else:
            for n in box:
                if self.check_bounding(coords, box[n]):
                    return True

        return False

    def get_bounding_scores(self, coords, box):
        """
        Get scores for bounding, closest = more score

        If object center is in bounding box, score is calculated by distance from center to bounding box.
        Closer to center = more score.

        :param coords: coords of object center
        :param box: bounding box
        :return: scores dict
        """
        scores = {}
        i = 0
        for item in box:
            if self.check_bounding(coords, item):
                scores[i] = self.get_bounding_score(coords, item)
            i += 1
        return scores

    def get_bounding_scores_dict(self, coords, box):
        """
        Get scores for bounding, closest = more score

        If object center is in bounding box, score is calculated by distance from center to bounding box.
        Closer to center = more score.

        :param coords: coords of object center
        :param box: bounding box
        :return: scores dict
        """
        scores = {}
        for i in box:
            if self.check_bounding(coords, box[i]['box']):
                scores[i] = self.get_bounding_score(coords, box[i]['box'])
            i += 1
        return scores

    def get_center_scores(self, coords, center):
        """
        Get scores for center, closest = more score

        If object center is in bounding box, score is calculated by distance from center to bounding box.
        Closer to center = more score.

        :param coords: coords of object center
        :param center: center of bounding box
        :return: scores dict
        """
        scores = {}
        i = 0
        for item in center:
            scores[i] = self.get_center_score(coords, item)
            i += 1
        return scores

    def check_bounding(self, coords, box):
        """
        Check if object center is in bounding box

        :param coords: coord to check
        :param box: bounding box
        :return: True if object center is in bounding box
        """
        x, y = coords
        box_x, box_y, box_width, box_height = box
        return box_x <= x <= box_x + box_width and box_y <= y <= box_y + box_height

    def get_bounding_score(self, coords, box):
        """
        Get score for bounding, closest = more score

        :param coords: coords to check
        :param box: bounding box
        :return: score
        """
        middle = [
            box[0] + (box[2] / 2),
            box[1] + (box[3] / 2)
        ]
        return math.sqrt(
            math.pow(coords[0] - middle[0], 2) + math.pow(coords[1] - middle[1], 2))  # TODO check if no reverse

    def get_center_score(self, coords, center):
        """
        Get score for center, closest = more score

        :param coords: coords to check
        :param center: center of bounding box
        :return: score
        """
        return math.sqrt(math.pow(coords[0] - center[0], 2) + math.pow(coords[1] - center[1], 2))

    def build_center(self, box):
        """
        Build center point for bounding box

        :param box: bounding box
        :return: center point
        """
        return [box[0] + (box[2] / 2), box[1] + (box[3] / 2)]

    def get_distance(self, x1, y1, x2, y2):
        """
        Get distance between two points

        :param x1: X coord of first point
        :param y1: Y coord of first point
        :param x2: X coord of second point
        :param y2: Y coord of second point
        :return: distance between points
        """
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def get_mean_point(self, coords):
        """
        Get mean point of array of coords

        :param coords: list of coords
        :return: mean point
        """
        if len(coords) == 0:
            return None
        x = 0
        y = 0
        for coord in coords:
            x += coord[0]
            y += coord[1]
        return [x / len(coords), y / len(coords)]

    def get_coord_distance(self, p1, p2):
        """
        Get distance between two points

        :param p1: coords of point 1
        :param p2: coords of point 2
        :return: distance between points
        """
        return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
