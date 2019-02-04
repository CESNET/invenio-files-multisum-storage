# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Flask extension for PyFS Multi-checksum File Storage."""

from __future__ import absolute_import, print_function

from invenio_files_rest.utils import load_or_import_from_config
from werkzeug.utils import cached_property

from . import config


class _PyFSMultisumState(object):
    """PyFS Multi-checksum File Storage State."""

    def __init__(self, app):
        """Initialize state."""
        self.app = app

    @cached_property
    def checksum_algos(self):
        """Load configured storage checksum algorithms."""
        return load_or_import_from_config(
            'MULTISUM_FILES_STORAGE_ALGOS', app=self.app
        )


class PyFSMultisumFileStorage(object):
    """PyFS Multi-checksum File Storage extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['pyfs-multisum-file-storage'] = _PyFSMultisumState(app)

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('MULTISUM_FILES_STORAGE_'):
                app.config.setdefault(k, getattr(config, k))
