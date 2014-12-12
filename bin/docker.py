#
# docker.py
#
# Copyright (c) 2014 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
import contextlib
import json
import requests
from adapter import SocketAdapter

BASE="http://127.0.0.1"
MONITORING="/events?since={0}"
LIST_CONTAINERS="/containers/json?"
INSPECT="/containers/{id}/json"


class Docker(object):

    def __init__(self, path):
        
        self._path = path

    def events(self):
    
        with contextlib.closing(self._new_session()) as session:
            res = session.get(BASE+"/events", stream=True)
            raw = res.raw
        
            buf = []
            while True:
                c = raw.read(1)
                if c == "":
                    break
            
                buf.append(c)
                if c == "}":
                    yield json.loads("".join(buf))
                    buf = []

    def list(self, all=None, since=None, before=None):
        # GET /containers/json?all=1&before=8dfafdbc3a40&size=1 HTTP/1.1
        query = []
        if all:
            query.append("all=true")
        if since:
            query.append("since=" + since)
        if before:
            query.append("before=" + since)
        
        with contextlib.closing(self._new_session()) as session:
            res = session.get(BASE+LIST_CONTAINERS + "&".join(query))
            return res.json()

    def inspect(self, id):
        
        with contextlib.closing(self._new_session()) as session:
            res = session.get(BASE+INSPECT.format(id=id))
            return res.json()
            
    def _new_session(self):

        s = requests.Session()
        s.mount('http://', SocketAdapter(self._path))
        return s
