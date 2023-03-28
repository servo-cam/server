#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Debug:
    def __init__(self, tracker=None):
        """
        Debug handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def toggle(self, id):
        """
        Toggles the debug window.

        :param id: window to toggle
        """
        if id in self.tracker.debug.active and self.tracker.debug.active[id]:
            self.tracker.window.ui.dialogs.close('debug.' + id)
            self.tracker.debug.active[id] = False
        else:
            self.tracker.window.ui.dialogs.open('debug.' + id)
            self.tracker.debug.active[id] = True

        # update menu
        self.update_menu()

    def update_menu(self):
        """Updates the debug menu."""
        for id in self.tracker.debug.ids:
            if id in self.tracker.debug.active and self.tracker.debug.active[id]:
                self.tracker.window.menu['debug.' + id].setChecked(True)
            else:
                self.tracker.window.menu['debug.' + id].setChecked(False)
