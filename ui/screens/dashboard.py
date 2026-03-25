# -*- coding: utf-8 -*-
from __future__ import division
import pygame

from core.state import global_state, AppScreen

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
            elif event.key == pygame.K_d:
                global_state.demo_mode = not global_state.demo_mode
                global_state.save()
            elif event.key == pygame.K_RIGHT:
                global_state.screen = AppScreen.LOG
            elif event.key == pygame.K_LEFT:
                pass # Already left-most

    def update(self, dt):
        if global_state.demo_mode:
            global_state.telemetry = self.simulator.update(dt)

    def draw(self, surface, fps):
        from config import settings as C
        from ui.panels import draw_top_bar, draw_tab_bar, draw_card, draw_afr_full
        
        surface.fill(C.BG)
        # Top bar
        draw_top_bar(surface, "DASHBOARD", "OBDII SYNCED", True, self.fonts)
        
        t = global_state.telemetry
        
        p = C.PAD 
        gap = p
        
        # Row 1
        r1_y = 50
        r1_h = 140
        w_total = C.WIDTH - (2 * p)
        w_rpm = int(w_total * 0.6)
        w_spd = w_total - w_rpm - gap
        
        rpm_rect = pygame.Rect(p, r1_y, w_rpm, r1_h)
        draw_card(surface, rpm_rect, "ENGINE RPM", "{0:.0f}".format(t.rpm), "RPM", self.fonts.huge, C.WHITE, self.fonts)
        
        spd_val = t.speed * 0.621371 if getattr(global_state.settings, 'is_mph', True) else t.speed
        spd_unit = "MPH" if getattr(global_state.settings, 'is_mph', True) else "KM/H"
        spd_rect = pygame.Rect(p + w_rpm + gap, r1_y, w_spd, r1_h)
        draw_card(surface, spd_rect, "SPEED", "{0:.0f}".format(spd_val), spd_unit, self.fonts.huge, C.WHITE, self.fonts)

        # Row 2
        r2_y = r1_y + r1_h + gap
        r2_h = 100
        w_third = (w_total - 2 * gap) // 3
        
        thr_rect = pygame.Rect(p, r2_y, w_third, r2_h)
        draw_card(surface, thr_rect, "THROTTLE", "{0:.0f}".format(t.throttle), "%", self.fonts.value, C.WHITE, self.fonts, progress_ratio=(t.throttle / 100.0))
        
        oil_rect = pygame.Rect(p + w_third + gap, r2_y, w_third, r2_h)
        oil_temp = t.coolant + 20
        
        is_f = False
        try:
            is_f = global_state.settings.is_fahrenheit
        except:
            is_f = True
            
        oil_unit = "°F" if is_f else "°C"
        oil_v = oil_temp * 9/5 + 32 if is_f else oil_temp
        draw_card(surface, oil_rect, "OIL TEMP", "{0:.0f}".format(oil_v), oil_unit, self.fonts.value, C.WHITE, self.fonts)
        
        cool_rect = pygame.Rect(p + 2 * (w_third + gap), r2_y, w_third, r2_h)
        cool_unit = "°F" if is_f else "°C"
        cool_v = t.coolant * 9/5 + 32 if is_f else t.coolant
        draw_card(surface, cool_rect, "COOLANT", "{0:.0f}".format(cool_v), cool_unit, self.fonts.value, C.ORANGE, self.fonts, alert=True)

        # Row 3
        r3_y = r2_y + r2_h + gap
        r3_h = 90
        afr_rect = pygame.Rect(p, r3_y, w_total, r3_h)
        draw_afr_full(surface, afr_rect, t.afr, self.fonts)
        
        # Bottom tab bar
        draw_tab_bar(surface, 0, self.fonts)
