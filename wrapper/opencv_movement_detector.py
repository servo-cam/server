#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import numpy as np
import imutils
import cv2


class OpenCVMovementDetector:
    def __init__(self, tracker):
        """
        OpenCV movement detector wrapper

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.objects = None
        self.model_name = None
        self.model = None
        self.accumWeight = 0.5
        self.bg = None
        self.total = 0
        self.frameCount = 32

    def prepare(self, model_name):
        """
        Prepare model for prediction

        :param model_name: model name
        """
        self.model_name = model_name
        self.total = 0

    def reset(self):
        """Reset model"""
        self.bg = None
        self.total = 0

    def predict(self, img):
        """
        Predict objects in image

        :param img: video frame to analyze
        """
        self.tracker.objects = []  # reset objects

        frame = imutils.resize(img, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        boxes = []
        if self.total > self.frameCount:
            # single object detection
            if self.model_name == 'opencv_movement_detect_single':
                boxes = self.detect_single(gray)

            # multi object detection
            elif self.model_name == 'opencv_movement_detect_multi':
                boxes = self.detect_all(gray)

        self.update(gray)
        self.total += 1

        if boxes is not None:
            i = 0
            for box in boxes:
                obj = {
                    self.tracker.IDX_KEYPOINTS: [],
                    self.tracker.IDX_CLASS: 'any',
                    self.tracker.IDX_ID: i,
                    self.tracker.IDX_BOX: box,
                    self.tracker.IDX_CENTER: self.tracker.keypoints.build_center(box),
                    self.tracker.IDX_SCORE: 1
                }

                # check score and filters (min score is defined in filter)
                if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_DETECT):
                    continue

                self.tracker.objects.append(obj)
                i += 1

    def append(self, img):
        """
        Append overlay to image

        :param img: image to append overlay
        :return: image with overlay
        """
        self.tracker.overlay.img = img  # needed reset here!!!
        if self.tracker.objects is not None:
            for obj in self.tracker.objects:
                if self.tracker.render.bounds:
                    # do not render label in this wrapper!!!
                    self.tracker.overlay.draw_bounding(obj[self.tracker.IDX_BOX])
                    self.tracker.overlay.draw_center(obj[self.tracker.IDX_CENTER])

        return self.tracker.overlay.img

    def unload(self):
        """Unload model"""
        self.total = 0
        self.bg = None

    def update(self, image):
        """
        Update background model

        :param image: image to update background model
        """
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect_all(self, image, tVal=25):
        """
        Detect all objects in image

        :param image: image to detect objects
        :param tVal: threshold value
        :return: list of objects
        """
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) == 0:
            return None

        h, w = image.shape
        objects = []
        for c in cnts:
            (x, y, width, height) = cv2.boundingRect(c)
            # append normalized coordinates
            objects.append([
                x / w,
                y / h,
                width / w,
                height / h
            ])
        return objects

    def detect_single(self, image, tVal=25):
        """
        Detect single object in image

        :param image: image to detect object
        :param tVal: threshold value
        :return: list of objects
        """
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        if len(cnts) == 0:
            return None

        h, w = image.shape
        objects = []
        for c in cnts:
            (x, y, width, height) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + width), max(maxY, y + height))

        objects.append([
            minX / w,
            minY / h,
            (maxX - minX) / w,
            (maxY - minY) / h
        ])
        return objects

    def get_target_point(self, name, idx):
        """
        Get center point of target

        :param name: target point name
        :param idx: object index
        :return: center point of object (x, y)
        """
        if self.tracker.objects is not None and idx < len(self.tracker.objects[idx]):
            return self.tracker.objects[idx][self.tracker.IDX_CENTER]
