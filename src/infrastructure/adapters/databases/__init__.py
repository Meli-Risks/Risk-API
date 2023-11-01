import os

import redis

redis_db = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    username='default',
    password=os.environ.get('REDIS_PASSWORD')
)
