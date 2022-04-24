"""Items for handling and processing events"""

__author__ = 'Jonathan Leeming'
__version__ = '0.1'
__all__ = ['Event', 'EventHandler', 'EventResult', 'event_handler', 'handle_event']

from dataclasses import dataclass
from typing import Callable

import pygame as pg
from pygame.event import Event

from library.maths.vector import Vec2


@dataclass(frozen=True)
class EventResult:
    """Represents the result of an event"""
    halt: bool = False


EventHandler = Callable[[Event], EventResult]

event_handlers: dict[int, EventHandler] = {}


class event_handler:
    """Decorator to mark a function as an event handler"""

    def __init__(self, event_type: int):
        self.type = event_type

    def __call__(self, handler: EventHandler):
        event_handlers[self.type] = handler
        return handler


def handle_event(event: Event) -> EventResult:
    """Handle an event"""
    if 'pos' in event.dict:
        event.dict['pos'] = Vec2.from_tuple(event.dict['pos'])
    return event_handlers.get(event.type, event_handlers[-1])(event)


@event_handler(-1)
def _handle_unknown_event(event: Event) -> EventResult:
    print(event)
    return EventResult()


@event_handler(pg.QUIT)
def _handle_quit_event(_: Event) -> EventResult:
    return EventResult(halt=True)
