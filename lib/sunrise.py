import time
import neopixel

from lib.configuration import config
from lib.time_sync import utc_to_eastern

COLOR = config.get("color", (220, 238, 247))
DELAY = config.get("delay", 60)
BRIGHTNESS = 0.1


class Sunrise:

    def __init__(self, pixels: neopixel.NeoPixel):
        self.pixels = pixels

    @staticmethod
    def next_alarm() -> int:
        date_ts = utc_to_eastern(time.time())
        tomorrow_ts = date_ts + 86400
        date_local = time.localtime(date_ts)
        week = config.get("week", {})
        hour, minute = week[date_local[6]]
        wake_today = time.mktime((
            date_local[0], # year
            date_local[1], # month 1-12
            date_local[2], # day 1-31
            hour,          # hour 0-23
            minute,        # minute 0-59
            0,             # second 0-59
            date_local[6], # weekday 0-6
            date_local[7], # yearday 1-366
        ))
        if wake_today <= date_ts:
            tomorrow_local = time.localtime(tomorrow_ts)
            hour, minute = week[tomorrow_local[6]]
            wake_tomorrow = time.mktime((
                tomorrow_local[0],
                tomorrow_local[1],
                tomorrow_local[2],
                hour,
                minute,
                0,
                tomorrow_local[6],
                tomorrow_local[7],
            ))
            return wake_tomorrow - date_ts
        return wake_today - date_ts

    def sunrise(self):
        """
        Start the sun to risin'
        """
        self.pixels.brightness = BRIGHTNESS
        light_order = [
            11, 20, 12, 19, 2, 5, 26, 29, 3, 4, 10, 13, 18, 21, 27, 28,
            1, 6, 9, 14, 17, 22, 25, 30, 0, 7, 8, 15, 16, 23, 24, 31,
        ]
        for light in light_order:
            self.pixels[light] = (
                round(COLOR[0] * BRIGHTNESS),
                round(COLOR[1] * BRIGHTNESS),
                round(COLOR[2] * BRIGHTNESS),
            )
            try:
                self.pixels.write()
                time.sleep(DELAY)
            except ValueError:
                time.sleep(1)
        self.brighten()

    def brighten(self):
        """
        Increase brightness
        """
        for br in range(1, 8):
            brighter = br * BRIGHTNESS
            try:
                self.pixels.fill((
                    round(COLOR[0] * brighter),
                    round(COLOR[1] * brighter),
                    round(COLOR[2] * brighter),
                ))
                self.pixels.write()
                time.sleep(DELAY)
            except OSError as e:
                print(f"OSError: {e}")
        self.stop()

    def stop(self):
        """
        Set all to off
        """
        self.pixels.fill((0, 0, 0))
        self.pixels.write()
        time.sleep(0.05)
        self.pixels.write()

