"""Items for drawing the user interface"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['GUI']

from dataclasses import dataclass, field

import pygame as pg

from client.events import handle_event, event_handler, Event, EventResult
from .colour import WHITE
from .components import UIComponent


@dataclass
class GUI:
    """Class to create a graphical user interface"""

    width: int
    height: int
    title: str
    _running: bool = field(default=False, init=False, repr=False)
    surface: pg.Surface = field(default=False, init=False, repr=False)
    _clock: pg.time.Clock = field(default=False, init=False, repr=False)
    _components: list[UIComponent] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if not pg.get_init():
            pg.init()
        self.size = self.width, self.height
        self.surface = pg.display.set_mode(self.size)

    def add_component(self, component: UIComponent) -> None:
        """Add a component to the UI"""
        self._components.append(component)

    def run(self) -> None:
        """Run the user interface"""
        self._setup()
        if self._running:
            return
        self._running = True

        while self._running:
            self._handle_events()
            self._draw()
            pg.display.update()
            self._clock.tick(60)

    def _setup(self) -> None:
        pg.display.set_caption(self.title)
        self._clock = pg.time.Clock()

        @event_handler(pg.MOUSEMOTION)
        def _on_mouse_motion(event: Event):
            for component in reversed(self._components):
                component.hovered = component.collide_point(event.dict['pos'])
            return EventResult()

        @event_handler(pg.MOUSEBUTTONDOWN)
        def _on_mouse_pressed(event: Event):
            for component in reversed(self._components):
                if clicked := component.collide_point(event.dict['pos']):
                    component.clicked = clicked
                    break
            return EventResult()

        @event_handler(pg.MOUSEBUTTONUP)
        def _on_mouse_released(event: Event):
            for component in reversed(self._components):
                component.clicked = -1
            return EventResult()

    @staticmethod
    def _teardown() -> None:
        pg.quit()

    def _handle_events(self) -> None:
        for event in pg.event.get():
            result = handle_event(event)
            self._running = not result.halt

    def _draw(self) -> None:
        self.surface.fill(WHITE)
        for component in self._components:
            component.render()
