#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6.QtGui import QAction, QIcon
from core.utils import trans


class UIMenu:
    def __init__(self, window=None):
        """
        Menu UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """Setup all menus"""
        self.window.menu = {}
        self.setup_app()
        self.setup_source()
        self.setup_model()
        self.setup_servo()
        self.setup_render()
        self.setup_filters()

        if self.window.tracker.is_debug:
            self.setup_debug()

        self.setup_config()
        self.setup_info()

    def setup_app(self):
        """Setup app menu"""
        self.window.menu['app'] = {}
        self.window.menu['app']['disabled'] = QAction(trans("menu.app.disable"),
                                                      self.window, checkable=True, shortcut="Ctrl+P",
                                                      triggered=self.window.tracker.controller.internals.toggle_disabled)
        self.window.menu['app']['exit'] = QAction(QIcon.fromTheme("application-exit"), trans("menu.app.exit"),
                                                  self.window, shortcut="Ctrl+Q", triggered=self.window.close)

        app_menu = self.window.menuBar().addMenu(trans("menu.app"))
        app_menu.addAction(self.window.menu['app']['disabled'])
        app_menu.addAction(self.window.menu['app']['exit'])

    def setup_source(self):
        """Setup source menu"""
        self.window.menu['source'] = {}
        self.window.menu['source']['cam'] = QAction(trans("menu.source.cam"), self.window, checkable=True)
        self.window.menu['source']['remote'] = QAction(trans("menu.source.remote"), self.window, checkable=True)
        self.window.menu['source']['video'] = QAction(trans("menu.source.video"), self.window, checkable=True)
        self.window.menu['source']['stream'] = QAction(trans("menu.source.stream"), self.window, checkable=True)

        self.window.menu['source']['cam'].triggered.connect(
            lambda: self.window.tracker.controller.source.toggle('cam'))
        self.window.menu['source']['remote'].triggered.connect(
            lambda: self.window.tracker.controller.source.toggle('remote'))
        self.window.menu['source']['video'].triggered.connect(
            lambda: self.window.tracker.controller.source.toggle('video'))
        self.window.menu['source']['stream'].triggered.connect(
            lambda: self.window.tracker.controller.source.toggle('stream'))

        source_menu = self.window.menuBar().addMenu(trans("menu.source"))
        source_menu.addAction(self.window.menu['source']['cam'])
        source_menu.addAction(self.window.menu['source']['remote'])
        source_menu.addAction(self.window.menu['source']['video'])
        source_menu.addAction(self.window.menu['source']['stream'])

    def setup_model(self):
        """Setup model menu"""
        self.window.menu['model'] = {}
        self.window.menu['model']['none'] = QAction(
            trans("menu.model.none"),
            self.window, checkable=True)
        self.window.menu['model']['movenet_single_pose_lightning_4'] = QAction(
            trans("menu.model.movenet_single_pose_lightning_4"),
            self.window, checkable=True)
        self.window.menu['model']['movenet_single_pose_thunder_4'] = QAction(
            trans("menu.model.movenet_single_pose_thunder_4"),
            self.window, checkable=True)
        self.window.menu['model']['movenet_multi_pose_lightning_1'] = QAction(
            trans("menu.model.movenet_multi_pose_lightning_1"),
            self.window, checkable=True)
        self.window.menu['model']['mobilenet'] = QAction(trans("menu.model.mobilenet"),
                                                         self.window,
                                                         checkable=True)
        self.window.menu['model']['opencv_movement_detect_single'] = QAction(
            trans("menu.model.opencv_movement_detect_single"),
            self.window,
            checkable=True)
        self.window.menu['model']['opencv_movement_detect_multi'] = QAction(
            trans("menu.model.opencv_movement_detect_multi"),
            self.window,
            checkable=True)

        self.window.menu['model']['none'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('none'))
        self.window.menu['model']['movenet_single_pose_lightning_4'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('movenet_single_pose_lightning_4'))
        self.window.menu['model']['movenet_single_pose_thunder_4'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('movenet_single_pose_thunder_4'))
        self.window.menu['model']['movenet_multi_pose_lightning_1'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('movenet_multi_pose_lightning_1'))
        self.window.menu['model']['mobilenet'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('mobilenet'))
        self.window.menu['model']['opencv_movement_detect_single'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('opencv_movement_detect_single'))
        self.window.menu['model']['opencv_movement_detect_multi'].triggered.connect(
            lambda: self.window.tracker.controller.internals.toggle_model('opencv_movement_detect_multi'))

        model_menu = self.window.menuBar().addMenu(trans("menu.model"))
        model_menu.addAction(self.window.menu['model']['none'])
        model_menu.addAction(self.window.menu['model']['movenet_single_pose_lightning_4'])
        model_menu.addAction(self.window.menu['model']['movenet_single_pose_thunder_4'])
        model_menu.addAction(self.window.menu['model']['movenet_multi_pose_lightning_1'])
        model_menu.addAction(self.window.menu['model']['mobilenet'])
        model_menu.addAction(self.window.menu['model']['opencv_movement_detect_single'])
        model_menu.addAction(self.window.menu['model']['opencv_movement_detect_multi'])

    def setup_servo(self):
        """Setup servo menu"""
        self.window.menu['servo.remote'] = {}
        self.window.menu['servo.stream'] = {}
        self.window.menu['servo.local'] = {}
        self.window.menu['servo.axis_x'] = None
        self.window.menu['servo.axis_y'] = None
        self.window.menu['servo.enable'] = None

        servo_menu = self.window.menuBar().addMenu(trans("menu.servo"))

        # servo: remote menu
        self.window.servo_remote = servo_menu.addMenu(trans("menu.servo.remote"))

        # servo: stream menu
        self.window.servo_stream = servo_menu.addMenu(trans("menu.servo.stream"))

        # servo: local menu
        self.window.servo_local = servo_menu.addMenu(trans("menu.servo.local"))

        # local serial ports
        ports = self.window.tracker.serial.get_ports()
        for port in ports:
            self.window.menu['servo.local'][port] = QAction(port, self.window,
                                                            checkable=True)
            self.window.menu['servo.local'][port].triggered.connect(
                lambda checked=None, port=port: self.window.tracker.controller.servo.toggle_local(port))
            self.window.servo_local.addAction(self.window.menu['servo.local'][port])

        servo_menu.addSeparator()

        self.window.menu['servo.enable'] = QAction(trans("menu.servo.enable"), self.window, checkable=True)
        self.window.menu['servo.enable'].triggered.connect(
            lambda: self.window.tracker.controller.servo.toggle_enable())
        servo_menu.addAction(self.window.menu['servo.enable'])

        # servo: enable/disable x,y axis menu
        self.window.menu['servo.axis_x'] = QAction(trans("menu.servo.enable.x"), self.window, checkable=True)
        self.window.menu['servo.axis_y'] = QAction(trans("menu.servo.enable.y"), self.window, checkable=True)

        self.window.menu['servo.axis_x'].triggered.connect(
            lambda: self.window.tracker.controller.servo.toggle('x'))
        self.window.menu['servo.axis_y'].triggered.connect(
            lambda: self.window.tracker.controller.servo.toggle('y'))

        servo_menu.addAction(self.window.menu['servo.axis_x'])
        servo_menu.addAction(self.window.menu['servo.axis_y'])

    def setup_render(self):
        """Setup render menu"""
        self.window.menu['render.full_screen'] = QAction(trans("menu.rendering.full_screen"), self.window,
                                                         checkable=True)
        self.window.menu['render.fit'] = QAction(trans("menu.rendering.fit"), self.window,
                                                 checkable=True)
        self.window.menu['render.center_lock'] = QAction(trans("menu.rendering.center_lock"), self.window,
                                                         checkable=True)

        self.window.menu['render.console'] = QAction(trans("menu.rendering.console"), self.window,
                                                     checkable=True)

        self.window.menu['render.tracking'] = QAction(trans("menu.rendering.tracking"), self.window, checkable=True)
        self.window.menu['render.targeting'] = QAction(trans("menu.rendering.targeting"), self.window, checkable=True)
        self.window.menu['render.bounds'] = QAction(trans("menu.rendering.bounds"), self.window, checkable=True)
        self.window.menu['render.labels'] = QAction(trans("menu.rendering.labels"), self.window, checkable=True)
        self.window.menu['render.text'] = QAction(trans("menu.rendering.text"), self.window, checkable=True)
        self.window.menu['render.simulator'] = QAction(trans("menu.rendering.simulator"), self.window, checkable=True)

        self.window.menu['render.full_screen'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('full_screen'))
        self.window.menu['render.fit'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('fit'))
        self.window.menu['render.center_lock'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('center_lock'))
        self.window.menu['render.console'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('console'))
        self.window.menu['render.tracking'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('tracking'))
        self.window.menu['render.targeting'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('targeting'))
        self.window.menu['render.bounds'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('bounds'))
        self.window.menu['render.labels'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('labels'))
        self.window.menu['render.text'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('text'))
        self.window.menu['render.simulator'].triggered.connect(
            lambda: self.window.tracker.controller.render.toggle('simulator'))

        render_menu = self.window.menuBar().addMenu(trans("menu.rendering"))
        render_menu.addAction(self.window.menu['render.full_screen'])
        render_menu.addAction(self.window.menu['render.fit'])
        render_menu.addAction(self.window.menu['render.center_lock'])

        render_menu.addSeparator()
        render_menu.addAction(self.window.menu['render.console'])
        render_menu.addAction(self.window.menu['render.simulator'])

        render_menu.addSeparator()
        render_menu.addAction(self.window.menu['render.tracking'])
        render_menu.addAction(self.window.menu['render.targeting'])
        render_menu.addAction(self.window.menu['render.bounds'])
        render_menu.addAction(self.window.menu['render.labels'])
        render_menu.addAction(self.window.menu['render.text'])

    def setup_filters(self):
        """Setup filters menu"""
        self.window.menu['filters'] = {}
        self.window.menu['filters.input'] = {}
        self.window.menu['filters.output'] = {}

        filters_menu = self.window.menuBar().addMenu(trans("menu.filters"))
        filters_input = filters_menu.addMenu(trans("menu.filters.input"))
        filters_output = filters_menu.addMenu(trans("menu.filters.output"))
        filters_list = self.window.tracker.video_filter.filters.keys()

        for name in filters_list:
            self.window.menu['filters.input'][name] = QAction(trans('video_filter.' + name), self.window,
                                                              checkable=True)
            self.window.menu['filters.input'][name].triggered.connect(
                lambda checked=None, name=name: self.window.tracker.controller.video_filter.toggle_input(name))
            filters_input.addAction(self.window.menu['filters.input'][name])

        for name in filters_list:
            self.window.menu['filters.output'][name] = QAction(trans('video_filter.' + name), self.window,
                                                               checkable=True)
            self.window.menu['filters.output'][name].triggered.connect(
                lambda checked=None, name=name: self.window.tracker.controller.video_filter.toggle_output(name))
            filters_output.addAction(self.window.menu['filters.output'][name])

    def setup_debug(self):
        """Setup debug menu"""
        self.window.menu['debug.performance'] = QAction(trans("menu.debug.performance"), self.window, checkable=True)
        self.window.menu['debug.tracker'] = QAction(trans("menu.debug.tracker"), self.window, checkable=True)
        self.window.menu['debug.render'] = QAction(trans("menu.debug.render"), self.window, checkable=True)
        self.window.menu['debug.keypoints'] = QAction(trans("menu.debug.keypoints"), self.window, checkable=True)
        self.window.menu['debug.network'] = QAction(trans("menu.debug.network"), self.window, checkable=True)
        self.window.menu['debug.manual'] = QAction(trans("menu.debug.manual"), self.window, checkable=True)
        self.window.menu['debug.targeting'] = QAction(trans("menu.debug.targeting"), self.window, checkable=True)
        self.window.menu['debug.target'] = QAction(trans("menu.debug.target"), self.window, checkable=True)
        self.window.menu['debug.action'] = QAction(trans("menu.debug.action"), self.window, checkable=True)
        self.window.menu['debug.patrol'] = QAction(trans("menu.debug.patrol"), self.window, checkable=True)
        self.window.menu['debug.area'] = QAction(trans("menu.debug.area"), self.window, checkable=True)
        self.window.menu['debug.servo'] = QAction(trans("menu.debug.servo"), self.window, checkable=True)
        self.window.menu['debug.command'] = QAction(trans("menu.debug.command"), self.window, checkable=True)
        self.window.menu['debug.sockets'] = QAction(trans("menu.debug.sockets"), self.window, checkable=True)
        self.window.menu['debug.camera'] = QAction(trans("menu.debug.camera"), self.window, checkable=True)
        self.window.menu['debug.filter'] = QAction(trans("menu.debug.filter"), self.window, checkable=True)

        self.window.menu['debug.performance'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('performance'))
        self.window.menu['debug.tracker'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('tracker'))
        self.window.menu['debug.render'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('render'))
        self.window.menu['debug.keypoints'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('keypoints'))
        self.window.menu['debug.network'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('network'))
        self.window.menu['debug.manual'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('manual'))
        self.window.menu['debug.targeting'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('targeting'))
        self.window.menu['debug.target'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('target'))
        self.window.menu['debug.action'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('action'))
        self.window.menu['debug.patrol'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('patrol'))
        self.window.menu['debug.area'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('area'))
        self.window.menu['debug.servo'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('servo'))
        self.window.menu['debug.command'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('command'))
        self.window.menu['debug.sockets'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('sockets'))
        self.window.menu['debug.camera'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('camera'))
        self.window.menu['debug.filter'].triggered.connect(
            lambda: self.window.tracker.controller.debug.toggle('filter'))

        debug_menu = self.window.menuBar().addMenu(trans("menu.debug"))
        debug_menu.addAction(self.window.menu['debug.performance'])
        debug_menu.addAction(self.window.menu['debug.tracker'])
        debug_menu.addAction(self.window.menu['debug.render'])
        debug_menu.addAction(self.window.menu['debug.keypoints'])
        debug_menu.addAction(self.window.menu['debug.network'])
        debug_menu.addAction(self.window.menu['debug.manual'])
        debug_menu.addAction(self.window.menu['debug.targeting'])
        debug_menu.addAction(self.window.menu['debug.target'])
        debug_menu.addAction(self.window.menu['debug.action'])
        debug_menu.addAction(self.window.menu['debug.patrol'])
        debug_menu.addAction(self.window.menu['debug.area'])
        debug_menu.addAction(self.window.menu['debug.servo'])
        debug_menu.addAction(self.window.menu['debug.command'])
        debug_menu.addAction(self.window.menu['debug.sockets'])
        debug_menu.addAction(self.window.menu['debug.camera'])
        debug_menu.addAction(self.window.menu['debug.filter'])

    def setup_config(self):
        """Setup the config menu."""
        self.window.menu['config.config'] = QAction(trans("menu.config.config"), self.window, checkable=True)
        self.window.menu['config.config'].triggered.connect(
            lambda: self.window.tracker.controller.configurator.toggle('config'))

        self.window.menu['config.hosts'] = QAction(trans("menu.config.hosts"), self.window, checkable=True)
        self.window.menu['config.hosts'].triggered.connect(
            lambda: self.window.tracker.controller.configurator.toggle('hosts'))

        self.window.menu['config.streams'] = QAction(trans("menu.config.streams"), self.window, checkable=True)
        self.window.menu['config.streams'].triggered.connect(
            lambda: self.window.tracker.controller.configurator.toggle('streams'))

        self.window.menu['config.save'] = QAction(trans("menu.config.save"), self.window, checkable=False)
        self.window.menu['config.save'].triggered.connect(
            lambda: self.window.tracker.controller.configurator.save())

        config_menu = self.window.menuBar().addMenu(trans("menu.config"))
        config_menu.addAction(self.window.menu['config.config'])
        config_menu.addAction(self.window.menu['config.hosts'])
        config_menu.addAction(self.window.menu['config.streams'])
        config_menu.addAction(self.window.menu['config.save'])

    def setup_info(self):
        """Setup the info menu."""
        self.window.menu['info.about'] = QAction(trans("menu.info.about"), self.window, checkable=True)
        self.window.menu['info.change_log'] = QAction(trans("menu.info.change_log"), self.window, checkable=True)
        self.window.menu['info.website'] = QAction(trans("menu.info.website"), self.window, checkable=False)

        self.window.menu['info.about'].triggered.connect(
            lambda: self.window.tracker.controller.info.toggle('about'))
        self.window.menu['info.change_log'].triggered.connect(
            lambda: self.window.tracker.controller.info.toggle('change_log'))
        self.window.menu['info.website'].triggered.connect(
            lambda: self.window.tracker.controller.info.goto_website())

        about_menu = self.window.menuBar().addMenu(trans("menu.info"))
        about_menu.addAction(self.window.menu['info.about'])
        about_menu.addAction(self.window.menu['info.change_log'])
        about_menu.addAction(self.window.menu['info.website'])
