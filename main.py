import json
import argparse
from core import Scrapper
from aparse import ValidateLimit
from utils import initialize_json
from joblib import Parallel, delayed
from loguru import logger

user_agent = "Mozilla/5.0 (Linux; Android 11; SM-N985F Build/RP1A.200720.012; wv) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Version/4.0 Chrome/100.0.4896.58 Mobile Safari/537.36 " \
             "Instagram 227.0.0.12.117 Android (30/11; 420dpi; " \
             "4000x4000 samsung; SM-N985F; c2s; exynos990 "


if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--sid', type=str, required=True)
    argp.add_argument('--uid', type=str, required=False)
    argp.add_argument('--limit', action=ValidateLimit, required=True)
    args = argp.parse_args()

    headers = {"Cookie": f"sessionid={args.sid}",
               "User-Agent": user_agent,
               }

    data = initialize_json()

    final = {}
    sessions = Parallel(n_jobs=10)(delayed(Scrapper)(user_id=v['user_id'], headers=headers, limit=args.limit, username=k) for k, v in data.items())
    for i in sessions:
        logger.debug(f'initialized core for {i.username}')

    result = Parallel(n_jobs=10)(delayed(s.parse)() for s in sessions)
    for data in result:
        final.update(data)
    with open(f'../autobot/followers_data.json', 'w') as file:
        json.dump(final, file)
