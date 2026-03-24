# -*- coding: utf-8 -*-
from __future__ import division
import pygame

from config import settings as C
from ui.color_logic import afr_zone_color

def draw_stat_panel(screen, rect, title, value_str, unit, ratio, bar_color, val_font, fonts, warning=False):
    # Background
    pygame.draw.rect(screen, C.PANEL, rect)
    pygame.draw.rect(screen, C.RED if warning else C.BORDER, rect, 2)
    
    # Title - Top Left
    title_color = C.RED if warning else C.DIM
    lbl = fonts.label.render(title, True, title_color)
    screen.blit(lbl, (rect.left + 15, rect.top + 15))
    
    # Value & Unit - Bottom Right (above bar)
    val = val_font.render(value_str, True, C.WHITE)
    un = fonts.unit.render(unit, True, C.DIM) if unit else None
    
    val_y = rect.bottom - 20 - val.get_height()
    
    total_w = val.get_width() + 8 + un.get_width() if un else val.get_width()
    start_x = rect.right - 15 - total_w
    
    screen.blit(val, (start_x, val_y))
    if un:
        # Align unit to the baseline of the value text
        screen.blit(un, (start_x + val.get_width() + 8, val_y + val.get_height() - un.get_height() - 5))
        
    # Bottom fill bar
    bar_h = 8
    bar_rect = pygame.Rect(rect.left + 2, rect.bottom - bar_h - 2, rect.width - 4, bar_h)
    pygame.draw.rect(screen, (25, 30, 40), bar_rect) # Empty background
    
    ratio = max(0.0, min(1.0, ratio))
    fill_w = int((rect.width - 4) * ratio)
    if fill_w > 0:
        pygame.draw.rect(screen, bar_color, pygame.Rect(rect.left + 2, rect.bottom - bar_h - 2, fill_w, bar_h))

def draw_afr_panel(screen, rect, afr, fonts):
    pygame.draw.rect(screen, C.PANEL, rect)
    pygame.draw.rect(screen, C.BORDER, rect, 2)
    
    lbl = fonts.label.render("AIR / FUEL RATIO", True, C.DIM)
    screen.blit(lbl, (rect.left + 15, rect.top + 15))
    
    # Draw large AFR value
    accent = afr_zone_color(afr)
    val = fonts.value.render("{0:.1f}".format(afr), True, accent)
    screen.blit(val, (rect.right - 15 - val.get_width(), rect.top + 10))
    
    # Draw AFR meter at the bottom
    bar_h = 24
    bar_w = rect.width - 30
    bar_x = rect.left + 15
    bar_y = rect.bottom - bar_h - 15
    meter_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
    
    afr_range = C.AFR_MAX - C.AFR_MIN
    curr_x = meter_rect.left
    for lo, hi, color in C.AFR_ZONES:
        w = int((hi - lo) / afr_range * meter_rect.width)
        pygame.draw.rect(screen, color, (curr_x, meter_rect.top, max(1, w), meter_rect.height))
        curr_x += w
    pygame.draw.rect(screen, C.BORDER, meter_rect, 1)

    needle_t = max(0.0, min(1.0, (afr - C.AFR_MIN) / afr_range))
    needle_x = int(meter_rect.left + needle_t * meter_rect.width)
    pygame.draw.line(screen, C.WHITE, (needle_x, meter_rect.top - 4), (needle_x, meter_rect.bottom + 4), 3)

def draw_dtc_panel(screen, dtcs, y, fonts):
    rect = pygame.Rect(C.PAD, y, C.WIDTH - 2 * C.PAD, 45)
    if not dtcs:
        pygame.draw.rect(screen, (15, 30, 20), rect) # Dark green bg
        pygame.draw.rect(screen, C.GREEN, rect, 2)
        msg = fonts.label.render("SYSTEM CLEAR - NO FAULT CODES", True, C.GREEN)
        screen.blit(msg, (rect.centerx - msg.get_width() // 2, rect.centery - msg.get_height() // 2))
        return

    pygame.draw.rect(screen, (40, 15, 15), rect) # Dark red bg
    pygame.draw.rect(screen, C.RED, rect, 2)
    warn = fonts.label.render("!", True, C.YELLOW)
    x = rect.left + 20
    screen.blit(warn, (x, rect.centery - warn.get_height() // 2))
    
    dtc_str = " ".join(dtcs)
    txt = fonts.label.render("FAULT CODES: " + dtc_str, True, C.YELLOW)
    screen.blit(txt, (x + warn.get_width() + 15, rect.centery - txt.get_height() // 2))
