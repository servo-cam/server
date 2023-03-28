#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import cv2
import numpy as np
from core.utils import is_cv2, trans


class Video:
    def __init__(self, tracker=None):
        """
        Video handling.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.is_seek = False

    def update(self):
        """Updates the video info and current frame."""
        cap = None
        if self.tracker.source != self.tracker.SOURCE_REMOTE:
            if '-' in self.tracker.capture:
                cap = self.tracker.capture['-']
        else:
            # if remote get capture from current remote ip
            if self.tracker.remote_ip is not None:
                if self.tracker.remote_ip in self.tracker.capture:
                    cap = self.tracker.capture[self.tracker.remote_ip]

        # if empty capture return
        if cap is None:
            return

        # loop video
        if self.tracker.stream.loop or self.tracker.video.loop:
            if self.tracker.source == self.tracker.SOURCE_STREAM and self.tracker.stream.loop or \
                    self.tracker.source == self.tracker.SOURCE_VIDEO and self.tracker.video.loop:
                if not is_cv2():
                    current = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                else:
                    current = int(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
                    total = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
                if current == total:
                    if not is_cv2():
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    else:
                        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)

        # get data
        if type(cap) is not np.ndarray:
            # if cv2 video capture
            if not is_cv2():
                # if cv > 2
                current = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                resolution = '{}x{}'.format(
                    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                )
            else:
                # if cv2
                current = int(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
                total = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
                fps = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))
                resolution = '{}x{}'.format(
                    int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
                )
        else:
            # if nd.array
            current = 1
            total = 1
            fps = self.tracker.fps
            resolution = '{}x{}'.format(cap.shape[1], cap.shape[0])

        frame_to_time = self.frame_to_time(current, fps)

        self.tracker.window.control_video['label_time'].setText(
            trans('video.control.time') + ': {}'.format(frame_to_time))
        self.tracker.window.control_video['label_frame'].setText(
            trans('video.control.frame') + ': {}/{}'.format(current, total))
        self.tracker.window.control_video['label_fps'].setText(
            trans('video.control.fps') + ': {} / {}'.format(fps, self.tracker.fps))
        self.tracker.window.control_video['label_resolution'].setText('{}'.format(resolution))

        # if manual seek active then return
        if self.is_seek:
            return

        # update seek bar with current frame
        perc = round((current / total) * 100, 0)
        self.tracker.window.control_video['seek'].setValue(perc)

    def frame_to_time(self, frame, fps):
        """
        Convert frame to time

        :param frame: frame number
        :param fps: fps
        :return: time in format hh:mm:ss
        """
        total_seconds = frame / fps
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def start_seek(self):
        """Start manual seek"""
        self.is_seek = True

    def stop_seek(self):
        """Stop manual seek"""
        self.seek(self.tracker.window.control_video['seek'].value())
        self.is_seek = False

    def play(self):
        """Play video"""
        self.tracker.paused = False

    def pause(self):
        """Pause video"""
        self.tracker.paused = True

    def seek(self, percent):
        """
        Seek video to percentage position of video

        :param percent: percent value of duration
        """
        if '-' not in self.tracker.capture:
            return

        if not is_cv2():
            frame = int((percent / 100) * self.tracker.capture['-'].get(cv2.CAP_PROP_FRAME_COUNT))
        else:
            frame = int((percent / 100) * self.tracker.capture['-'].get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

        if not is_cv2():
            self.tracker.capture['-'].set(cv2.CAP_PROP_POS_FRAMES, frame)
        else:
            self.tracker.capture['-'].set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frame)
