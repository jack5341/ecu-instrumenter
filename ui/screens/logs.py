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
        # Hint for Mini: Y=Clear, X=Export, B=Back
        hint = "[Y] CLEAR [X] EXPORT [B] BACK"
        btn_hint = self.fonts.unit.render(hint, True, C.DIM)
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
                msg = "[{0:.1f}] {1}".format(entry.timestamp, entry.message)
                surface.blit(self.fonts.tiny.render(msg, True, color), (C.PAD, y))
            y += 20
        if self.auto_scroll:
            self.scroll_y = max(0, len(logger.entries) * 20 - (C.HEIGHT - 60))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # B Button (LALT) or ESC -> Back
            if event.key in (pygame.K_ESCAPE, pygame.K_b, pygame.K_LALT):
                global_state.screen = AppScreen.DASHBOARD
            # Y Button (LCtrl / Backspace) -> Clear
            elif event.key in (pygame.K_y, pygame.K_BACKSPACE, pygame.K_LCTRL):
                logger.clear()
                self.scroll_y = 0
            # X Button (LShift) -> Export
            elif event.key in (pygame.K_x, pygame.K_LSHIFT):
                self._export_log()
            # D-Pad for scrolling
            elif event.key == pygame.K_UP:
                self.scroll_y = max(0, self.scroll_y - 40)
                self.auto_scroll = False
            elif event.key == pygame.K_DOWN:
                self.auto_scroll = (self.scroll_y >= max(0, len(logger.entries)*20 - (C.HEIGHT-60)))
                self.scroll_y = min(max(0, len(logger.entries)*20 - (C.HEIGHT-60)), self.scroll_y + 40)

    def _export_log(self):
        try:
            with open("ecu_log.txt", "w") as f:
                for e in logger.entries:
                    f.write("[{0:.1f}] {1}: {2}\n".format(e.timestamp, e.type_, e.message))
            logger.log("info", "Log exported.")
        except:
            pass
