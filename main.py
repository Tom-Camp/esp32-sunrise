import neopixel

from machine import deepsleep, Pin, RTC

import secrets
from lib.sunrise import Sunrise
from lib.time_sync import sync_and_set_rtc
from lib.wifi_manager import WiFiManager


sunrise = Sunrise(pixels=neopixel.NeoPixel(Pin(18), 32))

wifi = WiFiManager(ssid=secrets.SSID, password=secrets.PASSWORD)

sync_and_set_rtc()
rtc = RTC()

if is_set := rtc.memory():
    try:
        sunrise.sunrise()
    except KeyboardInterrupt:
        rtc.memory(b"")
        sunrise.stop()

sleep_time = sunrise.next_alarm()
rtc.memory(b"\x01")

deepsleep(sleep_time)
