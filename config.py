# -*- coding: utf-8 -*-
from __future__ import division
# Screen
WIDTH = 640
HEIGHT = 480
FPS = 30
PAD = 10

# App
APP_NAME = "ECU Instrumenter"

# Colors
BG = (10, 12, 18)
PANEL = (18, 22, 32)
BORDER = (35, 42, 60)
WHITE = (220, 228, 240)
DIM = (80, 90, 110)
CYAN = (0, 210, 255)
GREEN = (0, 230, 120)
ORANGE = (255, 160, 30)
RED = (255, 55, 55)
YELLOW = (255, 220, 0)
PURPLE = (160, 80, 255)

# AFR zones (min, max, color)
AFR_ZONES = [
    (10.0, 12.5, (180, 40, 40)),
    (12.5, 13.5, (255, 160, 30)),
    (13.5, 15.0, (0, 230, 120)),
    (15.0, 16.0, (255, 160, 30)),
    (16.0, 20.0, (180, 40, 40)),
]
AFR_MIN = 10.0
AFR_MAX = 20.0

# Thresholds
RPM_WARN = 5000
RPM_DANGER = 6500
COOL_DANGER = 105

# Phase accent colors for status line
PHASE_COLORS = {
    "Idle": DIM,
    "Cruising": CYAN,
    "Acceleration": ORANGE,
    "Deceleration": PURPLE,
}
