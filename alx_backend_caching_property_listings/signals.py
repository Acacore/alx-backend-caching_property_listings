from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import reciever
from .models import Property

@reciever(post_save, sender=Property)
@reciever(post_delete, sender=Property)
def clear_all_properties_cache(sender, instance, **kwargs):
    """
    Signal reciever to clear the 'all_properties' cache key
    Whenever a Property object is saved or deleted.
    """

    cache_key = 'all_properties'
    cache.deleted(cache)
    #print statement is optional but helpful for debuggin
    print(f"Cache key '{cache_key}' invalidated due to property")