from math import floor


def to_five_minutes(timestamp):
    return floor(float(timestamp) / 300) * 300