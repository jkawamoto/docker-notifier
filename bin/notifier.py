#!/usr/bin/env python
#
# notifier.py
#
# Copyright (c) 2014-2015 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
import argparse
import fnmatch
import json
import re
import sys
from docker import Docker
from pushover import Pushover

__APPLICATION__="docker-notifier"


class PushoverNotifier(object):

    def __init__(self, user, token):

        self._pushover = Pushover(user, token)

    def create(self, id, name=None):
        pass

    def die(self, id, name=None):
        if name:
            self._pushover.send("Container {0} exited.".format(name))


class StreamNotifier(object):

    def __init__(self, output):
        self._output = output
    
    def create(self, id, name=None):
        self._write(id, name, "create")

    def die(self, id, name=None):
        self._write(id, name, "die")

    def _write(self, id, name, status):

        data = {
            "posted-by": __APPLICATION__,
            "name": name,
            "id": id,
            "status": status
        }
        
        if name:
            data["name"] = name

        json.dump(data, self._output)
        self._output.write("\n")


def main(socket, filter, notifier, **kwargs):

    regex = None
    if filter:
        regex = fnmatch.translate(filter)

    docker = Docker(socket)
    push = notifier(**kwargs)
    names = {}
    
    for e in docker.events():
        
        if e["status"] == "create":
            
            id = e["id"]
            res = docker.inspect(id)
            name = res["Name"][1:]
            names[id] = name
            if not regex or regex.match(name):
                push.create(id, name)

        if e["status"] == "die":

            id = e["id"]
            name = names[id] if id in names else None
            if not regex or regex.match(name):
                push.die(id, name)
                if id in names:
                    del names[id]


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", default="/var/run/docker.sock", help="Unix socket file of docker.")
    parser.add_argument("--filter", help="Unix style pattern to filter containers.")

    subparsers = parser.add_subparsers()
    
    pushover_cmd = subparsers.add_parser("pushover", help="Notify events via Pushover.")
    pushover_cmd.add_argument("user", help="User key.")
    pushover_cmd.add_argument("token", help="Application key.")
    pushover_cmd.set_defaults(notifier=PushoverNotifier)

    stream_cmd = subparsers.add_parser("stream", help="Notify events via stdout/file.")
    stream_cmd.add_argument("--output", default=sys.stdout, type=argparse.FileType("w"))
    stream_cmd.set_defaults(notifier=StreamNotifier)

    try:
        main(**vars(parser.parse_args()))

    except KeyboardInterrupt:
        pass
