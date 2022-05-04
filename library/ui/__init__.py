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

    def __len__(self) -> int:
        return len(self.children)

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
            if isinstance(t, str):
                result += self.prepare_text(t)
            elif isinstance(t, _TagNode):
                if t.tag == 'br':
                    result += '\n\n'
                elif t.tag == 'tab':
                    result += '\t'
                else:
                    raise TypeError(f'Only <br> tags and plain text are allowed in text tags (got {t.tag})')
            else:
                raise TypeError(f'Unknown type {type(t)} in text node')
        return result

    def _create_label(self, text: str, parent: Union[tk.Tk, ttk.Frame]) -> ttk.Label:
        label = ttk.Label(parent, text=text, wraplength=self.width)
        return label

    def _create_menu(self, node: _TagNode, parent: Union[tk.Widget, tk.Tk]) -> tk.Menu:
        menu = tk.Menu(parent, tearoff=int('tearoff' in node))
        for item in node:
            if not isinstance(item, _TagNode):
                if isinstance(item, _TextNode):
                    if not item.text.strip():
                        continue
                raise TypeError(f'Menus should only contain `menuitem`s as children.')
            if item.tag not in {'menuitem', 'separator'}:
                raise TypeError(f'Menus should only contain `menuitem`s as children. (got {item.tag})')
            menu_item = self.build(item)
            kwargs = {}
            if 'disabled' in item:
                kwargs['state'] = 'disabled'
            if isinstance(menu_item, tk.Menu):
                menu.add_cascade(label=item['name'], menu=menu_item, **kwargs)
            elif isinstance(menu_item, _TagNode):
                if menu_item.tag == 'separator':
                    menu.add_separator()
            else:
                if 'ref' in item and hasattr(self.gui, 'Menu'):
                    click_handler_name = f'on_{item["ref"]}_clicked'
                    if hasattr(self.gui.Menu, click_handler_name):
                        click_handler = getattr(self.gui.Menu, click_handler_name)
                        kwargs['command'] = lambda f=click_handler, controller=self.gui: f(controller)
                    if hasattr(self.gui.Menu, 'disabled'):
                        if item['ref'] in self.gui.Menu.disabled:
                            kwargs['state'] = 'disabled'
                menu.add_command(label=item['name'], **kwargs)
        return menu

    def _load_icon(self, icon_name: str, height: int = None) -> Optional[tk.PhotoImage]:
        icon_path: Path = self.icons_dir / icon_name
        for suffix in self._icon_suffixes:
            path = icon_path.with_suffix(suffix)
            if path.exists():
                icon = tk.PhotoImage(file=os.fspath(path))
                if height is not None:
                    icon_height = icon.height()
                    icon = icon.subsample(icon_height // height)
                self.gui.images.append(icon)
                return icon
        return None

    def _get_options(self, node: _TagNode) -> tuple[list[str], dict[str, str]]:
        options_name = f'get_{node["ref"]}_options'
        refs = {}
        options = []
        if hasattr(self.gui, options_name):
            for option in getattr(self.gui, options_name)():
                if isinstance(option, tuple):
                    if len(option) == 1:
                        option = option[0]
                    else:
                        option, ref = option
                        refs[option] = ref
                options.append(option)
        return options, refs

    def _add_get_set_ref(self, ref: str, widget) -> None:
        def getter() -> str:
            """Get the value of the text widget"""
            return widget.get()

        def setter(value: Any) -> None:
            """Set the value of the text widget"""
            widget.config(text=str(value))

        setattr(self.gui, f'get_{ref}', getter)
        setattr(self.gui, f'set_{ref}', setter)

    def _build_unknown(self, element: _TagNode, _: Optional[tk.Tk]) -> tk.Tk:
        raise TypeError(f'Unknown element: {element.tag}')

    def _build_window(self, node: _TagNode, parent: Optional[tk.Tk]) -> GUI:
        if parent is not None:
            raise ValueError('Windows cannot be parented to another widget')
        else:
            window: GUI = self.widget_type(assets_dir=self.assets_dir, controller=self.controller)
        window.title(node['title'])
        if 'width' in node:
            w, h = node['width'], node['height']
            window.geometry(f'{w}x{h}')
            self.width, self.height = self.size = int(w), int(h)
        self.gui = window
        for row, child in enumerate(node):
            widget: Union[str, tk.Tk, ttk.Label, None] = self.build(child, window)
            if isinstance(widget, str):
                widget = self._create_label(widget, window)
            if isinstance(widget, tk.Menu):
                self.gui.config(menu=widget)
            elif widget is not None:
                widget.grid(row=row, column=0)
        return window

    def _build_row(self, node: _TagNode, parent: Optional[tk.Tk]) -> ttk.Frame:
        frame = ttk.Frame(parent)
        for col, child in enumerate(node):
            widget = self.build(child, frame)
            if isinstance(widget, str):
                widget = self._create_label(widget, frame)
            if widget is not None:
                widget.grid(row=0, column=col)
        return frame

    def _build_text(self, node: _TagNode, parent: Optional[tk.Tk]) -> ttk.Label:
        widget = self._create_label(self.prepare_text(map(self.build, node.children)), parent)
        if 'ref' in node:
            self._add_get_set_ref(node['ref'], widget)
        return widget

    def _build_input(self, node: _TagNode, parent: Optional[tk.Tk]):
        if node['type'] == 'number':
            kwargs = {}
            if 'from' in node:
                kwargs['from_'] = node['from']
            if 'to' in node:
                kwargs['to'] = node['to']
            if 'wrap' in node:
                kwargs['wrap'] = True
            widget = ttk.Spinbox(parent, **kwargs)
            if 'ref' in node:
                self._add_get_set_ref(node['ref'], widget)
                change_handler_name = f'on_{node["ref"]}_changed'
                if hasattr(self.gui, change_handler_name):
                    change_handler = getattr(self.gui, change_handler_name)
                    widget.config(command=change_handler)
            return widget
        elif node['type'] == 'text':
            widget = ttk.Entry(parent)
            if 'ref' in node:
                self._add_get_set_ref(node['ref'], widget)
                change_handler_name = f'on_{node["ref"]}_changed'
                if hasattr(self.gui, change_handler_name):
                    change_handler = getattr(self.gui, change_handler_name)
                    widget.prev_value = ''

                    def _change_handler(_):
                        value = widget.get()
                        if value != widget.prev_value:
                            change_handler()
                        widget.prev_value = value

                    widget.bind('<KeyRelease>', _change_handler)
            return widget
        elif node['type'] == 'dropdown':
            options = None
            if 'ref' in node:
                options, refs = self._get_options(node)
            if options is None:
                options = []
                refs = {}
                for child in node:
                    if isinstance(child, _TagNode):
                        if child.tag == 'option':
                            options.append(child['value'])
                            if 'ref' in child:
                                refs[child['value']] = child['ref']
                        else:
                            raise TypeError(f'{child.tag} elements cannot be children of drop down inputs.')
                        continue
                    elif isinstance(child, _TextNode):
                        if child.text.strip():
                            raise TypeError(f'Text elements cannot be children of drop down inputs (Got {child}).')
                        continue
                    raise NotImplementedError('Proper exception not implemented')
            if not options:
                raise NotImplementedError('Proper exception not implemented')
            dropdown_var = tk.StringVar(self.gui)
            if 'value' in node:
                options.insert(0, node['value'])
                dropdown_var.set(node['value'])

            def _on_dropdown_set(_value: tk.StringVar, controller: GUI = self.gui) -> None:
                # noinspection PyTypeChecker
                value: str = _value
                if value in refs:
                    handler_name = f'on_{refs[value]}_selected'
                    if hasattr(controller, handler_name):
                        handler = getattr(controller, handler_name)
                        handler(options[options.index(str(value))])

            dropdown = ttk.OptionMenu(parent, dropdown_var, *[str(o) for o in options], command=_on_dropdown_set)
            self.gui.variables.append(dropdown_var)

            if 'ref' in node:
                def _update_options():
                    nonlocal options, refs
                    options, refs = self._get_options(node)
                    dropdown.set_menu(node['value'] if 'value' in node else None, *[str(o) for o in options])

                setattr(self.gui, f'update_{node["ref"]}_options', _update_options)
                setattr(self.gui, node['ref'], dropdown_var)

            return dropdown
        else:
            raise TypeError(f'Unknown input type {node["type"]}')

    def _build_button(self, node: _TagNode, parent: Optional[tk.Tk]) -> ttk.Button:
        kwargs = {}
        if 'icon' in node:
            kwargs['image'] = self._load_icon(node['icon'], 20)
            kwargs['compound'] = tk.LEFT
        button = ttk.Button(parent, text=self.prepare_text(map(self.build, node.children)), **kwargs)
        if 'ref' in node:
            click_handler_name = f'on_{node["ref"]}_clicked'
            click_handler = getattr(self.gui, click_handler_name)
            button.config(command=click_handler)
        return button

    def _build_menu(self, node: _TagNode, parent: Optional[tk.Tk]):
        return self._create_menu(node, parent)

    def _build_menuitem(self, node: _TagNode, parent: Optional[tk.Tk]):
        if len(node) == 0:
            return None
        return self._create_menu(node, parent)

    def _build_include(self, node: _TagNode, parent: Optional[tk.Tk]):
        source_file = self.assets_dir / 'includes' / f'{node["name"]}.aml'
        if not source_file.exists():
            raise FileNotFoundError(f'Could not include {node["name"]}: the file could not be found ({source_file}).')
        return self._build_from_file(path=source_file, parent=parent)

    @staticmethod
    def _build_br(node: _TagNode, _: Optional[tk.Tk]) -> _TagNode:
        return node

    @staticmethod
    def _build_tab(node: _TagNode, _: Optional[tk.Tk]) -> _TagNode:
        return node

    @staticmethod
    def _build_separator(node: _TagNode, _: Optional[tk.Tk]) -> _TagNode:
        return node
