import os

import redis

if os.environ.get('ENABLE_REDIS'):
    redis_db = redis.Redis(
        host=os.environ.get('REDIS_HOST'),
        username='default',
        password=os.environ.get('REDIS_PASSWORD')
    )
