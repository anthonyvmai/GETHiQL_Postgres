""" TODO: find a better cache """
CACHE = {}

""" Set a cached value """
def set(key, val):
    CACHE[key] = val

""" Get a cached value """
def get(key):
    return CACHE.get(key, None)
