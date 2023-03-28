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


class Camera:
    def __init__(self, tracker=None):
        """
        Camera handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def init(self):
        """Initializes the camera menu."""
        # update idx if CSI or serial <--- TODO: not implemented yet
        if self.tracker.camera.csi:
            self.tracker.camera.idx = self.tracker.camera.max_local_idx + 1
        elif self.tracker.camera.serial:
            self.tracker.camera.idx = self.tracker.camera.max_local_idx + 2

    def toggle(self, idx):
        """
        Toggles the camera.

        :param idx: camera index
        """
        self.tracker.switch_cam(idx)
        self.tracker.controller.source.toggle(self.tracker.SOURCE_LOCAL, True)  # true = force

        # update menu
        self.update()

    def reload_indexes(self):
        """Reloads the list of available cameras."""
        index = -1
        for index in self.tracker.camera.get_indexes():
            self.tracker.window.source_camera_local.addItem(trans("menu.camera.prefix") + ": " + str(index), index)

        # TODO: external camera / serial camera
        '''
        # add raspberry pi (CSI) at next available index
        index += 1
        self.tracker.window.source_camera_local.addItem("Raspberry Pi (CSI)", index)

        # add raspberry pi (USB) at next available index
        index += 1
        self.tracker.window.source_camera_local.addItem("Raspberry Pi (USB)", index)
        '''

    def update(self):
        """Updates the camera menu."""
        self.tracker.window.source_camera_local.setCurrentText(
            trans("menu.camera.prefix") + ": " + str(self.tracker.camera.idx))
