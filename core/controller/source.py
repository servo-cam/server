#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6 import QtWidgets
from core.ui.style import Style
from core.utils import trans


class Source:
    def __init__(self, tracker=None):
        """
        Source handling.

        :param tracker: tracker object
        """
        self.tracker = tracker

    def browse(self):
        """Browses for a movie file."""
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(caption=trans('btn.source.address.browse.dialog'),
                                                                 dir='.')
        if filename:
            self.tracker.window.source_address.setText(filename)
            self.load(filename)

    def load(self, url, connect=True):
        """Loads a source address."""
        self.tracker.switch_addr(self.tracker.source, url)

        if self.tracker.source == self.tracker.SOURCE_VIDEO:
            self.toggle(self.tracker.source, True)
        elif self.tracker.source == self.tracker.SOURCE_REMOTE:
            self.toggle(self.tracker.source, True)
        elif self.tracker.source == self.tracker.SOURCE_STREAM:
            self.toggle(self.tracker.source, True)
            if connect:
                self.tracker.stream.connect(url)
        self.tracker.window.source_address.setText(url)

        # update menu
        self.update()

    def toggle(self, src, force=False):
        """
        Toggles the source.

        :param src: source to toggle
        :param force: force toggle
        """
        # reset only if source is different
        if self.tracker.source != src or force:
            for k in self.tracker.window.source_btn:
                self.tracker.window.source_btn[k].setStyleSheet(Style.BTN_DEFAULT)

            # reset actions
            self.tracker.action.reset()

        # local / camera
        if src == self.tracker.SOURCE_LOCAL and (self.tracker.source != self.tracker.SOURCE_LOCAL or force):
            self.tracker.switch_source(src)
            self.tracker.window.source_address.setHidden(True)
            self.tracker.window.source_load_btn.setHidden(True)
            self.tracker.window.source_browse_btn.setHidden(True)
            self.tracker.window.source_address_prefix.setText(trans('source.address.prefix.local'))
            self.tracker.window.source_address_prefix.setHidden(False)
            self.tracker.window.source_camera_local.setHidden(False)
            self.tracker.window.source_btn[src].setStyleSheet(Style.BTN_ACTIVE)
            self.tracker.window.tabs.setCurrentIndex(0)
            self.tracker.window.tabs.setTabEnabled(1, False)

        # video
        elif src == self.tracker.SOURCE_VIDEO and (self.tracker.source != self.tracker.SOURCE_VIDEO or force):
            self.tracker.switch_source(src)
            self.tracker.window.source_address.setText(self.tracker.video_url)
            self.tracker.window.source_load_btn.setText(trans('source.address.load.video'))
            self.tracker.window.source_address_prefix.setText(trans('source.address.prefix.video'))
            self.tracker.window.source_address_prefix.setHidden(False)
            self.tracker.window.source_address.setHidden(False)
            self.tracker.window.source_load_btn.setHidden(False)
            self.tracker.window.source_browse_btn.setHidden(False)
            self.tracker.window.source_camera_local.setHidden(True)
            self.tracker.window.source_btn[src].setStyleSheet(Style.BTN_ACTIVE)
            self.tracker.window.tabs.setCurrentIndex(0)
            self.tracker.window.tabs.setTabEnabled(1, False)
            self.tracker.window.controls_tabs.setTabEnabled(4, True)

        # remote
        elif src == self.tracker.SOURCE_REMOTE and (self.tracker.source != self.tracker.SOURCE_REMOTE or force):
            self.tracker.switch_source(src)
            self.tracker.window.source_address.setText(self.tracker.remote_host)
            self.tracker.window.source_load_btn.setText(trans('source.address.load.remote'))
            self.tracker.window.source_address_prefix.setText(trans('source.address.prefix.remote'))
            self.tracker.window.source_address_prefix.setHidden(False)
            self.tracker.window.source_address.setHidden(False)
            self.tracker.window.source_load_btn.setHidden(False)
            self.tracker.window.source_browse_btn.setHidden(True)
            self.tracker.window.source_camera_local.setHidden(True)
            self.tracker.window.source_btn[src].setStyleSheet(Style.BTN_ACTIVE)
            self.tracker.window.tabs.setTabEnabled(1, True)

        # stream
        elif src == self.tracker.SOURCE_STREAM and (self.tracker.source != self.tracker.SOURCE_STREAM or force):
            self.tracker.switch_source(src)
            self.tracker.window.source_address.setText(self.tracker.stream_url)
            self.tracker.window.source_load_btn.setText(trans('source.address.load.stream'))
            self.tracker.window.source_address_prefix.setText(trans('source.address.prefix.stream'))
            self.tracker.window.source_address_prefix.setHidden(False)
            self.tracker.window.source_address.setHidden(False)
            self.tracker.window.source_load_btn.setHidden(False)
            self.tracker.window.source_browse_btn.setHidden(True)
            self.tracker.window.source_camera_local.setHidden(True)
            self.tracker.window.source_btn[src].setStyleSheet(Style.BTN_ACTIVE)
            self.tracker.window.tabs.setCurrentIndex(0)
            self.tracker.window.tabs.setTabEnabled(1, False)

        # update menu
        self.update()

    def update(self):
        """Updates the menu."""
        if self.tracker.source == self.tracker.SOURCE_REMOTE:
            title = str(self.tracker.remote_host) + ' <' + str(self.tracker.remote_ip) + '>'
            if self.tracker.remote_host == self.tracker.remote_ip:
                title = str(self.tracker.remote_ip)
            self.tracker.window.tabs.setTabText(0, title)
        elif self.tracker.source == self.tracker.SOURCE_VIDEO:
            self.tracker.window.tabs.setTabText(0, trans('tab.output.video'))
        elif self.tracker.source == self.tracker.SOURCE_STREAM:
            self.tracker.window.tabs.setTabText(0, trans('tab.output.stream'))
        elif self.tracker.source == self.tracker.SOURCE_LOCAL:
            self.tracker.window.tabs.setTabText(0,
                                                trans('tab.output.local') + ' (' + str(self.tracker.camera.idx) + ')')

        for k in self.tracker.window.menu['source']:
            self.tracker.window.menu['source'][k].setChecked(False)
        self.tracker.window.menu['source'][self.tracker.source].setChecked(True)

    def handle(self):
        """Handles the source menu."""
        # if montages view then enable montages render
        if self.tracker.window.tabs.currentIndex() == 1:
            self.tracker.render.montage = True
        else:
            self.tracker.render.montage = False
