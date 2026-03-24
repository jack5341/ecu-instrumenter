# -*- coding: utf-8 -*-
import pygame

def mono_font(size, bold=False):
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
            font = pygame.font.SysFont(name, size, bold=bold)
            if font:
                return font
        except:
            continue
    return pygame.font.Font(None, size)

class UIFonts:
    def __init__(self, value_f, label_f, unit_f, tiny_f):
        self.value = value_f
        self.label = label_f
        self.unit = unit_f
        self.tiny = tiny_f

    @classmethod
    def create(cls):
        return cls(
            value_f=mono_font(38, bold=True),
            label_f=mono_font(22, bold=True),
            unit_f=mono_font(15),
            tiny_f=mono_font(12),
        )
