# -*- coding: utf-8 -*-
from __future__ import division
import pygame
from config import settings as C

def draw_top_bar(screen, title, right_text, is_streaming, fonts):
    h = 40
    rect = pygame.Rect(0, 0, C.WIDTH, h)
    pygame.draw.rect(screen, (15, 15, 15), rect)
    pygame.draw.line(screen, (40, 40, 40), (0, h-1), (C.WIDTH, h-1), 1)
    
    # Title - Aligned left, vertically centered
    t_surf = fonts.label.render(title, True, C.WHITE)
    t_y = (h - t_surf.get_height()) // 2
    screen.blit(t_surf, (15, t_y))

    # Right side (Status Badge)
    if right_text:
        pad_x = 8
        pad_y = 4
        badge_font = fonts.unit
        r_surf = badge_font.render(right_text, True, C.WHITE)
        badge_w = r_surf.get_width() + (pad_x * 2) + 15
        badge_h = r_surf.get_height() + (pad_y * 2)
        badge_rect = pygame.Rect(C.WIDTH - C.PAD - badge_w, (h - badge_h) // 2, badge_w, badge_h)
        
        # Draw dot
        dot_color = C.GREEN if is_streaming else C.RED
        dot_radius = 4
        pygame.draw.circle(screen, dot_color, (badge_rect.left + pad_x + dot_radius, badge_rect.centery), dot_radius)
        
        screen.blit(r_surf, (badge_rect.left + pad_x + 15, badge_rect.top + pad_y))

def draw_tab_bar(screen, active_tab_index, fonts):
    h = 50
    y = C.HEIGHT - h
    rect = pygame.Rect(0, y, C.WIDTH, h)
    pygame.draw.rect(screen, (10, 10, 10), rect)
    
    tabs = ["DASHBOARD", "LOGS", "SETTINGS"]
    tab_w = C.WIDTH // len(tabs)
    
    for i, tab in enumerate(tabs):
        t_rect = pygame.Rect(i * tab_w, y, tab_w, h)
        is_active = (i == active_tab_index)
        
        if is_active:
            pygame.draw.rect(screen, (50, 50, 50), t_rect)
            pygame.draw.line(screen, C.WHITE, (t_rect.left, t_rect.top), (t_rect.right, t_rect.top), 2)
        else:
            pygame.draw.rect(screen, (30, 30, 30), t_rect)
            pygame.draw.line(screen, (20, 20, 20), (t_rect.right-1, t_rect.top), (t_rect.right-1, t_rect.bottom), 1)

        # Draw icon
        icon_color = C.WHITE if is_active else C.DIM
        icon_cx = t_rect.centerx
        icon_cy = t_rect.top + 15
        
        if tab == "DASHBOARD":
            # 2x2 grid
            for dx in (-4, 2):
                for dy in (-4, 2):
                    pygame.draw.rect(screen, icon_color, (icon_cx + dx, icon_cy + dy, 4, 4))
        elif tab == "LOGS":
            # List
            for dy in (-4, 0, 4):
                pygame.draw.rect(screen, icon_color, (icon_cx - 6, icon_cy + dy, 3, 2))
                pygame.draw.rect(screen, icon_color, (icon_cx - 1, icon_cy + dy, 8, 2))
        elif tab == "SETTINGS":
            # Gear
            pygame.draw.circle(screen, icon_color, (icon_cx, icon_cy), 4, 2)
            for dy in (-5, 3):
                pygame.draw.rect(screen, icon_color, (icon_cx - 1, icon_cy + dy, 2, 2))
            for dx in (-5, 3):
                pygame.draw.rect(screen, icon_color, (icon_cx + dx, icon_cy - 1, 2, 2))

        # Text
        color = C.WHITE if is_active else C.DIM
        t_surf = fonts.tiny.render(tab, True, color)
        screen.blit(t_surf, (t_rect.centerx - t_surf.get_width() // 2, t_rect.bottom - 15))


def draw_card(screen, rect, title, value_str, unit_str, val_font, val_color, fonts, alert=False, progress_ratio=None):
    # Base card
    pygame.draw.rect(screen, (25, 25, 25), rect)
    
    # Title
    t_surf = fonts.unit.render(title, True, C.DIM if not alert else C.ORANGE)
    screen.blit(t_surf, (rect.left + 15, rect.top + 15))
    
    # Value
    v_surf = val_font.render(value_str, True, val_color)
    v_y = rect.bottom - 15 - v_surf.get_height()
    if progress_ratio is not None:
        v_y -= 10  # lift text slightly to make room for bar
    screen.blit(v_surf, (rect.left + 15, v_y))
    
    # Unit
    if unit_str:
        u_surf = fonts.unit.render(unit_str, True, C.DIM)
        # align to baseline
        screen.blit(u_surf, (rect.left + 15 + v_surf.get_width() + 5, v_y + v_surf.get_height() - u_surf.get_height() - 5))
        
    # Top Right Icons
    if title == "ENGINE RPM":
        pygame.draw.circle(screen, C.DIM, (rect.right - 20, rect.top + 20), 6, 2)
    elif title == "COOLANT":
        icon_r = pygame.Rect(rect.right - 40, rect.top, 40, 40)
        pygame.draw.rect(screen, (60, 20, 20), icon_r)
        cx, cy = icon_r.centerx, icon_r.centery
        pygame.draw.circle(screen, C.ORANGE, (cx, cy + 5), 4)
        pygame.draw.line(screen, C.ORANGE, (cx, cy + 5), (cx, cy - 8), 3)

    # Progress Bar at the bottom
    if progress_ratio is not None:
        bar_h = 6
        pad_x = 15
        bar_rect = pygame.Rect(rect.left + pad_x, rect.bottom - bar_h - 10, rect.width - pad_x * 2, bar_h)
        pygame.draw.rect(screen, (40, 40, 40), bar_rect)
        
        ratio = max(0.0, min(1.0, progress_ratio))
        fill_w = int(bar_rect.width * ratio)
        if fill_w > 0:
            fill_rect = pygame.Rect(bar_rect.left, bar_rect.top, fill_w, bar_h)
            # Pick color based on title (or simple orange for throttle)
            bar_color = C.ORANGE
            pygame.draw.rect(screen, bar_color, fill_rect)

def draw_afr_full(screen, rect, afr, fonts):
    pygame.draw.rect(screen, (25, 25, 25), rect)
    
    t_surf = fonts.unit.render("AIR/FUEL RATIO (AFR)", True, C.DIM)
    screen.blit(t_surf, (rect.left + 15, rect.top + 15))
    
    if afr > 15.0:
        badge_text = "LEAN"
        badge_color = C.RED
        val_color = C.RED
    elif afr < 13.5:
        badge_text = "RICH"
        badge_color = C.ORANGE
        val_color = C.ORANGE
    else:
        badge_text = "STABLE"
        badge_color = C.GREEN
        val_color = C.WHITE

    v_surf = fonts.huge.render("{0:.1f}".format(afr), True, val_color)
    screen.blit(v_surf, (rect.left + 15, rect.bottom - 15 - v_surf.get_height()))
    
    # Badge right
    b_surf = fonts.unit.render(badge_text, True, badge_color)
    b_rect = pygame.Rect(rect.right - 15 - b_surf.get_width() - 20, rect.top + 15, b_surf.get_width() + 20, b_surf.get_height() + 10)
    pygame.draw.rect(screen, badge_color, b_rect, 1)
    screen.blit(b_surf, (b_rect.left + 10, b_rect.top + 5))
