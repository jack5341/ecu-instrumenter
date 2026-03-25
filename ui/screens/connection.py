# -*- coding: utf-8 -*-
import pygame
from core.state import global_state, AppScreen
from core.obd_client import obd_client
from ui.widgets import MenuList, IpInputWidget, PortInputWidget, ButtonWidget

class ConnectionScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        
        self.ip_input = IpInputWidget("IP ADDRESS", "127.0.0.1")
        self.port_input = PortInputWidget("PORT", 35000)
        
        btn_connect = ButtonWidget("CONNECT", self._on_connect)
        btn_demo = ButtonWidget("DEMO MODE", self._on_demo)
        
        self.menu = MenuList([self.ip_input, self.port_input, btn_connect, btn_demo], fonts)
        
    def _on_connect(self):
        global_state.settings.ip = self.ip_input.value
        global_state.settings.port = self.port_input.value
        global_state.settings.was_connected = True
        global_state.demo_mode = False
        global_state.save()
        obd_client.start(global_state.settings.ip, global_state.settings.port)
        global_state.screen = AppScreen.DASHBOARD
        
    def _on_demo(self):
        global_state.demo_mode = True
        global_state.settings.was_connected = True
        global_state.save()
        global_state.connection_status = "connected"
        global_state.screen = AppScreen.DASHBOARD

    def draw(self, surface):
        from config import settings as C
        surface.fill(C.BG)
        # draw logo/name
        name = self.fonts.value.render("ECU INSTRUMENTER", True, C.CYAN)
        surface.blit(name, (C.WIDTH // 2 - name.get_width() // 2, 80))
        
        # draw menu
        self.menu.draw(surface, C.WIDTH // 2 - 200, 180, 60, 400)
        
        # draw status
        status_color = C.DIM
        if global_state.connection_status == "failed": status_color = C.RED
        elif global_state.connection_status == "connected": status_color = C.GREEN
        
        status_text = "STATUS: " + global_state.connection_status.upper()
        status = self.fonts.label.render(status_text, True, status_color)
        surface.blit(status, (C.WIDTH // 2 - status.get_width() // 2, 420))

    def handle_event(self, event):
        self.menu.handle_event(event)
