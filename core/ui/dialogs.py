#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.30 17:00
# =============================================================================

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QGridLayout, QLabel, QHBoxLayout, QVBoxLayout, QTreeView, QPushButton, QPlainTextEdit)
from core.ui.widgets import (DebugDialog, InfoDialog, ConfiguratorDialog, AlertDialog, UpdateDialog, SettingsSlider,
                             SettingsCheckbox, SettingsInput)
from core.utils import trans
from core.ui.style import Style


class UIDialogs:
    def __init__(self, window=None):
        """
        Dialogs UI setup

        :param window: main UI window object
        """
        self.window = window

    def setup(self):
        """Setup dialogs"""
        self.window.dialog = {}
        self.window.debug = {}
        self.window.editor = {}
        self.window.settings = {}

        for id in self.window.tracker.debug.ids:
            self.setup_debug(id)

        self.setup_network()
        self.setup_info_about()
        self.setup_info_change_log()

        self.window.path_label = {}
        self.window.path_label['config'] = QLabel('')
        self.window.path_label['hosts'] = QLabel('')
        self.window.path_label['streams'] = QLabel('')
        self.setup_configurator_config()
        self.setup_configurator_hosts()
        self.setup_configurator_streams()
        self.setup_configurator_servo()

        # alert
        self.window.alert_dialog = AlertDialog(self.window)
        self.window.update_dialog = UpdateDialog(self.window)

    def setup_debug(self, id):
        """
        Setup debug dialog

        :param id: debug id
        """
        self.window.debug[id] = QTreeView()
        self.window.debug[id].setRootIsDecorated(False)
        self.window.debug[id].setAlternatingRowColors(True)

        layout = QGridLayout()
        layout.addWidget(self.window.debug[id], 1, 0)

        self.window.dialog['debug.' + id] = DebugDialog(self.window, id)
        self.window.dialog['debug.' + id].setLayout(layout)
        self.window.dialog['debug.' + id].setWindowTitle(trans('dialog.debug.prefix') + ": " + id)

    def setup_network(self):
        """Setup network dialog"""
        id = 'network'
        self.window.debug[id] = QTreeView()
        self.window.debug[id].setRootIsDecorated(False)
        self.window.debug[id].setAlternatingRowColors(True)

        btns = {}
        btns['restart'] = QPushButton(trans("debug.network.restart"))
        btns['disconnect'] = QPushButton(trans("debug.network.disconnect"))
        btns['destroy'] = QPushButton(trans("debug.network.destroy"))

        btns['restart'].clicked.connect(
            lambda: self.window.tracker.remote.restart(self.window.tracker.remote_ip))
        btns['disconnect'].clicked.connect(
            lambda: self.window.tracker.remote.disconnect(self.window.tracker.remote_ip))
        btns['destroy'].clicked.connect(
            lambda: self.window.tracker.remote.remote_destroy(self.window.tracker.remote_ip))

        actions = QHBoxLayout()
        actions.addWidget(btns['restart'])
        actions.addWidget(btns['disconnect'])
        actions.addWidget(btns['destroy'])

        layout = QVBoxLayout()
        layout.addWidget(QLabel(
            trans("debug.network.client.label") + ": " + str(self.window.tracker.remote_host) + " <" + str(
                self.window.tracker.remote_ip) + ">"))
        layout.addLayout(actions)
        layout.addWidget(QLabel(trans("debug.network.clients.label")))
        layout.addWidget(self.window.debug[id])

        self.window.dialog['debug.' + id] = DebugDialog(self.window, id)
        self.window.dialog['debug.' + id].setLayout(layout)
        self.window.dialog['debug.' + id].setWindowTitle(trans('dialog.debug.prefix') + ": " + id)

    def setup_info_about(self):
        """Setup about dialog"""
        id = 'about'

        str = "SERVO CAM\n" \
              "-------------\n" \
              "version: {}\n" \
              "build: {}\n" \
              "email: {}\n" \
              "{}\n\n" \
              "(c) 2023 {}".format(self.window.tracker.version,
                                   self.window.tracker.build,
                                   self.window.tracker.email,
                                   self.window.tracker.www,
                                   self.window.tracker.author)

        pixmap = QtGui.QPixmap('./assets/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(QLabel(str))

        self.window.dialog['info.' + id] = InfoDialog(self.window, id)
        self.window.dialog['info.' + id].setLayout(layout)
        self.window.dialog['info.' + id].setWindowTitle(trans('dialog.info.about'))

    def setup_info_change_log(self):
        """Setup change log dialog"""
        id = 'change_log'

        txt = ''
        try:
            with open("CHANGELOG.txt", "r") as f:
                txt = f.read()
                f.close()
        except:
            self.window.tracker.debug.log('[ERROR] Error reading file: CHANGELOG.txt')

        textarea = QPlainTextEdit()
        textarea.setReadOnly(True)
        textarea.setPlainText(txt)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(trans('dialog.info.change_log.label')))
        layout.addWidget(textarea)

        self.window.dialog['info.' + id] = InfoDialog(self.window, id)
        self.window.dialog['info.' + id].setLayout(layout)
        self.window.dialog['info.' + id].setWindowTitle(trans('dialog.info.change_log'))

    def setup_configurator_config(self):
        """Setup config dialog"""
        id = 'config'

        self.window.editor['config'] = QPlainTextEdit()
        self.window.editor['config'].setReadOnly(False)

        # load data
        self.window.tracker.configurator.load(id)
        path = self.window.tracker.configurator.get_path(id)

        btns = {}
        btns['defaults'] = QPushButton(trans("dialog.config.btn.defaults"))
        btns['save'] = QPushButton(trans("dialog.config.btn.save"))
        btns['defaults'].clicked.connect(
            lambda: self.window.tracker.configurator.load_defaults('config'))
        btns['save'].clicked.connect(
            lambda: self.window.tracker.configurator.save('config'))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(btns['defaults'])
        bottom_layout.addWidget(btns['save'])

        self.window.path_label[id] = QLabel(str(path))
        self.window.path_label[id].setStyleSheet("font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(trans('dialog.config.config.label')))
        layout.addWidget(self.window.path_label[id])
        layout.addWidget(self.window.editor['config'])
        layout.addLayout(bottom_layout)

        self.window.dialog['config.' + id] = ConfiguratorDialog(self.window, id)
        self.window.dialog['config.' + id].setLayout(layout)
        self.window.dialog['config.' + id].setWindowTitle(trans('dialog.config.config'))

    def setup_configurator_hosts(self):
        """Setup hosts dialog"""
        id = 'hosts'

        self.window.editor['hosts'] = QPlainTextEdit()
        self.window.editor['hosts'].setReadOnly(False)

        # load data
        self.window.tracker.configurator.load(id)
        path = self.window.tracker.configurator.get_path(id)

        btns = {}
        btns['defaults'] = QPushButton(trans("dialog.config.btn.defaults"))
        btns['save'] = QPushButton(trans("dialog.config.btn.save"))
        btns['defaults'].clicked.connect(
            lambda: self.window.tracker.configurator.load_defaults('hosts'))
        btns['save'].clicked.connect(
            lambda: self.window.tracker.configurator.save('hosts'))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(btns['defaults'])
        bottom_layout.addWidget(btns['save'])

        self.window.path_label[id] = QLabel(str(path))
        self.window.path_label[id].setStyleSheet("font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(trans('dialog.config.hosts.label')))
        layout.addWidget(self.window.path_label[id])
        layout.addWidget(self.window.editor['hosts'])
        layout.addLayout(bottom_layout)

        self.window.dialog['config.' + id] = ConfiguratorDialog(self.window, id)
        self.window.dialog['config.' + id].setLayout(layout)
        self.window.dialog['config.' + id].setWindowTitle(trans('dialog.config.hosts'))

    def setup_configurator_streams(self):
        """Setup streams dialog"""
        id = 'streams'

        self.window.editor['streams'] = QPlainTextEdit()
        self.window.editor['streams'].setReadOnly(False)

        # load data
        self.window.tracker.configurator.load(id)
        path = self.window.tracker.configurator.get_path(id)

        btns = {}
        btns['defaults'] = QPushButton(trans("dialog.config.btn.defaults"))
        btns['save'] = QPushButton(trans("dialog.config.btn.save"))
        btns['defaults'].clicked.connect(
            lambda: self.window.tracker.configurator.load_defaults('streams'))
        btns['save'].clicked.connect(
            lambda: self.window.tracker.configurator.save('streams'))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(btns['defaults'])
        bottom_layout.addWidget(btns['save'])

        self.window.path_label[id] = QLabel(str(path))
        self.window.path_label[id].setStyleSheet("font-weight: bold;")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(trans('dialog.config.streams.label')))
        layout.addWidget(self.window.path_label[id])
        layout.addWidget(self.window.editor['streams'])
        layout.addLayout(bottom_layout)

        self.window.dialog['config.' + id] = ConfiguratorDialog(self.window, id)
        self.window.dialog['config.' + id].setLayout(layout)
        self.window.dialog['config.' + id].setWindowTitle(trans('dialog.config.streams'))

    def setup_configurator_servo(self):
        """Setup servo config dialog"""
        id = 'servo'

        # self.window.editor['servo'] = QPlainTextEdit()
        # self.window.editor['servo'].setReadOnly(False)

        # load data
        # self.window.tracker.configurator.load(id)
        path = self.window.tracker.configurator.get_path(id)

        btns = {}
        btns['defaults'] = QPushButton(trans("dialog.config.btn.defaults"))
        btns['save'] = QPushButton(trans("dialog.config.btn.save"))
        btns['defaults'].clicked.connect(
            lambda: self.window.tracker.configurator.load_defaults(id))
        btns['save'].clicked.connect(
            lambda: self.window.tracker.configurator.save(id))

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(btns['defaults'])
        bottom_layout.addWidget(btns['save'])

        self.window.path_label[id] = QLabel(str(path))
        self.window.path_label[id].setStyleSheet("font-weight: bold;")

        self.window.settings['servo.fov.x'] = SettingsSlider(self.window, 'servo.fov.x',
                                                             trans('settings.servo.fov.x'), 0, 180,
                                                             1, 0)
        self.window.settings['servo.fov.y'] = SettingsSlider(self.window, 'servo.fov.y',
                                                             trans('settings.servo.fov.y'), 0, 180,
                                                             1, 0)

        self.window.settings['servo.min.x'] = SettingsSlider(self.window, 'servo.min.x',
                                                           trans('settings.servo.min.x'), 0, 180,
                                                           1, 0)
        self.window.settings['servo.max.x'] = SettingsSlider(self.window, 'servo.max.x',
                                                             trans('settings.servo.max.x'), 0, 180,
                                                             1, 180)
        self.window.settings['servo.min.y'] = SettingsSlider(self.window, 'servo.min.y',
                                                             trans('settings.servo.min.y'), 0, 180,
                                                             1, 0)
        self.window.settings['servo.max.y'] = SettingsSlider(self.window, 'servo.max.y',
                                                             trans('settings.servo.max.y'), 0, 180,
                                                             1, 180)

        self.window.settings['servo.limit.min.x'] = SettingsSlider(self.window, 'servo.limit.min.x',
                                                             trans('settings.servo.limit.min.x'), 0, 180,
                                                             1, 0)
        self.window.settings['servo.limit.max.x'] = SettingsSlider(self.window, 'servo.limit.max.x',
                                                             trans('settings.servo.limit.max.x'), 0, 180,
                                                             1, 180)
        self.window.settings['servo.limit.min.y'] = SettingsSlider(self.window, 'servo.limit.min.y',
                                                             trans('settings.servo.limit.min.y'), 0, 180,
                                                             1, 0)
        self.window.settings['servo.limit.max.y'] = SettingsSlider(self.window, 'servo.limit.max.y',
                                                             trans('settings.servo.limit.max.y'), 0, 180,
                                                             1, 180)

        label_x = QLabel(trans('settings.servo.x.label'))
        label_x.setAlignment(Qt.AlignCenter)
        label_x.setStyleSheet("font-weight: bold;")

        label_y = QLabel(trans('settings.servo.y.label'))
        label_y.setAlignment(Qt.AlignCenter)
        label_y.setStyleSheet("font-weight: bold;")

        config_x = QVBoxLayout()
        config_x.addWidget(label_x)
        config_x.addWidget(self.window.settings['servo.fov.x'])
        config_x.addWidget(self.window.settings['servo.min.x'])
        config_x.addWidget(self.window.settings['servo.max.x'])
        config_x.addWidget(self.window.settings['servo.limit.min.x'])
        config_x.addWidget(self.window.settings['servo.limit.max.x'])

        config_y = QVBoxLayout()
        config_y.addWidget(label_y)
        config_y.addWidget(self.window.settings['servo.fov.y'])
        config_y.addWidget(self.window.settings['servo.min.y'])
        config_y.addWidget(self.window.settings['servo.max.y'])
        config_y.addWidget(self.window.settings['servo.limit.min.y'])
        config_y.addWidget(self.window.settings['servo.limit.max.y'])

        cols = QHBoxLayout()
        cols.addLayout(config_x)
        cols.addLayout(config_y)

        pixmap = QtGui.QPixmap('./assets/servo_axes.png')
        img = QLabel()
        img.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(img)
        layout.addLayout(cols)
        layout.addLayout(bottom_layout)

        self.window.dialog['config.' + id] = ConfiguratorDialog(self.window, id)
        self.window.dialog['config.' + id].setLayout(layout)
        self.window.dialog['config.' + id].setWindowTitle(trans('dialog.config.servo'))

    def alert(self, msg):
        """
        Show alert dialog

        :param msg: message to show
        """
        self.window.alert_dialog.message.setText(msg)
        self.window.alert_dialog.show()

    def open(self, id, width=Style.DIALOG_DEBUG_WIDTH, height=Style.DIALOG_DEBUG_HEIGHT):
        """
        Open debug/config dialog

        :param id: debug dialog id
        """
        if id not in self.window.dialog:
            return
        self.window.dialog[id].resize(width, height)
        self.window.dialog[id].show()
        self.window.tracker.controller.configurator.update()

    def close(self, id):
        """
        Close debug/config dialog

        :param id: debug dialog id
        """
        if id not in self.window.dialog:
            return
        self.window.dialog[id].close()
        self.window.tracker.controller.configurator.close(id)
