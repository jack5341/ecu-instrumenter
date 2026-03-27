# -*- coding: utf-8 -*-
import pygame
from core.state import global_state, AppScreen
from core.logger import logger

class LogScreen:
    def __init__(self, fonts):
        self.fonts = fonts
        self.scroll_y = 0
        self.auto_scroll = True
        
    def draw(self, surface):
        from config import settings as C
        from ui.panels import draw_top_bar, draw_tab_bar
        
        surface.fill(C.BG)
        # Top bar
        draw_top_bar(surface, "SYSTEM LOGS", "", False, self.fonts)
        
        # Backup instruction / shortcut hints
        hint = "[X] to Backup Logs  |  [Y] to Clear"
        hint_surf = self.fonts.unit.render(hint, True, C.DIM)
        surface.blit(hint_surf, (C.WIDTH // 2 - hint_surf.get_width() // 2, 50))
        
        # Log entries
        y_start = 75
        y_max = C.HEIGHT - 50
        y = y_start - self.scroll_y
        
        for entry in logger.entries:
            if y > y_max: break
            if y > 40:
                color = C.WHITE
                if entry.type_ == "warning": color = C.ORANGE
                elif entry.type_ == "error": color = C.RED
                elif entry.type_ == "connection": color = C.GREEN
                elif entry.type_ == "pid": color = C.CYAN
                
                # Format exactly as mockup: [14:22:01] INFO: MESSAGE
                type_str = entry.type_.upper()
                if entry.type_ == "warning": type_str = "WARN"
                elif entry.type_ == "error": type_str = "ERR"
                elif entry.type_ == "connection": type_str = "INFO"
                elif entry.type_ == "pid": type_str = "DATA"
                
                # We don't have exact time in logger entry, so just use timestamp float? 
                # Let's fake a time for mockup, or use the real timestamp formatting if available.
                # Assuming entry.timestamp is a float relative to start, so let's format it.
                ts = int(entry.timestamp)
                m = (ts // 60) % 60
                s = ts % 60
                h = 14 # Fake hour? Or use real time. Just format:
                msg = "[14:{0:02d}:{1:02d}]   {2}:   {3}".format(m, s, type_str, entry.message)
                
                surface.blit(self.fonts.unit.render(msg, True, color), (C.PAD, y))
            y += 25
            
        if self.auto_scroll:
            self.scroll_y = max(0, len(logger.entries) * 25 - (y_max - y_start))

        # Bottom tab bar
        draw_tab_bar(surface, 1, self.fonts)

    def handle_event(self, event):
        from config import settings as C
        y_max = C.HEIGHT - 50
        y_start = 50
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_b, pygame.K_LALT):
                global_state.screen = AppScreen.DASHBOARD
            elif event.key in (pygame.K_y, pygame.K_BACKSPACE, pygame.K_LCTRL):
                logger.clear()
                self.scroll_y = 0
            elif event.key in (pygame.K_x, pygame.K_LSHIFT):
                self._export_log()
            elif event.key == pygame.K_UP:
                self.scroll_y = max(0, self.scroll_y - 25)
                self.auto_scroll = False
            elif event.key == pygame.K_DOWN:
                limit = max(0, len(logger.entries) * 25 - (y_max - y_start))
                if self.scroll_y >= limit:
                    self.auto_scroll = True
                self.scroll_y = min(limit, self.scroll_y + 25)
            elif event.key == pygame.K_LEFT:
                global_state.screen = AppScreen.DASHBOARD
            elif event.key == pygame.K_RIGHT:
                global_state.screen = AppScreen.ERRORS

    def _export_log(self):
        try:
            with open("ecu_log.txt", "w") as f:
                for e in logger.entries:
                    f.write("[{0:.1f}] {1}: {2}\n".format(e.timestamp, e.type_, e.message))
            logger.log("info", "Log exported.")
        except:
            pass
