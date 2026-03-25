# -*- coding: utf-8 -*-
class DisplaySettings:
    def __init__(self):
        self.width = 640
        self.height = 480
        self.fps = 30
        self.pad = 10

class ThemeSettings:
    def __init__(self):
        self.bg = (10, 10, 10)
        self.panel = (28, 28, 28)
        self.border = (45, 45, 45)
        self.white = (245, 245, 245)
        self.dim = (160, 160, 160)
        self.cyan = (0, 210, 255)
        self.green = (25, 180, 25)
        self.orange = (255, 100, 30)
        self.red = (255, 55, 55)
        self.yellow = (255, 220, 0)
        self.purple = (100, 80, 255)

class ThresholdSettings:
    def __init__(self):
        self.rpm_warn = 5000
        self.rpm_danger = 6500
        self.coolant_danger = 105

class AFRSettings:
    def __init__(self):
        self.min_value = 10.0
        self.max_value = 20.0
        self.zones = (
            (10.0, 12.5, (180, 40, 40)),
            (12.5, 13.5, (255, 160, 30)),
            (13.5, 15.0, (0, 230, 120)),
            (15.0, 16.0, (255, 160, 30)),
            (16.0, 20.0, (180, 40, 40)),
        )

APP_NAME = "ECU Instrumenter"
DISPLAY = DisplaySettings()
THEME = ThemeSettings()
THRESHOLDS = ThresholdSettings()
AFR = AFRSettings()

PHASE_COLORS = {
    "Idle": THEME.dim,
    "Cruising": THEME.cyan,
    "Acceleration": THEME.orange,
    "Deceleration": THEME.purple,
}

# Backward-compatible aliases for existing imports.
WIDTH = DISPLAY.width
HEIGHT = DISPLAY.height
FPS = DISPLAY.fps
PAD = DISPLAY.pad

BG = THEME.bg
PANEL = THEME.panel
BORDER = THEME.border
WHITE = THEME.white
DIM = THEME.dim
CYAN = THEME.cyan
GREEN = THEME.green
ORANGE = THEME.orange
RED = THEME.red
YELLOW = THEME.yellow
PURPLE = THEME.purple

RPM_WARN = THRESHOLDS.rpm_warn
RPM_DANGER = THRESHOLDS.rpm_danger
COOL_DANGER = THRESHOLDS.coolant_danger

AFR_ZONES = list(AFR.zones)
AFR_MIN = AFR.min_value
AFR_MAX = AFR.max_value
