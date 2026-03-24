import json
import os

class AppSettings:
    def __init__(self, ip="192.168.0.10", port=35000, is_mph=False, is_fahrenheit=False, brightness=100, was_connected=False):
        self.ip = ip
        self.port = port
        self.is_mph = is_mph
        self.is_fahrenheit = is_fahrenheit
        self.brightness = brightness
        self.was_connected = was_connected

    def to_dict(self):
        return {
            "ip": self.ip,
            "port": self.port,
            "is_mph": self.is_mph,
            "is_fahrenheit": self.is_fahrenheit,
            "brightness": self.brightness,
            "was_connected": self.was_connected
        }

class AppScreen:
    CONNECTION = "connection"
    DASHBOARD = "dashboard"
    LOG = "log"
    SETTINGS = "settings"

class GlobalState:
    def __init__(self):
        self.screen = AppScreen.CONNECTION
        self.settings = AppSettings()
        from models.telemetry import TelemetryFrame
        self.telemetry = TelemetryFrame()
        self.connection_status = "disconnected" 
        self.demo_mode = False

    def save(self):
        try:
            with open("config.json", "w") as f:
                json.dump(self.settings.to_dict(), f)
        except:
            pass
            
    def load(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    self.settings = AppSettings(**data)
                    if self.settings.was_connected:
                        self.screen = AppScreen.DASHBOARD
            except:
                pass

global_state = GlobalState()
