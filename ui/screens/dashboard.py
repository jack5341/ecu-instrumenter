# -*- coding: utf-8 -*-
from __future__ import division
import pygame

from core.state import global_state, AppScreen
from ui.color_logic import rpm_arc_color

class DashboardScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        from sim.simulator import Simulator
        self.simulator = Simulator()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_l, pygame.K_x, pygame.K_LSHIFT):
                global_state.screen = AppScreen.LOG
            elif event.key in (pygame.K_s, pygame.K_RETURN, pygame.K_ESCAPE):
                global_state.screen = AppScreen.SETTINGS
            # D key -> Toggle Demo Mode
            elif event.key == pygame.K_d:
                global_state.demo_mode = not global_state.demo_mode
                global_state.save()

    def update(self, dt):
        if global_state.demo_mode:
            global_state.telemetry = self.simulator.update(dt)

    def draw(self, surface, fps):
        from config import settings as C
        from ui.panels import draw_stat_panel, draw_afr_panel, draw_dtc_panel
        
        surface.fill(C.BG)
        # Background lines for texture
        for i in range(0, C.WIDTH, 60): pygame.draw.line(surface, (15, 17, 20), (i, 0), (i, C.HEIGHT))
        for i in range(0, C.HEIGHT, 60): pygame.draw.line(surface, (15, 17, 20), (0, i), (C.WIDTH, i))

        t = global_state.telemetry
        
        # Grid Coordinates
        p = C.PAD # 10px
        gap = 10
        w_half = (C.WIDTH - (2 * p) - gap) // 2
        
        # Row 1: Huge RPM & Speed
        r1_y = p
        r1_h = 160
        
        rpm_color = rpm_arc_color(t.rpm)
        rpm_rect = pygame.Rect(p, r1_y, w_half, r1_h)
        draw_stat_panel(surface, rpm_rect, "ENGINE RPM", str(int(t.rpm)), "RPM", t.rpm / 8000.0, rpm_color, self.fonts.huge, self.fonts)
        
        spd_val = t.speed * 0.621371 if global_state.settings.is_mph else t.speed
        spd_unit = "MPH" if global_state.settings.is_mph else "KM/H"
        spd_rect = pygame.Rect(p + w_half + gap, r1_y, w_half, r1_h)
        draw_stat_panel(surface, spd_rect, "VEHICLE SPEED", "{0:.0f}".format(spd_val), spd_unit, spd_val / (140.0 if global_state.settings.is_mph else 200.0), C.PURPLE, self.fonts.huge, self.fonts)

        # Row 2: Secondary stats (Coolant, Throttle)
        r2_y = r1_y + r1_h + gap
        r2_h = 95
        
        cool_rect = pygame.Rect(p, r2_y, w_half, r2_h)
        cool_danger = t.coolant > C.COOL_DANGER
        draw_stat_panel(surface, cool_rect, "COOLANT", "{0:.0f}".format(t.coolant), "°C", (t.coolant - 40) / 80.0, C.CYAN if not cool_danger else C.RED, self.fonts.value, self.fonts, warning=cool_danger)
        
        thr_rect = pygame.Rect(p + w_half + gap, r2_y, w_half, r2_h)
        draw_stat_panel(surface, thr_rect, "THROTTLE", "{0:.0f}".format(t.throttle), "%", t.throttle / 100.0, C.ORANGE, self.fonts.value, self.fonts)

        # Row 3: Full width AFR
        r3_y = r2_y + r2_h + gap
        r3_h = 90
        afr_rect = pygame.Rect(p, r3_y, C.WIDTH - (2 * p), r3_h)
        draw_afr_panel(surface, afr_rect, t.afr, self.fonts)
        
        # Row 4: full width DTC
        r4_y = r3_y + r3_h + gap
        draw_dtc_panel(surface, t.dtcs, r4_y, self.fonts)
        
        self._draw_status(surface, fps)

    def _draw_status(self, surface, fps):
        from config import settings as C
        y = C.HEIGHT - 30
        pygame.draw.rect(surface, C.PANEL, (0, y, C.WIDTH, 30))
        pygame.draw.line(surface, C.BORDER, (0,y), (C.WIDTH,y), 1)
        surface.blit(self.fonts.unit.render(C.APP_NAME, True, C.DIM), (C.PAD, y + 5))
        status = "DEMO MODE" if global_state.demo_mode else global_state.connection_status.upper()
        mid = self.fonts.unit.render(status, True, C.GREEN if "CONNECTED" in status or "DEMO" in status else C.DIM)
        surface.blit(mid, (C.WIDTH//2 - mid.get_width()//2, y + 5))
        fps_t = self.fonts.unit.render("{0:.0f} FPS".format(fps), True, C.DIM)
        surface.blit(fps_t, (C.WIDTH - C.PAD - fps_t.get_width(), y + 5))
