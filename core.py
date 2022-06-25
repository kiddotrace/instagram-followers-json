import requests
from loguru import logger


def validation_request(request):
    try:
        data = request.json()
    except requests.exceptions.JSONDecodeError:
        print('invalid session id')
        raise SystemExit

    return data['status']


class Scrapper:
    url = 'https://i.instagram.com/api/v1/'

    def __init__(self, user_id, headers, limit, username):
        self.username = username
        self.user_id = user_id
        self.headers = headers
        self.limit = limit
        self.data = {
            self.username: {}
        }

    def parse(self):
        max_id = ''
        request = requests.get(Scrapper.url + f'users/{self.user_id}/info/', headers=self.headers)
        request_status = validation_request(request)

        if request_status == 'ok':
            for _, value in self.data.items():
                logger.warning(f'Account initialized {self.username}')
                limit_condition = int(self.limit) - 1

                while len(value) <= limit_condition:
                    request = requests.get(Scrapper.url + f'friendships/{self.user_id}/followers/?count={self.limit}&max_id={max_id}', headers=self.headers)
                    data = request.json()
                    users = data['users']

                    for line in users:
                        if not (len(value) <= limit_condition):
                            break
                        value[str(len(value))] = {
                            'user_id': line['pk'],
                            'username:': line['username']
                        }

                    try:
                        max_id = data['next_max_id']
                    except KeyError:
                        logger.warning(f'{self.username} followers limit! Wrote {len(value)} notes')
                        break
                    logger.info(f'{self.username} status: [{len(value)} / {int(self.limit)}]')
                logger.success(f'{self.username} finished!')
        return self.data
