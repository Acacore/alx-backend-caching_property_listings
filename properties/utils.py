from django.core.cache import cache
from .models import Property

def getallproperties(key):
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