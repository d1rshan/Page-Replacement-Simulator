import page as p
import frames as f
from EventType import EventType


class LFU(p.Page):
    def __init__(self, page_sequence, frame_count, page_count):
        super().__init__(page_sequence, frame_count, page_count)
        self.frames = []
        for i in range(frame_count):
            self.frames.append(LFU_Frames(i, page_count))
        self.lfu()

    def lfu(self):
        """
        Simulates the LFU algorithm.
        """
        index = 0
        for page in self.page_sequence:
            # Check if page is in a frame
            if self.check_for_page(page):
                self.page_hit_events(index)
                self.frames[self.find_page(page)].increment_page_frequency()
            # Check if there is an empty frame
            elif self.check_for_empty_frame():
                self.page_fault_events(index)
                self.add_page_to_empty_frame(page, index)
            # If there is no empty frame and page is not in a frame
            # Find the oldest page and replace it
            else:
                self.page_fault_events(index)
                self.page_replacement_event(
                    index, page, self.find_least_frequently_used())

            index += 1

        self.calculate_rates()
        self.print_lfu_table()

    def find_least_frequently_used(self):
        least_frequently_used = self.frames[0]
        for frame in self.frames:
            if frame.get_page_frequency() < least_frequently_used.get_page_frequency():
                least_frequently_used = frame
            elif frame.get_page_frequency() == least_frequently_used.get_page_frequency():
                if frame.get_frame_current_page_birth() < least_frequently_used.get_frame_current_page_birth():
                    least_frequently_used = frame
        return least_frequently_used.get_frame_id()

    def print_lfu_table(self):
        """
        Prints the LFU table.
        """
        print(f"+------------+")
        print(f"| LFU TABLE  |", )

        self.print_sequence()
        self.print_frames()
        self.print_rates()


class LFU_Frames(f.Frame):
    def __init__(self, frame_count, event_count):
        super().__init__(frame_count, event_count)
        self.page_frequency = 0

    def get_page_frequency(self):
        return self.page_frequency

    def increment_page_frequency(self):
        self.page_frequency += 1

    def replace_page(self, page, index):
        self.frame_current_page = page
        self.frame_current_page_age = 0
        self.frame_current_page_birth = index
        self.page_frequency = 0
        self.set_current_event(index, EventType.PAGE_REPLACEMENT, page)


def main():
    # page_sequence = [7, 0, 1, 2, 0, 3, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7]
    # frame_count = 3
    # page_count = 17

    page_sequence = [7, 0, 1, 2, 0, 3, 0, 4,
                     2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3
    page_count = 20
    lfu = LFU(page_sequence, frame_count, page_count)


if __name__ == "__main__":
    main()
