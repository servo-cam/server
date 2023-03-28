#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


class Encrypt:
    def __init__(self, tracker=None):
        """
        Encryption handling main class

        :param tracker: tracker object
        """
        self.tracker = tracker
        self.enabled_video = False
        self.enabled_data = False
        self.raw_key = None
        self.KEY = None
        self.initialized = False

    def init_key(self):
        """Initialize the AES encryption key from the raw key"""
        if self.KEY is None and self.raw_key is not None:
            self.KEY = hashlib.sha256(self.raw_key.encode('utf8')).digest()
            self.raw_key = None

    def encrypt(self, raw, bytes=False):
        """
        Encrypt data with AES

        :param raw: data to encrypt (string or bytes)
        :param bytes: if True, encrypt bytes, if False, encrypt string
        :return: encrypted data
        """
        # init key
        if not self.initialized:
            self.init_key()
            self.initialized = True

        # str
        if not bytes:
            BS = AES.block_size
            pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
            raw = base64.b64encode(pad(raw).encode('utf8'))
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key=self.KEY, mode=AES.MODE_CFB, iv=iv)
            return base64.b64encode(iv + cipher.encrypt(raw))
        else:
            # bytes
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key=self.KEY, mode=AES.MODE_CFB, iv=iv)
            return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc, bytes=False):
        """
        Decrypt data with AES

        :param enc: encrypted data to decrypt (string or bytes)
        :param bytes: if True, decrypt from bytes, if False, decrypt from string
        :return: decrypted data
        """
        # init key
        if not self.initialized:
            self.init_key()
            self.initialized = True

        # str
        if not bytes:
            unpad = lambda s: s[:-ord(s[-1:])]
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.KEY, AES.MODE_CFB, iv)
            return unpad(base64.b64decode(cipher.decrypt(enc[AES.block_size:])).decode('utf8'))
        else:
            # bytes
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.KEY, AES.MODE_CFB, iv)
            return cipher.decrypt(enc[AES.block_size:])
