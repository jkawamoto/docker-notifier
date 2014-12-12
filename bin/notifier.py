#!/usr/bin/env python
#
# notifier.py
#
# Copyright (c) 2014 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
import argparse
import re
from docker import Docker
from pushover import Pushover


def main(user, token, socket, filter, **kwags):

    regex = None
    if filter:
        regex = re.compile(filter)

    docker = Docker(socket)
    push = Pushover(user, token)
    names = {}
    
    for e in docker.events():
        
        if e["status"] == "create":
            
            res = docker.inspect(e["id"])
            names[e["id"]] = res["Name"][1:]

        if e["status"] == "die":

            if e["id"] in names:
                
                name = names[e["id"]] 
                if not regex or regex.match(name):

                    push.send("Container {0} exited.".format(name))
                    del names[e["id"]]


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("user", help="User key.")
    parser.add_argument("token", help="Application key.")
    parser.add_argument("--socket", default="/var/run/docker.sock", help="Unix socket file of docker.")
    parser.add_argument("--filter", help="Regular expression to filter containers.")

    try:

        main(**vars(parser.parse_args()))

    except KeyboardInterrupt:

        pass
