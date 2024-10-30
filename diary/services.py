def get_cache_key_from_request(request) -> str:
    cache_key = request.user.email + "_"
    if 'page' in request.GET:
        cache_key += request.GET['page'] + "_"
    return cache_key
