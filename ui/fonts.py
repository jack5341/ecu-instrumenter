# -*- coding: utf-8 -*-
import pygame

def mono_font(size, bold=False):
    font = pygame.font.Font(None, size)
    if bold:
        font.set_bold(True)
    return font

class UIFonts:
    def __init__(self, huge_f, value_f, label_f, unit_f, tiny_f):
        self.huge = huge_f
        self.value = value_f
        self.label = label_f
        self.unit = unit_f
        self.tiny = tiny_f

    @classmethod
    def create(cls):
        return cls(
            huge_f=mono_font(72, bold=True),
            value_f=mono_font(42, bold=True),
            label_f=mono_font(18, bold=True),
            unit_f=mono_font(14, bold=False),
            tiny_f=mono_font(12, bold=False),
        )
