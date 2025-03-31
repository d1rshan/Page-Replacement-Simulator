import page as p
import frames as f
from EventType import EventType


class LRU(p.Page):
    def __init__(self, page_sequence, frame_count, page_count):
        super().__init__(page_sequence, frame_count, page_count)
        self.frames = []
        for i in range(frame_count):
            self.frames.append(LRU_Frames(i, page_count))
        self.lru()

    def lru(self):
        """
        Simulates the LRU algorithm.
        """
        index = 0
        for page in self.page_sequence:
            # Check if page is in a frame
            if self.check_for_page(page):
                self.page_hit_events(index)
                self.frames[self.find_page(page)].update_last_used(index)
            # Check if there is an empty frame
            elif self.check_for_empty_frame():
                self.page_fault_events(index)
                self.add_page_to_empty_frame(page, index)
            # If there is no empty frame and page is not in a frame
            # Find the oldest page and replace it
            else:
                self.page_fault_events(index)
                self.page_replacement_event(
                    index, page, self.find_least_recently_used())

            index += 1

        self.calculate_rates()
        self.print_lru_table()

    def find_least_recently_used(self):
        least_recently_used = self.frames[0]
        for frame in self.frames:
            if frame.get_last_used() < least_recently_used.get_last_used():
                least_recently_used = frame
            # elif frame.get_last_used() == least_recently_used.get_last_used():
            #     if frame.get_frame_current_page_birth() < least_recently_used.get_frame_current_page_birth():
            #         least_recently_used = frame
        return least_recently_used.get_frame_id()

    def print_lru_table(self):
        """
        Prints the LRU table.
        """
        print(f"+------------+")
        print(f"| LRU TABLE  |", )

        self.print_sequence()
        self.print_frames()
        self.print_rates()


class LRU_Frames(f.Frame):
    def __init__(self, frame_count, event_count):
        super().__init__(frame_count, event_count)
        self.last_used = -1

    # Override
    def update_last_used(self, index):
        self.last_used = index

    def get_last_used(self):
        return self.last_used

    def set_last_used(self, last_used):
        self.last_used = last_used

    # Page Replacement (This situation means this frame's page is being replaced)
    def replace_page(self, page, index):
        self.frame_current_page = page
        self.frame_current_page_age = 0
        self.frame_current_page_birth = index
        self.last_used = index
        self.set_current_event(index, EventType.PAGE_REPLACEMENT, page)


def main():
    # page_sequence = [7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7]
    # frame_count = 3
    # page_count = 17

    page_sequence = [7, 0, 1, 2, 0, 3, 0, 4,
                     2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3
    page_count = 20
    lru = LRU(page_sequence, frame_count, page_count)


if __name__ == "__main__":
    main()
