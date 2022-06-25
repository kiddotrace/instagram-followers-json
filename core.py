import json
import requests
from utils import initialize_json

class Scrapper:
    next_max_id = ''

    def __init__(self, user_id, headers, limit, username):
        self.username = username
        self.user_id = user_id
        self.headers = headers
        self.limit = limit

    def solution(self):
        result = {
            self.username: {}
        }
        next_max_id = ''
        validation_request = requests.get(f'https://i.instagram.com/api/v1/users/{self.user_id}/info/',  headers=self.headers)

        try:
            validation_request = validation_request.json()
        except requests.exceptions.JSONDecodeError:
            print('Invalid ssid')
            raise SystemExit

        if validation_request['status'] == 'ok':
            for k, v in result.items():
                while len(v) <= int(self.limit):
                    request = requests.get(f'https://i.instagram.com/api/v1/friendships/{self.user_id}/followers/?count={self.limit}&max_id={next_max_id}',headers=self.headers, )
                    jrequest = request.json()
                    for line in jrequest['users']:
                        v[f'{len(v)}'] = {'user_id': line['pk'], 'username:': line['username']}
                    try:
                        next_max_id = jrequest['next_max_id']
                    except KeyError:
                        pass
                    print(len(v))

        return result
