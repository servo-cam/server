#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from datetime import datetime
import cv2
from core.utils import trans


class Overlay:
    def __init__(self, tracker=None):
        """
        Overlay drawing main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.img = None
        self.status_font_size = 1
        self.status_font_thickness = 2
        self.prev_status = {}

    def draw_path(self, from_x, from_y, to_x, to_y, r, g, b):
        """
        Draw path

        :param from_x: X coordinate of the starting point
        :param from_y: Y coordinate of the starting point
        :param to_x: X coordinate of the ending point
        :param to_y: Y coordinate of the ending point
        :param r: Red color value
        :param g: Green color value
        :param b: Blue color value
        """
        # draw connection
        self.draw_line(from_x, from_y, to_x, to_y, r, g, b)

        # draw joint
        self.draw_circle(from_x, from_y, r, g, b)

    def draw_line(self, from_x, from_y, to_x, to_y, r, g, b, t=2):
        """
        Draw line

        :param from_x: X coordinate of the starting point
        :param from_y: Y coordinate of the starting point
        :param to_x: X coordinate of the ending point
        :param to_y: Y coordinate of the ending point
        :param r: Red color value
        :param g: Green color value
        :param b: Blue color value
        :param t: Line thickness
        """
        if self.img is None:
            return

        h, w, _ = self.img.shape
        zoom = self.tracker.render.get_zoom_value()

        # calculate the cropping values based on the zoom level
        x_delta = int((w - (w / zoom)) / 2)  # current image x from original
        y_delta = int((h - (h / zoom)) / 2)  # current image y from original

        fx = int((from_x * w * zoom) - (x_delta * zoom))
        fy = int((from_y * h * zoom) - (y_delta * zoom))
        tx = int((to_x * w * zoom) - (x_delta * zoom))
        ty = int((to_y * h * zoom) - (y_delta * zoom))

        cv2.line(
            img=self.img,
            pt1=(int(fx), int(fy)),
            pt2=(int(tx), int(ty)),
            color=(r, g, b),
            thickness=t
        )

    def draw_bounding(self, box, label=None):
        """
        Draw bounding box

        :param box: Bounding box coordinates
        :param label: Label to draw on the bounding box
        """
        self.draw_rectangle(box[0], box[1], box[2], box[3], 0, 255, 0, 2, label)

    def draw_center(self, center):
        """
        Draw bounding box center

        :param center: Bounding box center coordinates
        """
        self.draw_circle(center[0], center[1], 0, 255, 0)

    def draw_rectangle(self, x, y, width, height, r, g, b, t=2, label=None, text_size=0.4, text_rgb=(255, 255, 255),
                       text_bg=True):
        """
        Draw rectangle

        :param x: X coordinate of the starting point
        :param y: Y coordinate of the starting point
        :param width: Width of the rectangle
        :param height: Height of the rectangle
        :param r: Red color value
        :param g: Green color value
        :param b: Blue color value
        :param t: Line thickness
        :param label: Label to draw on the bounding box
        :param text_size: Text size
        :param text_rgb: Text color
        :param text_bg: Draw text background
        """
        if self.img is None:
            return

        h, w, _ = self.img.shape
        zoom = self.tracker.render.get_zoom_value()

        # calculate the cropping values based on the zoom level
        x_delta = int((w - (w / zoom)) / 2)  # current image x from original
        y_delta = int((h - (h / zoom)) / 2)  # current image y from original

        fx = int((x * w * zoom) - (x_delta * zoom))
        fy = int((y * h * zoom) - (y_delta * zoom))
        tx = int(((x + width) * w * zoom) - (x_delta * zoom))
        ty = int(((y + height) * h * zoom) - (y_delta * zoom))

        cv2.rectangle(
            img=self.img,
            pt1=(int(fx), int(fy)),
            pt2=(int(tx), int(ty)),
            color=(r, g, b),
            thickness=t
        )

        if self.tracker.render.labels or not text_bg:
            if label is not None:
                if text_bg:
                    cv2.rectangle(
                        img=self.img,
                        pt1=(int(fx), int(fy) - 20),
                        pt2=(int(tx), int(fy)),
                        color=(0, 0, 0),
                        thickness=-1
                    )
                cv2.putText(self.img, label, (fx + 4, fy - 7), cv2.FONT_HERSHEY_SIMPLEX, text_size, text_rgb, 1)

    def draw_crosshair(self, x, y, r, g, b, t=2):
        """
        Draw crosshair

        :param x: X coordinate of the starting point
        :param y: Y coordinate of the starting point
        :param r: Red color value
        :param g: Green color value
        :param b: Blue color value
        :param t: Line thickness
        """
        self.draw_line(0, y, 1, y, r, g, b, t)
        self.draw_line(x, 0, x, 1, r, g, b, t)

    def draw_circle(self, from_x, from_y, r, g, b, t=2):
        """
        Draw circle

        :param from_x: X coordinate of the starting point
        :param from_y: Y coordinate of the starting point
        :param r: Red color value
        :param g: Green color value
        :param b: Blue color value
        :param t: Line thickness
        """
        if self.img is None:
            return

        h, w, _ = self.img.shape
        zoom = self.tracker.render.get_zoom_value()

        # calculate the cropping values based on the zoom level
        x_delta = int((w - (w / zoom)) / 2)  # current image x from original
        y_delta = int((h - (h / zoom)) / 2)  # current image y from original

        x = int((from_x * w * zoom) - (x_delta * zoom))
        y = int((from_y * h * zoom) - (y_delta * zoom))

        cv2.circle(self.img, (x, y), 2, (r, g, b), t)

    def show_video_label(self, label, text):
        """
        Show video label

        :param label: Label name
        :param text: Label text
        """
        if label in self.prev_status and self.prev_status[label] == text:
            return
        self.tracker.window.container_video.label[label].setText(text)
        self.tracker.window.container_video.label[label].adjustSize()
        self.tracker.window.container_video.update_pos()
        self.tracker.window.container_video.label[label].setVisible(True)
        self.prev_status[label] = text

    def hide_video_label(self, label):
        """
        Hide video label

        :param label: Label name
        """
        if label in self.prev_status and self.prev_status[label] is None:
            return
        self.tracker.window.container_video.label[label].setVisible(False)
        self.prev_status[label] = None

    def draw_info(self):
        """Draw info on the video, like status, mode, etc."""
        # remote status
        if self.tracker.remote.status is None:
            self.hide_video_label('remote')
        else:
            self.show_video_label('remote', self.tracker.remote.status)

        if not self.tracker.render.text:
            return

        # mode
        modes = []
        if self.tracker.window.controls_tabs.currentIndex() == 0:
            modes.append('MANUAL')

        if self.tracker.target_mode != self.tracker.TARGET_MODE_OFF and self.tracker.target_mode != self.tracker.TARGET_MODE_IDLE:
            modes.append('AUTO ({})'.format(self.tracker.target_mode))

        if self.tracker.action.enabled:
            modes.append('ACTION')

        # current control mode
        txt = ' + '.join(modes)

        if self.tracker.wrapper is None:
            txt += ' [NO AI]'

        self.show_video_label('mode', txt)

        # servos
        servos = []
        if self.tracker.servo.enable:
            if self.tracker.servo.remote is not None:
                servos.append('REMOTE ({})'.format(self.tracker.servo.remote))
            if self.tracker.servo.local is not None:
                servos.append('LOCAL ({})'.format(self.tracker.servo.local))
            if self.tracker.servo.stream is not None:
                servos.append('STREAM ({})'.format(self.tracker.servo.stream))
        if len(servos) > 0:
            self.show_video_label('servo', 'SERVO: ' + ' + '.join(servos))
        else:
            self.hide_video_label('servo')

        # fps
        info = ''
        info += 'FPS: ' + str(int(self.tracker.current_fps)) + ', '
        info += str(int(self.tracker.render.get_zoom_value())) + 'x, '
        info += str(self.tracker.render.size[0]) + 'x' + str(self.tracker.render.size[1])
        self.show_video_label('info.fps', info)

    def draw_status(self):
        """Draw status on the video, like searching, lost, locked, etc."""
        if self.img is None or not self.tracker.render.text:
            # clear status
            self.hide_video_label('status.state')
            self.hide_video_label('status.current')
            self.hide_video_label('status.action')
            return

        txt_state = None
        txt_current = None
        txt_action = None

        # state: searching, lost, locked
        if self.tracker.state[self.tracker.STATE_SEARCHING]:
            txt_state = trans('state.' + self.tracker.STATE_SEARCHING) + \
                        '(' + str(self.tracker.target.AS_LOST_MIN_TIME - self.tracker.target.counter_leave) + ')'
        elif self.tracker.state[self.tracker.STATE_LOST]:
            txt_state = trans('state.' + self.tracker.STATE_LOST)
        elif self.tracker.state[self.tracker.STATE_LOCKED]:
            txt_state = trans('state.' + self.tracker.STATE_LOCKED)

        # current work
        if self.tracker.state[self.tracker.STATE_TARGET]:
            txt_current = trans('state.' + self.tracker.STATE_TARGET) + '(' + str(self.tracker.target.counter_on) + ')'

        # action
        if self.tracker.state[self.tracker.STATE_ACTION]:
            txt_action = trans('state.' + self.tracker.STATE_ACTION)

            # add timer if not single action
            if self.tracker.action.auto_mode == self.tracker.ACTION_MODE_CONTINUOUS:
                txt_action += ' (' + str(self.tracker.action.action_counter) + ')'

        # state
        if txt_state is not None:
            self.show_video_label('status.state', txt_state)
        else:
            self.hide_video_label('status.state')

        # current work
        if txt_current is not None:
            self.show_video_label('status.current', txt_current)
        else:
            self.hide_video_label('status.current')

        # action
        if txt_action is not None:
            self.show_video_label('status.action', txt_action)
        else:
            self.hide_video_label('status.action')

    def draw_remote_status(self):
        """Draw remote status on the video, like device name, etc."""
        if self.img is None or self.tracker.remote_status is None:
            return

        current = None
        if self.tracker.source == self.tracker.SOURCE_REMOTE:
            if self.tracker.remote_ip is not None:
                if self.tracker.remote_ip in self.tracker.remote_status:
                    current = self.tracker.remote_status[self.tracker.remote_ip]
        else:
            if '-' in self.tracker.remote_status:
                current = self.tracker.remote_status['-']

        if current is None or current == '':
            self.hide_video_label('status.device')
            return

        self.show_video_label('status.device', str(current))

    def draw_debug_boxes(self):
        """Draw debug boxes on the video."""
        for id in self.tracker.sorter.prev_boxes:
            label = str(id) + ' (' + str(
                (datetime.now() - self.tracker.sorter.prev_boxes[id]['dt']).seconds) + ')' + ' x' + str(
                self.tracker.sorter.prev_boxes[id]['c'])
            self.draw_rectangle(self.tracker.sorter.prev_boxes[id]['box'][0],
                                self.tracker.sorter.prev_boxes[id]['box'][1],
                                self.tracker.sorter.prev_boxes[id]['box'][2],
                                self.tracker.sorter.prev_boxes[id]['box'][3], 50, 205, 50, 1, label, 1, (50, 205, 50),
                                False)

        for id in self.tracker.targets.box_last:
            if self.tracker.targets.box_last[id] is not None:
                self.draw_rectangle(self.tracker.targets.box_last[id][0],
                                    self.tracker.targets.box_last[id][1],
                                    self.tracker.targets.box_last[id][2],
                                    self.tracker.targets.box_last[id][3], 50, 5, 150, 1, str(id), 1, (50, 5, 150),
                                    False)

    def draw_area(self, coords, rgb, t=2):
        """
        Draw area on the video.

        :param coords: coordinates of the area
        :param rgb: color of the area
        :param t: thickness of border
        """
        if self.img is None:
            return

        self.draw_rectangle(coords[0], coords[1], coords[2], coords[3], rgb[0], rgb[1], rgb[2], t)
