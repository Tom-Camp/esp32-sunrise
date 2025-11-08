# ESP32 Sunrise Alarm Clock

A sunrise alarm clock using the [Adafruit NeoPixel FeatherWing](https://www.adafruit.com/product/2945)
and an [Adafruit QT Py ESP32S2](https://www.adafruit.com/product/5325).

[Dawn simulation](https://en.wikipedia.org/wiki/Dawn_simulation)

```text
Dawn simulation is a technique that involves timing lights, often called wake 
up lights, sunrise alarm clock or natural light alarm clocks, in the bedroom to
come on gradually, over a period of 30 minutes to 2 hours, before awakening to
simulate dawn.
```

## Setup

Install [Micropython](https://micropython.org/download/ESP32_GENERIC_S2/) on the _QT Py_ and
then upload the files to the board. The easiest way to do this is to use 
[Thonny](https://thonny.org).

`lib/time_sync.py` updates the ESP RTC clock to UTC, and contains a functions to calculate 
Daylight Savings and Eastern timezone. Adjust the _STD_OFFSET_ and _DST_OFFSET_ to your timezone.
The `eastern_to_utc` function will calculate using the offsets.

Connect GPIO 18 on the QT Py ESP32S2 to the data pin on the FeatherWing.

Set the times to wake in the `lib/configuration.py` file. You can set one time for each day
of the week using 24 hour time in hour and minute pairs, for example 0630 as (6, 30).

The alarm will start by lighting 2 LEDs and after a delay lighting more until all the
LEDs are lit. You can set the color and the delay in the configuration file.

```python
# Week days start with Monday and end with Sunday
config = {
    "week": [(6, 0), (6, 0), (6, 0), (6, 0), (6, 0), (6, 30), (6, 30)],
    "color": (51, 153, 255),
    "delay": 60
}
```

The `secrets.py` file contains the wifi credentials and should be formatted like a .env file.
Replace _YOUR_NETWORK_SSID_ and _YOUR_NETWORK_PASSWORD_ with your network values.

```dotenv
SSID="YOUR_NETWORK_SSID"
PASSWORD="YOUR_NETWORK_PASSWORD"
```

## Authors

[Tom Camp](https://github.com/Tom-Camp)

## Version

- 0.1
  - Initial release


## License

[Affero GPL](LICENSE)
