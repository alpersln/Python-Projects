from datetime import datetime

TIME_STAMP_PATTERN = '%m/%d/%Y, %H:%M:%S'


def is_more_than_one_hour(time):
    datetime_obj = datetime.strptime(time, TIME_STAMP_PATTERN)
    now = datetime.now()
    calculated_time = now - datetime_obj

    return bool(calculated_time.seconds // 3600)
