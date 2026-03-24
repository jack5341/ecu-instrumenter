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
        btn_back = ButtonWidget("BACK TO DASHBOARD", self._on_back)
        
        items = [self.ip_input, self.port_input, self.mph_toggle, self.bright_slider, btn_clear_dtc, btn_back]
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
        surface.fill(C.BG)
        # draw label
        lbl = self.fonts.value.render("SETTINGS", True, C.CYAN)
        surface.blit(lbl, (C.WIDTH // 2 - lbl.get_width() // 2, 40))
        
        self.menu.draw(surface, C.WIDTH // 2 - 200, 120, 55, 400)
        
        vers = self.fonts.unit.render("v1.0 - ECU Instrumenter", True, C.DIM)
        surface.blit(vers, (C.WIDTH // 2 - vers.get_width() // 2, 440))

    def handle_event(self, event):
        # We also want to support B button to go back.
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_b, pygame.K_LALT):
            self._on_back()
            return
        self.menu.handle_event(event)
