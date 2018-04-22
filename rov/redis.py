from config import config
from curio_redis.client import Client

redis_config = config.get('redis', {})


client = Client(**redis_config)


__all__ = ['client']
