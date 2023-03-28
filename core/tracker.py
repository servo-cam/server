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
import time
import re
from wrapper.movenet import Movenet
from wrapper.mobilenet import Mobilenet
from wrapper.opencv_movement_detector import OpenCVMovementDetector
from core.controller.main import Controller
from core.remote import Remote
from core.rendering import Rendering
from core.keypoints import Keypoints
from core.sockets import Sockets
from core.camera import Camera
from core.video import Video
from core.webstream import Webstream
from core.manual import Manual
from core.debugger import Debug
from core.overlay import Overlay
from core.console import Console
from core.storage import Storage
from core.servo import Servo
from core.targeting import Targeting
from core.targets import Targets
from core.target import Target
from core.finder import Finder
from core.matcher import Matcher
from core.filter import Filter
from core.area import Area
from core.patrol import Patrol
from core.action import Action
from core.sorter import Sorter
from core.mouse import Mouse
from core.serial import Serial
from core.command import Command
from core.info import Info
from core.drawing import Drawing
from core.video_filter import VideoFilter
from core.configurator import Configurator
from core.keyboard import Keyboard
from core.status import Status
from core.encrypt import Encrypt
from core.updater import Updater


class Tracker:
    # source types
    SOURCE_LOCAL = 'cam'
    SOURCE_REMOTE = 'remote'
    SOURCE_VIDEO = 'video'
    SOURCE_STREAM = 'stream'

    # movement types
    MOVEMENT_LEFT = 'LEFT'
    MOVEMENT_RIGHT = 'RIGHT'
    MOVEMENT_UP = 'UP'
    MOVEMENT_DOWN = 'DOWN'
    MOVEMENT_CENTER = 'CENTER'
    MOVEMENT_ZOOM_IN = 'ZOOM_IN'
    MOVEMENT_ZOOM_OUT = 'ZOOM_OUT'
    MOVEMENT_SPEED_UP = 'SPEED_UP'
    MOVEMENT_SPEED_DOWN = 'SPEED_DOWN'

    # action modes
    ACTION_MODE_OFF = 'OFF'
    ACTION_MODE_SINGLE = 'SINGLE'
    ACTION_MODE_SERIES = 'SERIES'
    ACTION_MODE_CONTINUOUS = 'CONTINUOUS'
    ACTION_MODE_TOGGLE = 'TOGGLE'
    ACTION_A1 = 'A1'
    ACTION_A2 = 'A2'
    ACTION_A3 = 'A3'
    ACTION_B4 = 'B4'
    ACTION_B5 = 'B5'
    ACTION_B6 = 'B6'

    # targeting modes
    TARGET_MODE_OFF = 'OFF'
    TARGET_MODE_IDLE = 'IDLE'
    TARGET_MODE_FOLLOW = 'FOLLOW'
    TARGET_MODE_PATROL = 'PATROL'
    TARGET_POINT_AUTO = 'AUTO'
    TARGET_POINT_HEAD = 'HEAD'
    TARGET_POINT_NECK = 'NECK'
    TARGET_POINT_BODY = 'BODY'
    TARGET_POINT_LEGS = 'LEGS'

    # control modes
    CONTROL_VIEW_MANUAL = 'MANUAL'
    CONTROL_VIEW_AUTO = 'AUTO'
    CONTROL_VIEW_AREA = 'AREA'

    # objects idx
    IDX_X = 0
    IDX_Y = 1
    IDX_SCORE = 2
    IDX_KEYPOINTS = 3
    IDX_CLASS = 4
    IDX_ID = 5
    IDX_BOX = 6
    IDX_CENTER = 7

    # states
    STATE_IDLE = 'IDLE'
    STATE_SEARCHING = 'SEARCHING'
    STATE_LOST = 'LOST'
    STATE_LOCKED = 'LOCKED'
    STATE_TARGET = 'TARGET'
    STATE_ACTION = 'ACTION'

    def __init__(self, window=None):
        """
        App main core class
        :param window: main window
        """
        self.version = None
        self.build = None
        self.author = "Marcin Szczygliński"
        self.email = "info@servocam.org"
        self.www = "https://servocam.org"

        self.wrappers = {}
        self.filters = {}
        self.devices = {}
        self.remote_status = {}
        self.remote_status['-'] = None

        self.wrappers['movenet'] = Movenet(self)
        self.wrappers['mobilenet'] = Mobilenet(self)
        self.wrappers['opencv_movement_detect'] = OpenCVMovementDetector(self)

        self.wrapper = None
        self.window = window

        # classes
        self.render = Rendering(self)
        self.keypoints = Keypoints(self)
        self.remote = Remote(self)
        self.sockets = Sockets(self)
        self.camera = Camera(self)
        self.video = Video(self)
        self.stream = Webstream(self)
        self.manual = Manual(self)
        self.mouse = Mouse(self)
        self.debug = Debug(self)
        self.overlay = Overlay(self)
        self.controller = Controller(self)
        self.console = Console(self)
        self.storage = Storage(self)
        self.servo = Servo(self)
        self.targeting = Targeting(self)
        self.targets = Targets(self)
        self.target = Target(self)
        self.finder = Finder(self)
        self.matcher = Matcher(self)
        self.filter = Filter(self)
        self.area = Area(self)
        self.sorter = Sorter(self)
        self.patrol = Patrol(self)
        self.action = Action(self)
        self.serial = Serial(self)
        self.command = Command(self)
        self.info = Info(self)
        self.drawing = Drawing(self)
        self.video_filter = VideoFilter(self)
        self.configurator = Configurator(self)
        self.keyboard = Keyboard(self)
        self.status = Status(self)
        self.encrypt = Encrypt(self)
        self.updater = Updater(self)

        self.source = self.SOURCE_LOCAL
        self.output = None
        self.capture = {}
        self.dx = 0
        self.dy = 0
        self.video_dim = (0, 0)
        self.objects = None
        self.model_name = None
        self.video_url = None
        self.stream_url = None
        self.remote_host = None
        self.remote_ip = None
        self.disabled = False
        self.paused = False
        self.processing = False
        self.ai_enabled = True
        self.is_debug = True
        self.socket = None
        self.target_mode = self.TARGET_MODE_OFF
        self.target_point = self.TARGET_POINT_AUTO
        self.control_view = self.CONTROL_VIEW_MANUAL
        self.fps = 30
        self.current_ts = time.time()
        self.current_fps = 0
        self.w = 0
        self.h = 0

        if self.window is not None:
            self.w = self.window.width()
            self.h = self.window.height()

        self.state = {
            self.STATE_SEARCHING: False,
            self.STATE_LOST: False,
            self.STATE_LOCKED: False,
            self.STATE_TARGET: False,
            self.STATE_ACTION: False
        }

        self.storage.init()  # load and append config.ini
        self.load_version()  # load version and build info

    def prepare(self, model_name=None):
        """
        Prepare model by name

        :param model_name: model name
        """
        # unload current model, clear memory, etc.
        if self.wrapper is not None:
            self.wrapper.unload()
        self.sorter.reset()

        # prepare wrapper for model
        if model_name == 'movenet_single_pose_lightning_4' \
                or model_name == 'movenet_single_pose_thunder_4' \
                or model_name == 'movenet_multi_pose_lightning_1':
            self.wrapper = self.wrappers['movenet']
        elif model_name == 'mobilenet':
            self.wrapper = self.wrappers['mobilenet']
        elif model_name == 'opencv_movement_detect_single' \
                or model_name == 'opencv_movement_detect_multi':
            self.wrapper = self.wrappers['opencv_movement_detect']
        else:
            self.wrapper = None

        # init model
        if self.wrapper is not None:
            self.wrapper.prepare(model_name)
        self.model_name = model_name

    def init(self, source, app=False):
        """
        Init source by name

        :param source: source name
        :param app: init from app
        """
        self.source = source

        # reset
        self.dx = 0
        self.dy = 0
        self.command.reset(True)

        if app:
            self.controller.source.toggle(source, True)
            return

        if source == self.SOURCE_LOCAL:
            self.render.blank_screen()  # clear screen
            self.capture = {'-': self.handle(source)}
        elif source == self.SOURCE_VIDEO:
            self.render.blank_screen()  # clear screen
            self.capture = {'-': self.handle(source)}
        elif source == self.SOURCE_STREAM:
            self.render.blank_screen()  # clear screen
            self.capture = {'-': self.handle(source)}
        elif source == self.SOURCE_REMOTE:
            self.render.blank_screen()  # clear screen
            if self.remote_ip is not None:
                self.remote.connect(self.remote_ip, True)

    def exec_console(self, args):
        """
        Console mode

        :param args: console arguments
        """
        print("Servo Cam console mode started. Type 'q' for exit.")
        self.console.handle(args)  # app loop

    def handle(self, mode):
        """
        Handle source by name

        :param mode: source name
        :return: source handle
        """
        if mode == self.SOURCE_LOCAL:
            return self.camera.handle(self.camera.idx)
        elif mode == self.SOURCE_VIDEO:
            return self.video.handle(self.video_url)
        elif mode == self.SOURCE_STREAM:
            return self.stream.handle(self.stream_url)
        elif mode == self.SOURCE_REMOTE:
            return self.remote.handle(self.remote_ip)

    def run(self, frame):
        """
        Run model predictions

        :param frame: frame
        :return: frame
        """
        self.objects = []
        if self.ai_enabled and not self.disabled and self.wrapper is not None:
            self.wrapper.predict(frame)
            self.sorter.apply()
        return frame

    def update(self):
        """Update frame, process, etc. (handle every frame)"""
        # get current active source frame
        if not self.paused and not self.disabled:
            self.output = self.render.get_frame()

        # process frame, get predictions, etc.
        self.output, w, h = self.render.process(self.output)

        # collect UI data, status, etc.
        self.controller.collect()

        # update controls
        self.manual.update()
        self.controller.update()
        self.mouse.update()

        # append output to overlay renderer
        self.overlay.img = self.output

        # update targeting
        if self.target_mode != self.TARGET_MODE_OFF:
            self.targeting.update()

        # update source handlers
        if self.source == self.SOURCE_REMOTE:
            self.remote.update()
        elif self.source == self.SOURCE_STREAM:
            self.stream.update()

        # update and send servo command
        if not self.disabled:
            self.command.update()

        # update remote status
        self.overlay.draw_remote_status()
        self.overlay.draw_info()

        # on video overlay drawing
        if self.drawing.enabled:
            self.drawing.update()

        # render view
        if self.output is not None:
            self.render.render(self.output, w, h)

        # montage view (multiple cameras preview)
        if self.source == self.SOURCE_REMOTE and self.render.montage:
            self.render.append_montage()

        # update debug and clients
        if self.window is not None:
            if self.is_debug:
                self.debug.update()
            self.debug.append_logs()

            # update remote clients
            self.window.ui.toolbox.remote.update()

        # video controls update (play/pause, etc.)
        if self.window.controls_tabs.currentIndex() == 4:  # 4 = video tab
            self.controller.video.update()

        # update device status
        if not self.disabled:
            self.serial.update()

        # update status
        self.controller.status.handle()

        # reset state indicator
        self.sockets.reset_state()
        self.serial.reset_state()

        # fps / ts calculation
        self.current_fps = round(1 / (time.time() - self.current_ts), 1)
        self.current_ts = time.time()

    def release(self):
        """Release all captures"""
        for ip in self.capture:
            if self.capture[ip] is not None \
                    and type(self.capture[ip]) is not np.ndarray:  # remote stream is numpy.ndarray
                self.capture[ip].release()
            else:
                self.capture[ip] = None
        self.capture = {}
        time.sleep(0.01)

    def switch_model(self, model):
        """
        Switch model by name

        :param model: model name
        """
        self.disabled = True
        self.prepare(model)
        self.disabled = False
        self.debug.log("[MODEL] SWITCHED TO: " + str(model))

    def switch_cam(self, idx):
        """
        Switch camera by idx

        :param idx: camera idx
        """
        if idx == self.camera.idx:
            self.debug.log("[CAMERA] CURRENT: " + str(idx))
            return

        # check if it is CSI camera
        if self.camera.is_csi(idx):
            self.debug.log("[CAMERA] USING CSI CAMERA")
            self.camera.csi = True
        else:
            self.camera.csi = False

        # check if it is external serial camera
        if self.camera.is_serial(idx):
            self.debug.log("[CAMERA] USING VIA SERIAL PORT CAMERA")
            self.camera.serial = True
        else:
            self.camera.serial = False

        self.disabled = True
        self.camera.idx = idx
        self.disabled = False
        self.debug.log("[CAMERA] SWITCHED TO: " + str(idx))

    def switch_source(self, src):
        """
        Switch source by name

        :param src: source name
        """
        # reset filters
        self.video_filter.clear()
        self.sorter.reset()

        # switch source
        if src == self.SOURCE_LOCAL:
            self.remote.active = False
            time.sleep(0.5)
            self.release()
            self.source = src
            try:
                self.capture = {'-': self.handle(src)}
                self.debug.log("[SOURCE] LOCAL CAMERA (USB)")
            except:
                self.capture = {}  # clear captures
                self.debug.log("[SOURCE] LOCAL CAMERA ACCESS ERROR")
        elif src == self.SOURCE_VIDEO:
            self.remote.active = False
            time.sleep(0.5)
            self.release()
            self.source = src
            try:
                self.capture = {'-': self.handle(src)}
                self.debug.log("[SOURCE] VIDEO")
            except:
                self.capture = {}  # clear captures
                self.debug.log("[SOURCE] VIDEO SRC ERROR")
        elif src == self.SOURCE_REMOTE:
            self.remote.active = True
            self.remote.send_conn_time = {}
            time.sleep(0.5)
            self.release()
            self.source = src
            if self.remote_ip is not None:
                self.remote.check(self.remote_ip, True)
            try:
                self.init(src)
                self.debug.log("[SOURCE] REMOTE CAMERA (IP)")
            except Exception as e:
                print(e)
                self.debug.log("[SOURCE] REMOTE INIT ERROR")
        elif src == self.SOURCE_STREAM:
            self.remote.active = False
            time.sleep(0.5)
            self.release()
            self.source = src
            try:
                self.capture = {'-': self.handle(src)}
                self.debug.log("[SOURCE] STREAM")
            except:
                self.capture = {}  # clear captures
                self.debug.log("[SOURCE] STREAM INIT ERROR")

        if self.wrapper is not None:
            self.wrapper.reset()

    def count_detected(self):
        """
        Count detected objects

        :return: count
        """
        if self.objects is None:
            return 0
        return len(self.objects)

    def switch_addr(self, src, addr):
        """
        Switch address by source

        :param src: source name
        :param addr: source address
        """
        # reset filters
        self.video_filter.clear()
        self.sorter.reset()

        # switch address
        if src == self.SOURCE_VIDEO:
            self.video_url = addr
        elif src == self.SOURCE_REMOTE:
            # find by custom name
            client = self.remote.get_client_by_name(addr)
            if client is not None:
                self.remote_host = client.hostname
                self.remote_ip = client.ip
            else:
                # set exact ip
                self.remote_host = addr
                if self.remote_host is not None:
                    self.remote_ip = self.remote.host2ip(self.remote_host)
                else:
                    self.remote_ip = None

            # unblock client if is disconnected or removed
            if self.remote_ip is not None:
                self.remote.unblock_ip(self.remote_ip)
                self.remote.toggle_servo(self.remote_ip)
        elif src == self.SOURCE_STREAM:
            self.stream_url = addr

        if self.wrapper is not None:
            self.wrapper.reset()

    def load_version(self):
        """Load version info from __init__.py"""
        try:
            self.version = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__version__"),
                                     open('./__init__.py').read()).group(1)
            self.build = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format("__build__"),
                                   open('./__init__.py').read()).group(1)
        except:
            self.debug.log('[ERROR] Error reading version file: __init__.py')
            self.version = "0.0.0"
            self.build = "0"

    def set_state(self, state, value=True):
        """
        Set state

        :param state: key
        :param value: value
        """
        self.state[state] = value
