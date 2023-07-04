import time
import redis
import json
import pytz
from datetime import datetime

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def read_sensor_weight():
    # TODO connect to FSR reading
    return 20


def is_within_off_limit_hours():
    current_datetime = datetime.now().replace(tzinfo=pytz.utc)
    time_ranges = r.lrange("off_limit_hours", 0, -1)

    for time_range in time_ranges:
        time_range = json.loads(time_range)

        start = time_range["start"].replace("Z", "+00:00")
        start_time = datetime.fromisoformat(start).replace(tzinfo=pytz.utc)

        end = time_range["end"].replace("Z", "+00:00")
        end_time = datetime.fromisoformat(end).replace(tzinfo=pytz.utc)

        if start_time <= current_datetime <= end_time:
            return True

    return False


def trigger_alarm():
    # TODO connect to Piezo buzzer
    print("ALARM TRIGGERED")


while True:
    if is_within_off_limit_hours() and read_sensor_weight() > 0:
        trigger_alarm()

    time.sleep(5)
