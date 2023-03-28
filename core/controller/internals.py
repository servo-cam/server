#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Internals:
    def __init__(self, tracker=None):
        """
        Core elements handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the internals."""
        self.update_model()
        self.update_disabled()

    def toggle_model(self, model):
        """
        Toggles the model.

        :param model: model to toggle
        """
        self.tracker.switch_model(model)

        # update menu
        self.update_model()

    def toggle_disabled(self):
        """Toggles the disabled state."""
        if self.tracker.disabled:
            self.tracker.disabled = False
        else:
            self.tracker.disabled = True

        # update menu
        self.update_disabled()

    def update_model(self):
        """Updates the model menu."""
        for k in self.tracker.window.menu['model']:
            self.tracker.window.menu['model'][k].setChecked(False)
        if self.tracker.model_name is None or self.tracker.model_name == 'none':
            self.tracker.window.menu['model']['none'].setChecked(True)
        else:
            self.tracker.window.menu['model'][self.tracker.model_name].setChecked(True)

    def update_disabled(self):
        """Updates the disabled menu item."""
        if self.tracker.disabled:
            self.tracker.window.menu['app']['disabled'].setChecked(True)
        else:
            self.tracker.window.menu['app']['disabled'].setChecked(False)
