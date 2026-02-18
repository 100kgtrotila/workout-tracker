from cashews import cache

from app.core.config import settings

cache.setup(str(settings.REDIS_URL))