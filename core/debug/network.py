#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

class Network:
    def __init__(self, tracker=None):
        """
        Network debug window updater.

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.id = 'network'

    def update(self):
        """Updates the network debug window."""
        self.tracker.debug.begin(self.id)

        # remote clients
        for ip in self.tracker.remote.clients:
            prefix = '[' + str(ip) + '] '

            self.tracker.debug.add(self.id, prefix + 'ip', str(self.tracker.remote.clients[ip].ip))
            self.tracker.debug.add(self.id, prefix + 'hostname', str(self.tracker.remote.clients[ip].hostname))
            self.tracker.debug.add(self.id, prefix + 'name', str(self.tracker.remote.clients[ip].name))
            self.tracker.debug.add(self.id, prefix + 'state', str(self.tracker.remote.clients[ip].state))
            self.tracker.debug.add(self.id, prefix + 'ping_video', str(self.tracker.remote.clients[ip].ping_video))
            self.tracker.debug.add(self.id, prefix + 'ping_data', str(self.tracker.remote.clients[ip].ping_data))

            if self.tracker.remote.clients[ip].last_active_time is not None:
                self.tracker.debug.add(self.id, prefix + 'last_active_time',
                                       str(self.tracker.remote.clients[ip].last_active_time))
            else:
                self.tracker.debug.add(self.id, prefix + 'last_active_time', 'None')

            if self.tracker.remote.clients[ip].hang_time is not None:
                self.tracker.debug.add(self.id, prefix + 'hang_time', str(self.tracker.remote.clients[ip].hang_time))
            else:
                self.tracker.debug.add(self.id, prefix + 'hang_time', 'None')

            self.tracker.debug.add(self.id, prefix + 'disconnected',
                                   str(self.tracker.remote.clients[ip].disconnected))

            self.tracker.debug.add(self.id, prefix + 'removed',
                                   str(self.tracker.remote.clients[ip].removed))

        # remote streams
        for unique in self.tracker.stream.streams:
            prefix = '[' + str(unique) + '] '

            self.tracker.debug.add(self.id, prefix + 'unique_id', str(self.tracker.stream.streams[unique].unique_id))
            self.tracker.debug.add(self.id, prefix + 'addr', str(self.tracker.stream.streams[unique].addr))
            self.tracker.debug.add(self.id, prefix + 'host', str(self.tracker.stream.streams[unique].host))
            self.tracker.debug.add(self.id, prefix + 'port', str(self.tracker.stream.streams[unique].port))
            self.tracker.debug.add(self.id, prefix + 'protocol', str(self.tracker.stream.streams[unique].protocol))
            self.tracker.debug.add(self.id, prefix + 'password', str(self.tracker.stream.streams[unique].password))
            self.tracker.debug.add(self.id, prefix + 'query', str(self.tracker.stream.streams[unique].query))
            self.tracker.debug.add(self.id, prefix + 'name', str(self.tracker.stream.streams[unique].name))
            self.tracker.debug.add(self.id, prefix + 'ping_video', str(self.tracker.stream.streams[unique].ping_video))
            self.tracker.debug.add(self.id, prefix + 'ping_data', str(self.tracker.stream.streams[unique].ping_data))

            self.tracker.debug.add(self.id, prefix + 'disconnected',
                                   str(self.tracker.stream.streams[unique].disconnected))

            self.tracker.debug.add(self.id, prefix + 'removed',
                                   str(self.tracker.stream.streams[unique].removed))

        # captures
        for i in self.tracker.remote.data.keys():
            if self.tracker.remote.data[i] is not None:
                self.tracker.debug.add(self.id, 'remote.data[' + str(i) + ']', str(self.tracker.remote.data[i].shape))
            else:
                self.tracker.debug.add(self.id, 'remote.data[' + str(i) + ']', 'None')

        # montages
        i = 0
        for montage in self.tracker.render.montage_frames:
            if montage is not None:
                self.tracker.debug.add(self.id, 'render.montage_frames[' + str(i) + ']', str(montage.shape))
            else:
                self.tracker.debug.add(self.id, 'render.montage_frames[' + str(i) + ']', 'None')
            i += 1

        self.tracker.debug.add(self.id, 'remote.last_active_check', str(self.tracker.remote.last_active_check))
        self.tracker.debug.add(self.id, 'remote.send_conn_time', str(self.tracker.remote.send_conn_time))
        self.tracker.debug.add(self.id, 'remote.conn_timer', str(self.tracker.remote.conn_timer))
        self.tracker.debug.add(self.id, 'remote.active', str(self.tracker.remote.active))
        self.tracker.debug.add(self.id, 'remote.status', str(self.tracker.remote.status))
        self.tracker.debug.add(self.id, 'remote.is_connecting', str(self.tracker.remote.is_connecting))

        # ping
        self.tracker.debug.add(self.id, 'remote.ping_video', str(self.tracker.remote.ping_video))
        self.tracker.debug.add(self.id, 'remote.ping_data', str(self.tracker.remote.ping_data))
        self.tracker.debug.add(self.id, 'sockets.packets_wait', str(self.tracker.sockets.packets_wait))

        self.tracker.debug.end(self.id)
