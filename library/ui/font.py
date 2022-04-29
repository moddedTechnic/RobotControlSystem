"""Items relating to fonts"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['init', 'Font']

from pathlib import Path
from typing import Optional

_fonts_dir: Optional[Path] = None


def init(assets_dir: Path) -> None:
    """Initialise the fonts module"""
    global _fonts_dir
    _fonts_dir = assets_dir / 'fonts'


def Font(name: str, /, size: int, *, weight: int = 400, italic: bool = False) -> None:
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
    font_file = _fonts_dir / name / variant
