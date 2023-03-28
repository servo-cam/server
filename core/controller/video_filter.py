#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class VideoFilter:
    def __init__(self, tracker=None):
        """
        Video filter handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the video filter."""
        self.update_menu()

    def toggle_input(self, name):
        """
        Toggles the input filter.

        :param name: input filter name to toggle
        """
        if name in self.tracker.video_filter.input_enabled and self.tracker.video_filter.input_enabled[name]:
            self.tracker.video_filter.input_enabled[name] = False
        else:
            self.tracker.video_filter.input_enabled[name] = True

        self.update_menu()

    def toggle_output(self, name):
        """
        Toggles the output filter.

        :param name: output filter name to toggle
        """
        if name in self.tracker.video_filter.output_enabled and self.tracker.video_filter.output_enabled[name]:
            self.tracker.video_filter.output_enabled[name] = False
        else:
            self.tracker.video_filter.output_enabled[name] = True

        self.update_menu()

    def update(self):
        """Updates the video filters menu."""
        self.update_menu()

    def update_menu(self):
        """Updates the video filters menu."""
        for name in self.tracker.video_filter.filters.keys():
            if name in self.tracker.video_filter.input_enabled and self.tracker.video_filter.input_enabled[name]:
                self.tracker.window.menu['filters.input'][name].setChecked(True)
            else:
                self.tracker.window.menu['filters.input'][name].setChecked(False)

        for name in self.tracker.video_filter.filters.keys():
            if name in self.tracker.video_filter.output_enabled and self.tracker.video_filter.output_enabled[name]:
                self.tracker.window.menu['filters.output'][name].setChecked(True)
            else:
                self.tracker.window.menu['filters.output'][name].setChecked(False)
