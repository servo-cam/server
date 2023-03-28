#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from core.controller.control_manual import ControlManual
from core.controller.control_auto import ControlAuto
from core.controller.control_area import ControlArea
from core.controller.control_filters import ControlFilters
from core.controller.status import Status
from core.controller.debug import Debug
from core.controller.info import Info
from core.controller.source import Source
from core.controller.camera import Camera
from core.controller.servo import Servo
from core.controller.render import Render
from core.controller.video import Video
from core.controller.internals import Internals
from core.controller.video_filter import VideoFilter
from core.controller.configurator import Configurator
from core.controller.options import Options


class Controller:
    def __init__(self, tracker):
        """
        Main Controller.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.internals = Internals(tracker)
        self.source = Source(tracker)
        self.camera = Camera(tracker)
        self.servo = Servo(tracker)
        self.render = Render(tracker)
        self.video = Video(tracker)
        self.control_manual = ControlManual(tracker)
        self.control_auto = ControlAuto(tracker)
        self.control_area = ControlArea(tracker)
        self.control_filters = ControlFilters(tracker)
        self.status = Status(tracker)
        self.debug = Debug(tracker)
        self.info = Info(tracker)
        self.video_filter = VideoFilter(tracker)
        self.configurator = Configurator(tracker)
        self.options = Options(tracker)

    def init(self, source):
        """
        Initializes an app.

        :param source: source name
        """
        # update UI at init
        self.source.update()
        self.internals.init()

        # init camera (check if csi or serial, if yes then update idx before camera update)
        self.camera.init()
        self.camera.update()

        # init source in tracker
        self.tracker.init(source, True)

        # update targeting UI
        self.control_auto.init()
        self.control_manual.init()
        self.control_area.init()
        self.control_filters.init()

        self.render.init()  # apply render settings
        self.tracker.remote.load()  # load remote hosts
        self.tracker.stream.load()  # load streams

        self.servo.update()  # clients must be loaded before servo update
        self.video_filter.update()  # filters can be loaded from config
        self.options.init()  # filters can be loaded from config

        self.tracker.updater.check()  # check for updates

    def update(self):
        """Updates the app UI on frame update."""
        self.control_manual.handle()  # update zoom, speed sliders
        self.status.handle()
        self.source.handle()

    def collect(self):
        """Collects data from UI and updates data."""
        if self.tracker.window.controls_tabs.currentIndex() == 0:
            self.tracker.control_view = self.tracker.CONTROL_VIEW_MANUAL
        elif self.tracker.window.controls_tabs.currentIndex() == 1:
            self.tracker.control_view = self.tracker.CONTROL_VIEW_AUTO
        elif self.tracker.window.controls_tabs.currentIndex() == 2:
            self.tracker.control_view = self.tracker.CONTROL_VIEW_AREA
