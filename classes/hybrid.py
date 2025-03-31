import page as p
import frames as f
from EventType import EventType

class Hybrid(p.Page):
    def __init__(self, page_sequence, frame_count, page_count):
        super().__init__(page_sequence, frame_count, page_count)
        self.frames = []
        for i in range(frame_count):
            self.frames.append(Hybrid_Frames(i, page_count))
        self.hybrid()

    def hybrid(self):
        """
        Simulates the Hybrid LFU-LRU algorithm.
        """
        index = 0
        for page in self.page_sequence:
            # Check if page is in a frame
            if self.check_for_page(page):
                self.page_hit_events(index)
                self.frames[self.find_page(page)].increment_page_frequency()
                self.frames[self.find_page(page)].update_recent_usage(index)
            # Check if there is an empty frame
            elif self.check_for_empty_frame():
                self.page_fault_events(index)
                self.add_page_to_empty_frame(page, index)
            # If there is no empty frame and page is not in a frame
            # Find the least valuable page and replace it
            else:
                self.page_fault_events(index)
                self.page_replacement_event(
                    index, page, self.find_least_valuable_page())
            
            index += 1

        self.calculate_rates()
        self.print_hybrid_table()

    def find_least_valuable_page(self):
        """
        Finds the page to replace based on LFU-LRU hybrid logic.
        """
        least_valuable = self.frames[0]
        for frame in self.frames:
            if frame.get_page_frequency() < least_valuable.get_page_frequency():
                least_valuable = frame
            elif frame.get_page_frequency() == least_valuable.get_page_frequency():
                if frame.get_last_used_time() < least_valuable.get_last_used_time():
                    least_valuable = frame
        return least_valuable.get_frame_id()

    def print_hybrid_table(self):
        """
        Prints the Hybrid LFU-LRU table.
        """
        print(f"+-------------------+")
        print(f"| Hybrid LFU-LRU TABLE |", )

        self.print_sequence()
        self.print_frames()
        self.print_rates()

class Hybrid_Frames(f.Frame):
    def __init__(self, frame_count, event_count):
        super().__init__(frame_count, event_count)
        self.page_frequency = 0
        self.last_used_time = -1

    def get_page_frequency(self):
        return self.page_frequency

    def increment_page_frequency(self):
        self.page_frequency += 1

    def update_recent_usage(self, index):
        self.last_used_time = index

    def get_last_used_time(self):
        return self.last_used_time

    def replace_page(self, page, index):
        self.frame_current_page = page
        self.frame_current_page_age = 0
        self.frame_current_page_birth = index
        self.page_frequency = 1
        self.last_used_time = index
        self.set_current_event(index, EventType.PAGE_REPLACEMENT, page)

def main():
    page_sequence = [7, 0, 1, 2, 0, 3, 0, 4,
                     2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3
    page_count = 20
    hybrid = Hybrid(page_sequence, frame_count, page_count)

if __name__ == "__main__":
    main()