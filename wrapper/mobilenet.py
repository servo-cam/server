#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2


class Mobilenet:
    def __init__(self, tracker):
        """
        Mobilenet model wrapper

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.objects = None
        self.model_name = None
        self.detector = None
        self.labels = []

    def prepare(self, model_name):
        """
        Prepare model for prediction

        :param model_name: model name
        """
        self.model_name = model_name
        self.detector = hub.load('./model/ssd_mobilenet_2')
        self.labels = [
            "person",
            "bicycle",
            "car",
            "motorcycle",
            "airplane",
            "bus",
            "train",
            "truck",
            "boat",
            "traffic light",
            "fire hydrant",
            "stop sign",
            "parking meter",
            "bench",
            "bird",
            "cat",
            "dog",
            "horse",
            "sheep",
            "cow",
            "elephant",
            "bear",
            "zebra",
            "giraffe",
            "backpack",
            "umbrella",
            "handbag",
            "tie",
            "suitcase",
            "frisbee",
            "skis",
            "snowboard",
            "sports ball",
            "kite",
            "baseball bat",
            "baseball glove",
            "skateboard",
            "surfboard",
            "tennis racket",
            "bottle",
            "wine glass",
            "cup",
            "fork",
            "knife",
            "spoon",
            "bowl",
            "banana",
            "apple",
            "sandwich",
            "orange",
            "broccoli",
            "carrot",
            "hot dog",
            "pizza",
            "donut",
            "cake",
            "chair",
            "couch",
            "potted plant",
            "bed",
            "dining table",
            "toilet",
            "tv",
            "laptop",
            "mouse",
            "remote",
            "keyboard",
            "cell phone",
            "microwave",
            "oven",
            "toaster",
            "sink",
            "refrigerator",
            "book",
            "clock",
            "vase",
            "scissors",
            "teddy bear",
            "hair drier",
            "toothbrush"
        ]

    def predict(self, img):
        """
        Predict objects in image

        :param img: video frame to analyze
        """
        self.tracker.objects = []  # reset objects

        dims = [256, 256]
        tf_img = np.asarray(img)
        tf_img = cv2.resize(tf_img, (dims[0], dims[1]))
        tf_img = np.expand_dims(tf_img, axis=0)
        tf_img = tf.image.resize_with_pad(tf_img, dims[0], dims[1])

        # resize and pad the image to keep the aspect ratio and fit the expected size
        image = tf.cast(tf_img, dtype=tf.uint8)

        # run model inference
        outputs = self.detector(image)

        i = 0
        for box in outputs["detection_boxes"]:
            b = []
            b.append(float(box[0][1]))
            b.append(float(box[0][0]))
            b.append(float(box[0][3] - box[0][1]))
            b.append(float(box[0][2] - box[0][0]))
            class_id = int(outputs["detection_classes"][i][0])
            obj = {
                self.tracker.IDX_KEYPOINTS: [],
                self.tracker.IDX_CLASS: self.get_label(class_id),
                self.tracker.IDX_ID: i,
                self.tracker.IDX_BOX: b,
                self.tracker.IDX_CENTER: self.tracker.keypoints.build_center(b),
                self.tracker.IDX_SCORE: float(outputs["detection_scores"][i][0])
            }

            # check score and filters (min score is defined in filter)
            if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_DETECT):
                continue

            self.tracker.objects.append(obj)
            i += 1

    def get_label(self, idx):
        """
        Get label for idx

        :param idx: index
        :return: label
        """
        idx = idx - 1
        if idx < len(self.labels):
            return self.labels[idx]

    def append(self, img):
        """
        Append overlay to image

        :param img: image frame
        :return: image frame with overlay
        """
        self.tracker.overlay.img = img  # needed reset here!!!
        if self.tracker.objects is not None:
            for idx in range(0, len(self.tracker.objects)):
                if self.tracker.render.bounds:
                    label = str(self.tracker.objects[idx][self.tracker.IDX_CLASS]) + \
                            ' ' + str(idx) + \
                            ' => ' + str(self.tracker.objects[idx][self.tracker.IDX_ID]) + \
                            ' (' + str(round(self.tracker.objects[idx][self.tracker.IDX_SCORE], 2)) + '%)'

                    self.tracker.overlay.draw_bounding(self.tracker.objects[idx][self.tracker.IDX_BOX], label)
                    self.tracker.overlay.draw_center(self.tracker.objects[idx][self.tracker.IDX_CENTER])
                    idx += 1

        return self.tracker.overlay.img

    def unload(self):
        """Unload model from memory"""
        self.detector = None
        self.labels = []

    def get_target_point(self, name, idx):
        """
        Get center point of target

        :param name: point name
        :param idx: index
        :return: center point
        """
        if self.tracker.objects is not None and idx < len(self.tracker.objects[idx]):
            return self.tracker.objects[idx][self.tracker.IDX_CENTER]
