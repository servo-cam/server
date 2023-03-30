#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.30 17:00
# =============================================================================

from core.ui.style import Style
from core.utils import trans


class Configurator:
    def __init__(self, tracker=None):
        """
        Configuration edit handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def toggle_editor(self, id):
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

    def toggle_settings(self, id):
        """
        Toggles the settings.

        :param id: settings id
        """
        width = Style.DIALOG_DEBUG_WIDTH
        height = Style.DIALOG_DEBUG_HEIGHT

        if id == 'servo':
            width = 800
            height = 600

        if id in self.tracker.configurator.active and self.tracker.configurator.active[id]:
            self.tracker.window.ui.dialogs.close('config.' + id)
            self.tracker.configurator.active[id] = False
        else:
            self.tracker.configurator.load(id)
            self.tracker.window.ui.dialogs.open('config.' + id, width=width, height=height)
            self.tracker.controller.settings.init(id)
            self.tracker.configurator.active[id] = True

        # update menu
        self.update()

    def close(self, id):
        """
        Closes the configurator menus.

        :param id: configurator id
        """
        if id in self.tracker.window.menu:
            self.tracker.window.menu[id].setChecked(False)

        allowed_settings = ['servo']
        if id in allowed_settings and id in self.tracker.window.menu:
            self.tracker.window.menu[id].setChecked(False)

    def update(self):
        """Updates the configurator."""
        self.update_menu()
        self.update_menu_settings()

    def update_menu(self):
        """Updates the configurator menu."""
        for id in self.tracker.configurator.ids:
            if id in self.tracker.configurator.active and self.tracker.configurator.active[id]:
                self.tracker.window.menu['config.' + id].setChecked(True)
            else:
                self.tracker.window.menu['config.' + id].setChecked(False)

    def update_menu_settings(self):
        """Updates the configurator menu."""
        allowed = ['servo']
        for id in self.tracker.configurator.ids:
            if id not in allowed:
                continue
            if id in self.tracker.configurator.active and self.tracker.configurator.active[id]:
                self.tracker.window.menu[id + '.config'].setChecked(True)
            else:
                self.tracker.window.menu[id + '.config'].setChecked(False)

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
