# -*- coding: utf-8 -*-
import pygame
from core.state import global_state, AppScreen
from ui.widgets import MenuList, IpInputWidget, PortInputWidget, ToggleWidget, ButtonWidget, SliderWidget

class SettingsScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        
        self.oil_slider = SliderWidget("OIL ALARM", getattr(global_state.settings, 'oil_warn', 130), 80, 150)
        self.coolant_slider = SliderWidget("COOLANT ALARM", getattr(global_state.settings, 'coolant_warn', 105), 80, 130)
        self.mph_toggle = ToggleWidget("USE MPH / F", getattr(global_state.settings, 'is_mph', False))
        self.demo_toggle = ToggleWidget("DEMO MODE", getattr(global_state, 'demo_mode', False))
        self.history_toggle = ToggleWidget("SAVE HISTORY", getattr(global_state.settings, 'save_history', False))
        
        btn_clear_dtc = ButtonWidget("CLEAR FAULT CODES", self._on_clear_dtc)
        
        items = [self.oil_slider, self.coolant_slider, self.mph_toggle, self.demo_toggle, self.history_toggle, btn_clear_dtc]
        self.menu = MenuList(items, self.fonts)
        
    def _on_clear_dtc(self):
        global_state.telemetry.dtcs = []
        
    def _save_settings(self):
        global_state.settings.oil_warn = self.oil_slider.value
        global_state.settings.coolant_warn = self.coolant_slider.value
        global_state.settings.is_mph = self.mph_toggle.value
        global_state.settings.is_fahrenheit = self.mph_toggle.value
        global_state.demo_mode = self.demo_toggle.value
        global_state.settings.save_history = self.history_toggle.value
        global_state.save()

    def _on_back(self):
        self._save_settings()
        global_state.screen = AppScreen.DASHBOARD

    def draw(self, surface):
        from config import settings as C
        from ui.panels import draw_top_bar, draw_tab_bar
        surface.fill(C.BG)
        # Top bar
        draw_top_bar(surface, "SETTINGS", "ONLINE", True, self.fonts)
        
        # Menu
        self.menu.draw(surface, C.WIDTH // 2 - 200, 80, 50, 400)
        
        vers = self.fonts.unit.render("v1.0 - ECU Instrumenter", True, C.DIM)
        surface.blit(vers, (C.WIDTH // 2 - vers.get_width() // 2, C.HEIGHT - 80))
        
        # Bottom tab bar
        draw_tab_bar(surface, 2, self.fonts)

    def handle_event(self, event):
        # Allow menu to consume event first (e.g. editing a slider)
        if self.menu.handle_event(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_b, pygame.K_LALT):
                self._on_back()
                return
            elif event.key == pygame.K_LEFT:
                self._save_settings()
                global_state.screen = AppScreen.LOG
                return
            elif event.key == pygame.K_RIGHT:
                pass # Already right-most
