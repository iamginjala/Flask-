import redis

redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)

def save_url(short_url, long_url):
    redis_client.set(short_url, long_url)

def get_url(short_url):
    return redis_client.get(short_url)
