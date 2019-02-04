# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxies for PyFS Multi-checksum File Storage."""

from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy

current_multisum_storage = LocalProxy(
    lambda: current_app.extensions['pyfs-multisum-file-storage'])
"""Helper proxy to access multisum files storage state object."""
