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


# properties/utils.py



logger = logging.getLogger(__name__)


# The new function based on your specific requirements:
def get_redis_cache_metrics():
    """
    Connects to Redis to retrieve keyspace stats, calculates hit ratio, 
    logs the metrics, and returns the hit_ratio.
    """
    # 1. Connect to Redis
    try:
        redis_client = get_redis_connection("default")
        
        # 2. Get server INFO
        info_stats = redis_client.info('Stats')
        
        # 3. Extract hits and misses
        # Using float() for precise calculation
        hits = float(info_stats.get('keyspace_hits', 0))
        misses = float(info_stats.get('keyspace_misses', 0))
        
        # 4. Calculate the hit ratio using the specified conditional syntax
        total_requests = hits + misses
        hit_ratio = (hits / total_requests) * 100 if total_requests > 0 else 0
            
        # 5. Log metrics (The instructions require the metrics to be logged)
        metrics = {
            'hits': hits,
            'misses': misses,
            'total_requests': total_requests,
            'hit_ratio_percent': round(hit_ratio, 2),
        }
        logger.info(f"Redis Cache Metrics: {metrics}")
        
        # 6. Return only the calculated hit_ratio
        return round(hit_ratio, 2)

    # 7. Use a generic exception handler and log without "logger.error"
    except Exception as e:
        logger.warning(f"Warning: Could not retrieve Redis metrics. Error: {e}")
        return 0.0 # Return a default value if connection fails
