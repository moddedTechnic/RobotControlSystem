"""Items for drawing the user interface"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['GUI', 'GUIBuilder']

import os
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from typing import Type, Union, Optional, Iterator, Iterable, Any, Callable


class GUI(tk.Tk):
    """Class to create a graphical user interface"""

    def __init__(self, *args, assets_dir: Path, controller: Optional['GUI'], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.assets_dir = assets_dir
        self.controller = controller
        self.images = []
        self.modals = []
        self.variables = []

    def run(self) -> None:
        """Run the application"""
        self.mainloop()

    def open_modal_from_file(self, controller_type: Type['GUI'], name: str) -> 'GUI':
        """Open a modal from a file"""
        modal = GUIBuilder(controller_type, self.assets_dir, controller=self).build_from_file(name)
        self.modals.append(modal)
        return modal


Attributes = list[tuple[str, str | None]]


class _Node:
    """Represents a node in the document"""


@dataclass
class _TextNode(_Node):
    text:  str


@dataclass
class _TagNode(_Node):
    tag: str
    attributes: dict[str, Union[str, None]]
    children: list[_Node] = field(default_factory=list)

    def __iter__(self) -> Iterator[_Node]:
        return iter(self.children)

    def __getitem__(self, name: str):
        return self.attributes[name]

    def __contains__(self, name: str):
        return name in self.attributes


class _DocumentParser(HTMLParser):
    """Parse a document to create a navigable tree of nodes"""

    def __init__(self):
        super().__init__()
        self.stack: list[_TagNode] = []
        self.result: Optional[_Node] = None

    def handle_starttag(self, tag: str, attrs: Attributes) -> None:
        """Push a node to the stack"""
        self.stack.append(_TagNode(tag, dict(attrs)))

    def handle_endtag(self, tag: str) -> None:
        """Pop the last node from the stack and add it to its parent"""
        node = self.stack.pop()
        if node.tag != tag:
            raise TypeError(f'Unexpected tag {tag}: the {node.tag} tag was never closed')
        if self.stack:
            self.stack[-1].children.append(node)
        else:
            self.result = node

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Create the node and add it to its parent"""
        node = _TagNode(tag, dict(attrs))
        if self.stack:
            self.stack[-1].children.append(node)
        else:
            self.result = node

    def handle_data(self, data: str) -> None:
        """Add text to the parent node"""
        if self.stack:
            self.stack[-1].children.append(_TextNode(data))


class GUIBuilder:
    """Tool to build GUIs"""

    _icon_suffixes: list[str] = [
        '.svg', '.png', '.jpg', '.jpeg',
    ]

    def __init__(self, widget_type: Type[GUI], assets_dir: Path, controller: Optional[GUI] = None) -> None:
        self.widget_type = widget_type
        self.document_parser = _DocumentParser()
        self.width, self.height = self.size = 0, 0
        self.assets_dir = assets_dir
        self.icons_dir = assets_dir / 'icons'
        self.controller = controller

    def build_from_file(self, name: str) -> Optional[GUI]:
        """Build a GUI from an XML file"""
        return self._build_from_file(name=name)

    def _build_from_file(
            self, *,
            name: Optional[str] = None, path: Optional[Path] = None,
            parent: Union[tk.Tk, tk.Widget, None] = None,
    ) -> Union[tk.Widget, tk.Tk, None]:
        if name is not None:
            path = self.assets_dir / 'layouts' / f'{name}.aml'
        self.document_parser.feed(path.read_text())
        if (result := self.document_parser.result) is not None:
            return self.build(result, parent)
        return None

    def build(self, node: _Node, parent: Union[tk.Tk, ttk.Frame, None] = None) -> Union[GUI, tk.Tk, str]:
        """Build a GUI"""
        if isinstance(node, _TextNode):
            return node.text
        if isinstance(node, _TagNode):
            func_name = f'_build_{node.tag}'
            func: Callable[[_Node, Optional[tk.Tk, ttk.Frame]], Union[GUI, tk.Tk, str]] = \
                getattr(self, func_name, self._build_unknown)
            return func(node, parent)

    def prepare_text(self, text: Union[str, Iterable[str]]) -> str:
        """Prepare the text parameter in a similar manner to how HTML does it"""
        if isinstance(text, str):
            text = text.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
            while '  ' in text:
                text = text.replace('  ', ' ')
            return text.strip()
        result = ''
        for t in text:
            print(t)
            if isinstance(t, str):
                result += self.prepare_text(t)
            elif isinstance(t, _TagNode):
                if t.tag == 'br':
                    result += '\n\n'
                else:
                    raise TypeError(f'Only <br> tags and plain text are allowed in text tags (got {t.tag})')
            else:
                raise TypeError(f'Unknown type {type(t)} in text node')
        return result

    def _create_label(self, text: str, parent: tk.Tk) -> ttk.Label:
        label = ttk.Label(parent, text=text, wraplength=self.width)
        return label

    def _build_unknown(self, element: _TagNode, _: Optional[tk.Tk]) -> tk.Tk:
        raise TypeError(f'Unknown element: {element.tag}')

    def _build_window(self, node: _TagNode, parent: Optional[tk.Tk]) -> GUI:
        if parent is not None:
            raise ValueError('Windows cannot be parented to another widget')
        else:
            window: GUI = self.widget_type()
        window.title(node['title'])
        if 'width' in node:
            w, h = node['width'], node['height']
            window.geometry(f'{w}x{h}')
            self.width, self.height = self.size = int(w), int(h)
        for row, child in enumerate(node):
            widget: Union[str, tk.Tk, ttk.Label, None] = self.build(child, window)
            if isinstance(widget, str):
                widget = self._create_label(widget, window)
            if widget is not None:
                widget.grid(row=row, column=0)
        return window

    def _build_text(self, node: _TagNode, parent: Optional[tk.Tk]) -> ttk.Label:
        widget = self._create_label(self.prepare_text(map(self.build, node.children)), parent)
        if 'ref' in node:
            ref = node['ref']
        return widget

    @staticmethod
    def _build_br(node: _TagNode, _: Optional[tk.Tk]) -> _TagNode:
        return node

    @staticmethod
    def _build_tab(node: _TagNode, _: Optional[tk.Tk]) -> _TagNode:
        return node

    @staticmethod
    def _build_separator(node: _TagNode, _: Optional[tk.Tk]) -> _TagNode:
        return node