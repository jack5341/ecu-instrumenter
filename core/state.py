# -*- coding: utf-8 -*-
import json
import os

class AppSettings:
    def __init__(self, ip="127.0.0.1", port=35000, is_mph=False, is_fahrenheit=False, brightness=100, was_connected=False, demo_mode=False, oil_warn=130, coolant_warn=105, save_history=False):
        self.ip = ip
        self.port = port
        self.is_mph = is_mph
        self.is_fahrenheit = is_fahrenheit
        self.brightness = brightness
        self.was_connected = was_connected
        self.demo_mode = demo_mode
        self.oil_warn = oil_warn
        self.coolant_warn = coolant_warn
        self.save_history = save_history

    def to_dict(self):
        return {
            "ip": self.ip,
            "port": self.port,
            "is_mph": self.is_mph,
            "is_fahrenheit": self.is_fahrenheit,
            "brightness": self.brightness,
            "was_connected": self.was_connected,
            "demo_mode": self.demo_mode,
            "oil_warn": getattr(self, 'oil_warn', 130),
            "coolant_warn": getattr(self, 'coolant_warn', 105),
            "save_history": getattr(self, 'save_history', False)
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

    @property
    def demo_mode(self):
        return self.settings.demo_mode
        
    @demo_mode.setter
    def demo_mode(self, val):
        self.settings.demo_mode = val

    def save(self):
        try:
            with open("settings.json", "w") as f:
                json.dump(self.settings.to_dict(), f)
        except:
            pass
            
    def load(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    data = json.load(f)
                    self.settings = AppSettings(**data)
                    if self.settings.was_connected:
                        self.screen = AppScreen.DASHBOARD
            except:
                pass

global_state = GlobalState()
