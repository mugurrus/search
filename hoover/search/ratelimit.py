from django.conf import settings

if settings.HOOVER_RATELIMIT_USER:
    from django.http import HttpResponse
    from hoover.contrib.ratelimit import signals, models
    from hoover.contrib.ratelimit.limit import RateLimit

    class HttpLimitExceeded(HttpResponse):

        def __init__(self):
            super().__init__(
                "Rate limit exceeded\n", 'text/plain',
                429, 'Too Many Requests',
            )

    (_l, _i) = settings.HOOVER_RATELIMIT_USER
    _user_limit = RateLimit(_l, _i)

    def limit_user(view):
        def wrapper(request, *args, **kwargs):
            key = 'user:' + request.user.get_username()
            if _user_limit.access(key):
                signals.rate_limit_exceeded.send(
                    models.Count,
                    request=request,
                )
                return HttpLimitExceeded()
            return view(request, *args, **kwargs)
        return wrapper

else:
    def limit_user(view):
        return view
