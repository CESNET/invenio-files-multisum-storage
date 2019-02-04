# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# PyFS Multi-checksum File Storage is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""PyFS Multi-checksum File Storage classes."""
from invenio_files_rest.errors import StorageError
from invenio_files_rest.helpers import compute_checksum, chunk_size_or_default
from invenio_files_rest.storage import PyFSFileStorage, pyfs_storage_factory
from invenio_files_rest.storage.base import check_sizelimit, check_size

from .proxies import current_multisum_storage

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
        return current_multisum_storage.checksum_algos

    def _compute_checksum(self, stream, size=None, chunk_size=None,
                          progress_callback=None, **kwargs):
        """Get helper method to compute checksum from a stream.

        Naive implementation that can be overwritten by subclasses in order to
        provide more efficient implementation.
        """
        checksums = []

        if progress_callback and size:
            progress_callback = partial(progress_callback, size)
        else:
            progress_callback = None

        try:
            for algo, m in self._init_hash():
                checksums.append(compute_checksum(
                    stream, algo, m,
                    chunk_size=chunk_size,
                    progress_callback=progress_callback
                ))
        except Exception as e:
            raise StorageError(
                'Could not compute checksum of file: {0}'.format(e))

        print(';'.join(checksums))

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

    def _write_stream(self, src, dst, size=None, size_limit=None, chunk_size=None, progress_callback=None):
        """Get helper to save stream from src to dest + compute checksum.
        :param src: Source stream.
        :param dst: Destination stream.
        :param size: If provided, this exact amount of bytes will be
            written to the destination file.
        :param size_limit: ``FileSizeLimit`` instance to limit number of bytes
            to write.
        """
        chunk_size = chunk_size_or_default(chunk_size)

        algos = self._init_hash()
        bytes_written = 0

        while 1:
            # Check that size limits aren't bypassed
            check_sizelimit(size_limit, bytes_written, size)
            chunk = src.read(chunk_size)

            if not chunk:
                if progress_callback:
                    progress_callback(bytes_written, bytes_written)
                break

            dst.write(chunk)

            bytes_written += len(chunk)

            for algo, m in algos:
                if m:
                    m.update(chunk)

            if progress_callback:
                progress_callback(None, bytes_written)

        checksums = ';'.join(['{0}:{1}'.format(algo, m.hexdigest()) for algo, m in algos])
        check_size(bytes_written, size)

        return bytes_written, checksums


def pyfs_multichecksum_storage_factory(fileinstance=None, default_location=None,
                                       default_storage_class=None,
                                       filestorage_class=PyFSMultiChecksumFileStorage, fileurl=None,
                                       size=None, modified=None, clean_dir=True):
    """Get factory function for creating a PyFS file storage instance."""
    return pyfs_storage_factory(fileinstance, default_location, default_storage_class,
                         filestorage_class, fileurl, size, modified, clean_dir)
