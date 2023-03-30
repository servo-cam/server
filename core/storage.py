#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.30 17:00
# =============================================================================

import configparser
import os
from pathlib import Path
import shutil


class Storage:
    TYPE_STR = 0
    TYPE_INT = 1
    TYPE_FLOAT = 2
    TYPE_BOOL = 3

    def __init__(self, tracker=None):
        """
        Config storage handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.config = None
        self.installed = False
        self.user_path = str(Path(os.path.join(Path.home(), '.config', 'servocam_org')))

    def install(self):
        """Install user config files"""
        if self.installed:
            return

        try:
            # create user config dir
            path = Path(self.user_path)
            path.mkdir(parents=True, exist_ok=True)

            # install config file
            dst = self.get_user_config_path()
            if not os.path.exists(dst):
                src = self.get_default_config_path()
                # copy defaults to user file
                shutil.copyfile(src, dst)

            # install hosts file
            dst = self.get_user_hosts_path()
            if not os.path.exists(dst):
                src = self.get_default_hosts_path()
                # copy defaults to user file
                shutil.copyfile(src, dst)

            # install streams file
            dst = self.get_user_streams_path()
            if not os.path.exists(dst):
                src = self.get_default_streams_path()
                # copy defaults to user file
                shutil.copyfile(src, dst)
        except:
            self.tracker.debug.log('[ERROR] Unable to install user config files in {}'.format(self.user_path))
            self.tracker.debug.log('[ERROR] Error installing user config files. Permissions problem?')

        self.installed = True

    def init(self):
        """Initialize config"""
        if self.tracker is None:
            return

        # install user config files
        self.install()

        # core
        self.tracker.model_name = self.get_cfg('app.model')
        self.tracker.source = self.get_cfg('app.source')
        self.tracker.video_url = self.get_cfg('app.video_url')
        self.tracker.remote_host = self.get_cfg('app.remote_host')

        if self.tracker.remote_host is not None:
            self.tracker.remote_ip = self.tracker.remote.host2ip(self.tracker.remote_host)

        self.tracker.stream_url = self.get_cfg('app.stream_url')
        self.tracker.ai_enabled = self.get_cfg('app.ai', self.TYPE_BOOL)
        self.tracker.is_debug = self.get_cfg('app.debug', self.TYPE_BOOL)
        self.tracker.disabled = self.get_cfg('app.disabled', self.TYPE_BOOL)

        # target
        self.tracker.target_mode = self.get_cfg('target.mode')
        self.tracker.target_point = self.get_cfg('target.point')
        self.tracker.targets.locked = self.get_cfg('target.locked', self.TYPE_BOOL)
        self.tracker.targets.single = self.get_cfg('target.single', self.TYPE_BOOL)

        self.tracker.target.AS_TARGET_MIN_TIME = self.get_cfg('target.time.as_target', self.TYPE_INT)
        self.tracker.target.AS_LOST_MIN_TIME = self.get_cfg('target.time.as_lost', self.TYPE_INT)
        self.tracker.target.BEFORE_TARGET_MIN_TIME = self.get_cfg('target.time.before_target', self.TYPE_FLOAT)
        self.tracker.target.ON_TARGET_MAX_VALUE = self.get_cfg('target.limit.on_target', self.TYPE_INT)

        # action
        self.tracker.action.enabled = self.get_cfg('target.action.enable', self.TYPE_BOOL)
        self.tracker.action.switch_value = self.get_cfg('target.action.switch', self.TYPE_INT)
        self.tracker.action.length_value = self.get_cfg('target.action.length', self.TYPE_INT)
        self.tracker.action.auto_mode = self.get_cfg('target.action.mode')
        self.tracker.action.auto_name = self.get_cfg('target.action.name')
        self.tracker.action.manual_mode = self.get_cfg('manual.action.mode')

        # fix min / max
        if self.tracker.action.switch_value < 0:
            self.tracker.action.switch_value = 0
        if self.tracker.action.switch_value > 99:
            self.tracker.action.switch_value = 99
        if self.tracker.action.length_value < 0:
            self.tracker.action.length_value = 0
        if self.tracker.action.length_value > 99:
            self.tracker.action.length_value = 99

        # manual control
        self.tracker.manual.speed = self.get_cfg('manual.speed', self.TYPE_INT)

        # fix min / max
        if self.tracker.manual.speed < 1:
            self.tracker.manual.speed = 1
        if self.tracker.manual.speed > 99:
            self.tracker.manual.speed = 99
        if self.tracker.render.zoom < 0:
            self.tracker.render.zoom = 0
        if self.tracker.render.zoom > 99:
            self.tracker.render.zoom = 99

        # view / render
        self.tracker.render.full_screen = self.get_cfg('render.full_screen', self.TYPE_BOOL)
        self.tracker.render.fit = self.get_cfg('render.fit', self.TYPE_BOOL)
        self.tracker.render.minimized = self.get_cfg('render.minimized', self.TYPE_BOOL)
        self.tracker.render.maximized = self.get_cfg('render.maximized', self.TYPE_BOOL)
        self.tracker.render.zoom = self.get_cfg('render.zoom', self.TYPE_INT)
        self.tracker.render.tracking = self.get_cfg('render.tracking', self.TYPE_BOOL)
        self.tracker.render.targeting = self.get_cfg('render.targeting', self.TYPE_BOOL)
        self.tracker.render.labels = self.get_cfg('render.labels', self.TYPE_BOOL)
        self.tracker.render.text = self.get_cfg('render.text', self.TYPE_BOOL)
        self.tracker.render.bounds = self.get_cfg('render.bounds', self.TYPE_BOOL)
        self.tracker.render.console = self.get_cfg('render.console', self.TYPE_BOOL)
        self.tracker.render.montage_columns = self.get_cfg('render.montage.cols', self.TYPE_INT)
        self.tracker.render.montage_rows = self.get_cfg('render.montage.rows', self.TYPE_INT)
        self.tracker.render.montage_width = self.get_cfg('render.montage.width', self.TYPE_INT)
        self.tracker.render.simulator = self.get_cfg('servo.simulator', self.TYPE_BOOL)

        # render / overlay
        self.tracker.overlay.status_font_size = self.get_cfg('render.overlay.status.font.size', self.TYPE_FLOAT)
        self.tracker.overlay.status_font_thickness = self.get_cfg('render.overlay.status.font.thickness', self.TYPE_INT)

        # video
        self.tracker.video.loop = self.get_cfg('video.loop', self.TYPE_BOOL)

        # stream
        self.tracker.stream.loop = self.get_cfg('stream.loop', self.TYPE_BOOL)

        # camera source
        tmp_idx = self.get_cfg('camera.idx')
        if str(tmp_idx) == '' or tmp_idx is None:
            self.tracker.camera.idx = 0
        else:
            # if raspberry pi camera TODO: rpi support
            if tmp_idx.startswith('csi'):
                self.tracker.camera.idx = 0
                self.tracker.camera.csi = True
            # if serial connected pi camera (Raspberry -> USB -> here) TODO: serial support
            elif tmp_idx.startswith('serial'):
                self.tracker.camera.idx = 0
                self.tracker.camera.serial = True
            else:
                self.tracker.camera.idx = int(tmp_idx)

        # fov, resolution, fps, etc.
        self.tracker.camera.fov = [
            self.tracker.storage.get_cfg('camera.fov.x', self.tracker.storage.TYPE_INT),
            self.tracker.storage.get_cfg('camera.fov.y', self.tracker.storage.TYPE_INT)]
        self.tracker.camera.width = self.get_cfg('camera.width', self.TYPE_INT)
        self.tracker.camera.height = self.get_cfg('camera.height', self.TYPE_INT)
        self.tracker.camera.fps = self.get_cfg('camera.fps', self.TYPE_INT)

        # remote / clients
        self.tracker.remote.CLIENT_CONN_WAIT = self.get_cfg('clients.conn_wait', self.TYPE_INT)
        self.tracker.remote.CLIENT_HANG_TIME = self.get_cfg('clients.hang_time', self.TYPE_INT)
        self.tracker.remote.CLIENT_INACTIVE_TIME = self.get_cfg('clients.inactive_time', self.TYPE_INT)
        self.tracker.remote.STREAM_JPEG = self.get_cfg('clients.stream.jpeg', self.TYPE_BOOL)

        # encryption
        self.tracker.encrypt.enabled_video = self.tracker.storage.get_cfg('security.aes.video', self.TYPE_BOOL)
        self.tracker.encrypt.enabled_data = self.tracker.storage.get_cfg('security.aes.data', self.TYPE_BOOL)
        self.tracker.encrypt.raw_key = self.tracker.storage.get_cfg('security.aes.key')

        # REQUIRED: auto-enable JPEG compression if encryption is enabled
        if self.tracker.encrypt.enabled_video:
            self.tracker.remote.STREAM_JPEG = True

        # serial
        self.tracker.serial.data_format = self.tracker.storage.get_cfg('serial.data.format')
        self.tracker.serial.BAUD_RATE = self.tracker.storage.get_cfg('serial.baud_rate', self.tracker.storage.TYPE_INT)

        if self.tracker.servo.local is not None:
            print("SERVO: local serial port: " + self.tracker.servo.local)
            self.tracker.serial.port = self.tracker.servo.local

        # servo
        self.tracker.servo.enable = self.get_cfg('servo.enabled', self.TYPE_BOOL)
        self.tracker.servo.x = self.get_cfg('servo.enabled.x', self.TYPE_BOOL)
        self.tracker.servo.y = self.get_cfg('servo.enabled.y', self.TYPE_BOOL)
        self.tracker.servo.map_fov = self.get_cfg('servo.map_fov', self.TYPE_BOOL)
        self.tracker.servo.use_limit = self.get_cfg('servo.use_limit', self.TYPE_BOOL)
        self.tracker.servo.local = self.get_cfg('servo.local')
        self.tracker.servo.remote = self.get_cfg('servo.remote')

        self.tracker.servo.ANGLE_START_X = self.tracker.storage.get_cfg('servo.angle.start.x',
                                                                        self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_START_Y = self.tracker.storage.get_cfg('servo.angle.start.y',
                                                                        self.tracker.storage.TYPE_INT)

        self.tracker.servo.ANGLE_MIN_X = self.tracker.storage.get_cfg('servo.angle.min.x',
                                                                      self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_MAX_X = self.tracker.storage.get_cfg('servo.angle.max.x',
                                                                      self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_MIN_Y = self.tracker.storage.get_cfg('servo.angle.min.y',
                                                                      self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_MAX_Y = self.tracker.storage.get_cfg('servo.angle.max.y',
                                                                      self.tracker.storage.TYPE_INT)

        self.tracker.servo.ANGLE_STEP_X = self.tracker.storage.get_cfg('servo.angle.step.x',
                                                                       self.tracker.storage.TYPE_FLOAT)
        self.tracker.servo.ANGLE_STEP_Y = self.tracker.storage.get_cfg('servo.angle.step.y',
                                                                       self.tracker.storage.TYPE_FLOAT)

        self.tracker.servo.ANGLE_MULTIPLIER_X = self.tracker.storage.get_cfg('servo.angle.multiplier.x',
                                                                             self.tracker.storage.TYPE_FLOAT)
        self.tracker.servo.ANGLE_MULTIPLIER_Y = self.tracker.storage.get_cfg('servo.angle.multiplier.y',
                                                                             self.tracker.storage.TYPE_FLOAT)

        self.tracker.servo.ANGLE_LIMIT_MIN_X = self.tracker.storage.get_cfg('servo.limit.min.x',
                                                                            self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_LIMIT_MAX_X = self.tracker.storage.get_cfg('servo.limit.max.x',
                                                                            self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_LIMIT_MIN_Y = self.tracker.storage.get_cfg('servo.limit.min.y',
                                                                            self.tracker.storage.TYPE_INT)
        self.tracker.servo.ANGLE_LIMIT_MAX_Y = self.tracker.storage.get_cfg('servo.limit.max.y',
                                                                            self.tracker.storage.TYPE_INT)

        # sockets
        self.tracker.sockets.PORT_DATA = self.tracker.storage.get_cfg('server.port.data',
                                                                      self.tracker.storage.TYPE_INT)
        self.tracker.sockets.PORT_CONN = self.tracker.storage.get_cfg('server.port.conn',
                                                                      self.tracker.storage.TYPE_INT)
        self.tracker.sockets.PORT_STATUS = self.tracker.storage.get_cfg('server.port.status',
                                                                        self.tracker.storage.TYPE_INT)

        # targeting
        self.tracker.targeting.DELAY_MULTIPLIER = self.tracker.storage.get_cfg('target.delay',
                                                                               self.tracker.storage.TYPE_FLOAT)
        self.tracker.targeting.SPEED_MULTIPLIER = self.tracker.storage.get_cfg('target.speed',
                                                                               self.tracker.storage.TYPE_FLOAT)
        self.tracker.targeting.SMOOTH_MULTIPLIER = self.tracker.storage.get_cfg('target.smooth',
                                                                                self.tracker.storage.TYPE_FLOAT)

        self.tracker.targeting.threshold = [
            self.tracker.storage.get_cfg('target.threshold.x', self.tracker.storage.TYPE_FLOAT),
            self.tracker.storage.get_cfg('target.threshold.y', self.tracker.storage.TYPE_FLOAT)]

        self.tracker.targeting.SMOOTH_FOLLOW = self.tracker.storage.get_cfg('target.smooth.follow',
                                                                            self.tracker.storage.TYPE_BOOL)
        self.tracker.targeting.SMOOTH_CAMERA = self.tracker.storage.get_cfg('target.smooth.camera',
                                                                            self.tracker.storage.TYPE_BOOL)
        self.tracker.targeting.BRAKE = self.tracker.storage.get_cfg('target.brake',
                                                                    self.tracker.storage.TYPE_BOOL)

        self.tracker.targeting.MEAN_TARGET = self.tracker.storage.get_cfg('target.mean.target',
                                                                          self.tracker.storage.TYPE_BOOL)
        self.tracker.targeting.MEAN_NOW = self.tracker.storage.get_cfg('target.mean.now',
                                                                       self.tracker.storage.TYPE_BOOL)
        self.tracker.targeting.MEAN_CAM = self.tracker.storage.get_cfg('target.mean.cam',
                                                                       self.tracker.storage.TYPE_BOOL)

        self.tracker.targeting.MEAN_STEP_TARGET = self.tracker.storage.get_cfg('target.mean.target.step',
                                                                               self.tracker.storage.TYPE_FLOAT)
        self.tracker.targeting.MEAN_STEP_NOW = self.tracker.storage.get_cfg('target.mean.now.step',
                                                                            self.tracker.storage.TYPE_FLOAT)
        self.tracker.targeting.MEAN_STEP_CAM = self.tracker.storage.get_cfg('target.mean.cam.step',
                                                                            self.tracker.storage.TYPE_FLOAT)

        self.tracker.targeting.MEAN_DEPTH_TARGET = self.tracker.storage.get_cfg('target.mean.target.depth',
                                                                                self.tracker.storage.TYPE_FLOAT)
        self.tracker.targeting.MEAN_DEPTH_NOW = self.tracker.storage.get_cfg('target.mean.now.depth',
                                                                             self.tracker.storage.TYPE_FLOAT)
        self.tracker.targeting.MEAN_DEPTH_CAM = self.tracker.storage.get_cfg('target.mean.cam.depth',
                                                                             self.tracker.storage.TYPE_FLOAT)

        # patrol
        self.tracker.patrol.STEP = self.get_cfg('patrol.step', self.TYPE_FLOAT)
        self.tracker.patrol.TIMEOUT = self.get_cfg('patrol.timeout', self.TYPE_FLOAT)
        self.tracker.patrol.INTERVAL_TIME = self.get_cfg('patrol.interval', self.TYPE_INT)
        self.tracker.patrol.direction = self.get_cfg('patrol.direction')

        # area: target
        self.tracker.area.enabled[self.tracker.area.TYPE_TARGET] = self.get_cfg('area.target', self.TYPE_BOOL)
        self.tracker.area.world[self.tracker.area.TYPE_TARGET] = self.get_cfg('area.target.world', self.TYPE_BOOL)
        self.tracker.area.areas[self.tracker.area.TYPE_TARGET][0] = self.get_cfg('area.target.x', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_TARGET][1] = self.get_cfg('area.target.y', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_TARGET][2] = self.get_cfg('area.target.w', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_TARGET][3] = self.get_cfg('area.target.h', self.TYPE_FLOAT)

        # area: patrol
        self.tracker.area.enabled[self.tracker.area.TYPE_PATROL] = self.get_cfg('area.patrol', self.TYPE_BOOL)
        self.tracker.area.world[self.tracker.area.TYPE_PATROL] = self.get_cfg('area.patrol.world', self.TYPE_BOOL)
        self.tracker.area.areas[self.tracker.area.TYPE_PATROL][0] = self.get_cfg('area.patrol.x', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_PATROL][1] = self.get_cfg('area.patrol.y', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_PATROL][2] = self.get_cfg('area.patrol.w', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_PATROL][3] = self.get_cfg('area.patrol.h', self.TYPE_FLOAT)

        # area: action
        self.tracker.area.enabled[self.tracker.area.TYPE_ACTION] = self.get_cfg('area.action', self.TYPE_BOOL)
        self.tracker.area.world[self.tracker.area.TYPE_ACTION] = self.get_cfg('area.action.world', self.TYPE_BOOL)
        self.tracker.area.areas[self.tracker.area.TYPE_ACTION][0] = self.get_cfg('area.action.x', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_ACTION][1] = self.get_cfg('area.action.y', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_ACTION][2] = self.get_cfg('area.action.w', self.TYPE_FLOAT)
        self.tracker.area.areas[self.tracker.area.TYPE_ACTION][3] = self.get_cfg('area.action.h', self.TYPE_FLOAT)

        # filters: classes
        self.tracker.filter.set_classes(self.tracker.filter.FILTER_DETECT, self.get_cfg('filter.detect.classes'))
        self.tracker.filter.set_classes(self.tracker.filter.FILTER_TARGET, self.get_cfg('filter.target.classes'))
        self.tracker.filter.set_classes(self.tracker.filter.FILTER_ACTION, self.get_cfg('filter.action.classes'))

        # filters: min score
        self.tracker.filter.set_min_score(self.tracker.filter.FILTER_DETECT, self.get_cfg('filter.detect.min_score'))
        self.tracker.filter.set_min_score(self.tracker.filter.FILTER_TARGET, self.get_cfg('filter.target.min_score'))
        self.tracker.filter.set_min_score(self.tracker.filter.FILTER_ACTION, self.get_cfg('filter.action.min_score'))

        # video filters
        self.tracker.video_filter.set_input_filters(self.get_cfg('video_filter.input'))
        self.tracker.video_filter.set_output_filters(self.get_cfg('video_filter.input'))

    def get_default_config_path(self):
        """
        Get default config path

        :return: path to default config
        """
        return os.path.join('.', 'config.ini')

    def get_user_config_path(self):
        """
        Get user config path

        :return: path to user config
        """
        return os.path.join(self.user_path, 'config.ini')

    def get_default_hosts_path(self):
        """
        Get default hosts path

        :return: path to default hosts
        """
        return os.path.join('.', 'hosts.txt')

    def get_user_hosts_path(self):
        """
        Get user hosts path

        :return: path to user hosts
        """
        return os.path.join(self.user_path, 'hosts.txt')

    def get_default_streams_path(self):
        """
        Get default streams path

        :return: path to default streams
        """
        return os.path.join('.', 'streams.txt')

    def get_user_streams_path(self):
        """
        Get user streams path

        :return: path to user streams
        """
        return os.path.join(self.user_path, 'streams.txt')

    def parse_cfg(self, cfg):
        """
        Parse config

        :param cfg: config
        """
        # app
        cfg['CONFIG']['app.source'] = str(self.tracker.source)
        cfg['CONFIG']['app.model'] = str(self.tracker.model_name)
        cfg['CONFIG']['app.video_url'] = str(self.tracker.video_url)
        cfg['CONFIG']['app.stream_url'] = str(self.tracker.stream_url)
        cfg['CONFIG']['app.remote_host'] = str(self.tracker.remote_host)
        cfg['CONFIG']['app.disabled'] = str(int(self.tracker.disabled))
        cfg['CONFIG']['app.ai'] = str(int(self.tracker.ai_enabled))

        # camera
        cfg['CONFIG']['camera.idx'] = str(self.tracker.camera.idx)
        cfg['CONFIG']['camera.fov.x'] = str(int(self.tracker.camera.fov[0]))
        cfg['CONFIG']['camera.fov.y'] = str(int(self.tracker.camera.fov[1]))

        # targeting
        cfg['CONFIG']['target.mode'] = str(self.tracker.target_mode)
        cfg['CONFIG']['target.point'] = str(self.tracker.target_point)
        cfg['CONFIG']['target.locked'] = str(int(self.tracker.targets.locked))
        cfg['CONFIG']['target.single'] = str(int(self.tracker.targets.single))

        cfg['CONFIG']['target.delay'] = str(self.tracker.targeting.DELAY_MULTIPLIER)
        cfg['CONFIG']['target.speed'] = str(self.tracker.targeting.SPEED_MULTIPLIER)
        cfg['CONFIG']['target.smooth'] = str(self.tracker.targeting.SMOOTH_MULTIPLIER)

        cfg['CONFIG']['target.smooth.follow'] = str(int(self.tracker.targeting.SMOOTH_FOLLOW))
        cfg['CONFIG']['target.smooth.camera'] = str(int(self.tracker.targeting.SMOOTH_CAMERA))
        cfg['CONFIG']['target.brake'] = str(int(self.tracker.targeting.BRAKE))

        cfg['CONFIG']['target.mean.target'] = str(int(self.tracker.targeting.MEAN_TARGET))
        cfg['CONFIG']['target.mean.now'] = str(int(self.tracker.targeting.MEAN_NOW))
        cfg['CONFIG']['target.mean.cam'] = str(int(self.tracker.targeting.MEAN_CAM))
        cfg['CONFIG']['mean.target.depth'] = str(self.tracker.targeting.MEAN_DEPTH_TARGET)
        cfg['CONFIG']['mean.now.depth'] = str(self.tracker.targeting.MEAN_DEPTH_NOW)
        cfg['CONFIG']['mean.cam.depth'] = str(self.tracker.targeting.MEAN_DEPTH_CAM)

        # action
        cfg['CONFIG']['target.action.enable'] = str(int(self.tracker.action.enabled))
        cfg['CONFIG']['target.action.switch'] = str(self.tracker.action.switch_value)
        cfg['CONFIG']['target.action.length'] = str(self.tracker.action.length_value)
        cfg['CONFIG']['target.action.mode'] = str(self.tracker.action.auto_mode)
        cfg['CONFIG']['target.action.name'] = str(self.tracker.action.auto_name)
        cfg['CONFIG']['manual.action.mode'] = str(self.tracker.action.manual_mode)
        cfg['CONFIG']['manual.speed'] = str(self.tracker.manual.speed)

        # render
        cfg['CONFIG']['render.full_screen'] = str(int(self.tracker.render.full_screen))
        cfg['CONFIG']['render.fit'] = str(int(self.tracker.render.fit))
        cfg['CONFIG']['render.zoom'] = str(int(self.tracker.render.zoom))
        cfg['CONFIG']['render.tracking'] = str(int(self.tracker.render.tracking))
        cfg['CONFIG']['render.targeting'] = str(int(self.tracker.render.targeting))
        cfg['CONFIG']['render.labels'] = str(int(self.tracker.render.labels))
        cfg['CONFIG']['render.text'] = str(int(self.tracker.render.text))
        cfg['CONFIG']['render.bounds'] = str(int(self.tracker.render.bounds))
        cfg['CONFIG']['render.console'] = str(int(self.tracker.render.console))
        cfg['CONFIG']['servo.simulator'] = str(int(self.tracker.render.simulator))

        # patrol
        cfg['CONFIG']['patrol.step'] = str(self.tracker.patrol.STEP)
        cfg['CONFIG']['patrol.timeout'] = str(self.tracker.patrol.TIMEOUT)

        # area: target
        cfg['CONFIG']['area.target'] = str(int(self.tracker.area.enabled[self.tracker.area.TYPE_TARGET]))
        cfg['CONFIG']['area.target.world'] = str(int(self.tracker.area.world[self.tracker.area.TYPE_TARGET]))
        cfg['CONFIG']['area.target.x'] = str(self.tracker.area.areas[self.tracker.area.TYPE_TARGET][0])
        cfg['CONFIG']['area.target.y'] = str(self.tracker.area.areas[self.tracker.area.TYPE_TARGET][1])
        cfg['CONFIG']['area.target.w'] = str(self.tracker.area.areas[self.tracker.area.TYPE_TARGET][2])
        cfg['CONFIG']['area.target.h'] = str(self.tracker.area.areas[self.tracker.area.TYPE_TARGET][3])

        # area: patrol
        cfg['CONFIG']['area.patrol'] = str(int(self.tracker.area.enabled[self.tracker.area.TYPE_PATROL]))
        cfg['CONFIG']['area.patrol.world'] = str(int(self.tracker.area.world[self.tracker.area.TYPE_PATROL]))
        cfg['CONFIG']['area.patrol.x'] = str(self.tracker.area.areas[self.tracker.area.TYPE_PATROL][0])
        cfg['CONFIG']['area.patrol.y'] = str(self.tracker.area.areas[self.tracker.area.TYPE_PATROL][1])
        cfg['CONFIG']['area.patrol.w'] = str(self.tracker.area.areas[self.tracker.area.TYPE_PATROL][2])
        cfg['CONFIG']['area.patrol.h'] = str(self.tracker.area.areas[self.tracker.area.TYPE_PATROL][3])

        # area: action
        cfg['CONFIG']['area.action'] = str(int(self.tracker.area.enabled[self.tracker.area.TYPE_ACTION]))
        cfg['CONFIG']['area.action.world'] = str(int(self.tracker.area.world[self.tracker.area.TYPE_ACTION]))
        cfg['CONFIG']['area.action.x'] = str(self.tracker.area.areas[self.tracker.area.TYPE_ACTION][0])
        cfg['CONFIG']['area.action.y'] = str(self.tracker.area.areas[self.tracker.area.TYPE_ACTION][1])
        cfg['CONFIG']['area.action.w'] = str(self.tracker.area.areas[self.tracker.area.TYPE_ACTION][2])
        cfg['CONFIG']['area.action.h'] = str(self.tracker.area.areas[self.tracker.area.TYPE_ACTION][3])

        # filters
        cfg['CONFIG']['filter.detect.classes'] = str(self.tracker.filter.get_classes(self.tracker.filter.FILTER_DETECT))
        cfg['CONFIG']['filter.target.classes'] = str(self.tracker.filter.get_classes(self.tracker.filter.FILTER_TARGET))
        cfg['CONFIG']['filter.action.classes'] = str(self.tracker.filter.get_classes(self.tracker.filter.FILTER_ACTION))
        cfg['CONFIG']['filter.detect.min_score'] = str(
            self.tracker.filter.get_min_score(self.tracker.filter.FILTER_DETECT))
        cfg['CONFIG']['filter.target.min_score'] = str(
            self.tracker.filter.get_min_score(self.tracker.filter.FILTER_TARGET))
        cfg['CONFIG']['filter.action.min_score'] = str(
            self.tracker.filter.get_min_score(self.tracker.filter.FILTER_ACTION))

        # servo
        cfg['CONFIG']['servo.enabled'] = str(int(self.tracker.servo.enable))
        cfg['CONFIG']['servo.enabled.x'] = str(int(self.tracker.servo.x))
        cfg['CONFIG']['servo.enabled.y'] = str(int(self.tracker.servo.y))
        cfg['CONFIG']['servo.local'] = str(self.tracker.servo.local)
        cfg['CONFIG']['servo.remote'] = str(self.tracker.servo.remote)

        cfg['CONFIG']['servo.angle.min.x'] = str(self.tracker.servo.ANGLE_MIN_X)
        cfg['CONFIG']['servo.angle.min.y'] = str(self.tracker.servo.ANGLE_MIN_Y)
        cfg['CONFIG']['servo.angle.max.x'] = str(self.tracker.servo.ANGLE_MAX_X)
        cfg['CONFIG']['servo.angle.max.y'] = str(self.tracker.servo.ANGLE_MAX_Y)
        cfg['CONFIG']['servo.limit.min.x'] = str(self.tracker.servo.ANGLE_LIMIT_MIN_X)
        cfg['CONFIG']['servo.limit.min.y'] = str(self.tracker.servo.ANGLE_LIMIT_MIN_Y)
        cfg['CONFIG']['servo.limit.max.x'] = str(self.tracker.servo.ANGLE_LIMIT_MAX_X)
        cfg['CONFIG']['servo.limit.max.y'] = str(self.tracker.servo.ANGLE_LIMIT_MAX_Y)

        cfg['CONFIG']['servo.angle.step.x'] = str(self.tracker.servo.ANGLE_STEP_X)
        cfg['CONFIG']['servo.angle.step.y'] = str(self.tracker.servo.ANGLE_STEP_Y)
        cfg['CONFIG']['servo.angle.multiplier.x'] = str(self.tracker.servo.ANGLE_MULTIPLIER_X)
        cfg['CONFIG']['servo.angle.multiplier.y'] = str(self.tracker.servo.ANGLE_MULTIPLIER_Y)

    def get_cfg(self, key, astype=0):
        """
        Get config value by key

        :param key: key
        :param astype: type of value
        :return: value
        """
        if self.config is None:
            self.config = configparser.ConfigParser()

            # try to load stored user config first from user home directory
            f = self.get_user_config_path()
            if not os.path.exists(f):
                # try to load default config from app directory
                f = self.get_default_config_path()
                if not os.path.exists(f):
                    err_msg = "FATAL ERROR: config.ini not found!"
                    if self.tracker is not None:
                        self.tracker.debug.log(err_msg)
                    else:
                        print(err_msg)
                    return None

            self.config.read(f)
            if self.tracker is not None:
                self.tracker.debug.log("[CONFIG] Loaded config file: {}".format(f))

        if self.config.has_option("CONFIG", key):
            if astype == self.TYPE_STR:
                if str(self.config['CONFIG'][key]) == '' \
                        or self.config['CONFIG'][key] is None \
                        or str(self.config['CONFIG'][key]).lower() == 'none':
                    return None
                else:
                    return str(self.config['CONFIG'][key])
            elif astype == self.TYPE_BOOL:
                if str(self.config['CONFIG'][key]) == '' or self.config['CONFIG'][key] is None:
                    return False
                else:
                    return self.str2bool(self.config['CONFIG'][key])
            elif astype == self.TYPE_INT:
                if str(self.config['CONFIG'][key]) == '' or self.config['CONFIG'][key] is None:
                    return 0
                else:
                    return int(self.config['CONFIG'][key])
            elif astype == self.TYPE_FLOAT:
                if str(self.config['CONFIG'][key]) == '' or self.config['CONFIG'][key] is None:
                    return 0.0
                else:
                    return float(self.config['CONFIG'][key])
            else:
                return self.config['CONFIG'][key]
        else:
            if astype == self.TYPE_STR:
                return None
            elif astype == self.TYPE_BOOL:
                return False
            elif astype == self.TYPE_INT:
                return 0
            elif astype == self.TYPE_FLOAT:
                return 0.0

    def str2bool(self, val):
        """
        Convert string to bool

        :param val: string
        :return: bool
        """
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return True
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return False
        else:
            raise ValueError("Invalid bool value %r" % (val,))
