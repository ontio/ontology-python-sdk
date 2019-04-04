"""
Copyright (C) 2018 The ontology Authors
This file is part of The ontology library.

The ontology is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The ontology is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with The ontology.  If not, see <http://www.gnu.org/licenses/>.
"""

from io import BytesIO
from binascii import hexlify

__mstreams__ = []
__mstreams_available__ = []


class StreamManager:

    @staticmethod
    def TotalBuffers():
        """
        Get the total number of buffers stored in the StreamManager.

        Returns:
            int:
        """
        return len(__mstreams__)

    @staticmethod
    def get_stream(data=None):
        """
        Get a MemoryStream instance.

        Args:
            data (bytes, bytearray, BytesIO): (Optional) data to create the stream from.

        Returns:
            MemoryStream: instance.
        """
        if len(__mstreams_available__) == 0:
            if data:
                mstream = MemoryStream(data)
                mstream.seek(0)
            else:
                mstream = MemoryStream()
            __mstreams__.append(mstream)
            return mstream

        mstream = __mstreams_available__.pop()

        if data is not None and len(data):
            mstream.clean_up()
            mstream.write(data)

        mstream.seek(0)

        return mstream

    @staticmethod
    def release_stream(mstream):
        """
        Release the memory stream
        Args:
            mstream (MemoryStream): instance.
        """
        mstream.clean_up()
        __mstreams_available__.append(mstream)


class MemoryStream(BytesIO):
    """
    Description:
        MemoryStream

    Usage:
    from ontology.io.memory_stream import MemoryStream
    """

    def __init__(self, *args, **kwargs):
        """
        Create an instance.

        Args:
            *args:
            **kwargs:
        """
        super().__init__(*args, **kwargs)

    def readable(self):
        """
        Get readable status.

        Returns:
            bool: True if the stream can be read from. False otherwise.
        """
        return self.readable()

    def seekable(self):
        """
        Get random access support status.

        Returns:
            bool: True if random access is supported. False otherwise.
        """
        return self.seekable

    def writable(self):
        """
        Get writeable status.

        Returns:
            bool: True if the stream is writeable. False otherwise.
        """
        return self.writable()

    def to_bytes(self) -> bytes:
        return self.getvalue()

    def hexlify(self) -> bytes:
        """
        Hexlify the stream data.

        Returns:
            bytes: b"" object containing the data.
        """
        data = self.to_bytes()
        return hexlify(data)

    def clean_up(self):
        """
        clean_up the stream by truncating it to size 0.
        """
        self.seek(0)
        self.truncate(0)
