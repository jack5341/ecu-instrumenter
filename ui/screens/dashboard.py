from __future__ import division
import math
import pygame
from core.state import global_state, AppScreen
from ui.panels import draw_panel, draw_bar_gauge, draw_afr_row, draw_dtc_panel
from ui.color_logic import rpm_arc_color

class DashboardScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        from sim.simulator import Simulator
        self.simulator = Simulator()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                global_state.screen = AppScreen.LOG
            elif event.key == pygame.K_s:
                global_state.screen = AppScreen.SETTINGS

    def _draw_arc_gauge(self, surface, rect, value, vmin, vmax, title, unit, color):
        from config import settings as C
        a_start = -math.pi / 4
        a_end = 5 * math.pi / 4
        
        pygame.draw.arc(surface, (30, 40, 50), rect, a_start, a_end, 8)
        
        ratio = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.0
        ratio = max(0.0, min(1.0, ratio))
        
        sweep = ratio * (a_end - a_start)
        cur_angle = a_end - sweep
        
        if cur_angle < a_end:
            pygame.draw.arc(surface, color, rect, cur_angle, a_end, 10)
        
        center_x = rect.centerx
        center_y = rect.centery + 10
        
        lbl = self.fonts.label.render(title, True, color)
        surface.blit(lbl, (center_x - lbl.get_width() // 2, center_y - 45))
        
        val_txt = self.fonts.value.render(str(int(value)), True, C.WHITE)
        surface.blit(val_txt, (center_x - val_txt.get_width() // 2, center_y - 5))
        
        if unit:
            u_txt = self.fonts.unit.render(unit, True, C.DIM)
            surface.blit(u_txt, (center_x - u_txt.get_width() // 2, center_y + 35))

    def update(self, dt):
        if global_state.demo_mode:
            frame = self.simulator.update(dt)
            global_state.telemetry = frame

    def draw(self, surface, fps):
        from config import settings as C
        from ui.panels import draw_grid
        surface.fill(C.BG)
        draw_grid(surface)
        frame = global_state.telemetry

        gauge_w = (C.WIDTH - C.PAD * 3) // 2
        gauge_h = 160
        rpm_rect = pygame.Rect(C.PAD, C.PAD, gauge_w, gauge_h)
        spd_rect = pygame.Rect(C.PAD * 2 + gauge_w, C.PAD, gauge_w, gauge_h)
        draw_panel(surface, rpm_rect)
        draw_panel(surface, spd_rect)
        
        a1 = rpm_rect.inflate(-40, -40)
        a2 = spd_rect.inflate(-40, -40)

        self._draw_arc_gauge(surface, a1, frame.rpm, 0, 8000, "RPM", "", rpm_arc_color(frame.rpm))
        speed = frame.speed * 0.621371 if global_state.settings.is_mph else frame.speed
        s_unit = "mph" if global_state.settings.is_mph else "km/h"
        s_max = 140 if global_state.settings.is_mph else 200
        
        self._draw_arc_gauge(surface, a2, speed, 0, s_max, "SPEED", s_unit, C.PURPLE)

        bars_y = rpm_rect.bottom + 15
        bar_height = 42
        bars_rect = pygame.Rect(C.PAD, bars_y, C.WIDTH - 2 * C.PAD, bar_height * 2 + 30)
        draw_panel(surface, bars_rect)
        
        bw = bars_rect.width - 30
        draw_bar_gauge(surface, C.PAD + 15, bars_y + 10, bw, bar_height, "COOLANT", frame.coolant, 40, 120, "C", self.fonts, C.COOL_DANGER)
        draw_bar_gauge(surface, C.PAD + 15, bars_y + 10 + bar_height + 10, bw, bar_height, "THROTTLE", frame.throttle, 0, 100, "%", self.fonts, None)
        
        afr_y = bars_rect.bottom + 15
        afr_rect = pygame.Rect(C.PAD, afr_y, bars_rect.width, 50)
        draw_panel(surface, afr_rect)
        draw_afr_row(surface, frame.afr, afr_y, self.fonts)
        
        dtc_y = afr_rect.bottom + 15
        draw_dtc_panel(surface, frame.dtcs, dtc_y, self.fonts)
        
        self._draw_status(surface, fps)

    def _draw_status(self, surface, fps):
        from config import settings as C
        y = C.HEIGHT - 30
        rect = pygame.Rect(0, y, C.WIDTH, 30)
        pygame.draw.rect(surface, C.PANEL, rect)
        pygame.draw.line(surface, C.BORDER, (0, y), (C.WIDTH, y), 1)
        
        left = self.fonts.unit.render(C.APP_NAME, True, C.DIM)
        surface.blit(left, (C.PAD, y + 5))
        
        status = global_state.connection_status.upper()
        if global_state.demo_mode: status = "DEMO MODE"
        color = C.GREEN if status in ("CONNECTED", "DEMO MODE") else C.DIM
        mid = self.fonts.unit.render(status, True, color)
        surface.blit(mid, (C.WIDTH // 2 - mid.get_width() // 2, y + 5))
        
        fps_t = self.fonts.unit.render("{0:.0f} FPS".format(fps), True, C.DIM)
        surface.blit(fps_t, (C.WIDTH - C.PAD - fps_t.get_width(), y + 5))
