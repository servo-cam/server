#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Targets:
    def __init__(self, tracker=None):
        """
        Targets handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.idx = None
        self.tmp_idx = None
        self.identifier = None
        self.tmp_identifier = None
        self.change_idx = None

        # states
        self.matched = False
        self.is_target = False
        self.search = False
        self.lost = False

        # mode
        self.single = False
        self.locked = False

        # center of target
        self.center_last = [0, 0]
        self.center_current = [0, 0]

        # bounding box of target
        self.box_current = [0, 0, 0, 0]
        self.box_lock = [0, 0, 0, 0]
        self.box_last = {}

    def choose(self):
        """Choose target idx"""
        # ui self.tracker.render.build_target_buttons()
        self.handle_switch()

        # get current target candidate
        current = self.tracker.finder.find()
        if current is not None:
            self.matched = True
        else:
            self.matched = False

        self.assign(current)
        # ui self.tracker.render.update_target_buttons()
        self.is_target = self.matched

        if self.has_target():
            self.idx = current  # update current idx with current
            self.tmp_idx = current

        # check for target lost
        self.tracker.target.check()

        # clear target lost counter
        if not self.is_locked() or self.has_target():
            self.tracker.target.clr()

        # check if object found
        if current is None or current >= len(self.tracker.objects):
            return

        # update identifier
        if self.tracker.IDX_ID in self.tracker.objects[current].keys():
            self.identifier = self.tracker.objects[current][self.tracker.IDX_ID]
            self.tmp_identifier = self.tracker.objects[current][self.tracker.IDX_ID]

        return self.idx

    def assign(self, idx):
        """
        Assign current target

        :param idx: index of object
        """
        if idx is None:
            return

        if idx < len(self.tracker.objects):
            self.center_last = self.tracker.objects[idx][self.tracker.IDX_CENTER]
            self.center_current = self.tracker.objects[idx][self.tracker.IDX_CENTER]
            self.box_current = self.tracker.objects[idx][self.tracker.IDX_BOX]

            if self.is_locked():
                self.box_lock = self.tracker.objects[idx][self.tracker.IDX_BOX]

            if self.tracker.IDX_ID in self.tracker.objects[idx].keys():
                self.identifier = self.tracker.objects[idx][self.tracker.IDX_ID]
                self.tmp_identifier = self.tracker.objects[idx][self.tracker.IDX_ID]

        # remove unused objects
        for i in self.box_last.keys():
            if i < len(self.tracker.objects):
                # remove old objects
                self.box_last[i] = None

        # update last lock bounding box
        for obj in self.tracker.objects:
            if self.tracker.IDX_BOX in obj.keys():
                self.box_last[idx] = obj[self.tracker.IDX_BOX]

    def handle_switch(self):
        """Handle target change"""
        if self.change_idx is not None:
            self.idx = self.change_idx
            self.tmp_idx = self.change_idx

            if self.idx < len(self.tracker.objects):
                self.center_last = self.tracker.objects[self.idx][self.tracker.IDX_CENTER]
                if self.tracker.IDX_ID in self.tracker.objects[self.idx].keys():
                    self.identifier = self.tracker.objects[self.idx][self.tracker.IDX_ID]
                if self.is_locked():
                    self.box_lock = self.tracker.objects[self.idx][self.tracker.IDX_BOX]
            self.change_idx = None

    def switch_target(self, idx):
        """
        Switch target

        :param idx: index of object
        """
        self.idx = idx
        self.change_idx = idx
        self.enable_lock()

    def get_target_point(self, name, idx=0):
        """
        Get target point

        :param name: name of target point
        :param idx: index of target point
        :return: target point
        """
        target = self.tracker.targeting.now
        if self.tracker.wrapper is None:
            return target

        tmp = self.tracker.wrapper.get_target_point(name, idx)
        if tmp is not None:
            target = tmp

        return target

    def lock(self, clear=True):
        """
        Lock on object

        :param clear: clear search and lost
        """
        if clear:
            self.search = False
            self.lost = False

        self.identifier = self.tmp_identifier
        if self.idx in self.box_last and self.box_last[self.idx] is not None:
            self.box_lock = self.box_last[self.idx]

        self.enable_lock()

    def unlock(self, clear=True):
        """
        Unlock from object

        :param clear: clear search and lost
        """
        self.locked = False

        if clear:
            self.search = False
            self.lost = False

        self.tmp_identifier = -1
        self.box_lock = [0, 0, 0, 0]
        self.tracker.controller.control_auto.update_target_lock()
        self.tracker.target.clr()

    def on_click(self, coords):
        """
        Handle click on object on video

        :param coords: coordinates of click
        """
        if self.tracker.render.simulator:
            coords[0] -= self.tracker.dx
            coords[1] -= self.tracker.dy
        idx = 0
        for obj in self.tracker.objects:
            if self.tracker.IDX_BOX in obj.keys():
                if self.tracker.keypoints.check_bounding(coords, obj[self.tracker.IDX_BOX]):
                    self.switch_target(idx)
                    return
            idx += 1

    def enable_lock(self):
        """Enable lock mode"""
        self.locked = True
        self.tracker.controller.control_auto.update_target_lock()

    def next(self):
        """Switch to next object"""
        idx = self.tracker.finder.find_next()
        if idx is None:
            idx = self.tracker.finder.find_first()
            if idx is None:
                if self.idx is not None:
                    idx = self.idx
                    idx += 1
                    if idx >= len(self.tracker.objects):
                        idx = 0

        if idx is not None and idx < len(self.tracker.objects):
            self.idx = idx
            self.change_idx = idx
            self.box_lock = self.tracker.objects[idx][self.tracker.IDX_BOX]
            if self.tracker.IDX_ID in self.tracker.objects[idx].keys():
                self.identifier = self.tracker.objects[idx][self.tracker.IDX_ID]
            self.enable_lock()

    def prev(self):
        """Switch to previous object"""
        idx = self.tracker.finder.find_prev()
        if idx is None:
            idx = self.tracker.finder.find_last()
            if idx is None:
                if self.idx is not None:
                    idx = self.idx
                    idx -= 1
                    if idx < 0:
                        idx = len(self.tracker.objects) - 1

        if idx is not None and idx < len(self.tracker.objects):
            self.idx = idx
            self.change_idx = idx
            self.box_lock = self.tracker.objects[idx][self.tracker.IDX_BOX]
            if self.tracker.IDX_ID in self.tracker.objects[idx].keys():
                self.identifier = self.tracker.objects[idx][self.tracker.IDX_ID]
            self.enable_lock()

    def reset_bounding(self):
        """Reset lock and tmp bounding"""
        self.box_lock = [0, 0, 0, 0]
        self.box_current = [0, 0, 0, 0]

    def resize_bounding(self):
        """Increase lock bounding when searching"""
        self.box_lock[0] -= 0.01
        self.box_lock[1] -= 0.01
        self.box_lock[2] += 0.02
        self.box_lock[3] += 0.02

    def is_locked(self):
        """
        Return true if locked

        :return: true if locked
        """
        return self.locked

    def is_search(self):
        """
        Return true if search mode

        :return: true if search mode
        """
        return self.search

    def is_single(self):
        """
        Return true if single target mode

        :return: true if single target mode
        """
        return self.single

    def is_lost(self):
        """
        Return true if target lost

        :return: true if target lost
        """
        return self.lost

    def has_target(self):
        """
        Return true if target detected

        :return: true if target
        """
        return self.matched
