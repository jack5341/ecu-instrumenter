from __future__ import annotations

import pygame

from config import settings as C
from models.telemetry import TelemetryFrame
from ui.color_logic import rpm_arc_color
from ui.fonts import UIFonts
from ui.panels import (
    draw_afr_row,
    draw_bar_gauge,
    draw_dtc_panel,
    draw_grid,
    draw_panel,
    draw_status_bar,
    draw_value_panel,
)


RPM_MIN = 0.0
RPM_MAX = 8000.0
SPD_MIN = 0.0
SPD_MAX = 160.0


class Renderer:
    def __init__(self) -> None:
        self.fps = 30.0
        self.fonts = UIFonts.create()

    def draw(self, screen: pygame.Surface, frame: TelemetryFrame) -> None:
        screen.fill(C.BG)
        draw_grid(screen)

        gauge_width = (C.WIDTH - C.PAD * 3) // 2
        gauge_height = 160
        left_x = C.PAD
        right_x = C.PAD * 2 + gauge_width

        rpm_rect = pygame.Rect(left_x, C.PAD, gauge_width, gauge_height)
        spd_rect = pygame.Rect(right_x, C.PAD, gauge_width, gauge_height)
        draw_panel(screen, rpm_rect)
        draw_panel(screen, spd_rect)

        draw_value_panel(screen, rpm_rect, frame.rpm, "RPM", rpm_arc_color(frame.rpm), "", self.fonts)
        draw_value_panel(screen, spd_rect, frame.speed, "SPEED", C.PURPLE, "km/h", self.fonts)

        bars_y = C.PAD + gauge_height + 15
        bar_height = 42
        bars_rect = pygame.Rect(C.PAD, bars_y, C.WIDTH - 2 * C.PAD, bar_height * 2 + 30)
        draw_panel(screen, bars_rect)

        bar_width = C.WIDTH - 2 * C.PAD - 30
        draw_bar_gauge(
            screen,
            C.PAD + 15,
            bars_y + 10,
            bar_width,
            bar_height,
            "COOLANT",
            frame.coolant,
            40.0,
            120.0,
            "°C",
            self.fonts,
            C.COOL_DANGER,
        )
        draw_bar_gauge(
            screen,
            C.PAD + 15,
            bars_y + 10 + bar_height + 10,
            bar_width,
            bar_height,
            "THROTTLE",
            frame.throttle,
            0.0,
            100.0,
            "%",
            self.fonts,
            None,
        )

        afr_y = bars_y + bar_height * 2 + 30 + 15
        afr_rect = pygame.Rect(C.PAD, afr_y, C.WIDTH - 2 * C.PAD, 50)
        draw_panel(screen, afr_rect)
        draw_afr_row(screen, frame.afr, afr_y, self.fonts)

        dtc_y = afr_y + 50 + 15
        draw_dtc_panel(screen, frame.dtcs, dtc_y, self.fonts)

        draw_status_bar(screen, frame.phase_name, 440, self.fps, self.fonts)
