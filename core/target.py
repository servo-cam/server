#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Target:
    def __init__(self, tracker=None):
        """
        Target handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.counter_on = 0
        self.counter_leave = 0
        self.interval_leave = False

        self.AS_TARGET_MIN_TIME = 3
        self.AS_LOST_MIN_TIME = 15
        self.BEFORE_TARGET_MIN_TIME = 0.3
        self.ON_TARGET_MAX_VALUE = 999

    def update(self):
        """Handle target (on target, lost, etc)"""
        # handle target lost interval
        if self.interval_leave:
            self.update_lost()

        result = False
        idx = self.tracker.targets.idx

        # if object still exists
        # and object is allowed
        # and object is in bounds
        # and object is in area
        # and object is not in ignore area
        if self.tracker.count_detected() > 0 \
                and idx is not None \
                and idx < len(self.tracker.objects) \
                and self.tracker.filter.is_allowed(self.tracker.objects[idx], self.tracker.filter.FILTER_ACTION) \
                and (self.tracker.keypoints.in_bounding(self.tracker.targeting.cam,
                                                        self.tracker.objects[idx][self.tracker.IDX_BOX])
                     or (self.tracker.targeting.dist_cn[0] <= self.tracker.targeting.threshold[0] and
                         self.tracker.targeting.dist_cn[1] <= self.tracker.targeting.threshold[1])):
            result = True
            self.counter_on += 1

            # prevent from going to infinity
            if self.counter_on > self.ON_TARGET_MAX_VALUE:
                self.counter_on = self.ON_TARGET_MAX_VALUE
        else:
            self.counter_on = 0

        # if is target but has not time required
        if (result and self.counter_on < self.AS_TARGET_MIN_TIME) or not self.tracker.targets.has_target():
            result = False

        # if on target
        if result:
            # check restrict to action area
            if not self.tracker.area.is_enabled(self.tracker.area.TYPE_ACTION) \
                    or self.tracker.area.in_area(self.tracker.targeting.cam, self.tracker.area.TYPE_ACTION):
                if self.tracker.action.is_enabled() \
                        and not self.tracker.action.is_active() \
                        and self.counter_on >= self.BEFORE_TARGET_MIN_TIME:
                    self.tracker.action.start()  # start action execute

                # on action active
                if self.tracker.action.is_active():
                    self.tracker.action.update()
            else:
                # if area leaved then stop action now!
                if self.tracker.action.is_active():
                    self.tracker.action.stop()

            # show status monit
            self.tracker.set_state(self.tracker.STATE_LOST, False)
            self.tracker.set_state(self.tracker.STATE_LOCKED, True)
            self.tracker.set_state(self.tracker.STATE_TARGET, True)

            # lock object again if no target lock and lost
            if not self.tracker.targets.is_locked() and self.tracker.targets.is_lost():
                self.tracker.targets.lock(False)  # False = don't auto-clear search and lost state
                self.tracker.targets.lost = False  # clear only is lost here

        else:
            # stop current action if no target
            if self.tracker.action.is_active():
                self.tracker.action.stop()

            # lock object again if locked and is lost and not matched
            if self.tracker.targets.is_locked() and (
                    self.tracker.targets.is_lost() or not self.tracker.targets.has_target()):
                self.tracker.targets.lock(False)  # False = don't auto-clear search and lost state

            # hide status locked monit
            self.tracker.set_state(self.tracker.STATE_LOCKED, False)
            self.tracker.set_state(self.tracker.STATE_TARGET, False)

    def check(self):
        """Check if target is lost"""
        # if locked and not matched then start counting target leave
        if self.tracker.targets.is_locked() \
                and not self.tracker.targets.has_target() \
                and not self.tracker.targets.is_search():
            self.counter_leave = 0
            self.interval_leave = True

    def update_lost(self):
        """Handle target lost interval"""
        # if not locked then do nothing
        if self.tracker.targets.box_lock is None:
            return

        self.counter_leave += 1
        self.tracker.targets.search = True  # enable search mode

        # if not locked on single target then increase search area
        if not self.tracker.targets.is_single():
            self.tracker.targets.resize_bounding()

        # show searching mode monit
        self.tracker.set_state(self.tracker.STATE_LOST, False)
        self.tracker.set_state(self.tracker.STATE_SEARCHING, True)

        # if searching timer reached (target is lost after searching)
        if self.counter_leave > self.AS_LOST_MIN_TIME:
            # print("LEAVE MAX")
            # if not single target
            if self.tracker.objects is not None and not self.tracker.targets.is_single():
                # if current tmp object still exists (it is first available object)
                if self.tracker.targets.tmp_idx is not None and self.tracker.targets.tmp_idx < len(
                        self.tracker.objects):
                    self.tracker.targets.box_lock = self.tracker.objects[self.tracker.targets.tmp_idx][
                        self.tracker.IDX_BOX]
                    self.tracker.targets.idx = self.tracker.targets.tmp_idx
                    self.tracker.targets.reset_bounding()  # reset lock and tmp bounding to zero coords
                    self.clr()  # clear leave counter, hide searching and mark target as LOST
                    self.tracker.targets.unlock()  # unlock from object

                else:
                    self.clr()  # clear leave counter, hide searching and unmark target as LOST
                    self.tracker.targets.unlock()  # unlock from object
            else:
                self.clr()  # clear leave counter, hide searching and unmark target as LOST
                self.tracker.targets.unlock()  # unlock from object

            # if not locked then set is lost
            if not self.tracker.targets.is_locked():
                self.tracker.set_state(self.tracker.STATE_LOST, True)
                self.tracker.targets.lost = True
                self.tracker.targets.reset_bounding()  # reset lock and tmp bounding to zero coords

    def clr(self):
        """Clear leave counter, disable search mode and un-mark target as LOST"""
        if self.interval_leave:
            self.interval_leave = False
            self.counter_leave = 0
            self.tracker.targets.lost = False
            self.tracker.targets.search = False

            # hide searching mode monit
            self.tracker.set_state(self.tracker.STATE_SEARCHING, False)
