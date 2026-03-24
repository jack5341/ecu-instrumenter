# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import division
import pygame

from config import settings as C
from ui.color_logic import afr_zone_color

def draw_panel(screen, rect):
    pygame.draw.rect(screen, C.PANEL, rect)
    pygame.draw.rect(screen, C.BORDER, rect, 1)

def draw_grid(screen):
    grid_color = (15, 17, 23)
    for x in range(0, C.WIDTH + 1, 40):
        pygame.draw.line(screen, grid_color, (x, 0), (x, C.HEIGHT), 1)
    for y in range(0, C.HEIGHT + 1, 40):
        pygame.draw.line(screen, grid_color, (0, y), (C.WIDTH, y), 1)

def draw_value_panel(screen, rect, value, title, accent, unit, fonts):
    center_x = rect.centerx
    center_y = rect.centery

    label = fonts.label.render(title, True, accent)
    label_rect = label.get_rect(center=(int(center_x), int(center_y - 25)))
    screen.blit(label, label_rect)

    val = fonts.value.render(str(int(round(value))), True, C.WHITE)
    value_rect = val.get_rect(center=(int(center_x), int(center_y + 15)))
    screen.blit(val, value_rect)

    if unit:
        unit_img = fonts.unit.render(unit, True, C.DIM)
        unit_rect = unit_img.get_rect(center=(int(center_x), int(center_y + 55)))
        screen.blit(unit_img, unit_rect)

def draw_bar_gauge(screen, x, y, width, height, label, value, vmin, vmax, unit, fonts, danger_hi):
    ratio = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.0
    ratio = max(0.0, min(1.0, ratio))

    if danger_hi is not None and value > danger_hi:
        fill_color = C.RED
        edge_glow = (255, 120, 120)
    elif label == "THROTTLE":
        fill_color = C.ORANGE
        edge_glow = (255, 200, 120)
    else:
        fill_color = C.CYAN
        edge_glow = (120, 240, 255)

    bg = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, C.PANEL, bg)
    pygame.draw.rect(screen, C.BORDER, bg, 1)

    fill_width = max(4, int((width - 8) * ratio))
    inner = pygame.Rect(x + 4, y + 4, fill_width, height - 8)
    pygame.draw.rect(screen, fill_color, inner)
    if fill_width > 6:
        glow = pygame.Rect(x + 4 + fill_width - 5, y + 5, 5, height - 10)
        pygame.draw.rect(screen, edge_glow, glow)

    lbl = fonts.label.render(label, True, C.WHITE)
    screen.blit(lbl, (x + 12, y + (height - lbl.get_height()) // 2))

    value_txt = fonts.unit.render("{0:.0f}{1}".format(value, unit), True, C.WHITE)
    screen.blit(value_txt, (x + width - value_txt.get_width() - 12, y + (height - value_txt.get_height()) // 2))

def draw_afr_row(screen, afr, y, fonts):
    left_pad = C.PAD + 15
    width_total = C.WIDTH - 2 * C.PAD - 30
    zone_width = width_total - 120
    zone_x = left_pad + 110

    accent = afr_zone_color(afr)
    afr_text = fonts.label.render("AFR {0:.1f}".format(afr), True, accent)
    screen.blit(afr_text, (left_pad, y + 10))

    zone_rect = pygame.Rect(zone_x, y + 10, zone_width, 24)
    afr_range = C.AFR_MAX - C.AFR_MIN
    seg_start_x = zone_rect.left
    for lo, hi, color in C.AFR_ZONES:
        seg_w = int((hi - lo) / afr_range * zone_rect.width)
        seg = pygame.Rect(seg_start_x, zone_rect.top, max(1, seg_w), zone_rect.height)
        pygame.draw.rect(screen, color, seg)
        seg_start_x += seg_w
    pygame.draw.rect(screen, C.BORDER, zone_rect, 1)

    needle_t = (afr - C.AFR_MIN) / afr_range
    needle_t = max(0.0, min(1.0, needle_t))
    needle_x = int(zone_rect.left + needle_t * zone_rect.width)
    pygame.draw.line(screen, C.WHITE, (needle_x, zone_rect.top - 2), (needle_x, zone_rect.bottom + 2), 3)

    marks = [
        (10.0, "10"),
        (12.5, "12.5"),
        (13.5, "13.5"),
        (15.0, "15"),
        (16.0, "16"),
        (20.0, "20"),
    ]
    for mark, label in marks:
        text_x = zone_rect.left + (mark - C.AFR_MIN) / afr_range * zone_rect.width
        txt = fonts.tiny.render(label, True, C.DIM)
        screen.blit(txt, (int(text_x - txt.get_width() // 2), zone_rect.bottom + 4))

def draw_dtc_panel(screen, dtcs, y, fonts):
    rect = pygame.Rect(C.PAD, y, C.WIDTH - 2 * C.PAD, 40)
    if not dtcs:
        pygame.draw.rect(screen, C.GREEN, rect, 2)
        msg = fonts.label.render("* NO FAULT CODES", True, C.GREEN)
        screen.blit(msg, (rect.centerx - msg.get_width() // 2, rect.centery - msg.get_height() // 2))
        return

    pygame.draw.rect(screen, C.RED, rect, 2)
    warn = fonts.label.render("!", True, C.YELLOW) # Python 2 fix for special char if needed
    x = rect.left + 14
    screen.blit(warn, (x, rect.centery - warn.get_height() // 2))
    x += warn.get_width() + 8
    for code in dtcs:
        txt = fonts.label.render(code, True, C.YELLOW)
        screen.blit(txt, (x, rect.centery - txt.get_height() // 2))
        x += txt.get_width() + 14

def draw_status_bar(screen, phase_name, y, fps, fonts):
    rect = pygame.Rect(0, y, C.WIDTH, C.HEIGHT - y)
    pygame.draw.rect(screen, C.PANEL, rect)
    pygame.draw.line(screen, C.BORDER, (0, y), (C.WIDTH, y), 1)

    left = fonts.unit.render(C.APP_NAME, True, C.DIM)
    screen.blit(left, (C.PAD, y + 5))

    phase_color = C.PHASE_COLORS.get(phase_name, C.WHITE)
    mid = fonts.unit.render("DEMO . {0}".format(phase_name.upper()), True, phase_color)
    screen.blit(mid, (C.WIDTH // 2 - mid.get_width() // 2, y + 5))

    fps_txt = fonts.unit.render("{0:.0f} FPS".format(fps), True, C.DIM)
    screen.blit(fps_txt, (C.WIDTH - C.PAD - fps_txt.get_width(), y + 5))
