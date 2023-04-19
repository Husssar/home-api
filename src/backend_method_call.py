from datetime import datetime
import pytz
def date_now():
    sweden = pytz.timezone('Europe/Stockholm')
    now = datetime.now(sweden)


    return {
        "now": str(now),
        "now_date_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "now_date_time2": now.strftime("%Y-%m-%d %H:%M"),
        "now_time": now.strftime("%H:%M"),
        "now_time2": now.strftime("%H:%M:%S"),
        "now_date": now.strftime("%Y-%m-%d"),
        "now_date_text": now.strftime("%A %d %B"),
        "now_week": now.strftime("%W")
    }