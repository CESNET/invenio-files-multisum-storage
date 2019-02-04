# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""
import hashlib

MULTISUM_FILES_STORAGE_ALGOS = [
    ('md5', hashlib.md5()),
    ('sha1', hashlib.sha1())
]
