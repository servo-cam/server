#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from PySide6 import QtCore
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import QLabel, QDialog, QTreeView, QMenu, QLineEdit, QAbstractItemView, \
    QDialogButtonBox, QVBoxLayout, QWidget, QHBoxLayout, QSlider, QCheckBox, QScrollArea, QPushButton
from core.utils import trans


# video output container (with scroll
class VideoContainer(QScrollArea):
    def __init__(self, window=None):
        """
        Video container with scroll

        :param window: main window
        """
        super(VideoContainer, self).__init__()
        self.window = window
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #000000;")

        self.label = {}

        # state
        self.label['status.state'] = QLabel('', self)
        self.label['status.state'].setStyleSheet("background-color: #000000; color: #ffffff; padding: 4px")
        self.label['status.state'].move(15, 10)
        self.label['status.state'].setVisible(False)

        # current work
        self.label['status.current'] = QLabel('', self)
        self.label['status.current'].setStyleSheet("background-color: #000000; color: #ffff00; padding: 4px")
        self.label['status.current'].move(15, 40)
        self.label['status.current'].setVisible(False)

        # action
        self.label['status.action'] = QLabel('', self)
        self.label['status.action'].setStyleSheet(
            "background-color: #000000; color: #ff0000; font-size: 20px; padding: 4px")
        self.label['status.action'].move(15, 75)
        self.label['status.action'].setVisible(False)

        # device status (bottom)
        self.label['status.device'] = QLabel('DEVICE STATUS', self)
        self.label['status.device'].setStyleSheet("background-color: #000000; color: #ffff00; padding: 4px")
        y = self.height() - 40
        self.label['status.device'].move(15, y)

        # sys info (to right)
        x = self.width() - 230

        css = "background-color: #000000; color: #ffffff; padding: 4px; font-size: 10px"
        self.label['info.fps'] = QLabel('FPS', self)
        self.label['info.fps'].setStyleSheet(css)
        self.label['info.fps'].move(x, 10)

        # mode
        self.label['mode'] = QLabel('', self)
        self.label['mode'].setStyleSheet(
            "background-color: #000000; color: #ffffff; font-size: 10px; padding: 4px")
        x = self.width() - 15
        y = self.height() - 40
        self.label['mode'].move(x, y)
        self.label['mode'].setVisible(False)

        # servo
        self.label['servo'] = QLabel('', self)
        self.label['servo'].setStyleSheet(
            "background-color: #000000; color: #ffff00; font-size: 10px; padding: 4px")
        x = self.width() - 15
        y = self.height() - 65
        self.label['servo'].move(x, y)
        self.label['servo'].setVisible(False)

        # remote
        self.label['remote'] = QLabel('', self)
        self.label['remote'].setStyleSheet("background-color: #000000; color: #ffffff; padding: 4px")
        self.label['remote'].move(15, 10)
        self.label['remote'].setVisible(False)

    def update_pos(self):
        """Update labels position"""
        # update device status bottom position
        y = self.height() - 40
        self.label['status.device'].move(15, y)
        x = self.width() - self.label['info.fps'].width() - 15
        self.label['info.fps'].move(x, 10)

        # action on center
        x = int(self.width() / 2 - self.label['status.action'].width() / 2)
        self.label['status.action'].move(x, 25)

        # mode
        x = self.width() - self.label['mode'].width() - 15
        y = self.height() - 40
        self.label['mode'].move(x, y)

        # servo
        x = self.width() - self.label['servo'].width() - 15
        y = self.height() - 65
        self.label['servo'].move(x, y)

        # remote
        x = int(self.width() / 2 - self.label['remote'].width() / 2)
        y = self.height() - 100
        self.label['remote'].move(x, y)

    # on resize
    def resizeEvent(self, event):
        """
        On resize event

        :param event: resize event
        """
        self.update_pos()
        super(VideoContainer, self).resizeEvent(event)


