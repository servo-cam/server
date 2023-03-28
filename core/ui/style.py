#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtGui import QFont


class Style:
    BTN_DEFAULT = 'background-color: none;'
    BTN_ACTIVE = 'background-color: #32CD32;'
    BTN_DANGER = 'background-color: #FF0000;'
    BTN_DANGER_IMPORTANT = 'background-color: #FF0000;'
    BADGE_DEFAULT = 'background-color: none; border: none'
    BADGE_ACTIVE = 'background-color: #32CD32; border: none'
    FONT_CONSOLE = QFont()
    FONT_DEBUG = QFont("", 8)
    FONT_BOLD = QFont("", weight=75)
    TOOLBOX_WIDTH = 340
    TOOLBOX_MIN_HEIGHT = 340
    CONTROL_GRID_BTN_WIDTH = 50
    CONTROL_GRID_BTN_HEIGHT = 50
    FOOTER_MIN_WIDTH = 300
    FOOTER_HEIGHT = 100
    FOOTER_STATUS_MIN_WIDTH = 180
    LABEL_MAX_HEIGHT = 20
    SOURCE_BUTTONS_MAX_WIDTH = 350
    SOURCE_ADDRESS_MIN_WIDTH = 450
    DIALOG_DEBUG_WIDTH = 300
    DIALOG_DEBUG_HEIGHT = 400

    def __init__(self):
        pass
