"""Run the client."""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = []

import os
import sys
from pathlib import Path

__dir__ = Path(__file__).parent
sys.path.insert(0, os.fspath(__dir__))
sys.path.insert(1, os.fspath(__dir__.parent))

import pygame as pg

from library.maths.vector import Vec2

from ui import GUI
from ui.components import Button


def main():
    """Put code here to be run when the module is run"""
    assets_dir = __dir__ / 'assets'
    fonts_dir = assets_dir / 'fonts'
    gui = GUI(720, 540, 'Robot Control System')
    font = pg.font.Font(fonts_dir / 'ubuntu' / 'regular.ttf', 19)
    gui.add_component(Button("Click me!", font, Vec2(100, 100), gui.surface))
    gui.run()


if __name__ == '__main__':
    main()