# video output label
class VideoLabel(QLabel):
    def __init__(self, text=None, window=None):
        """
        Video output label

        :param text: text
        :param window: main window
        """
        super(VideoLabel, self).__init__(text)
        self.window = window

    def update_coords(self, event):
        """
        Update coords

        :param event: mouse event
        """
        coords = self.mapFromParent(event.pos())
        px = self.pixmap()
        w = coords.x() + (self.window.container_video.width() - px.width())
        h = coords.y() + (self.window.container_video.height() - px.height())
        x = w - ((self.window.container_video.width() - px.width()) / 2)
        y = h - ((self.window.container_video.height() - px.height()) / 2)
        x = x - self.window.container_video.horizontalScrollBar().value()
        y = y - self.window.container_video.verticalScrollBar().value()

        # fix min/max
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x > px.width():
            x = px.width()
        if y > px.height():
            y = px.height()

        # check if image is empty
        if px.width() == 0:
            x = 0  # avoid division by zero
        else:
            # normalize
            x = x / px.width()

        if px.height() == 0:
            y = 0  # avoid division by zero
        else:
            # normalize
            y = y / px.height()

        # update mouse coords
        self.window.tracker.mouse.coords = (x, y)

    def mousePressEvent(self, event):
        """
        Mouse click

        :param event: mouse event
        """
        if event.button() == Qt.LeftButton:
            self.update_coords(event)
            self.window.tracker.mouse.click(self.window.tracker.mouse.MOUSE_LEFT)
        elif event.button() == Qt.RightButton:
            self.update_coords(event)
            self.window.tracker.mouse.click(self.window.tracker.mouse.MOUSE_RIGHT)
            # menu = QMenu(self)
            # menu.addAction(QAction("test", self))
            # menu.exec_(event.globalPos())
        elif event.button() == Qt.MiddleButton:
            self.update_coords(event)
            self.window.tracker.mouse.click(self.window.tracker.mouse.MOUSE_MIDDLE)

    def mouseDoubleClickEvent(self, event):
        """
        Mouse double click

        :param event: mouse event
        """
        if event.button() == Qt.LeftButton:
            self.update_coords(event)
            self.window.tracker.mouse.dbl_click(self.window.tracker.mouse.MOUSE_LEFT)
        elif event.button() == Qt.RightButton:
            self.update_coords(event)
            self.window.tracker.mouse.dbl_click(self.window.tracker.mouse.MOUSE_RIGHT)
            # menu = QMenu(self)
            # menu.addAction(QAction("test", self))
            # menu.exec_(event.globalPos())
        elif event.button() == Qt.MiddleButton:
            self.update_coords(event)
            self.window.tracker.mouse.dbl_click(self.window.tracker.mouse.MOUSE_MIDDLE)

    def mouseReleaseEvent(self, event):
        """
        Mouse release

        :param event: mouse event
        """
        if event.button() == Qt.LeftButton:
            self.update_coords(event)
            self.window.tracker.mouse.release(self.window.tracker.mouse.MOUSE_LEFT)
        elif event.button() == Qt.RightButton:
            self.update_coords(event)
            self.window.tracker.mouse.release(self.window.tracker.mouse.MOUSE_RIGHT)
            # menu = QMenu(self)
            # menu.addAction(QAction("test", self))
            # menu.exec_(event.globalPos())
        elif event.button() == Qt.MiddleButton:
            self.update_coords(event)
            self.window.tracker.mouse.release(self.window.tracker.mouse.MOUSE_MIDDLE)

    def mouseMoveEvent(self, event):
        """Mouse move"""
        self.update_coords(event)

    def keyPressEvent(self, event):
        """Key press"""
        super(VideoLabel, self).keyPressEvent(event)
        self.window.tracker.keyboard.on_key_press(event)


