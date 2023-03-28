#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import socket
import time
import zmq
from datetime import datetime
from core.utils import to_json, json_decode


class Sockets:
    # data formats
    FORMAT_RAW = "RAW"
    FORMAT_JSON = "JSON"

    # data types keys
    DATA_TYPE_CMD = "CMD"

    # ports
    PORT_DATA = 6666
    PORT_CONN = 6667
    PORT_STATUS = 6668

    # max packets wait limit before reset
    MAX_PACKETS_WAIT = 1000000

    def __init__(self, tracker=None):
        """
        Sockets handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.receiver = None
        self.sender = None
        self.started = False
        self.is_send = False
        self.is_recv = False
        self.last_reset = datetime.now()
        self.push_context = {}
        self.push_socket = {}
        self.pull_context = {}
        self.pull_socket = {}
        self.is_connected = False
        self.packets_wait = 0

        # data format
        self.data_format = self.FORMAT_JSON

    def init(self, ip=None, force=False):
        """
        Initialize sockets

        :param ip: IP address of peer
        :param force: force recreate sockets
        """
        if ip is not None and (force or ip not in self.push_socket or self.push_socket[ip] is None):
            self.tracker.debug.log(
                "[SOCKET] Connecting with remote PULL socket to {} on port {} ".format(ip, self.PORT_DATA))

            # destroy old socket
            if ip in self.push_socket and self.push_socket[ip] is not None:
                self.push_socket[ip].close()
            if ip in self.push_context and self.push_context[ip] is not None:
                self.push_context[ip].destroy()
            time.sleep(0.1)

            try:
                self.push_context[ip] = zmq.Context()
                self.push_socket[ip] = self.push_context[ip].socket(zmq.PUSH)
                self.push_socket[ip].setsockopt(zmq.LINGER, 0)  # needed to avoid blocking on exit
                self.push_socket[ip].setsockopt(zmq.CONFLATE, 1)
                self.push_socket[ip].connect("tcp://{}:{}".format(ip, self.PORT_DATA))
            except Exception as e:
                self.tracker.debug.log(
                    "[SOCKET] Error connecting with remote PULL socket to {} on port {} ".format(ip, self.PORT_DATA))
                self.tracker.debug.log("[SOCKET] Error: {}".format(e))

        if ip is not None and (force or ip not in self.pull_socket or self.pull_socket[ip] is None):
            self.tracker.debug.log(
                "[SOCKET] Connecting with remote PUSH socket to {} on port {} ".format(ip, self.PORT_STATUS))

            # destroy old socket
            if ip in self.pull_socket and self.pull_socket[ip] is not None:
                self.pull_socket[ip].close()
            if ip in self.pull_context and self.pull_context[ip] is not None:
                self.pull_context[ip].destroy()
            time.sleep(0.1)

            try:
                self.pull_context[ip] = zmq.Context()
                self.pull_socket[ip] = self.pull_context[ip].socket(zmq.PULL)
                self.pull_socket[ip].setsockopt(zmq.LINGER, 0)  # needed to avoid blocking on exit
                self.pull_socket[ip].setsockopt(zmq.CONFLATE, 1)
                self.pull_socket[ip].connect("tcp://{}:{}".format(ip, self.PORT_STATUS))
            except Exception as e:
                self.tracker.debug.log(
                    "[SOCKET] Error connecting with remote PUSH socket to {} on port {} ".format(ip, self.PORT_STATUS))
                self.tracker.debug.log("[SOCKET] Error: {}".format(e))

        self.started = True

    def connect(self, ip, force=False):
        """
        Connect to remote server

        :param ip: IP address of peer
        :param force: force recreate sockets
        """
        self.init(ip, force)
        self.is_connected = True

        tmp_socket = None
        try:
            # temporary socket to only send server ip
            cmd = to_json('NEW', "CONN")
            if self.tracker.encrypt.enabled_data:
                msg = self.tracker.encrypt.encrypt(cmd)  # as bytes
            else:
                msg = bytes(cmd, "utf-8")

            tmp_socket = socket.socket()  # instantiate
            tmp_socket.settimeout(5)  # destroy after 5 seconds
            tmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tmp_socket.connect((ip, self.PORT_CONN))  # connect to the client
            tmp_socket.send(msg)  # send message
            response = tmp_socket.recv(1024)
            tmp_socket.close()  # close the connection

            if response is not None:
                # decrypt
                if self.tracker.encrypt.enabled_data:
                    response = bytes(self.tracker.encrypt.decrypt(response), 'UTF-8')  # as bytes
                # handle connection response
                self.handle_thread(response.decode('UTF-8'), ip)
        except Exception as e:
            try:
                if tmp_socket is not None:
                    tmp_socket.close()
                    time.sleep(1)
            except Exception as e:
                print("[SOCKET] Socket close failed: {}, error: {}".format(ip, e))

            print("[SOCKET] Connection failed to {}, error: {}".format(ip, e))

    def listen(self):
        """
        Listen for messages from client

        :return: message from client
        """
        if self.tracker.remote_ip is None:
            return

        ip = self.tracker.remote_ip

        self.init(ip)

        if ip not in self.pull_socket \
                or self.pull_socket[ip] is None \
                or self.pull_socket[ip].closed:
            return

        try:
            result = self.pull_socket[ip].recv()
        except Exception as e:
            print(e)
            self.tracker.debug.log("[SOCKET] Failed to receive data from {}".format(ip))
            time.sleep(0.1)
            return

        # decrypt
        if result is not None and self.tracker.encrypt.enabled_data:
            result = bytes(self.tracker.encrypt.decrypt(result), 'UTF-8')  # as bytes

        self.is_recv = True
        return result

    def send(self, ip, data):
        """
        Send message to client

        :param ip: IP address of peer
        :param data: data to send
        """
        self.init(ip)

        if ip not in self.push_socket \
                or self.push_socket[ip] is None \
                or self.push_socket[ip].closed:
            return

        # reset packets wait
        if self.packets_wait > self.MAX_PACKETS_WAIT:
            self.packets_wait = 0

        result = None
        if ip is not None:
            # convert to json if needed
            if self.data_format == self.FORMAT_JSON:
                data = to_json(data, self.DATA_TYPE_CMD)

            try:
                # encrypt
                if self.tracker.encrypt.enabled_data:
                    data = self.tracker.encrypt.encrypt(data)
                    result = self.push_socket[ip].send(data)  # already bytes
                else:
                    result = self.push_socket[ip].send(bytes(data, 'UTF-8'))
                    self.packets_wait += 1  # increase packets wait
            except Exception as e:
                print(e)
                self.tracker.debug.log("[SOCKET] Failed to send data to {}".format(ip))
                time.sleep(0.1)
                return

        self.is_send = True
        return result

    def handle_thread(self, buff, ip):
        """
        Handle socket thread

        :param buff: Received data
        :param ip: IP address of peer
        """
        if self.tracker.source != self.tracker.SOURCE_REMOTE:
            return

        # convert from json if needed
        if self.data_format == self.FORMAT_JSON:
            try:
                buff = json_decode(buff)  # buff is already a decoded UTF-8 string
            except Exception as e:
                self.tracker.debug.log("[SOCKET] Received invalid JSON from {}".format(ip))
                print(e)
                return

        if self.data_format == self.FORMAT_JSON:
            if 'v' in buff:
                if buff['v'] == "ACCEPT" or buff['v'] == "OK" or buff['v'] == "ERROR":
                    self.tracker.debug.log("[SOCKET] Received `{}` from {}".format(buff['v'], ip))
        elif buff == "ACCEPT" or buff == "OK" or buff == "ERROR":
            self.tracker.debug.log("[SOCKET] Received `{}` from {}".format(buff, ip))

        self.tracker.remote.handle_socket(buff, ip)

    def reset_state(self):
        """Reset sockets state"""
        # wait a little before reset
        if (datetime.now() - self.last_reset).microseconds < 100000:
            return

        self.is_send = False
        self.is_recv = False
        self.last_reset = datetime.now()
