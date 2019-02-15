# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""PyFS Multi-checksum File Storage classes."""
from invenio_files_rest.storage import PyFSFileStorage, pyfs_storage_factory


class PyFSMultiChecksumFileStorage(PyFSFileStorage):
    """File system storage extending PyFSFileStorage with multiple checksum algorithms support.
    """

    def send_file(self, filename, mimetype=None, restricted=True,
                  checksum=None, trusted=False, chunk_size=None,
                  as_attachment=False):
        """Send the file to the client."""
        checksums = checksum.split(';')
        for sum in checksums:
            if sum.split(':')[0] == 'md5':
                checksum = sum
                break
        else:
            checksum = None

        return super(PyFSMultiChecksumFileStorage, self).send_file(filename, mimetype, restricted, checksum,
                                                                   trusted, chunk_size, as_attachment)


def pyfs_multichecksum_storage_factory(fileinstance=None, default_location=None,
                                       default_storage_class=None,
                                       filestorage_class=PyFSMultiChecksumFileStorage, fileurl=None,
                                       size=None, modified=None, clean_dir=True):
    """Get factory function for creating a PyFS file storage instance."""
    return pyfs_storage_factory(fileinstance, default_location, default_storage_class,
                         filestorage_class, fileurl, size, modified, clean_dir)
