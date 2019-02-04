# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""PyFS File Storage supporting multiple checksum algos"""

from __future__ import absolute_import, print_function

from .ext import PyFSMultisumFileStorage
from .version import __version__
from .storage import PyFSMultiChecksumFileStorage, pyfs_multichecksum_storage_factory
from .proxies import current_multisum_storage

__all__ = ('__version__', 'PyFSMultisumFileStorage', 'current_multisum_storage',
           'pyfs_multichecksum_storage_factory' ,'PyFSMultiChecksumFileStorage')
