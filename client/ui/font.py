"""Items relating to fonts"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['init', 'Font']

from pathlib import Path
from typing import Optional

import pygame as pg

_fonts_dir: Optional[Path] = None


def init(assets_dir: Path) -> None:
    """Initialise the fonts module"""
    global _fonts_dir
    _fonts_dir = assets_dir / 'fonts'


def Font(name: str, /, size: int, *, weight: int = 400, italic: bool = False) -> pg.font.Font:
    """Load a font"""
    variant = {
        300: 'light',
        400: 'regular',
        500: 'medium',
        700: 'bold',
    }.get(weight)
    if italic:
        variant += 'italic'
    variant += '.ttf'
    return pg.font.Font(_fonts_dir / name / variant, size)
