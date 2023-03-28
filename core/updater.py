#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from urllib.request import urlopen, Request
from packaging.version import parse as parse_version
import json
import ssl
from core.utils import trans


class Updater:
    def __init__(self, tracker=None):
        """
        Updates handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker

    def check(self):
        """Check for updates"""
        print("Checking for updates...")
        url = self.tracker.www + "/api/version?v=" + str(self.tracker.version)
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response = urlopen(req, context=ctx, timeout=3)
            data_json = json.loads(response.read())
            newest_version = data_json["version"]
            newest_build = data_json["build"]

            parsed_newest_version = parse_version(newest_version)
            parsed_current_version = parse_version(self.tracker.version)
            if parsed_newest_version > parsed_current_version:
                self.show_version_dialog(newest_version, newest_build)
        except Exception as e:
            print("Failed to check for updates")
            print(e)

    def show_version_dialog(self, version, build):
        """
        Show new version dialog

        :param version: version number
        :param build: build date
        """
        txt = trans('update.new_version') + ": " + str(version) + " (" + trans('update.released') + ": " + str(
            build) + ")"
        txt += "\n" + trans('update.current_version') + ": " + self.tracker.version
        self.tracker.window.update_dialog.message.setText(txt)
        self.tracker.window.update_dialog.show()
