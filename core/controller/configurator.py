#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from core.utils import trans


class Configurator:
    def __init__(self, tracker=None):
        """
        Configuration edit handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def toggle(self, id):
        """
        Toggles the configurator.
        :param id: configurator id
        """
        if id in self.tracker.configurator.active and self.tracker.configurator.active[id]:
            self.tracker.window.ui.dialogs.close('config.' + id)
            self.tracker.configurator.active[id] = False
        else:
            self.tracker.configurator.load(id)
            self.tracker.window.ui.dialogs.open('config.' + id)
            self.tracker.configurator.active[id] = True

        # update menu
        self.update_menu()

    def update_menu(self):
        """Updates the configurator menu."""
        for id in self.tracker.configurator.ids:
            if id in self.tracker.configurator.active and self.tracker.configurator.active[id]:
                self.tracker.window.menu['config.' + id].setChecked(True)
            else:
                self.tracker.window.menu['config.' + id].setChecked(False)

    def save(self):
        """Save the configuration to files."""
        try:
            self.tracker.configurator.dump_config()
            self.tracker.configurator.dump_hosts()
            self.tracker.configurator.dump_streams()
            self.tracker.window.ui.dialogs.alert(trans('dialog.info.save_config'))
            self.tracker.debug.log("[CONFIG] SAVED")
        except Exception as e:
            self.tracker.debug.log("[ERROR] Error saving config: {}".format(e))
