#
# pushover.py
#
# Copyright (c) 2014 Junpei Kawamoto
#
# This software is released under the MIT License.
#
# http://opensource.org/licenses/mit-license.php
#
import requests

URL="https://api.pushover.net/1/messages.json"

class Pushover(object):

    def __init__(self, user, token):

        self._user = user
        self._token = token

    def send(self, message, device=None, title=None):

        query = {
            "message": message,
            "token": self._token,
            "user": self._user
        }

        if device:
            query["device"] = device
        if title:
            query["title"] = title
    
        return requests.post(URL, data=query).json()



