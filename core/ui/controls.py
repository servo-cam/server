#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtWidgets import QTabWidget
from core.ui.control_manual import UIControlManual
from core.ui.control_auto import UIControlAuto
from core.ui.control_area import UIControlArea
from core.ui.control_filter import UIControlFilter
from core.ui.control_video import UIControlVideo
from core.ui.control_options import UIControlOptions
from core.utils import trans
from core.ui.style import Style


class UIControls:
    def __init__(self, window=None):
        """
        Controls UI setup

        :param window: main UI window object
        """
        self.window = window
        self.ui_controls_manual = UIControlManual(window)
        self.ui_controls_auto = UIControlAuto(window)
        self.ui_controls_area = UIControlArea(window)
        self.ui_controls_filter = UIControlFilter(window)
        self.ui_controls_video = UIControlVideo(window)
        self.ui_controls_options = UIControlOptions(window)

    def setup(self):
        """
        Setup controls

        :return: QTabWidget
        """
        manual = self.ui_controls_manual.setup()
        auto = self.ui_controls_auto.setup()
        area = self.ui_controls_area.setup()
        filters = self.ui_controls_filter.setup()
        video = self.ui_controls_video.setup()
        options = self.ui_controls_options.setup()

        # controls tabs
        self.window.controls_tabs = QTabWidget()
        self.window.controls_tabs.addTab(manual, trans("tab.controls.manual"))
        self.window.controls_tabs.addTab(auto, trans("tab.controls.auto"))
        self.window.controls_tabs.addTab(area, trans("tab.controls.area"))
        self.window.controls_tabs.addTab(filters, trans("tab.controls.filters"))
        self.window.controls_tabs.addTab(video, trans("tab.controls.video"))  # idx 4
        self.window.controls_tabs.addTab(options, trans("tab.controls.options"))  # idx 4
        self.window.controls_tabs.setMinimumHeight(Style.TOOLBOX_MIN_HEIGHT)

        return self.window.controls_tabs
