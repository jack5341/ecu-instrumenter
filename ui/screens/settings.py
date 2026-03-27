# -*- coding: utf-8 -*-
import pygame
from core.state import global_state, AppScreen
from ui.widgets import MenuList, IpInputWidget, PortInputWidget, ToggleWidget, ButtonWidget, SliderWidget

class SettingsScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        
        self.ip_input = IpInputWidget("IP ADDRESS", getattr(global_state.settings, 'ip', '127.0.0.1'))
        self.port_input = PortInputWidget("PORT", getattr(global_state.settings, 'port', 35000))
        self.oil_slider = SliderWidget("OIL ALARM", getattr(global_state.settings, 'oil_warn', 130), 80, 150)
        self.coolant_slider = SliderWidget("COOLANT ALARM", getattr(global_state.settings, 'coolant_warn', 105), 80, 130)
        self.mph_toggle = ToggleWidget("USE MPH / F", getattr(global_state.settings, 'is_mph', False))
        self.demo_toggle = ToggleWidget("DEMO MODE", getattr(global_state, 'demo_mode', False))
        self.history_toggle = ToggleWidget("SAVE HISTORY", getattr(global_state.settings, 'save_history', False))
        
        items = [self.ip_input, self.port_input, self.oil_slider, self.coolant_slider, self.mph_toggle, self.demo_toggle, self.history_toggle]
        self.menu = MenuList(items, self.fonts)
        
    def _save_settings(self):
        old_ip = getattr(global_state.settings, 'ip', '127.0.0.1')
        old_port = getattr(global_state.settings, 'port', 35000)
        
        global_state.settings.ip = self.ip_input.value
        global_state.settings.port = self.port_input.value
        global_state.settings.oil_warn = self.oil_slider.value
        global_state.settings.coolant_warn = self.coolant_slider.value
        global_state.settings.is_mph = self.mph_toggle.value
        global_state.settings.is_fahrenheit = self.mph_toggle.value
        global_state.demo_mode = self.demo_toggle.value
        global_state.settings.save_history = self.history_toggle.value
        global_state.save()
        
        return (old_ip != self.ip_input.value) or (old_port != self.port_input.value)

    def _on_back(self):
        reconnect = self._save_settings()
        if reconnect and not global_state.demo_mode:
            from core.obd_client import obd_client
            obd_client.start(global_state.settings.ip, global_state.settings.port)
            global_state.screen = AppScreen.LOADING
        else:
            global_state.screen = AppScreen.DASHBOARD

    def draw(self, surface):
        from config import settings as C
        from ui.panels import draw_top_bar, draw_tab_bar
        surface.fill(C.BG)
        # Top bar
        draw_top_bar(surface, "SETTINGS", "", False, self.fonts)
        
        # Menu
        self.menu.draw(surface, C.WIDTH // 2 - 200, 70, 45, 400)
        
        vers = self.fonts.unit.render("v1.0 - ECU Instrumenter", True, C.DIM)
        surface.blit(vers, (C.WIDTH // 2 - vers.get_width() // 2, C.HEIGHT - 55))
        
        # Bottom tab bar
        draw_tab_bar(surface, 3, self.fonts)

    def handle_event(self, event):
        # Allow menu to consume event first (e.g. editing a slider)
        if self.menu.handle_event(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_b, pygame.K_LALT):
                self._on_back()
                return
            elif event.key == pygame.K_LEFT:
                reconnect = self._save_settings()
                if reconnect and not global_state.demo_mode:
                    from core.obd_client import obd_client
                    obd_client.start(global_state.settings.ip, global_state.settings.port)
                    global_state.screen = AppScreen.LOADING
                else:
                    global_state.screen = AppScreen.ERRORS
                return
            elif event.key == pygame.K_RIGHT:
                pass # Already right-most
