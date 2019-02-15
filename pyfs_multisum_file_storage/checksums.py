# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Checksum algorithms."""
from collections import OrderedDict
from invenio_files_rest.proxies import current_files_rest


class MultiHash(object):
    """ Class for computing/verifying multiple hash algorithms """

    algos = OrderedDict()

    def __init__(self, algos: list):
        """ Initialize class with supported algos """
        for algo in algos:
            try:
                self.algos[algo] = current_files_rest.supported_checksums[algo]
            except KeyError:
                raise AttributeError('Unsupported checksum algo {}'.format(algo))

    def __call__(self, *args, **kwargs):
        """ Initialize individual algos and return self as message digest """
        for algo, m in self.algos.items():
            self.algos[algo] = m()

        return self

    def update(self, chunk):
        """ Update algos digests with chunk """
        for digest in self.algos.values():
            digest.update(chunk)

    def hexdigest(self):
        """ Return hexdigest of all algo digests combined """
        return ';'.join([d.hexdigest() for d in self.algos.values()])
