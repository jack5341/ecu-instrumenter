from __future__ import annotations

from dataclasses import dataclass

import pygame


def mono_font(size: int, bold: bool = False) -> pygame.font.Font:
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
        except (OSError, pygame.error):
            continue
    return pygame.font.Font(None, size)


@dataclass
class UIFonts:
    value: pygame.font.Font
    label: pygame.font.Font
    unit: pygame.font.Font
    tiny: pygame.font.Font

    @classmethod
    def create(cls) -> "UIFonts":
        return cls(
            value=mono_font(38, bold=True),
            label=mono_font(22, bold=True),
            unit=mono_font(15),
            tiny=mono_font(12),
        )
