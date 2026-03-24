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
        surface.fill(C.BG)
        
        title = self.fonts.label.render("SYSTEM LOGS", True, C.WHITE)
        surface.blit(title, (C.PAD, C.PAD))
        
        btn_hint = self.fonts.unit.render("[Y] CLEAR LOG  [X] EXPORT  [B/ESC] BACK", True, C.DIM)
        surface.blit(btn_hint, (C.WIDTH - C.PAD - btn_hint.get_width(), C.PAD + 5))
        
        y = 50 - self.scroll_y
        for entry in logger.entries:
            if y > C.HEIGHT: break
            if y > 40:
                color = C.WHITE
                if entry.type_ == "warning": color = C.YELLOW
                elif entry.type_ == "error": color = C.RED
                elif entry.type_ == "connection": color = C.GREEN
                elif entry.type_ == "pid": color = C.CYAN
                
                msg_txt = "[{0:.1f}] {1}".format(entry.timestamp, entry.message)
                txt = self.fonts.tiny.render(msg_txt, True, color)
                surface.blit(txt, (C.PAD, y))
            y += 20
            
        if self.auto_scroll:
            max_scroll = max(0, len(logger.entries) * 20 - (C.HEIGHT - 60))
            self.scroll_y = max_scroll

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_b):
                global_state.screen = AppScreen.DASHBOARD
            elif event.key == pygame.K_y:
                logger.clear()
                self.scroll_y = 0
            elif event.key == pygame.K_x:
                self._export_log()
            elif event.key == pygame.K_UP:
                self.scroll_y = max(0, self.scroll_y - 40)
                self.auto_scroll = False
            elif event.key == pygame.K_DOWN:
                max_scroll = max(0, len(logger.entries) * 20 - (C.HEIGHT - 60))
                self.scroll_y = min(max_scroll, self.scroll_y + 40)
                if self.scroll_y == max_scroll:
                    self.auto_scroll = True

    def _export_log(self):
        try:
            with open("ecu_log.txt", "w") as f:
                for e in logger.entries:
                    line = "[{0:.1f}] {1}: {2}\n".format(e.timestamp, e.type_, e.message)
                    f.write(line)
            logger.log("info", "Log exported to ecu_log.txt")
            self.auto_scroll = True
        except Exception as ex:
            logger.log("error", "Export failed: " + str(ex))
