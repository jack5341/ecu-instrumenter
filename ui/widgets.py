# -*- coding: utf-8 -*-
from __future__ import division
import pygame
from core.logger import logger

class Widget:
    def draw(self, surface, x, y, width, is_selected, fonts):
        pass
    def handle_left(self): pass
    def handle_right(self): pass
    def handle_click(self): pass

class IpInputWidget(Widget):
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.parts = [int(p) for p in value.split(".")]
        self.selected_part = 3

    def draw(self, surface, x, y, width, is_selected, fonts):
        from config import settings as C
        color = C.CYAN if is_selected else C.WHITE
        lbl = fonts.label.render(self.label, True, C.DIM)
        surface.blit(lbl, (x, y))
        
        val_x = x + 200
        for i, p in enumerate(self.parts):
            p_color = C.CYAN if (is_selected and self.selected_part == i) else color
            txt = fonts.label.render(str(p), True, p_color)
            surface.blit(txt, (val_x, y))
            val_x += txt.get_width()
            if i < 3:
                dot = fonts.label.render(".", True, C.WHITE)
                surface.blit(dot, (val_x, y))
                val_x += dot.get_width()

    def handle_left(self):
        # Change value down
        self.parts[self.selected_part] = max(0, self.parts[self.selected_part] - 1)
        self.value = ".".join([str(p) for p in self.parts])
    
    def handle_right(self):
        # Change value up
        self.parts[self.selected_part] = min(255, self.parts[self.selected_part] + 1)
        self.value = ".".join([str(p) for p in self.parts])
        
    def handle_click(self):
        # Cycle through segments
        self.selected_part = (self.selected_part + 1) % 4

class PortInputWidget(Widget):
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def draw(self, surface, x, y, width, is_selected, fonts):
        from config import settings as C
        color = C.CYAN if is_selected else C.WHITE
        lbl = fonts.label.render(self.label, True, C.DIM)
        surface.blit(lbl, (x, y))
        val = fonts.label.render(str(self.value), True, color)
        surface.blit(val, (x + 200, y))

    def handle_left(self): self.value = max(0, self.value - 1)
    def handle_right(self): self.value = min(65535, self.value + 1)
    def handle_click(self): self.value += 100 # Quick jump

class ToggleWidget(Widget):
    def __init__(self, label, value):
        self.label = label
        self.value = value
        
    def draw(self, surface, x, y, width, is_selected, fonts):
        from config import settings as C
        color = C.CYAN if is_selected else C.WHITE
        lbl = fonts.label.render(self.label, True, C.DIM)
        surface.blit(lbl, (x, y))
        val = fonts.label.render("ON" if self.value else "OFF", True, color)
        surface.blit(val, (x + 200, y))

    def handle_left(self): self.value = not self.value
    def handle_right(self): self.value = not self.value
    def handle_click(self): self.value = not self.value

class SliderWidget(Widget):
    def __init__(self, label, value, min_val, max_val):
        self.label = label
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

    def draw(self, surface, x, y, width, is_selected, fonts):
        from config import settings as C
        color = C.CYAN if is_selected else C.WHITE
        lbl = fonts.label.render(self.label, True, C.DIM)
        surface.blit(lbl, (x, y))
        
        bar_x = x + 180
        bar_w = width - 240
        pygame.draw.rect(surface, (40, 50, 60), (bar_x, y + 15, bar_w, 4))
        
        ratio = float(self.value - self.min_val) / max(1, self.max_val - self.min_val)
        knob_x = bar_x + int(ratio * bar_w)
        pygame.draw.circle(surface, color, (knob_x, y + 17), 10)
        
        val_txt = fonts.label.render(str(self.value), True, color)
        surface.blit(val_txt, (bar_x + bar_w + 15, y))

    def handle_left(self): self.value = max(self.min_val, self.value - 5)
    def handle_right(self): self.value = min(self.max_val, self.value + 5)

class ButtonWidget(Widget):
    def __init__(self, label, on_click):
        self.label = label
        self.on_click = on_click
        
    def draw(self, surface, x, y, width, is_selected, fonts):
        from config import settings as C
        border_color = C.CYAN if is_selected else C.BORDER
        bg_color = (30, 40, 60) if is_selected else C.PANEL
        rect = pygame.Rect(x, y, width, 40)
        pygame.draw.rect(surface, bg_color, rect)
        pygame.draw.rect(surface, border_color, rect, 2)
        txt = fonts.label.render(self.label, True, C.WHITE)
        surface.blit(txt, (x + width//2 - txt.get_width()//2, y + 20 - txt.get_height()//2))

    def handle_click(self):
        if self.on_click: self.on_click()

class MenuList:
    def __init__(self, items, fonts):
        self.items = items
        self.fonts = fonts
        self.selected_idx = 0

    def draw(self, surface, x, y, item_height=50, width=300):
        for i, item in enumerate(self.items):
            item.draw(surface, x, y + i * item_height, width, i == self.selected_idx, self.fonts)

    def handle_event(self, event):
        if not self.items: return
        item = self.items[self.selected_idx]
        
        if event.type == pygame.KEYDOWN:
            # UP/DOWN ALWAYS naviage the list
            if event.key == pygame.K_UP:
                if self.selected_idx > 0:
                    self.selected_idx -= 1
            elif event.key == pygame.K_DOWN:
                if self.selected_idx < len(self.items) - 1:
                    self.selected_idx += 1
            # LEFT/RIGHT change values
            elif event.key == pygame.K_LEFT:
                item.handle_left()
            elif event.key == pygame.K_RIGHT:
                item.handle_right()
            # A / SPACE clicks
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_z, pygame.K_x):
                item.handle_click()
