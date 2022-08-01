from datetime import datetime, timedelta

def check_valid_time(iat: float) -> bool:
    timeA = datetime.fromtimestamp(iat)
    timeB = timeA + timedelta(days=3)

    now = datetime.now()
    return now > timeA and now < timeB