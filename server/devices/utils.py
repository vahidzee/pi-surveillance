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


def time_passed(time, granularity=2):
    timediff = datetime.datetime.utcnow().replace(tzinfo=utc) - time
    return display_time(timediff.total_seconds(), granularity=granularity)
