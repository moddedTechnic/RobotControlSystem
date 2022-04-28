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

from library.maths.vector import Vec2

from ui import GUI, GUIBuilder, font


class RobotController(GUI):
    """The GUI which controls the robots"""


def main():
    """Put code here to be run when the module is run"""
    assets_dir = __dir__ / 'assets'
    font.init(assets_dir)
    gui_builder = GUIBuilder(InteractivePromptController, assets_dir)
    gui = gui_builder.build_from_file('interactive_prompt')
    gui.run()


if __name__ == '__main__':
    main()
