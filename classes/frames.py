from event import Event
from EventType import EventType


class Frame:
    def __init__(self, frame_id, event_count):
        self.frame_id = frame_id
        self.event_count = event_count
        self.events = []
        for i in range(event_count):
            self.events.append(Event(i))

        # Experimental variables
        self.frame_current_page = -1
        self.frame_current_page_birth = -1

    # Getters
    def get_frame_id(self):
        return self.frame_id

    def get_frame_current_page(self):
        return self.frame_current_page

    def get_frame_current_page_birth(self):
        return self.frame_current_page_birth

    # Unique methods
    # Check if frame is empty

    def is_empty(self):
        return self.frame_current_page == -1

    # Check if frame is equal to a page
    def is_equal_to(self, page):
        return self.frame_current_page == page

    # Check if frame is equal to a page
    def is_equal_to_page_number(self, page_number):
        return self.frame_current_page == page_number

    # Page Replacement (This situation means this frame's page is being replaced)

    def replace_page(self, page, index):
        self.frame_current_page = page
        self.frame_current_page_age = 0
        self.frame_current_page_birth = index
        self.set_current_event(index, EventType.PAGE_REPLACEMENT, page)

    # Page Hit (This situation means this frame's page or a different frame's page is being hit)
    def page_hit(self, index):
        self.set_current_event(index, EventType.PAGE_HIT,
                               self.get_frame_current_page())

    # Page Fault (This situation means a different frame is being replaced but this frame's page is not being replaced)
    def page_fault(self, index):
        self.set_current_event(index, EventType.PAGE_FAULT,
                               self.get_frame_current_page())

    # Methods associated with events
    # Set Current Event Type
    def set_current_event_type(self, index, event_type):
        self.events[index].set_event_type(event_type)

    # Set current event data
    def set_current_event_data(self, index, event_data):
        self.events[index].set_event_data(event_data)

    # Set Current Event
    def set_current_event(self, index, event_type, event_data):
        self.set_current_event_type(index, event_type)
        self.set_current_event_data(index, event_data)
