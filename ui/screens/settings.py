# -*- coding: utf-8 -*-
import pygame
from core.state import global_state, AppScreen
from ui.widgets import MenuList, IpInputWidget, PortInputWidget, ToggleWidget, ButtonWidget, SliderWidget

class SettingsScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        
        self.ip_input = IpInputWidget("IP ADDRESS", global_state.settings.ip)
        self.port_input = PortInputWidget("PORT", global_state.settings.port)
        self.mph_toggle = ToggleWidget("USE MPH / F", global_state.settings.is_mph)
        self.bright_slider = SliderWidget("BRIGHTNESS", global_state.settings.brightness, 10, 100)
        
        btn_clear_dtc = ButtonWidget("CLEAR FAULT CODES", self._on_clear_dtc)
        
        items = [self.ip_input, self.port_input, self.mph_toggle, self.bright_slider, btn_clear_dtc]
        self.menu = MenuList(items, self.fonts)
        
    def _on_clear_dtc(self):
        global_state.telemetry.dtcs = []
        
    def _on_back(self):
        global_state.settings.ip = self.ip_input.value
        global_state.settings.port = self.port_input.value
        global_state.settings.is_mph = self.mph_toggle.value
        global_state.settings.is_fahrenheit = self.mph_toggle.value
        global_state.settings.brightness = self.bright_slider.value
        global_state.save()
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
        # We also want to support B button to go back.
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_b, pygame.K_LALT):
                self._on_back()
                return
            elif event.key == pygame.K_LEFT:
                global_state.screen = AppScreen.LOG
                return
            elif event.key == pygame.K_RIGHT:
                pass # Already right-most
        self.menu.handle_event(event)
