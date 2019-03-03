import os
import time
from datetime import datetime
import re
import requests
import json

class SlackPosts2JSON(object):

    """docstring for SlackPosts2JSON."""

    def __init__(self, **kwarg):
        super(SlackPosts2JSON, self).__init__()
        self.channel_id = kwarg['channel_id']
        self.token = kwarg['token']
        self.url = "https://slack.com/api/channels.history"
        self.URLreg = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'

    def __history_fetch(self, chanlel_id, token):
        payload = {
            "channel": chanlel_id,
            "token": token
        }
        response = requests.get(self.url, params=payload)
        json_data = response.json()
        messages = json_data['messages']
        posts = {
            str(datetime.fromtimestamp(float(msg['ts']))): [msg['user'], msg['text']]
            if (('attachments' in msg) or ('client_msg_id' in msg)) else None for msg in messages
        }
        links = {}
        for key, value in posts.items():
            if value != None and re.search(self.URLreg, value[1]):
                links[key] = [value[0],re.findall(self.URLreg, value[1])]

        return links

    def json_dump(self):
        links = self.__history_fetch(self.channel_id, self.token)
        try:
            if not os.path.isdir('result'):
                os.makedirs('result')
        except FileExistsError:
            pass
        with open('result/link.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(links))
