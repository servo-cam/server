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
from PySide6.QtGui import QImage, QPixmap


class Rendering:
    def __init__(self, tracker=None):
        """
        Rendering handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.orig_frame = None
        self.frame = None
        self.montage_frames = []
        self.pixmap = None
        self.tracking = True
        self.targeting = True
        self.bounds = True
        self.labels = True
        self.text = True
        self.center_lock = False
        self.simulator = False
        self.zoom = 1
        self.fit = True
        self.full_screen = False
        self.minimized = False
        self.maximized = False
        self.montage = False
        self.size = (0, 0)

    def handle_thread(self, frame):
        """
        Handle video from remote video thread

        :param frame: frame
        """
        if frame is None:
            return
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_frame(self):
        """
        Get frame from capture

        :return: frame
        """
        # get frame
        frame = None
        success = False
        if self.tracker.source != self.tracker.SOURCE_REMOTE:
            for ip in self.tracker.capture:

                # allow only local capture here
                if ip != '-':
                    continue

                # check if capture is not numpy array (remote)
                if self.tracker.capture[ip] is not None and type(self.tracker.capture[ip]) is not np.ndarray:
                    success, self.orig_frame = self.tracker.capture[ip].read()
                if success:
                    # only if window app
                    if self.tracker.window is not None:
                        frame = cv2.cvtColor(self.orig_frame, cv2.COLOR_BGR2RGB)
                    else:
                        frame = self.orig_frame.copy()

                    self.size = (frame.shape[1], frame.shape[0])
        else:
            # remote video frame
            if self.tracker.remote.active and self.frame is not None:
                frame = self.frame.copy()
                self.size = (frame.shape[1], frame.shape[0])

        # video filter apply (input)
        if self.tracker.video_filter.has_input_filter():
            frame = self.tracker.video_filter.apply_input(frame)

        return frame

    def process(self, frame=None):
        """
        Process frame

        :param frame: source frame
        :return: processed frame
        """
        label_width = 0
        label_height = 0

        if frame is not None:
            # send to model
            if not self.tracker.processing:
                self.tracker.processing = True
                frame = self.tracker.run(frame)  # run AI model
            self.tracker.processing = False

            # max_width is max label width, max_height is max label height
            max_width, max_height = self.get_max_size()

            # output_width is max label width, output_height is ratio-calculated height
            output_width, output_height = self.get_output_size(frame.shape[1], frame.shape[0])  # 0 = height, 1 = width

            # get current zoom value
            zoom = self.get_zoom_value()

            # prepare destination width and height
            resize_width = int(max_width * zoom)
            resize_height = int(output_height * zoom)
            label_width = int(output_width * zoom)
            label_height = int(output_height * zoom)

            # apply zoom
            if zoom > 1:
                frame, resize_width, resize_height, label_width, label_height = self.apply_zoom(frame, zoom)

            # video filter apply (output)
            if self.tracker.video_filter.has_output_filter():
                frame = self.tracker.video_filter.apply_output(frame)

            # resize video to max label width
            frame = self.resize(frame, resize_width, resize_height)  # resize output to max label width

            if self.tracking and self.tracker.wrapper is not None:  # if view render tracking enabled
                frame = self.tracker.wrapper.append(frame)  # add overlays to image

            # append debug boxes
            if self.tracker.debug.active['keypoints']:
                self.tracker.overlay.draw_debug_boxes()

        return frame, label_width, label_height

    def render(self, frame, w, h):
        """
        Render frame to window

        :param frame: frame
        :param w: Width
        :param h: Height
        """

        # translate with delta
        frame = self.translate(frame, self.tracker.dx, self.tracker.dy)  # translate output with dx, dy

        # render in video label - only if window app
        if self.tracker.window is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0],
                           frame.strides[0], QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(image).scaled(w, h)

            self.tracker.window.output.setPixmap(self.pixmap)
            self.tracker.window.output.resize(w, h)

    def blank_screen(self):
        """
        Blank screen - clear output label
        """
        if self.tracker.window is not None:
            self.tracker.window.output.clear()

    def render_montage(self, frame=None):
        """
        Render montage - append montage render to window

        :param frame: frame
        """
        if frame is not None:

            # max_width is max label width, max_height is max label height
            max_width, max_height = self.get_max_size()

            # output_width is max label width, output_height is ratio-calculated height
            output_width, output_height = self.get_output_size(frame.shape[1],
                                                               frame.shape[0])  # 0 = height, 1 = width

            # get current zoom value
            zoom = self.get_zoom_value()

            # prepare destination width and height
            resize_width = int(max_width * zoom)
            resize_height = int(output_height * zoom)
            label_width = int(output_width * zoom)
            label_height = int(output_height * zoom)

            # apply zoom
            if zoom > 1:
                frame, resize_width, resize_height, label_width, label_height = self.apply_zoom(frame, zoom)

            # resize video to max label width
            frame = self.resize(frame, resize_width, resize_height)  # resize output to max label width

            # translate with delta
            frame = self.translate(frame, self.tracker.dx, self.tracker.dy)  # translate output with dx, dy

            # render in video label - only if window app
            if self.tracker.window is not None:
                image = QImage(frame, frame.shape[1], frame.shape[0],
                               frame.strides[0], QImage.Format_RGB888)
                self.pixmap = QPixmap.fromImage(image).scaled(label_width, label_height)

                self.tracker.window.montage.setPixmap(self.pixmap)
                self.tracker.window.montage.resize(label_width, label_height)

    def append_montage(self):
        """Append montage render to window"""
        if self.montage_frames is not None:
            for (i, montage) in enumerate(self.montage_frames):
                montage = cv2.cvtColor(montage, cv2.COLOR_BGR2RGB)
                self.render_montage(montage)

    def apply_zoom(self, frame, zoom):
        """
        Apply zoom to frame

        :param frame: frame
        :param zoom: zoom value
        :return: frame, resize_width, resize_height, label_width, label_height
        """
        max_width, max_height = self.get_max_size()

        x_from = int((frame.shape[1] - (frame.shape[1] / zoom)) / 2)
        x_to = int((frame.shape[1] + (frame.shape[1] / zoom)) / 2)
        y_from = int((frame.shape[0] - (frame.shape[0] / zoom)) / 2)
        y_to = int((frame.shape[0] + (frame.shape[0] / zoom)) / 2)

        frame = frame[y_from:y_to, x_from:x_to]  # crop
        frame = np.ascontiguousarray(frame)  # required for opencv

        ratio = frame.shape[0] / frame.shape[1]
        resize_width = int(frame.shape[1] * zoom)
        resize_height = int(frame.shape[0] * zoom)
        label_width = max_width
        label_height = max_width * ratio

        return frame, resize_width, resize_height, label_width, label_height

    def get_zoom_value(self):
        """
        Get zoom value

        :return: zoom value
        """
        zoom = (self.zoom + 10) / 10
        if zoom < 1:
            zoom = 1
        elif zoom > 9:
            zoom = 9
        return zoom

    def cv_render(self, frame):
        """
        Display native OpenCV frame

        :param frame: frame
        """
        cv2.imshow('Servo Cam', frame)

    def resize(self, img, w, h):
        """
        Resize image with width and height

        :param img: image
        :param w: width
        :param h: height
        :return: resized image
        """
        return cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)

    def translate(self, img, dx, dy):
        """
        Translate image with delta

        :param img: image
        :param dx: delta x
        :param dy: delta y
        :return: translated image
        """
        if not self.simulator:
            return img

        if dx != 0 or dy != 0:
            num_rows, num_cols = img.shape[:2]
            translation_matrix = np.float32([[1, 0, dx * num_cols], [0, 1, dy * num_rows]])
            img = cv2.warpAffine(img, translation_matrix, (num_cols, num_rows))
        return img

    def fit_and_translate(self, img, w, h, dx, dy):
        """
        Resize and translate image

        :param img: image
        :param w: width
        :param h: height
        :param dx: delta x
        :param dy: delta y
        :return: resized and translated image
        """
        return self.translate(self.resize(img, w, h), dx, dy)

    def get_max_size(self):
        """
        Calculate max video size

        :return: max width, max height
        """
        sub_width = self.tracker.window.layout_toolbox.width() + 60 + 10
        sub_height = self.tracker.window.source_widget.height() + self.tracker.window.footer_widget.height() + 80

        # if full screen then no sub
        if self.full_screen:
            sub_width = 20
            sub_height = 0

        w = self.tracker.window.main_widget.width() - sub_width
        h = self.tracker.window.main_widget.height() - sub_height
        return int(w), int(h)

    def get_output_size(self, vx, vy):
        """
        Calculate output size

        :param vx: video width
        :param vy: video height
        :return: output width, output height
        """
        if self.tracker.window is None:
            return vx, vy

        max_w, max_h = self.get_max_size()
        w = max_w

        # set minimum width
        if w < 200:
            w = 200

        ratio = vy / vx
        h = w * ratio

        if not self.fit:
            return max_w, int(h)

        if h > max_h:
            ratio = vx / vy
            h = max_h
            w = h * ratio

        return int(w), int(h)

    @staticmethod
    def is_resizing(window):
        """
        Check if window is resizing

        :param window: window
        :return: True if resizing, False if not
        """
        if window.w != window.width() or window.h != window.height():
            window.w = window.width()
            window.h = window.height()
            return True
        else:
            window.w = window.width()
            window.h = window.height()
            return False
