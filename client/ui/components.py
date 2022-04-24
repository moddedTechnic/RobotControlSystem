"""Represent UI components such as buttons"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = [
    'UIComponent',
    'Button',
]

from abc import ABC, abstractmethod

import pygame as pg

from library.maths.vector import Vec2

from .colour import RED, GREEN, BLUE, BLACK


class UIComponent(ABC):
    """Represents a UI Component"""

    def __init__(self, position: Vec2, surface: pg.Surface) -> None:
        self.position = position
        self.surface = surface
        self.hovered: bool = False
        self.clicked: int = -1

    @abstractmethod
    def render(self) -> None:
        """Render the component"""

    @abstractmethod
    def collide_point(self, point: Vec2) -> bool:
        """Checks if the point collides with the UI component"""

    def check_hovered(self, mouse: Vec2) -> None:
        """Check if the mouse is hovering over the component"""
        self.hovered = self.collide_point(mouse)

    def check_clicked(self, mouse: Vec2, button: int) -> None:
        """Check if the mouse clicked the component"""
        if button < 0:
            self.clicked = button
        if self.collide_point(mouse):
            self.clicked = button


class RectComponent(UIComponent, ABC):
    """Represents component which is rectangular in form"""

    def __init__(self, position: Vec2, surface: pg.Surface) -> None:
        super().__init__(position, surface)

    def collide_point(self, point: Vec2) -> bool:
        """Checks if the point collides with the UI component"""
        return self.rect.collidepoint(*point.to_tuple())

    @property
    def rect(self) -> pg.Rect:
        """Get the bounding rect of the component"""
        return pg.Rect(self.position.to_tuple(), self.size.to_tuple())

    @property
    @abstractmethod
    def size(self) -> Vec2:
        """The size of the component"""


class _RectComponent(RectComponent):
    """Represents a component which is a simple rectangle"""

    def __init__(self, position: Vec2, size: Vec2, surface: pg.Surface, colour: tuple[int, int, int] = RED) -> None:
        super().__init__(position, surface)
        self._size = size
        self.colour = colour

    def render(self) -> None:
        """Render a rectangle"""
        pg.draw.rect(self.surface, self.colour, self.rect)

    @property
    def size(self) -> Vec2:
        """Get the size of the component"""
        return self._size


class Label(RectComponent):
    """Represents a label"""

    def collide_point(self, point: Vec2) -> bool:
        """Check if the point collides with the label"""
        return self.rect.collidepoint(point.to_tuple())

    def __init__(self, text: str, font: pg.font.Font, position: Vec2, surface: pg.Surface):
        super().__init__(position, surface)
        self._text_surface = text_surface = font.render(text, True, BLACK)
        self._text_rect = text_rect = text_surface.get_rect()
        text_rect.center = (self.position + self.size / 2).to_tuple()

    def render(self) -> None:
        """Render the label"""
        self.surface.blit(self._text_surface, self._text_rect)

    @property
    def size(self) -> Vec2:
        """Get the size of the label"""
        return Vec2.from_tuple(self._text_rect.size)


class Button(RectComponent):
    """Represents a button"""

    def __init__(self, text: str, font: pg.font.Font, position: Vec2, surface: pg.Surface) -> None:
        super().__init__(position, surface)
        self.label = Label(text, font, position, surface)
        self.base = _RectComponent(position, self.size, surface)

    def render(self) -> None:
        """Render the button"""
        self.base.colour = RED
        if self.hovered:
            self.base.colour = GREEN
        if self.clicked >= 0:
            self.base.colour = BLUE
        self.base.render()
        self.label.render()

    @property
    def size(self) -> Vec2:
        """Get the size of the button"""
        return self.label.size
