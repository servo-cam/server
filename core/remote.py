#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

from imutils import build_montages
from datetime import datetime
import imagezmq
import socket
import time
import os
import imutils
import cv2
import simplejpeg
from core.client import Client
from core.utils import trans


class Remote:
    # timeouts
    CLIENT_CONN_WAIT = 5
    CLIENT_CONN_TIMEOUT = 10
    CLIENT_HANG_TIME = 5
    CLIENT_INACTIVE_TIME = 5
    STREAM_JPEG = False

    # states
    STATE_CONNECTING = trans('client.state.CONNECTING')
    STATE_CONNECTED = trans('client.state.CONNECTED')
    STATE_DISCONNECTED = trans('client.state.DISCONNECTED')
    STATE_DESTROYED = trans('client.state.DESTROYED')
    STATE_REMOVED = trans('client.state.REMOVED')
    STATE_TIMEOUT = trans('client.state.TIMEOUT')
    STATE_RESTARTING = trans('client.state.RESTARTING')

    def __init__(self, tracker=None):
        """
        Remote clients handling class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.imageHub = imagezmq.ImageHub()
        self.clients = {}
        self.data = {}
        self.last_active_check = datetime.now()
        self.send_conn_time = {}
        self.conn_timer = datetime.now()
        self.is_connecting = False
        self.montage_columns = 2
        self.montage_rows = 2
        self.montage_width = 400
        self.active = False
        self.status = None

        # ping
        self.ping_video = 0
        self.ping_data = 0

    def add(self, ip, hostname=None, name=None):
        """
        Add client to list

        :param ip: Client IP address
        :param hostname: Client hostname
        :param name: Custom client name
        """
        if ip is None:
            return
        if hostname is None:
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = ip

        # add client
        if ip not in self.clients.keys():
            client = Client()
            client.ip = ip
            client.hostname = hostname
            client.name = name
            client.last_active_time = None
            client.hang_time = datetime.now()
            self.clients[ip] = client
            self.tracker.debug.log("[REMOTE] Client added: {}".format(ip))
        else:
            if hostname is not None:
                self.clients[ip].hostname = hostname
            self.clients[ip].last_active_time = None
            self.clients[ip].hang_time = datetime.now()

    def add_host(self, host, hostname=None, name=None):
        """
        Add host to list

        :param host: Client IP address or hostname
        :param hostname: Client hostname
        :param name: Custom client name
        """
        try:
            socket.inet_aton(host)
            ip = host
        except socket.error:
            ip = None
        if ip is None:
            ip = self.host2ip(host)
        if ip is not None:
            self.add(ip, hostname, name)

    def get_client_by_name(self, name):
        """
        Get client by custom name

        :param name: Custom client name
        :return: Client object
        """
        for client in self.clients.values():
            if client.name == name:
                return client
        return None

    def ping(self, ip):
        """
        Send ping to client

        :param ip: Client IP address
        """
        self.tracker.sockets.send(ip, "1")
        self.tracker.debug.log("[REMOTE] PING {}".format(ip))

    def connect(self, ip, force=False):
        """
        Connect with client

        :param ip: Client IP address
        :param force: Force connect
        """
        self.status = None
        if ip is None:
            self.tracker.window.ui.dialogs.alert(trans('alert.remote.invalid_ip'))
            self.tracker.debug.log("[REMOTE] CONNECT: Empty IP address! ABORTING!")
            self.status = self.STATE_DISCONNECTED
            if ip in self.clients.keys():
                self.clients[ip].state = self.STATE_DISCONNECTED
                self.clients[ip].disconnected = True
                self.clients[ip].last_active_time = None
            time.sleep(0.5)
            return

        self.status = self.STATE_CONNECTING
        self.is_connecting = True
        self.conn_timer = datetime.now()

        if ip in self.clients.keys():
            self.clients[ip].state = self.STATE_CONNECTING
            if force:
                self.clients[ip].disconnected = False
                self.clients[ip].removed = False
                self.clients[ip].last_active_time = None

        # if connect was called then wait some seconds before sending next hello
        if ip in self.send_conn_time.keys() and self.CLIENT_CONN_WAIT > 0:
            if (datetime.now() - self.send_conn_time[ip]).seconds < self.CLIENT_CONN_WAIT:
                time.sleep(0.2)
                return
        self.tracker.debug.log("[REMOTE] Sending CONNECT to {}".format(ip))
        self.tracker.sockets.connect(ip)
        self.send_conn_time[ip] = datetime.now()

    def check(self, ip, force=False):
        """
        Check if client connected, if not then connect

        :param ip: Client IP address
        :param force: Force connect
        """
        if not self.is_connected(ip):
            if force or (not self.is_disconnected(ip) and not self.is_removed(ip)):
                if ip in self.clients.keys():
                    self.clients[ip].state = self.STATE_CONNECTING
                    self.connect(ip)
            time.sleep(0.2)

    def is_connected(self, ip):
        """
        Check if client connected

        :param ip: Client IP address
        :return: True if connected
        """
        if ip in self.clients.keys():
            if self.is_disconnected(ip) or self.is_removed(ip):
                return False

            if self.clients[ip].last_active_time is None:
                return True

            # if lost connection then dispose now!
            if 0 < self.CLIENT_INACTIVE_TIME < (
                    datetime.now() - self.clients[ip].last_active_time).seconds:
                self.tracker.debug.log("[REMOTE] Lost connection to {}".format(ip))
                self.tracker.window.ui.dialogs.alert(trans('alert.remote.disconnected'))
                self.status = self.STATE_DISCONNECTED
                self.dispose(ip)
                return False
            else:
                return True
        return False

    def is_disconnected(self, ip):
        """
        Check if client disconnected

        :param ip: Client IP address
        :return: True if disconnected
        """
        if ip in self.clients.keys():
            return self.clients[ip].disconnected
        return False

    def is_removed(self, ip):
        """
        Check if client removed

        :param ip: Client IP address
        :return: True if removed
        """
        if ip in self.clients.keys():
            return self.clients[ip].removed
        return False

    def dispose(self, ip):
        """
        Remove client

        :param ip: Client IP address
        :return: True if removed
        """
        if ip in self.clients:
            self.clients[ip].last_active_time = None
            self.clients[ip].disconnected = True

        # remove from clients
        if ip in self.data:
            self.data.pop(ip)

        # clear
        if ip == self.tracker.remote_ip:
            self.tracker.remote_ip = None
        if ip == self.tracker.remote_host:
            self.tracker.remote_host = None

    def restart(self, ip):
        """
        Restart client

        :param ip: Client IP address
        """
        self.tracker.debug.log("[REMOTE] Sending restart command to: {}...".format(ip))
        self.tracker.sockets.send(ip, "RESTART")

    def toggle_servo(self, ip):
        """
        Toggle servo remote

        :param ip: Client IP address
        """
        self.tracker.servo.remote = ip
        self.tracker.controller.servo.update_remote()  # update menu UI

    def disconnect(self, ip):
        """
        Disconnect client

        :param ip: Client IP address
        """
        self.tracker.debug.log("[REMOTE] Sending disconnect command to: {}...".format(ip))
        self.tracker.sockets.send(ip, "DISCONNECT")
        if ip in self.clients:
            self.clients[ip].state = self.STATE_DISCONNECTED
            self.clients[ip].disconnected = True
            self.clients[ip].last_active_time = None
            self.status = self.STATE_DISCONNECTED

        # remove from clients
        if ip in self.data:
            self.data.pop(ip)

        # disconnect servo
        if self.tracker.servo.remote == ip:
            self.toggle_servo(None)

        # clear
        if ip == self.tracker.remote_ip:
            self.tracker.remote_ip = None
        if ip == self.tracker.remote_host:
            self.tracker.remote_host = None

    def remove(self, ip):
        """
        Remove client

        :param ip: Client IP address
        """
        self.disconnect(ip)
        self.tracker.debug.log("[REMOTE] Removing client: {}...".format(ip))
        if ip in self.clients:
            self.clients[ip].state = self.STATE_REMOVED
            self.clients[ip].removed = True
            self.clients[ip].disconnected = True
            self.clients[ip].last_active_time = None
            self.status = self.STATE_DISCONNECTED

        # remove from clients
        if ip in self.data:
            self.data.pop(ip)

        # disconnect servo
        if self.tracker.servo.remote == ip:
            self.toggle_servo(None)

        # clear
        if ip == self.tracker.remote_ip:
            self.tracker.remote_ip = None
        if ip == self.tracker.remote_host:
            self.tracker.remote_host = None

    def remote_destroy(self, ip):
        """
        Destroy client

        :param ip: Client IP address
        """
        self.clients[ip].state = self.STATE_DESTROYED
        self.tracker.debug.log("[REMOTE] Sending destroy command to: {}...".format(ip))
        self.tracker.sockets.send(ip, "DESTROY")
        self.status = self.STATE_DISCONNECTED

        # disconnect servo
        if self.tracker.servo.remote == ip:
            self.toggle_servo(None)

        # clear
        if ip == self.tracker.remote_ip:
            self.tracker.remote_ip = None
        if ip == self.tracker.remote_host:
            self.tracker.remote_host = None

    def handle_socket(self, buff, ip):
        """
        Handle socket data

        :param buff: Received data buffer - decoded JSON
        :param ip: Client IP address
        """
        # get timestamp from packet and calculate ping
        if 't' in buff:
            ping = round(time.time() * 1000) - int(buff['t'])
            if ping < 0:
                ping = 0
            self.ping_data = ping

            # store in client
            if ip in self.clients:
                self.clients[ip].ping_data = ping

        # handle commands
        if "k" in buff and "v" in buff and buff['k'] == 'CMD':
            cmd = buff['v']

            # connection accepted
            if cmd == "ACCEPT":
                hostname = buff['hostname']
                self.add(ip, hostname)
                self.tracker.sockets.packets_wait -= 1  # decrease packets wait
                self.status = None
                self.is_connecting = False

            # ping
            elif cmd == "1":
                self.check(ip)

            # device cmd receive confirmation
            elif cmd == "RECV":
                self.tracker.sockets.packets_wait -= 1  # decrease packets wait

            # cmd confirmation
            elif cmd == "OK":
                self.tracker.sockets.packets_wait -= 1  # decrease packets wait

            # update remote status
            else:
                self.tracker.remote_status[ip] = cmd

    def update(self):
        """Handle on app loop"""
        if self.is_connecting and (datetime.now() - self.conn_timer).seconds >= self.CLIENT_CONN_TIMEOUT:
            self.tracker.debug.log("[REMOTE] Client <{}> not responding...".format(self.tracker.remote_ip))
            self.is_connecting = False
            self.status = self.STATE_DISCONNECTED
            self.tracker.sockets.packets_wait -= 1

            if self.tracker.remote_ip is not None:
                if self.tracker.remote_ip in self.clients.keys():
                    self.clients[self.tracker.remote_ip].state = self.STATE_TIMEOUT

        # check if any clients are not active
        '''
        for ip in self.clients:
            if 0 < self.CLIENT_HANG_TIME < (datetime.now() - self.clients[ip].hang_time).seconds:
                if not self.is_disconnected(ip) and not self.is_removed(ip):
                    if ip == self.tracker.remote_ip:
                        self.tracker.debug.log(
                            "[REMOTE] Client <{}> not responding... Trying to re-connect client via remote command...".format(
                                ip))
                        self.clients[ip].state = self.STATE_RESTARTING
                        self.restart(ip)
                    self.clients[ip].hang_time = datetime.now()
        '''

        # check if any clients are not unable to connect
        for ip in self.send_conn_time:
            if not self.is_connected(ip) and 0 < self.CLIENT_CONN_WAIT < (
                    datetime.now() - self.send_conn_time[ip]).seconds:
                if not self.is_disconnected(ip) and not self.is_removed(ip):
                    self.tracker.debug.log("[REMOTE] Client <{}> not responding... Trying to re-connect...".format(ip))
                    if ip in self.clients:
                        self.clients[ip].state = self.STATE_CONNECTING
                    self.connect(ip)

        # update clients list
        if self.tracker.window is not None:
            self.tracker.window.ui.toolbox.remote.update()

    def update_client_by_hostname(self, hostname):
        """
        Update client by received hostname

        :param hostname: Received hostname
        """
        for ip in self.clients:
            # update active time if not disconnected
            if self.is_disconnected(ip) or self.is_removed(ip):
                continue

            if self.clients[ip].hostname == hostname:
                self.clients[ip].hang_time = datetime.now()  # end hang time
                if self.clients[ip].last_active_time is None:
                    self.tracker.debug.log("[REMOTE] Client <{}> is now active...".format(ip))
                    self.tracker.debug.log(
                        "[REMOTE] Receiving data from {} <{}>...".format(self.clients[ip].hostname, ip))
                self.clients[ip].last_active_time = datetime.now()
                # don't return yet - allow update other clients with same hostname

    def update_client_by_ip(self, ip):
        """
        Update client by IP

        :param ip: Client IP address
        """
        if ip in self.clients:
            self.clients[ip].hang_time = datetime.now()  # end hang time
            if self.clients[ip].last_active_time is None:
                self.tracker.debug.log("[REMOTE] Client <{}> is now active...".format(ip))
                self.tracker.debug.log(
                    "[REMOTE] Receiving data from {} <{}>...".format(self.clients[ip].hostname, ip))
            self.clients[ip].last_active_time = datetime.now()

    def unblock_ip(self, ip):
        """
        Unblock IP if was disconnected or removed from list

        :param ip: Client IP address
        """
        if ip in self.clients:
            self.clients[ip].disconnected = False
            self.clients[ip].removed = False

    def handle(self, ip):
        """
        Handle client on app loop

        :param ip: Client IP address
        :return: Captures dict
        """
        # try to connect, abort if not connected yet
        if ip is not None and not self.is_connected(ip):
            if not self.is_disconnected(ip) and not self.is_removed(ip):
                print("RECONNECTING")
                self.connect(ip)
            return {}  # return empty captures dict

        # update hang time (re-connects client if not responding
        if ip in self.clients:
            self.clients[ip].hang_time = datetime.now()  # begin hang time

            # set remote servo to current client
            if self.tracker.servo.remote != ip:
                self.toggle_servo(ip)

        # receive image from client
        if self.STREAM_JPEG:
            data, frame = self.imageHub.recv_jpg()
        else:
            data, frame = self.imageHub.recv_image()

        # send reply
        self.imageHub.send_reply(b'OK')

        # get hostname and timestamp
        data_parts = data.split('@')
        hostname = data_parts[0]
        timestamp = data_parts[1]
        ping = round(time.time() * 1000) - int(timestamp)
        if ping < 0:
            ping = 0
        self.ping_video = ping

        # store in client
        if ip in self.clients:
            self.clients[ip].ping_video = ping
            self.status = None

        # if JPEG compression
        if self.STREAM_JPEG:
            # decrypt
            if self.tracker.encrypt.enabled_video:
                frame = self.tracker.encrypt.decrypt(frame, True)
            frame = simplejpeg.decode_jpeg(frame, colorspace='BGR', fastdct=True, fastupsample=True)

        # update active time
        self.update_client_by_ip(ip)

        # reset state on list
        if ip in self.clients:
            self.clients[ip].state = None

        # add frame to data, if montage is enabled then add to montage frames, if not then add only host frame
        w, h = 0, 0
        if self.tracker.render.montage:
            for tmp_ip in self.clients:
                if self.clients[tmp_ip].hostname == hostname:
                    frame = imutils.resize(frame, width=self.montage_width)
                    (h, w) = frame.shape[:2]
                    cv2.putText(frame, hostname, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    self.data[tmp_ip] = frame
                    break
        else:
            if ip is not None and self.clients[ip].hostname == hostname:
                self.data[ip] = frame

        # build montage view
        if self.tracker.render.montage:
            self.tracker.render.montage_frames = build_montages(self.data.values(), (w, h),
                                                                (self.montage_columns, self.montage_rows))

        # check last active hosts
        if 0 < self.CLIENT_INACTIVE_TIME < (datetime.now() - self.last_active_check).seconds:
            for ip in self.clients:
                if self.clients[ip].last_active_time is not None and (
                        datetime.now() - self.clients[ip].last_active_time).seconds > self.CLIENT_INACTIVE_TIME:
                    self.tracker.debug.log("[REMOTE] Lost connection to {}".format(ip))
                    self.tracker.window.ui.dialogs.alert(trans('alert.remote.disconnected'))
                    self.clients[ip].state = self.STATE_TIMEOUT
                    self.status = self.STATE_DISCONNECTED
                    self.dispose(ip)
            self.last_active_check = datetime.now()

        return self.data

    def host2ip(self, hostname):
        """
        Get IP address from hostname

        :param hostname: Hostname
        :return: IP address
        """
        try:
            socket.inet_aton(hostname)
            return hostname  # already an IP
        except socket.error:
            ip = None

        if hostname is not None:
            try:
                ip = socket.gethostbyname(hostname)
            except socket.gaierror:
                return None
            if ip.startswith('127.') or hostname == 'localhost':
                ip = '127.0.0.1'
        return ip

    def load(self):
        """Load clients from hosts.txt"""
        # user
        f = self.tracker.storage.get_user_hosts_path()
        if not os.path.exists(f):
            # default
            f = self.tracker.storage.get_default_hosts_path()

        # abort if no file
        if not os.path.exists(f):
            return

        with open(f, 'r') as file:
            lines = file.readlines()
            self.tracker.debug.log("[REMOTE] Loaded {} host(s) from file: {}".format(len(lines), f))
            for line in lines:
                if line.startswith('#'):
                    continue
                if line.strip() == '':
                    continue
                line = ' '.join(line.strip().split())
                parts = line.split(' ')

                ip = None
                hostname = None
                name = None

                if len(parts) == 1:
                    ip = parts[0]
                    hostname = parts[0]
                    name = parts[0]
                elif len(parts) == 2:
                    ip = parts[0]
                    hostname = parts[1]
                    name = parts[1]
                elif len(parts) == 3:
                    ip = parts[0]
                    hostname = parts[1]
                    name = parts[2]

                self.tracker.remote.add_host(ip, hostname, name)
