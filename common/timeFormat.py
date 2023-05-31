import time
from datetime import datetime


def timeFormat(timestamp):
    try:
        datetime.strptime(timestamp, "%Y-%m-%d")
        return timestamp
    except Exception as e:
        timestamp = int(timestamp) / 1000
        time_array = time.localtime(timestamp)
        result_date = time.strftime("%Y-%m-%d", time_array)
        return result_date


if __name__ == '__main__':
    g = timeFormat("1687190400000")
    f = timeFormat("2023-06-28")
    print(g)
    print(f)
