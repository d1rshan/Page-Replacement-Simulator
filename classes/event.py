from EventType import EventType


class Event:
    def __init__(self, event_index):
        self.event_index = event_index
        self.event_data = -1
        self.event_type = EventType.NOT_USED

    # Getters
    def get_event_index(self):
        return self.event_index

    def get_event_data(self):
        return self.event_data

    def get_event_type(self):
        return self.event_type

    # Setters
    def set_event_data(self, event_data):
        self.event_data = event_data

    def set_event_type(self, event_type):
        self.event_type = event_type

    # Unique methods

    # Check if event is empty
    def is_empty(self):
        return self.event_data == -1

    # Check if event data is equal to a number
    def is_equal_to(self, number):
        return self.event_data == number

    # Copy previous event
    def copy_event(self, event):
        self.event_data = event.get_event_data()
