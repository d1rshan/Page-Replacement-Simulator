from enum import Enum


class EventType(Enum):
    PAGE_FAULT = 1
    PAGE_HIT = 2
    NOT_USED = 3
    PAGE_REPLACEMENT = 4
