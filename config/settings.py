from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DisplaySettings:
    width: int = 640
    height: int = 480
    fps: int = 30
    pad: int = 10


@dataclass(frozen=True)
class ThemeSettings:
    bg: tuple[int, int, int] = (10, 12, 18)
    panel: tuple[int, int, int] = (18, 22, 32)
    border: tuple[int, int, int] = (35, 42, 60)
    white: tuple[int, int, int] = (220, 228, 240)
    dim: tuple[int, int, int] = (80, 90, 110)
    cyan: tuple[int, int, int] = (0, 210, 255)
    green: tuple[int, int, int] = (0, 230, 120)
    orange: tuple[int, int, int] = (255, 160, 30)
    red: tuple[int, int, int] = (255, 55, 55)
    yellow: tuple[int, int, int] = (255, 220, 0)
    purple: tuple[int, int, int] = (160, 80, 255)


@dataclass(frozen=True)
class ThresholdSettings:
    rpm_warn: int = 5000
    rpm_danger: int = 6500
    coolant_danger: int = 105


@dataclass(frozen=True)
class AFRSettings:
    min_value: float = 10.0
    max_value: float = 20.0
    zones: tuple[tuple[float, float, tuple[int, int, int]], ...] = (
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
