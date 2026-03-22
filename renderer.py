# -*- coding: utf-8 -*-
from __future__ import division
"""
640×480 ECU dashboard — pure pygame drawing.
"""

import math
import pygame

import config as C


RPM_MIN = 0.0
RPM_MAX = 8000.0
SPD_MIN = 0.0
SPD_MAX = 160.0


def _mono_font(size, bold=False):
    names = [
        "dejavusansmono",
        "dejavu sans mono",
        "DejaVu Sans Mono",
        "liberation mono",
        "courier new",
        "courier",
        "monospace",
    ]
    for name in names:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except (OSError, pygame.error):
            pass
    return pygame.font.Font(None, size)


def _afr_zone_color(afr):
    n = len(C.AFR_ZONES)
    for i, (lo, hi, col) in enumerate(C.AFR_ZONES):
        last = i == n - 1
        if last:
            if lo <= afr <= hi:
                return col
        elif lo <= afr < hi:
            return col
    return C.WHITE


def _rpm_arc_color(rpm):
    if rpm >= C.RPM_DANGER:
        return C.RED
    if rpm >= C.RPM_WARN:
        return C.ORANGE
    return C.CYAN


class Renderer:
    def __init__(self):
        self.fps = 30.0
        self._val_font = _mono_font(38, bold=True)
        self._label_font = _mono_font(22, bold=True)
        self._unit_font = _mono_font(15, bold=False)
        self._tiny_font = _mono_font(12, bold=False)

    def _draw_panel(self, screen, rect):
        pygame.draw.rect(screen, C.PANEL, rect)
        pygame.draw.rect(screen, C.BORDER, rect, 1)

    def draw(self, screen, sim):
        screen.fill(C.BG)
        self._draw_grid(screen)

        gw = (C.WIDTH - C.PAD * 3) // 2
        gh = 160
        gx0 = C.PAD
        gx1 = C.PAD * 2 + gw

        # Panels
        r_rpm = pygame.Rect(gx0, C.PAD, gw, gh)
        r_spd = pygame.Rect(gx1, C.PAD, gw, gh)
        self._draw_panel(screen, r_rpm)
        self._draw_panel(screen, r_spd)

        self._draw_value_panel(
            screen, r_rpm, sim.rpm, RPM_MIN, RPM_MAX, "RPM",
            _rpm_arc_color(sim.rpm), int(round(sim.rpm)), ""
        )
        self._draw_value_panel(
            screen, r_spd, sim.speed, SPD_MIN, SPD_MAX, "SPEED",
            C.PURPLE, int(round(sim.speed)), "km/h"
        )

        y_bars = C.PAD + gh + 15
        bar_h = 42
        r_bars = pygame.Rect(C.PAD, y_bars, C.WIDTH - 2 * C.PAD, bar_h * 2 + 30)
        self._draw_panel(screen, r_bars)

        self._draw_bar_gauge(
            screen, C.PAD + 15, y_bars + 10, C.WIDTH - 2 * C.PAD - 30, bar_h,
            "COOLANT", sim.coolant, 40.0, 120.0, "°C", danger_hi=C.COOL_DANGER
        )
        self._draw_bar_gauge(
            screen, C.PAD + 15, y_bars + 10 + bar_h + 10, C.WIDTH - 2 * C.PAD - 30, bar_h,
            "THROTTLE", sim.throttle, 0.0, 100.0, "%", danger_hi=None
        )

        y_afr = y_bars + bar_h * 2 + 30 + 15
        r_afr = pygame.Rect(C.PAD, y_afr, C.WIDTH - 2 * C.PAD, 50)
        self._draw_panel(screen, r_afr)
        self._draw_afr_row(screen, sim.afr, y_afr)

        y_dtc = y_afr + 50 + 15
        self._draw_dtc_panel(screen, sim.dtcs, y_dtc)

        self._draw_status_bar(screen, sim.phase_name, 440)

    def _draw_grid(self, screen):
        g = (15, 17, 23)
        for x in range(0, C.WIDTH + 1, 40):
            pygame.draw.line(screen, g, (x, 0), (x, C.HEIGHT), 1)
        for y in range(0, C.HEIGHT + 1, 40):
            pygame.draw.line(screen, g, (0, y), (C.WIDTH, y), 1)

    def _draw_value_panel(self, screen, rect, value, vmin, vmax, title, accent, display_int, unit):
        cx = rect.centerx
        cy = rect.centery

        lab = self._label_font.render(title, True, accent)
        lr = lab.get_rect(center=(int(cx), int(cy - 25)))
        screen.blit(lab, lr)

        val_s = str(display_int)
        val_img = self._val_font.render(val_s, True, C.WHITE)
        vr = val_img.get_rect(center=(int(cx), int(cy + 15)))
        screen.blit(val_img, vr)

        if unit:
            u_img = self._unit_font.render(unit, True, C.DIM)
            ur = u_img.get_rect(center=(int(cx), int(cy + 55)))
            screen.blit(u_img, ur)

    def _draw_bar_gauge(self, screen, x, y, w, h, label, value, vmin, vmax, unit, danger_hi):
        ratio = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.0
        ratio = max(0.0, min(1.0, ratio))

        if danger_hi is not None and value > danger_hi:
            fill_c = C.RED
            edge_glow = (255, 120, 120)
        elif label == "THROTTLE":
            fill_c = C.ORANGE
            edge_glow = (255, 200, 120)
        else:
            fill_c = C.CYAN
            edge_glow = (120, 240, 255)

        bg = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, C.PANEL, bg)
        pygame.draw.rect(screen, C.BORDER, bg, 1)

        fill_w = max(4, int((w - 8) * ratio))
        inner = pygame.Rect(x + 4, y + 4, fill_w, h - 8)
        pygame.draw.rect(screen, fill_c, inner)
        # Leading edge glow
        if fill_w > 6:
            glow = pygame.Rect(x + 4 + fill_w - 5, y + 5, 5, h - 10)
            pygame.draw.rect(screen, edge_glow, glow)

        lbl = self._label_font.render(label, True, C.WHITE)
        screen.blit(lbl, (x + 12, y + (h - lbl.get_height()) // 2))

        val_s = "{0:.0f}{1}".format(value, unit)
        val_img = self._unit_font.render(val_s, True, C.WHITE)
        screen.blit(val_img, (x + w - val_img.get_width() - 12, y + (h - val_img.get_height()) // 2))

    def _draw_afr_row(self, screen, afr, y):
        left_pad = C.PAD + 15
        w_total = C.WIDTH - 2 * C.PAD - 30
        zone_w = w_total - 120
        zx = left_pad + 110

        accent = _afr_zone_color(afr)
        afr_txt = self._label_font.render("AFR {0:.1f}".format(afr), True, accent)
        screen.blit(afr_txt, (left_pad, y + 10))

        zrect = pygame.Rect(zx, y + 10, zone_w, 24)
        rng = C.AFR_MAX - C.AFR_MIN
        x0 = zrect.left
        for lo, hi, col in C.AFR_ZONES:
            seg_w = int((hi - lo) / rng * zrect.width)
            seg = pygame.Rect(x0, zrect.top, max(1, seg_w), zrect.height)
            pygame.draw.rect(screen, col, seg)
            x0 += seg_w
        pygame.draw.rect(screen, C.BORDER, zrect, 1)

        # Needle
        t = (afr - C.AFR_MIN) / rng
        t = max(0.0, min(1.0, t))
        nx = int(zrect.left + t * zrect.width)
        pygame.draw.line(screen, C.WHITE, (nx, zrect.top - 2), (nx, zrect.bottom + 2), 3)

        # Boundary labels
        marks = [
            (10.0, "10"),
            (12.5, "12.5"),
            (13.5, "13.5"),
            (15.0, "15"),
            (16.0, "16"),
            (20.0, "20"),
        ]
        for m, label in marks:
            tx = zrect.left + (m - C.AFR_MIN) / rng * zrect.width
            s = self._tiny_font.render(label, True, C.DIM)
            screen.blit(s, (int(tx - s.get_width() // 2), zrect.bottom + 4))

    def _draw_dtc_panel(self, screen, dtcs, y):
        r = pygame.Rect(C.PAD, y, C.WIDTH - 2 * C.PAD, 40)
        if not dtcs:
            pygame.draw.rect(screen, C.GREEN, r, 2)
            msg = self._label_font.render("● NO FAULT CODES", True, C.GREEN)
            screen.blit(msg, (r.centerx - msg.get_width() // 2, r.centery - msg.get_height() // 2))
        else:
            pygame.draw.rect(screen, C.RED, r, 2)
            warn = self._label_font.render("⚠", True, C.YELLOW)
            x = r.left + 14
            screen.blit(warn, (x, r.centery - warn.get_height() // 2))
            x += warn.get_width() + 8
            for code in dtcs:
                t = self._label_font.render(code, True, C.YELLOW)
                screen.blit(t, (x, r.centery - t.get_height() // 2))
                x += t.get_width() + 14

    def _draw_status_bar(self, screen, phase_name, y):
        r = pygame.Rect(0, y, C.WIDTH, C.HEIGHT - y)
        pygame.draw.rect(screen, C.PANEL, r)
        pygame.draw.line(screen, C.BORDER, (0, y), (C.WIDTH, y), 1)

        left = self._unit_font.render(C.APP_NAME, True, C.DIM)
        screen.blit(left, (C.PAD, y + 5))

        phase_c = C.PHASE_COLORS.get(phase_name, C.WHITE)
        mid = self._unit_font.render("DEMO \xc2\xb7 {0}".format(phase_name.upper()), True, phase_c)
        screen.blit(mid, (C.WIDTH // 2 - mid.get_width() // 2, y + 5))

        fps_s = "{0:.0f} FPS".format(self.fps)
        right = self._unit_font.render(fps_s, True, C.DIM)
        screen.blit(right, (C.WIDTH - C.PAD - right.get_width(), y + 5))