# debug window dialog
class DebugDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Debug window dialog

        :param window: main window
        :param id: debug window id
        """
        super(DebugDialog, self).__init__(window)
        self.window = window
        self.id = id

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.tracker.debug.active[self.id] = False
        self.window.tracker.controller.debug.update_menu()


# address input
class AddressInput(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        Address input

        :param window: main window
        :param id: address input id
        """
        super(AddressInput, self).__init__(window)
        self.window = window
        self.id = id

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(AddressInput, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.window.tracker.controller.source.load(self.window.source_address.text())


# filter input
class FilterInput(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        Filter input

        :param window: main window
        :param id: filter input id
        """
        super(FilterInput, self).__init__(window)
        self.window = window
        self.id = id

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(FilterInput, self).keyPressEvent(event)
        self.window.tracker.controller.control_filters.apply()


# coords input
class CoordsInput(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        Coords input

        :param window: main window
        :param id: coords input id
        """
        super(CoordsInput, self).__init__(window)
        self.window = window
        self.id = id
        self.setMaximumWidth(200)

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(CoordsInput, self).keyPressEvent(event)
        self.window.tracker.controller.control_area.apply(self.id)


# about window dialog
class InfoDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Info window dialog

        :param window: main window
        :param id: info window id
        """
        super(InfoDialog, self).__init__(window)
        self.window = window
        self.id = id

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.tracker.info.active[self.id] = False
        self.window.tracker.controller.info.update_menu()


# configuration edit dialog
class ConfiguratorDialog(QDialog):
    def __init__(self, window=None, id=None):
        """
        Configurator dialog

        :param window: main window
        :param id: configurator id
        """
        super(ConfiguratorDialog, self).__init__(window)
        self.window = window
        self.id = id

    def closeEvent(self, event):
        """
        Close event

        :param event: close event
        """
        self.window.tracker.configurator.active[self.id] = False
        self.window.tracker.controller.configurator.update_menu()


class AlertDialog(QDialog):
    def __init__(self, window=None):
        """
        Alert dialog

        :param window: main window
        """
        super(AlertDialog, self).__init__(window)
        self.window = window
        self.setWindowTitle(trans('alert.title'))

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.message = QLabel("")
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class UpdateDialog(QDialog):
    def __init__(self, window=None):
        """
        Update dialog

        :param window: main window
        """
        super(UpdateDialog, self).__init__(window)
        self.window = window
        self.setWindowTitle(trans('update.title'))

        download = QPushButton(trans('update.download'))
        download.clicked.connect(
            lambda: self.window.tracker.controller.info.goto_update())

        self.layout = QVBoxLayout()
        self.message = QLabel("")
        self.layout.addWidget(self.message)
        self.layout.addWidget(download)
        self.setLayout(self.layout)


class OptionSlider(QWidget):
    def __init__(self, window=None, id=None, title=None, min=None, max=None, step=None, value=None):
        """
        Option slider

        :param window: main window
        :param id: option id
        :param title: option title
        :param min: min value
        :param max: max value
        :param step: value step
        :param value: current value
        """
        super(OptionSlider, self).__init__(window)
        self.window = window
        self.id = id
        self.title = title
        self.min = min
        self.max = max
        self.step = step
        self.value = value

        self.label = QLabel(title)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)
        self.slider.setSingleStep(step)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(
            lambda: self.window.tracker.controller.options.apply(self.id, self.slider.value(), 'slider'))

        self.input = OptionInputInline(self.window, self.id)
        self.input.setText(str(value))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.input)

        self.setLayout(self.layout)


class OptionCheckbox(QWidget):
    def __init__(self, window=None, id=None, title=None, value=False):
        """
        Option checkbox

        :param window: main window
        :param id: option id
        :param title: option title
        :param value: current value
        """
        super(OptionCheckbox, self).__init__(window)
        self.window = window
        self.id = id
        self.title = title
        self.value = value

        self.label = QLabel(title)
        self.box = QCheckBox()
        self.box.setChecked(value)
        self.box.stateChanged.connect(
            lambda: self.window.tracker.controller.options.toggle(self.id, self.box.isChecked()))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.box)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


class OptionInputInline(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        Option input inline

        :param window: main window
        :param id: option id
        """
        super(OptionInputInline, self).__init__(window)
        self.window = window
        self.id = id
        self.setMaximumWidth(60)

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(OptionInputInline, self).keyPressEvent(event)
        self.window.tracker.controller.options.apply(self.id, self.text(), 'input')


class OptionInput(QLineEdit):
    def __init__(self, window=None, id=None):
        """
        Option input

        :param window: main window
        :param id: option id
        """
        super(OptionInput, self).__init__(window)
        self.window = window
        self.id = id
        self.setMaximumWidth(60)

    def keyPressEvent(self, event):
        """
        Key press event

        :param event: key event
        """
        super(OptionInput, self).keyPressEvent(event)
        self.window.tracker.controller.options.change(self.id, self.text())


class ClientsMenu(QTreeView):
    REMOTE_HOST, REMOTE_IP, REMOTE_TIME = range(3)  # list columns

    def __init__(self, window=None):
        """
        Clients menu

        :param window: main window
        """
        super(ClientsMenu, self).__init__(window)
        self.window = window
        self.setStyleSheet("QTreeView {"
                           "padding: 0px;"
                           "margin: 0px;"
                           "};"
                           "QTreeView::item {"
                           "padding: 0px;"
                           "margin: 0px;"
                           "}")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: context menu event \
        """
        menu = QMenu(self)
        actions = {}
        actions['connect'] = QAction(trans("clients.context.connect"), self)
        actions['disconnect'] = QAction(trans("clients.context.disconnect"), self)
        actions['restart'] = QAction(trans("clients.context.restart"), self)
        actions['destroy'] = QAction(trans("clients.context.destroy"), self)
        actions['remove'] = QAction(trans("clients.context.remove"), self)

        actions['connect'].triggered.connect(
            lambda: self.client_connect(event))
        actions['disconnect'].triggered.connect(
            lambda: self.client_disconnect(event))
        actions['restart'].triggered.connect(
            lambda: self.client_restart(event))
        actions['destroy'].triggered.connect(
            lambda: self.client_destroy(event))
        actions['remove'].triggered.connect(
            lambda: self.client_remove(event))

        menu.addAction(actions['connect'])
        menu.addAction(actions['disconnect'])
        menu.addAction(actions['restart'])
        menu.addAction(actions['destroy'])
        menu.addAction(actions['remove'])

        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            menu.exec_(event.globalPos())

    def client_connect(self, event):
        """
        Connect to client

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            ip = item.sibling(idx, ClientsMenu.REMOTE_IP).data()
            host = self.window.tracker.remote.clients[ip].hostname
            if host is None:
                host = ip
            self.window.tracker.remote_ip = ip
            self.window.tracker.remote_host = host
            if self.window.tracker.source != self.window.tracker.SOURCE_REMOTE:
                self.window.tracker.controller.source.toggle(self.window.tracker.SOURCE_REMOTE, True)
                self.window.tracker.controller.source.load(ip)
            else:
                self.window.tracker.controller.source.load(ip)

    def client_disconnect(self, event):
        """
        Disconnect from client

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            ip = item.sibling(idx, ClientsMenu.REMOTE_IP).data()
            self.window.tracker.remote.disconnect(ip)

    def client_restart(self, event):
        """
        Restart client

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            ip = item.sibling(idx, ClientsMenu.REMOTE_IP).data()
            self.window.tracker.remote.restart(ip)

    def client_destroy(self, event):
        """
        Destroy client

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            ip = item.sibling(idx, ClientsMenu.REMOTE_IP).data()
            self.window.tracker.remote.remote_destroy(ip)

    def client_remove(self, event):
        """
        Remove client

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            ip = item.sibling(idx, ClientsMenu.REMOTE_IP).data()
            self.window.tracker.remote.remove(ip)

    '''
    def mousePressEvent(self, event):
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            print(idx)
        super(ClientsMenu, self).mousePressEvent(event)
    '''


class StreamsMenu(QTreeView):
    STREAM_NAME, STREAM_HOST, STREAM_PORT, STREAM_STATUS = range(4)  # list columns

    def __init__(self, window=None):
        """
        Streams menu

        :param window: main window
        """
        super(StreamsMenu, self).__init__(window)
        self.window = window
        self.setStyleSheet("QTreeView {"
                           "padding: 0px;"
                           "margin: 0px;"
                           "};"
                           "QTreeView::item {"
                           "padding: 0px;"
                           "margin: 0px;"
                           "}")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def contextMenuEvent(self, event):
        """
        Context menu event

        :param event: mouse event
        """
        menu = QMenu(self)
        actions = {}
        actions['connect'] = QAction(trans("clients.context.connect"), self)
        actions['destroy'] = QAction(trans("clients.context.destroy"), self)
        actions['remove'] = QAction(trans("clients.context.remove"), self)

        actions['connect'].triggered.connect(
            lambda: self.client_connect(event))
        actions['destroy'].triggered.connect(
            lambda: self.client_destroy(event))
        actions['remove'].triggered.connect(
            lambda: self.client_remove(event))

        menu.addAction(actions['connect'])
        # menu.addAction(actions['destroy'])
        menu.addAction(actions['remove'])

        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            menu.exec_(event.globalPos())

    def client_connect(self, event):
        """
        Connect to stream

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            uniq_id = item.sibling(idx, StreamsMenu.STREAM_HOST).data() + "_" + item.sibling(idx,
                                                                                             StreamsMenu.STREAM_PORT).data()
            self.window.tracker.stream.connect(uniq_id)

    def client_destroy(self, event):
        """
        Destroy stream

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            uniq_id = item.sibling(idx, StreamsMenu.STREAM_HOST).data() + "_" + item.sibling(idx,
                                                                                             StreamsMenu.STREAM_PORT).data()
            self.window.tracker.stream.remote_destroy(uniq_id)

    def client_remove(self, event):
        """
        Remove stream

        :param event: mouse event
        """
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            uniq_id = item.sibling(idx, StreamsMenu.STREAM_HOST).data() + "_" + item.sibling(idx,
                                                                                             StreamsMenu.STREAM_PORT).data()
            self.window.tracker.stream.remove(uniq_id)

    '''
    def mousePressEvent(self, event):
        item = self.indexAt(event.pos())
        idx = item.row()
        if idx >= 0:
            print(idx)
        super(ClientsMenu, self).mousePressEvent(event)
    '''
