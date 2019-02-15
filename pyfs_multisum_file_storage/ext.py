# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for PyFS Multi-checksum File Storage."""

from __future__ import absolute_import, print_function


class PyFSMultisumFileStorage(object):
    """PyFS Multi-checksum File Storage extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
