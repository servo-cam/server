#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from video_filter.grayscale import GrayscaleFilter
from video_filter.predator import PredatorFilter
from video_filter.nightvision import NightVision
from video_filter.median import MedianFilter


class VideoFilter:
    FILTER_GRAYSCALE = 'GRAYSCALE'
    FILTER_PREDATOR = 'PREDATOR'
    FILTER_NIGHTVISION = 'NIGHTVISION'
    FILTER_MEDIAN = 'MEDIAN'

    def __init__(self, tracker=None):
        """
        Video filter handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

        self.filters = {}
        self.filters[self.FILTER_GRAYSCALE] = GrayscaleFilter(self.tracker)
        self.filters[self.FILTER_PREDATOR] = PredatorFilter(self.tracker)
        self.filters[self.FILTER_NIGHTVISION] = NightVision(self.tracker)
        self.filters[self.FILTER_MEDIAN] = MedianFilter(self.tracker)

        self.input_enabled = {}
        self.output_enabled = {}

    def has_input_filter(self):
        """
        Check if any input filter is enabled

        :return: True if any input filter is enabled, False otherwise
        """
        for name in self.input_enabled:
            if self.input_enabled[name]:
                return True

        return False

    def has_output_filter(self):
        """
        Check if any output filter is enabled

        :return: True if any output filter is enabled, False otherwise
        """
        for name in self.output_enabled:
            if self.output_enabled[name]:
                return True

        return False

    def set_input_filters(self, str):
        """
        Set input filters from string

        :param str: string with filter names separated by comma
        """
        if str == '' or str is None:
            return

        self.input_enabled = {}
        for name in str.split(','):
            self.input_enabled[name] = True

    def set_output_filters(self, str):
        """
        Set output filters from string

        :param str: string with filter names separated by comma
        """
        if str == '' or str is None:
            return

        self.output_enabled = {}
        for name in str.split(','):
            self.output_enabled[name] = True

    def clear(self):
        """Clear all filters"""
        for name in self.filters:
            self.filters[name].clear()

    def apply_input(self, frame):
        """
        Apply input filters

        :param frame: frame to apply filters
        :return: frame with applied filters
        """
        if frame is None:
            return None

        # apply filters
        for name in self.input_enabled:
            if self.input_enabled[name]:
                frame = self.filters[name].apply(frame)

        return frame

    def apply_output(self, frame):
        """
        Apply output filters

        :param frame: frame to apply filters
        :return: frame with applied filters
        """
        if frame is None:
            return None

        # apply filters
        for name in self.output_enabled:
            if self.output_enabled[name]:
                frame = self.filters[name].apply(frame)

        return frame
