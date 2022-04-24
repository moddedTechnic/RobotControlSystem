"""Items for drawing the user interface"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['GUI']

from pathlib import Path
import tkinter as tk


class GUI(tk.Tk):
    """Class to create a graphical user interface"""

    @classmethod
    def from_file(cls, path: Path) -> 'GUI':
        """Create a GUI from a file"""

