#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class ControlFilters:
    def __init__(self, tracker=None):
        """
        Filters control.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the control filters."""
        self.update_classes()

    def apply(self):
        """Applies the filters."""
        # classes
        detect_classes = self.tracker.window.control_filter['detect.classes'].text()
        self.tracker.filter.set_classes(self.tracker.filter.FILTER_DETECT, detect_classes)
        target_classes = self.tracker.window.control_filter['target.classes'].text()
        self.tracker.filter.set_classes(self.tracker.filter.FILTER_TARGET, target_classes)
        action_classes = self.tracker.window.control_filter['action.classes'].text()
        self.tracker.filter.set_classes(self.tracker.filter.FILTER_ACTION, action_classes)

        # min_score
        detect_min_score = self.tracker.window.control_filter['detect.min_score'].text()
        self.tracker.filter.set_min_score(self.tracker.filter.FILTER_DETECT, detect_min_score)
        target_min_score = self.tracker.window.control_filter['target.min_score'].text()
        self.tracker.filter.set_min_score(self.tracker.filter.FILTER_TARGET, target_min_score)
        action_min_score = self.tracker.window.control_filter['action.min_score'].text()
        self.tracker.filter.set_min_score(self.tracker.filter.FILTER_ACTION, action_min_score)

    def update(self):
        """Updates the filters."""
        self.update_classes()

    def update_classes(self):
        """Updates the classes."""
        # classes
        detect_classes = self.tracker.filter.get_classes(self.tracker.filter.FILTER_DETECT)
        self.tracker.window.control_filter['detect.classes'].setText(detect_classes)
        target_classes = self.tracker.filter.get_classes(self.tracker.filter.FILTER_TARGET)
        self.tracker.window.control_filter['target.classes'].setText(target_classes)
        action_classes = self.tracker.filter.get_classes(self.tracker.filter.FILTER_ACTION)
        self.tracker.window.control_filter['action.classes'].setText(action_classes)

        # min_score
        detect_min_score = self.tracker.filter.get_min_score(self.tracker.filter.FILTER_DETECT)
        self.tracker.window.control_filter['detect.min_score'].setText(detect_min_score)
        target_min_score = self.tracker.filter.get_min_score(self.tracker.filter.FILTER_TARGET)
        self.tracker.window.control_filter['target.min_score'].setText(target_min_score)
        action_min_score = self.tracker.filter.get_min_score(self.tracker.filter.FILTER_ACTION)
        self.tracker.window.control_filter['action.min_score'].setText(action_min_score)
