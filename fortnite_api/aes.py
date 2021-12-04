"""
MIT License

Copyright (c) 2019 Lucas Hardt

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import re
from datetime import datetime


class AES:
    """Represents a AES Code.

    Attributes
    -----------
    main_key: :class:`str`
        The main encryption key.
    build: :class:`str`
        The current build where the AES key refers to.
    version: :class:`str`
        The current version where the AES key refers to.
    updated: :class:`datetime.datetime`
        The date where the AES was updates.
    dynamic_keys: :class:`datetime.datetime`
        All current dynamic keys
    raw_data: :class:`dict`
        The raw data from request. Can be used for saving and re-creating the class.
    """

    def __init__(self, data):
        self.main_key = data.get('mainKey')
        self.build = data.get('build')
        self.version = re.search(r'\d\d.\d\d', self.build)[0] if self.build else None
        try:
            self.updated = datetime.strptime(data.get('updated'), '%Y-%m-%dT%H:%M:%S%z')
        except (ValueError, TypeError):
            self.updated = None

        self.dynamic_keys = []
        for key_data in data.get('dynamicKeys', []) if data.get('dynamicKeys') else []:
            self.dynamic_keys.append(DynamicKey(key_data))
        self.raw_data = data

    def __str__(self):
        return self.main_key


class DynamicKey:

    def __init__(self, data):
        self.pak_filename = data.get('pakFilename')
        self.pak_guid = data.get('pakGuid')
        self.key = data.get('key')
