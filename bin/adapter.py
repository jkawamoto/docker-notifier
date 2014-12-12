#
# adapter.py
#
# Copyright (c) 2014 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
import socket
from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import PoolManager, HTTPConnectionPool
from httplib import HTTPConnection


class SocketAdapter(HTTPAdapter):

    def __init__(self, sockfile, **kwargs):
        self._sockfile = sockfile
        super(SocketAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, **kwargs):

        self.poolmanager = SocketPoolManager(self._sockfile, num_pools=connections, maxsize=maxsize)


class SocketPoolManager(PoolManager):

    def __init__(self, sockfile, **kwargs):
        self._sockfile = sockfile
        super(SocketPoolManager, self).__init__(**kwargs)

    def _new_pool(self, scheme, host, port):

        return SocketConnectionPool(self._sockfile, host, port, **self.connection_pool_kw)


class SocketConnectionPool(HTTPConnectionPool):

    def __init__(self, sockfile, host, port, **kwargs):
        self._sockfile = sockfile
        super(SocketConnectionPool, self).__init__(host, port, **kwargs)

    def _new_conn(self):

        self.num_connections += 1
        return SocketConnection(self._sockfile, host=self.host, port=self.port, strict=self.strict)
    
    
class SocketConnection(HTTPConnection):

    def __init__(self, sockfile, **kwargs):
        self._sockfile = sockfile
        HTTPConnection.__init__(self, **kwargs)

    def connect(self):

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self._sockfile)

        if self._tunnel_host:
            self._tunnel()

