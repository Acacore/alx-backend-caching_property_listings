from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging


def getallproperties():
    '''
    Retrieves all property object fro the cache or the database,
    and caches them in 1 hour.
    '''

    CACHE_KEY = 'all_properties'

    #check Redis for the caced data
    properties_queryset = cache.get.get(CACHE_KEY)


    # If the data is not found in the cache (it is None)
    if properties_queryset  is None:
        # Fetch data from the database 
        properties_queryset = Property.objects.all()

        TIMEOUT_SECONDS = 3600      
        cache.set(CACHE_KEY, properties_queryset, TIMEOUT_SECONDS)  # Cache for 1 hour
    
        print(f"Data for '{CACHE_KEY}' fetched form DB and stored in cached.")
    
    else:
        print(f"Data '{CACHE_KEY}' fetched form")
    
    return properties_queryset



logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Connects to Redis directly to retrieve global cache hit/miss metrics 
    and calculates the hit ratio.
    """
    # 1. Get the raw Redis client connection managed by django_redis
    # 'default' refers to the CACHES['default'] setting in settings.py
    try:
        connection = get_redis_connection("default")
    except ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return None

    # 2. Get the INFO statistics from the Redis server
    # The 'INFO stats' command retrieves general statistics
    info = connection.info(section='stats')

    # Extract the relevant metrics
    keyspace_hits = info.get('keyspace_hits', 0)
    keyspace_misses = info.get('keyspace_misses', 0)

    # 3. Calculate the hit ratio
    total_requests = keyspace_hits + keyspace_misses
    if total_requests > 0:
        hit_ratio = (keyspace_hits / total_requests) * 100
    else:
        hit_ratio = 0.0

    # 4. Log the metrics
    logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, Total={total_requests}, Ratio={hit_ratio:.2f}%")

    # 5. Return a dictionary
    metrics = {
        'hits': keyspace_hits,
        'misses': keyspace_misses,
        'total_requests': total_requests,
        'hit_ratio_percent': round(hit_ratio, 2),
    }

    return metrics

