# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""PyFS Multi-checksum File Storage classes."""
from invenio_files_rest.errors import StorageError
from invenio_files_rest.helpers import compute_checksum
from invenio_files_rest.storage import PyFSFileStorage, pyfs_storage_factory

from pyfs_multisum_file_storage import current_multisum_storage

from functools import partial


class PyFSMultiChecksumFileStorage(PyFSFileStorage):
    """File system storage extending PyFSFileStorage with multiple checksum
    algorithms support. Checksums that are computed on the FileInstance are
    determined by the *MULTISUM_FILES_STORAGE_ALGOS* config option.
    """

    def _init_hash(self) -> list:
        """Initialize message digest object.
        Overwrite this method if you want to use different checksum
        algorithm for your storage backend."""
        return current_multisum_storage.checksum_algos()

    def _compute_checksum(self, stream, size=None, chunk_size=None,
                          progress_callback=None, **kwargs):
        """Get helper method to compute checksum from a stream.

        Naive implementation that can be overwritten by subclasses in order to
        provide more efficient implementation.
        """
        checksums = []
        for algo, m in self._init_hash():
            if progress_callback and size:
                progress_callback = partial(progress_callback, size)
            else:
                progress_callback = None

            try:
                checksums.append(compute_checksum(
                    stream, algo, m,
                    chunk_size=chunk_size,
                    progress_callback=progress_callback
                ))
            except Exception as e:
                raise StorageError(
                    'Could not compute checksum of file: {0}'.format(e))

        return ';'.join(checksums)


    def send_file(self, filename, mimetype=None, restricted=True,
                  checksum=None, trusted=False, chunk_size=None,
                  as_attachment=False):
        """Send the file to the client."""
        checksums = checksum.split(';')
        for sum in checksums:
            if sum.split(':')[0] == 'md5':
                checksum = sum

        if not checksum and len(checksums) > 0:
            checksum = checksums[0]

        return super(PyFSMultiChecksumFileStorage, self).send_file(filename, mimetype, restricted, checksum,
                                                            trusted, chunk_size, as_attachment)


def pyfs_multichecksum_storage_factory(fileinstance=None, default_location=None,
                                       default_storage_class=None,
                                       filestorage_class=PyFSMultiChecksumFileStorage, fileurl=None,
                                       size=None, modified=None, clean_dir=True):
    """Get factory function for creating a PyFS file storage instance."""
    return pyfs_storage_factory(fileinstance, default_location, default_storage_class,
                         filestorage_class, fileurl, size, modified, clean_dir)
