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
from wrapper.config import movenet as config


class Movenet:
    def __init__(self, tracker):
        """
        Movenet model wrapper

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.objects = None
        self.model_name = None
        self.model = None
        self.net = None
        self.idx = {}
        self.joints = []
        self.target_idx = []

    def prepare(self, model_name):
        """
        Prepare model for prediction

        :param model_name: model name
        """
        self.model_name = model_name
        self.model = hub.load('./model/' + model_name)
        # self.model = hub.load('https://tfhub.dev/google/movenet/singlepose/thunder/3')
        self.net = self.model.signatures['serving_default']
        self.cache_config()

    def reset(self):
        """Reset predictions"""
        self.objects = None

    def predict(self, img):
        """
        Make predictions and get objects

        :param img: video frame to analyze
        """
        dims = config['detector'][self.model_name]['dims']
        tf_img = np.asarray(img)
        tf_img = cv2.resize(tf_img, (dims[0], dims[1]))
        tf_img = np.expand_dims(tf_img, axis=0)
        tf_img = tf.image.resize_with_pad(tf_img, dims[0], dims[1])

        # resize and pad the image to keep the aspect ratio and fit the expected size
        image = tf.cast(tf_img, dtype=tf.int32)

        # run model inference
        outputs = self.net(image)

        # parse predictions
        self.tracker.objects = []

        # multi pose [lightning]
        if self.model_name == 'movenet_multi_pose_lightning_1':
            for pose in outputs['output_0'].numpy()[0]:  # output_0 is a float32 [1, 6, 56] tensor
                obj = {
                    self.tracker.IDX_KEYPOINTS: []
                }
                x = 0
                for i in range(0, 17):  # 17 keypoints [x, y, score]
                    obj[self.tracker.IDX_KEYPOINTS].append({
                        self.tracker.IDX_X: pose[1 + x],  # x
                        self.tracker.IDX_Y: pose[0 + x],  # y
                        self.tracker.IDX_SCORE: pose[2 + x]  # score
                    })
                    x += 3

                # build bounding box and center
                obj[self.tracker.IDX_ID] = 0
                obj[self.tracker.IDX_CLASS] = 'person'
                obj[self.tracker.IDX_SCORE] = pose[55]  # score is the last value in the array
                obj[self.tracker.IDX_BOX] = [pose[52], pose[51], (pose[54] - pose[52]), (pose[53] - pose[51])]
                obj[self.tracker.IDX_CENTER] = self.tracker.keypoints.build_center(obj[self.tracker.IDX_BOX])

                # check score and filters (min score is defined in filter)
                if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_DETECT):
                    continue

                self.tracker.objects.append(obj)
        else:
            # single pose [lightning and thunder]
            for pose in outputs['output_0'].numpy()[0]:  # output_0 is a float32 [1, 1, 17, 3] tensor
                obj = {
                    self.tracker.IDX_KEYPOINTS: []
                }
                for coord in pose:
                    obj[self.tracker.IDX_KEYPOINTS].append({
                        self.tracker.IDX_X: coord[1],  # x
                        self.tracker.IDX_Y: coord[0],  # y
                        self.tracker.IDX_SCORE: coord[2]  # score
                    })

                # build bounding box and center
                obj[self.tracker.IDX_ID] = 0
                obj[self.tracker.IDX_CLASS] = 'person'
                obj[self.tracker.IDX_SCORE] = self.calc_score(obj[self.tracker.IDX_KEYPOINTS])
                obj[self.tracker.IDX_BOX] = self.tracker.keypoints.build_bounding(obj[self.tracker.IDX_KEYPOINTS])
                obj[self.tracker.IDX_CENTER] = self.tracker.keypoints.build_center(obj[self.tracker.IDX_BOX])

                # check score and filters (min score is defined in filter)
                if not self.tracker.filter.is_allowed(obj, self.tracker.filter.FILTER_DETECT):
                    continue

                self.tracker.objects.append(obj)

        # list of box, center and 17 keypoints (x, y, score)

    def calc_score(self, keypoints):
        """
        Calculate score

        :param keypoints: keypoints
        :return: score
        """
        score = 0
        for point in keypoints:
            score += point[self.tracker.IDX_SCORE]
        return score / len(keypoints)

    def append(self, img):
        """
        Append predictions to image

        :param img: video frame
        :return: image with overlay
        """
        self.tracker.overlay.img = img

        if self.tracker.objects is not None and len(self.tracker.objects) > 0:
            for idx in range(0, len(self.tracker.objects)):
                j = 0
                for joint in self.joints:
                    if not self.has_score(idx, j):
                        j += 1
                        continue

                    from_x, from_y, to_x, to_y = self.get_coords(idx, j)
                    score = self.get_score(idx, j)

                    if score > 0.3:
                        self.tracker.overlay.draw_path(from_x, from_y, to_x, to_y, joint[5][0], joint[5][1],
                                                       joint[5][2])
                    j += 1
                if self.tracker.render.bounds:
                    label = str(self.tracker.objects[idx][self.tracker.IDX_CLASS]) + \
                            ' ' + str(idx) + \
                            ' => ' + str(self.tracker.objects[idx][self.tracker.IDX_ID]) + \
                            ' (' + str(round(self.tracker.objects[idx][self.tracker.IDX_SCORE], 2)) + '%)'
                    self.tracker.overlay.draw_bounding(self.tracker.objects[idx][self.tracker.IDX_BOX], label)
                    self.tracker.overlay.draw_center(self.tracker.objects[idx][self.tracker.IDX_CENTER])

        return self.tracker.overlay.img

    def unload(self):
        """Unload model from memory"""
        self.model = {}
        self.net = {}
        self.model = None
        self.net = None
        self.idx = {}
        self.joints = []
        self.target_idx = []
        self.tracker.debug.log('MODEL UNLOAD: MEMORY CLEANED')

    def cache_config(self):
        """Cache pose joints"""
        self.idx = config['idx']
        paths = config['paths']
        keys = paths.keys()
        for path in keys:
            data = paths[path]
            joint = {
                0: [],  # from x
                1: [],  # from y
                2: [],  # to x
                3: [],  # to y
                4: [],  # score
                5: [],  # rgb
            }
            for point in data['fx']:
                joint[0].append(self.idx[point])
            for point in data['fy']:
                joint[1].append(self.idx[point])
            for point in data['tx']:
                joint[2].append(self.idx[point])
            for point in data['ty']:
                joint[3].append(self.idx[point])
            for point in data['score']:
                joint[4].append(self.idx[point])
            for point in data['rgb']:
                joint[5].append(point)

            self.joints.append(joint)

        self.cache_target_anchors()

    def cache_target_anchors(self):
        """Cache target anchors"""
        self.target_idx.append(self.idx['nose'])
        self.target_idx.append(self.idx['left_ear'])
        self.target_idx.append(self.idx['right_ear'])
        self.target_idx.append(self.idx['left_shoulder'])
        self.target_idx.append(self.idx['right_shoulder'])
        self.target_idx.append(self.idx['left_hip'])
        self.target_idx.append(self.idx['right_hip'])
        self.target_idx.append(self.idx['left_knee'])
        self.target_idx.append(self.idx['right_knee'])

    def find_pose_point(self, idx, n, axis):
        """
        Find point in pose

        :param idx: object index
        :param n: point index
        :param axis: axis index
        :return: point coordinate
        """
        return self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][n][axis]

    def get_coord(self, idx, n, part, axis):
        """
        Get coordinate

        :param idx: object index
        :param n: point index
        :param part: from/to
        :param axis: axis index
        :return: coordinate
        """
        # if only one point then return coordinate for this one
        if len(self.joints[n][part]) == 1:
            return self.find_pose_point(idx, self.joints[n][part][0], axis)
        else:
            # if multiple points then calculate coordinate between them
            sum = 0.0
            for joint in self.joints[n][part]:
                sum += self.find_pose_point(idx, joint, axis)
            return sum / len(self.joints[n][part])

    def get_coords(self, idx, n):
        """
        Get coordinates

        :param idx: object index
        :param n: point index
        :return: coordinates
        """
        from_x = self.get_coord(idx, n, 0, self.tracker.IDX_X)
        from_y = self.get_coord(idx, n, 1, self.tracker.IDX_Y)
        to_x = self.get_coord(idx, n, 2, self.tracker.IDX_X)
        to_y = self.get_coord(idx, n, 3, self.tracker.IDX_Y)

        return from_x, from_y, to_x, to_y

    def get_score(self, idx, n):
        """
        Get score

        :param idx: object index
        :param n: point index
        :return: score
        """
        # if only one point then check score for this one
        if len(self.joints[n][4]) == 1:  # score is the fourth element in the array
            return self.find_pose_point(idx, self.joints[n][4][0], self.tracker.IDX_SCORE)
        else:
            # if multiple points then check score for all
            sum = 0.0
            for joint in self.joints[n][4]:
                sum += self.find_pose_point(idx, joint, self.tracker.IDX_SCORE)
            return sum / len(self.joints[n][4])

    def has_score(self, idx, n):
        """
        Check if score is sufficient

        :param idx: object index
        :param n: point index
        :return: True if score is sufficient
        """
        res = True
        # if only one point then check score for this one
        if len(self.joints[n][4]) == 1:
            if self.find_pose_point(idx, self.joints[n][4][0], self.tracker.IDX_SCORE) < 0.35:  # TODO: score to config
                res = False
        else:
            # if multiple points then check score for all
            for point in self.joints[n][4]:
                if self.find_pose_point(idx, point, self.tracker.IDX_SCORE) < 0.35:  # TODO: score to config
                    res = False
                    break
        return res

    def get_target_point(self, name, idx=0):
        """
        Get target point

        :param name: point name
        :param idx: object index
        :return: point coordinate (x, y)
        """
        if self.tracker.objects is None or len(self.tracker.objects) == 0:
            return

        # if self.objects[idx][self.tracker.IDX_SCORE] < 0.35:
        # return

        point = {
            'nose': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[0]],
            'left_ear': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[1]],
            'right_ear': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[2]],
            'left_shoulder': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[3]],
            'right_shoulder': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[4]],
            'left_hip': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[5]],
            'right_hip': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[6]],
            'left_knee': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[7]],
            'right_knee': self.tracker.objects[idx][self.tracker.IDX_KEYPOINTS][self.target_idx[8]],
            'mid_head': {},
            'mid_body': {},
            'mid_body_hip': {},
            'body_heart': {},
            'left_leg': {},
            'right_leg': {}
        }

        # initial
        target = [point['nose'][0], point['nose'][1]]

        # head
        point['mid_head'][0] = (point['left_ear'][0] + point['right_ear'][0]) / 2
        point['mid_head'][1] = (point['left_ear'][1] + point['right_ear'][1]) / 2

        # neck
        point['mid_body'][0] = (point['left_shoulder'][0] + point['right_shoulder'][0]) / 2
        point['mid_body'][1] = (point['left_shoulder'][1] + point['right_shoulder'][1]) / 2

        # mid hip
        point['mid_body_hip'][0] = (point['left_hip'][0] + point['right_hip'][0]) / 2
        point['mid_body_hip'][1] = (point['left_hip'][1] + point['right_hip'][1]) / 2

        # heart
        point['body_heart'][0] = point['mid_body'][0] + (point['mid_body_hip'][0] - point['mid_body'][0]) / 2
        point['body_heart'][1] = point['mid_body'][1] + (point['mid_body_hip'][1] - point['mid_body'][1]) / 3.5

        # left leg
        point['left_leg'][0] = point['left_hip'][0] + (point['mid_head'][0] - point['left_hip'][0]) / 3
        point['left_leg'][1] = point['left_hip'][1] + (point['mid_head'][1] - point['left_hip'][1]) / 2

        # right leg
        point['right_leg'][0] = point['right_hip'][0] + (point['right_knee'][0] - point['right_hip'][0]) / 3
        point['right_leg'][1] = point['right_hip'][1] + (point['right_knee'][1] - point['right_hip'][1]) / 2

        if name == self.tracker.TARGET_POINT_HEAD:
            target[0] = point['mid_head'][0]
            target[1] = point['mid_head'][1]
        elif name == self.tracker.TARGET_POINT_NECK:
            target[0] = point['mid_body'][0]
            target[1] = point['mid_body'][1]
        elif name == self.tracker.TARGET_POINT_BODY:
            target[0] = point['body_heart'][0]
            target[1] = point['body_heart'][1]
        elif name == self.tracker.TARGET_POINT_LEGS:
            if point['left_knee'].score > point['right_knee'].score:
                target[0] = point['left_leg'][0]
                target[1] = point['left_leg'][1]
            else:
                target[0] = point['right_leg'][0]
                target[1] = point['right_leg'][1]
        else:
            # auto
            if point['left_ear'][self.tracker.IDX_SCORE] > point['left_shoulder'][self.tracker.IDX_SCORE] \
                    and point['left_shoulder'][self.tracker.IDX_SCORE] < 0.3 \
                    and (
                    point['left_ear'][self.tracker.IDX_SCORE] - point['left_shoulder'][self.tracker.IDX_SCORE] >= 0.5):
                target[0] = point['mid_head'][0]
                target[1] = point['mid_head'][1]
            else:
                target[0] = point['body_heart'][0]
                target[1] = point['body_heart'][1]

        return target
