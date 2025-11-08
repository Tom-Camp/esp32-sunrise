import network
import time


class WiFiManager:
    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        self.sta_if = network.WLAN(network.STA_IF)

    def connect(self, timeout: int = 10):
        # Toggle interface to prevent errors
        self.sta_if.active(False)
        time.sleep(0.5)
        self.sta_if.active(True)
        time.sleep(0.5)

        if not self.sta_if.isconnected():
            print("Connecting to network...")
            try:
                self.sta_if.connect(self.ssid, self.password)
            except OSError as e:
                print(f"Connection error: {e}")
                return False

            max_wait = timeout
            while max_wait > 0:
                if self.sta_if.isconnected():
                    print("Connected!")
                    print("Network config:", self.sta_if.ifconfig())
                    return True
                max_wait -= 1
                time.sleep(1)

            print("Connection timeout")
            return False

        return True

    def disconnect(self):
        if self.sta_if.isconnected():
            try:
                self.sta_if.disconnect()
                print("Disconnected from WiFi")
            except OSError as e:
                print(f"Disconnect error: {e}")
                return False

        self.sta_if.active(False)
        return True

    def is_connected(self):
        return self.sta_if.isconnected()

    def get_status(self):
        return self.sta_if.status()
