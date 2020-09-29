import redis


def get_redis_connection(number):

    return redis.StrictRedis(
        host='127.0.0.1',
        port=6379,
        db=number
    )

