#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Render:
    def __init__(self, tracker=None):
        """
        Render handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def toggle(self, mode):
        """
        Toggles the render mode.
        :param mode: mode to toggle
        """
        if mode == 'full_screen':
            if self.tracker.render.full_screen:
                self.tracker.render.full_screen = False
            else:
                self.tracker.render.full_screen = True
                self.tracker.window.showMaximized()
        elif mode == 'fit':
            if self.tracker.render.fit:
                self.tracker.render.fit = False
            else:
                self.tracker.render.fit = True
        elif mode == 'tracking':
            if self.tracker.render.tracking:
                self.tracker.render.tracking = False
            else:
                self.tracker.render.tracking = True
        elif mode == 'targeting':
            if self.tracker.render.targeting:
                self.tracker.render.targeting = False
            else:
                self.tracker.render.targeting = True
        elif mode == 'bounds':
            if self.tracker.render.bounds:
                self.tracker.render.bounds = False
            else:
                self.tracker.render.bounds = True
        elif mode == 'labels':
            if self.tracker.render.labels:
                self.tracker.render.labels = False
            else:
                self.tracker.render.labels = True
        elif mode == 'text':
            if self.tracker.render.text:
                self.tracker.render.text = False
            else:
                self.tracker.render.text = True
        elif mode == 'simulator':
            if self.tracker.render.simulator:
                self.tracker.render.simulator = False
            else:
                self.tracker.render.simulator = True
                if self.tracker.servo.enable:
                    if self.tracker.source == self.tracker.SOURCE_REMOTE or self.tracker.source == self.tracker.SOURCE_LOCAL:
                        self.tracker.servo.enable = False
                        self.tracker.debug.log('[WARNING] Servo disabled due to simulator')
                if not self.tracker.render.center_lock:
                    self.tracker.render.center_lock = True
                    self.tracker.targeting.center()
                    self.tracker.debug.log('[INFO] Center lock enabled due to simulator')
                self.tracker.controller.servo.update()
        elif mode == 'center_lock':
            if self.tracker.render.center_lock:
                self.tracker.render.center_lock = False
                if self.tracker.servo.enable:
                    if self.tracker.source == self.tracker.SOURCE_REMOTE or self.tracker.source == self.tracker.SOURCE_LOCAL:
                        self.tracker.servo.enable = False
                        self.tracker.debug.log('[WARNING] Servo disabled due to disabled center lock')
                self.tracker.controller.servo.update()
            else:
                self.tracker.render.center_lock = True
                self.tracker.targeting.center()
        elif mode == 'console':
            if self.tracker.render.console:
                self.tracker.render.console = False
            else:
                self.tracker.render.console = True

        # apply changes
        self.apply()

        # update menu
        self.update()

    def init(self):
        """Initializes the render modes."""
        # apply changes
        self.apply(True)

        # update menu
        self.update()

        if self.tracker.render.minimized:
            self.tracker.window.showMinimized()
        elif self.tracker.render.maximized:
            self.tracker.window.showMaximized()

    def apply(self, init=False):
        """
        Applies the render modes.

        :param init: True if called when app is initializing
        """
        # console
        if self.tracker.render.console:
            self.tracker.window.layout_bottom.show()
        else:
            self.tracker.window.layout_bottom.hide()

        # full screen
        if self.tracker.render.full_screen:
            self.tracker.window.layout_top.hide()
            self.tracker.window.layout_toolbox.hide()
            self.tracker.window.layout_bottom.hide()
            self.tracker.window.layout.setContentsMargins(0, 0, 0, 0)
            self.tracker.window.layout_main.setContentsMargins(0, 0, 0, 0)
            self.tracker.window.main_widget.setContentsMargins(0, 0, 0, 0)
            # self.tracker.window.setContentsMargins(0, 0, 0, 0)
            # self.tracker.window.layout_center.setContentsMargins(0, 0, 0, 0)

            if init:
                self.tracker.window.showMaximized()
        else:
            self.tracker.window.layout_top.show()
            self.tracker.window.layout_toolbox.show()

            if self.tracker.render.console:
                self.tracker.window.layout_bottom.show()

    def update(self):
        """Updates the menu."""
        # full screen
        if self.tracker.render.full_screen:
            self.tracker.window.menu['render.full_screen'].setChecked(True)
        else:
            self.tracker.window.menu['render.full_screen'].setChecked(False)

        # fit
        if self.tracker.render.fit:
            self.tracker.window.menu['render.fit'].setChecked(True)
        else:
            self.tracker.window.menu['render.fit'].setChecked(False)

        # tracking
        if self.tracker.render.tracking:
            self.tracker.window.menu['render.tracking'].setChecked(True)
        else:
            self.tracker.window.menu['render.tracking'].setChecked(False)

        # targeting
        if self.tracker.render.targeting:
            self.tracker.window.menu['render.targeting'].setChecked(True)
        else:
            self.tracker.window.menu['render.targeting'].setChecked(False)

        # bounds
        if self.tracker.render.bounds:
            self.tracker.window.menu['render.bounds'].setChecked(True)
        else:
            self.tracker.window.menu['render.bounds'].setChecked(False)

        # labels
        if self.tracker.render.labels:
            self.tracker.window.menu['render.labels'].setChecked(True)
        else:
            self.tracker.window.menu['render.labels'].setChecked(False)

        # text
        if self.tracker.render.text:
            self.tracker.window.menu['render.text'].setChecked(True)
        else:
            self.tracker.window.menu['render.text'].setChecked(False)

        # simulator
        if self.tracker.render.simulator:
            self.tracker.window.menu['render.simulator'].setChecked(True)
        else:
            self.tracker.window.menu['render.simulator'].setChecked(False)

        # center_lock
        if self.tracker.render.center_lock:
            self.tracker.window.menu['render.center_lock'].setChecked(True)
        else:
            self.tracker.window.menu['render.center_lock'].setChecked(False)

        # console
        if self.tracker.render.console:
            self.tracker.window.menu['render.console'].setChecked(True)
        else:
            self.tracker.window.menu['render.console'].setChecked(False)
