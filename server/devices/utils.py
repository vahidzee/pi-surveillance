from django.utils.timezone import utc
import datetime

TIME_INTERVALS = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),  # 60 * 60 * 24
    ('h', 3600),  # 60 * 60
    ('m', 60),
    ('s', 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in TIME_INTERVALS:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{:d}{}".format(int(value), name))
    return ', '.join(result[:granularity])


def time_passed(time, granularity=2, return_unformated=False):
    timediff = datetime.datetime.utcnow().replace(tzinfo=utc) - time
    if return_unformated:
        return timediff.total_seconds()
    return display_time(timediff.total_seconds(), granularity=granularity)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def base_response(response=None, ok=True, message=''):
    """creates base response model of form {ok, description, [response]}"""
    res = dict(ok=ok, message=message)
    if response is not None:
        res['response'] = response
    return res
