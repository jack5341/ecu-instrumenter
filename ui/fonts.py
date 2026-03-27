# -*- coding: utf-8 -*-
import pygame

import os

def load_font(filename, size):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "assets", "fonts", filename)
    try:
        return pygame.font.Font(path, size)
    except:
        return pygame.font.Font(None, size)

class UIFonts:
    def __init__(self, huge_f, value_f, label_f, unit_f, tiny_f, title_f, button_f):
        self.huge = huge_f
        self.value = value_f
        self.label = label_f
        self.unit = unit_f
        self.tiny = tiny_f
        self.title = title_f
        self.button = button_f

    @classmethod
    def create(cls):
        return cls(
            huge_f=load_font("Space_Grotesk/static/SpaceGrotesk-Bold.ttf", 72),
            value_f=load_font("Space_Grotesk/static/SpaceGrotesk-Bold.ttf", 42),
            label_f=load_font("Syncopate/Syncopate-Bold.ttf", 16),
            unit_f=load_font("JetBrains_Mono/static/JetBrainsMono-Medium.ttf", 14),
            tiny_f=load_font("JetBrains_Mono/static/JetBrainsMono-Regular.ttf", 12),
            title_f=load_font("Syncopate/Syncopate-Bold.ttf", 42),
            button_f=load_font("Space_Grotesk/static/SpaceGrotesk-Bold.ttf", 18),
        )
