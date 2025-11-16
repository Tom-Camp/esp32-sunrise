import machine
import neopixel

import secrets
from lib.sunrise import Sunrise
from lib.time_sync import sync_and_set_rtc, next_alarm
from lib.wifi_manager import WiFiManager

wifi = WiFiManager(ssid=secrets.SSID, password=secrets.PASSWORD)

sync_and_set_rtc()

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    light_pin = machine.Pin(18)
    sunrise = Sunrise(pixels=neopixel.NeoPixel(light_pin, 32))
    try:
        sunrise.sunrise()
    except KeyboardInterrupt:
        sunrise.stop()

sleep_time = next_alarm()
machine.deepsleep(sleep_time * 1000)
