#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import json
import os
import cv2
import requests
from urllib.parse import urlparse
from datetime import datetime
from core.stream import Stream


class Webstream:
    STATUS_CHECK_INTERVAL = 5

    def __init__(self, tracker=None):
        """
        Webstream handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.streams = {}
        self.loop = 1
        self.sending = False
        self.last_status_check = datetime.now()
        self.check_status = True

    def handle(self, src):
        """
        Handle video source

        :param src: video source
        :return: video capture
        """
        return cv2.VideoCapture(src)

    def parse_as_entry(self, stream):
        """
        Parse stream to storage entry

        :param stream: stream
        :return: storage entry
        """
        txt = ''
        if stream.removed:
            txt += '# '
        txt += stream.protocol + '://' + stream.host + ':' + str(stream.port)
        if stream.name is not None:
            txt += ' ' + stream.name
        if stream.password is not None:
            txt += ' pass=' + stream.password
        return txt

    def update(self):
        """On update"""
        if self.check_status and self.tracker.servo.stream is not None:
            self.send_status_check(self.tracker.servo.stream)

    def send_status_check(self, unique_id):
        """
        Send status check to device

        :param unique_id: unique id
        """
        if self.sending:
            return

        # check only in specified seconds period
        if (datetime.now() - self.last_status_check).seconds > self.STATUS_CHECK_INTERVAL:
            url = self.get_status_url(unique_id)
            if url is not None:
                try:
                    response = requests.get(url)
                    self.handle_status(response.text, False)
                except Exception as e:
                    print(e)
            self.last_status_check = datetime.now()

    def handle_status(self, data, json=True):
        """
        Handle status response

        :param data: received data
        :param json: True if data is in json format
        """
        status = None
        if json:
            try:
                status = json.loads(data)['v']  # buff is already a decoded UTF-8 string
            except:
                pass
        else:
            status = data

        if status is not None:
            self.tracker.remote_status['-'] = status

    def send_command(self, unique_id, command):
        """
        Send command to servo

        :param unique_id: stream unique id
        :param command: command to send
        """
        url = self.get_servo_url(unique_id)
        if url is not None:
            self.sending = True
            try:
                response = requests.post(url, data={'cmd': command})
                self.handle_status(response.text)
            except Exception as e:
                print(e)
            self.sending = False

    def get_unique_id(self, addr):
        """
        Get unique id from address

        :param addr: address
        :return: unique id
        """
        parsed_uri = urlparse(addr)
        uri_host = '{uri.netloc}'.format(uri=parsed_uri).split(':')[0]
        uri_port = '{uri.port}'.format(uri=parsed_uri)
        return uri_host + '_' + uri_port

    def get_servo_url(self, unique_id):
        """
        Get servo control url

        :param unique_id: unique id
        :return: servo control url
        """
        if unique_id in self.streams.keys():
            if self.streams[unique_id].protocol == 'https':
                url = 'https://'
            else:
                url = 'http://'
            url += self.streams[unique_id].host + ':' + self.streams[unique_id].port + '/cmd'
            if self.streams[unique_id].password is not None:
                url += '?token=' + self.streams[unique_id].password
            return url
        return None

    def get_status_url(self, unique_id):
        """
        Get status get url

        :param unique_id: unique id
        :return: status url
        """
        if unique_id in self.streams.keys():
            if self.streams[unique_id].protocol == 'https':
                url = 'https://'
            else:
                url = 'http://'
            url += self.streams[unique_id].host + ':' + self.streams[unique_id].port + '/status'
            if self.streams[unique_id].password is not None:
                url += '?token=' + self.streams[unique_id].password
            return url
        return None

    def toggle_servo(self, unique_id):
        """
        Toggle servo

        :param unique_id: unique id
        """
        self.tracker.servo.stream = unique_id
        self.tracker.controller.servo.update_stream()  # update menu UI

    def connect(self, unique_id):
        """
        Connect to stream

        :param unique_id: unique id
        """
        if unique_id in self.streams.keys():
            addr = self.get_full_address(unique_id)
            self.streams[unique_id].disconnected = False
            self.tracker.debug.log("[STREAM] Stream connecting: {}".format(addr))
        else:
            # add to list
            addr = unique_id
            self.add(addr)

        if self.tracker.stream != self.tracker.SOURCE_STREAM:
            self.tracker.controller.source.toggle(self.tracker.SOURCE_STREAM, True)
            self.tracker.controller.source.load(addr, False)
        else:
            self.tracker.controller.source.load(addr, False)

        self.toggle_servo(unique_id)

    def add(self, addr, name=None, pwd=None):
        """
        Add stream to streams dictionary

        :param addr: address
        :param name: name
        :param pwd: password
        """
        if addr is None:
            return

        parsed_uri = urlparse(addr)
        uri_host = '{uri.netloc}'.format(uri=parsed_uri).split(':')[0]
        uri_port = '{uri.port}'.format(uri=parsed_uri)
        uri_protocol = '{uri.scheme}'.format(uri=parsed_uri)
        uri_query = '{uri.query}'.format(uri=parsed_uri)

        if name is None:
            name = uri_host

        unique_id = self.get_unique_id(addr)

        # add client
        if unique_id not in self.streams.keys():
            stream = Stream()
            stream.unique_id = unique_id
            stream.addr = addr
            stream.host = uri_host
            stream.protocol = uri_protocol
            stream.port = uri_port
            stream.query = uri_query
            stream.name = name
            stream.password = pwd
            self.streams[unique_id] = stream
            self.tracker.debug.log("[STREAM] Stream added: {}".format(addr))
        else:
            if name is not None:
                self.streams[unique_id].name = name
            if pwd is not None:
                self.streams[unique_id].password = pwd
            self.streams[unique_id].removed = False
            self.streams[unique_id].disconnected = False

    def remove(self, unique_id):
        """
        Remove stream from streams dictionary

        :param unique_id: unique id
        """
        if unique_id in self.streams.keys():
            self.streams[unique_id].removed = True
            self.tracker.debug.log("[STREAM] Stream removed: {}".format(unique_id))

            # disconnect servo
            if self.tracker.servo.stream == unique_id:
                self.toggle_servo(None)

            # clear
            if self.tracker.stream_url == self.get_full_address(unique_id):
                self.tracker.stream_url = None

    def remote_destroy(self, unique_id):
        """
        Remote destroy client

        :param unique_id: unique id
        """
        if unique_id in self.streams.keys():
            self.streams[unique_id].disconnected = True
            self.tracker.debug.log("[STREAM] Stream disconnected: {}".format(unique_id))

    def get_full_address(self, unique_id):
        """
        Get full address

        :param unique_id: unique id
        :return: full address
        """
        if unique_id in self.streams.keys():
            addr = self.streams[unique_id].protocol + '://' + self.streams[unique_id].host + ':' + self.streams[
                unique_id].port
            if self.streams[unique_id].password is not None:
                addr += '?token=' + self.streams[unique_id].password
            return addr
        return None

    def load(self):
        """Load streams from file"""
        # user file
        f = self.tracker.storage.get_user_streams_path()
        if not os.path.exists(f):
            # default file
            f = self.tracker.storage.get_default_streams_path()

        # abort if no file
        if not os.path.exists(f):
            return

        with open(f, 'r') as file:
            lines = file.readlines()
            self.tracker.debug.log("[REMOTE] Loaded {} stream(s) from file: {}".format(len(lines), f))
            for line in lines:
                if line.startswith('#'):
                    continue
                if line.strip() == '':
                    continue
                line = ' '.join(line.strip().split())
                parts = line.split(' ')

                addr = None
                name = None
                pwd = None

                if len(parts) == 1:
                    addr = parts[0]
                    name = parts[0]
                elif len(parts) == 2:
                    addr = parts[0]
                    name = parts[1]
                elif len(parts) == 3:
                    addr = parts[0]
                    name = parts[1]
                    tmp = parts[2].split('pass=')
                    if len(tmp) == 2:
                        pwd = tmp[1]

                self.tracker.stream.add(addr, name, pwd)
