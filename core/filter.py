#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Filter:
    FILTER_DETECT = 'DETECT'
    FILTER_TARGET = 'TARGET'
    FILTER_ACTION = 'ACTION'

    def __init__(self, tracker=None):
        """
        Filter handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.filters = {
            self.FILTER_DETECT: {
                'classes': [],
                'min_score': 0.5
            },
            self.FILTER_TARGET: {
                'classes': [],
                'min_score': 0.5
            },
            self.FILTER_ACTION: {
                'classes': [],
                'min_score': 0.5
            }
        }
        self.classes = ['person']

    def get_classes(self, mode):
        """
        Get classes as string

        :param mode: filter mode
        :return: classes parsed as string
        """
        return ','.join(self.filters[mode]['classes'])

    def set_classes(self, mode, classes):
        """
        Set classes from string

        :param mode: filter mode
        :param classes: classes parsed as string
        """
        if classes is None:
            self.filters[mode]['classes'] = []
            return
        self.filters[mode]['classes'] = classes.split(',')
        if '' in self.filters[mode]['classes']:
            self.filters[mode]['classes'].remove('')

    def get_min_score(self, mode):
        """
        Get min score as string

        :param mode: filter mode
        :return: min score parsed as string
        """
        return str(self.filters[mode]['min_score'])

    def set_min_score(self, mode, min_score):
        """
        Set min score from string

        :param mode: filter mode
        :param min_score: min score parsed as string
        """
        try:
            self.filters[mode]['min_score'] = float(min_score)
        except ValueError:
            self.filters[mode]['min_score'] = 0.0

    def is_allowed(self, obj, mode):
        """
        Check if object is allowed to detect

        :param obj: predicted object
        :param mode: filter mode
        :return: True if allowed
        """
        if obj is None:
            return False

        # on detect
        if mode == self.FILTER_DETECT:
            if obj[self.tracker.IDX_SCORE] < self.filters[mode]['min_score']:
                return False

            if self.filters[mode]['classes'] is not None and len(self.filters[mode]['classes']) > 0:
                if obj[self.tracker.IDX_CLASS] not in self.filters[mode]['classes']:
                    return False

        # on target
        elif mode == self.FILTER_TARGET:
            if obj[self.tracker.IDX_SCORE] < self.filters[mode]['min_score']:
                return False

            if self.filters[mode]['classes'] is not None and len(self.filters[mode]['classes']) > 0:
                if obj[self.tracker.IDX_CLASS] not in self.filters[mode]['classes']:
                    return False

            if self.tracker.area.is_enabled(self.tracker.area.TYPE_TARGET) \
                    and not self.tracker.area.in_area(obj[self.tracker.IDX_CENTER],
                                                      self.tracker.area.TYPE_TARGET):
                return False

        # on action
        elif mode == self.FILTER_ACTION:
            if obj[self.tracker.IDX_SCORE] < self.filters[mode]['min_score']:
                return False

            if self.filters[mode]['classes'] is not None and len(self.filters[mode]['classes']) > 0:
                if obj[self.tracker.IDX_CLASS] not in self.filters[mode]['classes']:
                    return False

            if self.tracker.area.is_enabled(self.tracker.area.TYPE_ACTION) \
                    and not self.tracker.area.in_area(obj[self.tracker.IDX_CENTER],
                                                      self.tracker.area.TYPE_ACTION):
                return False

        return True
