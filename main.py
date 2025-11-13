import machine
import neopixel

import secrets
from lib.sunrise import Sunrise
from lib.time_sync import sync_and_set_rtc
from lib.wifi_manager import WiFiManager


sunrise = Sunrise(pixels=neopixel.NeoPixel(machine.Pin(18), 32))

wifi = WiFiManager(ssid=secrets.SSID, password=secrets.PASSWORD)

sync_and_set_rtc()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    try:
        sunrise.sunrise()
    except KeyboardInterrupt:
        sunrise.stop()

sleep_time = sunrise.next_alarm()

machine.deepsleep(sleep_time * 1000)
