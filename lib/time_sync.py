import ntptime
import time
import secrets

from lib.wifi_manager import WiFiManager

STD_OFFSET: int = 5 * 3600
DST_OFFSET: int = 4 * 3600
NTP_SERVER: str = "us.pool.ntp.org"


def nth_weekday(nth_year: int, nth_month: int, target_wday: int, n: int) -> int:
    # target_wday: Monday=0 … Sunday=6
    first_day_wday = time.mktime((nth_year, nth_month, 1, 0, 0, 0, 0, 0)) // 86400 % 7
    # days to the first occurrence of target_wday
    delta = (target_wday - first_day_wday) % 7
    day = 1 + delta + (n - 1) * 7
    return day


def is_dst(utc_tuple: tuple) -> bool:
    """Return True if the given UTC tuple falls within US DST period."""
    year, month, mday, hour, minute, second, weekday, yearday = utc_tuple

    # DST start: second Sunday in March at 02:00 UTC‑05 → 07:00 UTC
    dst_start_day: int = nth_weekday(year, 3, 6, 2)
    dst_start_ts: int = time.mktime((year, 3, dst_start_day, 7, 0, 0, 0, 0))

    # DST end: first Sunday in November at 02:00 UTC‑04 → 06:00 UTC
    dst_end_day: int = nth_weekday(year, 11, 6, 1)
    dst_end_ts: int = time.mktime((year, 11, dst_end_day, 6, 0, 0, 0, 0))

    now_ts = time.mktime(utc_tuple)
    return dst_start_ts <= now_ts < dst_end_ts


def sync_and_set_rtc() -> None:
    wifi = WiFiManager(ssid=secrets.SSID, password=secrets.PASSWORD)
    wifi.connect(10)
    try:
        ntptime.settime()
    except OSError as e:
        print("NTP sync failed:", e)
        return None
    return None


def utc_to_eastern(local_ts: int) -> int:
    offset = DST_OFFSET if is_dst(time.localtime(local_ts)) else STD_OFFSET
    return local_ts + (offset * -1)
