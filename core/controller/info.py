#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import webbrowser


class Info:
    def __init__(self, tracker=None):
        """
        Info handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def toggle(self, id):
        """
        Toggles the info window.

        :param id: window to toggle
        """
        if id in self.tracker.info.active and self.tracker.info.active[id]:
            self.tracker.window.ui.dialogs.close('info.' + id)
            self.tracker.info.active[id] = False
        else:
            self.tracker.window.ui.dialogs.open('info.' + id)
            self.tracker.info.active[id] = True

        # update menu
        self.update_menu()

    def goto_website(self):
        """Opens the project website."""
        webbrowser.open(self.tracker.www)

    def goto_update(self):
        """Opens the project download page."""
        webbrowser.open(self.tracker.www + '/download')

    def update_menu(self):
        """Updates the info menu."""
        for id in self.tracker.info.ids:
            if id in self.tracker.info.active and self.tracker.info.active[id]:
                self.tracker.window.menu['info.' + id].setChecked(True)
            else:
                self.tracker.window.menu['info.' + id].setChecked(False)
