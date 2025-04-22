import frames as f
import shutil
term_width = shutil.get_terminal_size().columns
chunk_size = max(5, (term_width - 15) // 6)




class Page:
    def __init__(self, page_sequence, frame_count, page_count):
        self.page_sequence = page_sequence
        self.page_count = page_count
        self.frame_count = frame_count

        self.frames = []
        for i in range(frame_count):
            self.frames.append(f.Frame(i, page_count))

        self.page_faults = 0
        self.page_hits = 0
        self.page_fault_rate = 0.0
        self.page_hit_rate = 0.0

    # Getters
    def get_page_faults(self):
        return self.page_faults

    def get_page_hits(self):
        return self.page_hits

    def get_page_fault_rate(self):
        return self.page_fault_rate

    def get_page_hit_rate(self):
        return self.page_hit_rate

    # Unique methods
    def increment_page_faults(self):
        self.page_faults += 1

    def increment_page_hits(self):
        self.page_hits += 1

    def calculate_rates(self):
        self.page_fault_rate = self.page_faults / len(self.page_sequence)
        self.page_hit_rate = self.page_hits / len(self.page_sequence)

    # Methods for Frames control
    # Check every frame for same page
    def check_for_page(self, page):
        for frame in self.frames:
            if frame.is_equal_to(page):
                return True
        return False

    # Check for empty frame
    def check_for_empty_frame(self):
        for frame in self.frames:
            if frame.is_empty():
                return True
        return False

    # Add page to empty frame
    def add_page_to_empty_frame(self, page, index):
        for frame in self.frames:
            if frame.is_empty():
                frame.replace_page(page, index)
                return

    # Find the frame with the same page and return its index
    def find_page(self, page):
        for frame in self.frames:
            if frame.is_equal_to(page):
                return frame.get_frame_id()
        return -1

    # Page Hit
    def page_hit_events(self, index):
        for frame in self.frames:
            frame.page_hit(index)
        self.increment_page_hits()

    # Page Fault
    def page_fault_events(self, index):
        for frame in self.frames:
            frame.page_fault(index)
        self.increment_page_faults()

    # Page Replacement
    def page_replacement_event(self, index, page, frame_id):
        self.frames[frame_id].replace_page(page, index)

    # Find the oldest page from the frames and return its index
    def find_oldest_page(self):
        oldest_page = self.frames[0]
        for frame in self.frames:
            if frame.get_frame_current_page_birth() < oldest_page.get_frame_current_page_birth():
                oldest_page = frame
        return oldest_page.get_frame_id()

    # Print methods
    def print_sequence(self):
        chunk_size = 15
        for chunk_start in range(0, len(self.page_sequence), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(self.page_sequence))
            chunk = self.page_sequence[chunk_start:chunk_end]

            print(f"+------------+", end="")
            for _ in chunk:
                print("-----+", end="")
            print(f"\n| \033[94mPCount: {self.page_count:<2}\033[0m |", end="")
            for page in chunk:
                print(f"  \033[94m{page:<3}\033[0m|", end="")
            print(f"\n+------------+", end="")
            for _ in chunk:
                print("-----+", end="")
            print()

    def print_frames(self):
        chunk_size = 15
        for chunk_start in range(0, len(self.page_sequence), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(self.page_sequence))
            for frame in self.frames:
                print(f"\n| Frame {frame.get_frame_id()+1:<3}  |", end="")
                for i in range(chunk_start, chunk_end):
                    event = frame.events[i]
                    if event.get_event_type() == f.EventType.NOT_USED or event.get_event_data() == -1:
                        print(f"  -  |", end="")
                    else:
                        data = str(event.get_event_data())
                        if event.get_event_data() == self.page_sequence[i]:
                            if event.get_event_type() == f.EventType.PAGE_HIT:
                                print(f" \033[92m {data:<3}\033[0m|", end="")
                            elif event.get_event_type() in [f.EventType.PAGE_FAULT, f.EventType.PAGE_REPLACEMENT]:
                                print(f" \033[91m {data:<3}\033[0m|", end="")
                        else:
                            print(f"  {data:<3}|", end="")
                print(f"\n+------------+", end="")
                for _ in range(chunk_start, chunk_end):
                    print("-----+", end="")

            # Page Faults row
            print(f"\n| \033[91mPage F: {self.get_page_faults():<2}\033[0m |", end="")
            for i in range(chunk_start, chunk_end):
                event = self.frames[0].events[i]
                if event.get_event_type() in [f.EventType.PAGE_FAULT, f.EventType.PAGE_REPLACEMENT]:
                    print(f" \033[91m F \033[0m |", end="")
                else:
                    print(f"  -  |", end="")
            print(f"\n+------------+", end="")
            for _ in range(chunk_start, chunk_end):
                print("-----+", end="")

            # Page Hits row
            print(f"\n| \033[92mPage H: {self.get_page_hits():<2}\033[0m |", end="")
            for i in range(chunk_start, chunk_end):
                event = self.frames[0].events[i]
                if event.get_event_type() == f.EventType.PAGE_HIT:
                    print(f" \033[92m H \033[0m |", end="")
                else:
                    print(f"  -  |", end="")
            print(f"\n+------------+", end="")
            for _ in range(chunk_start, chunk_end):
                print("-----+", end="")
            print()


    def print_rates(self):
        fault_rate = "{:.2f}%".format(self.get_page_fault_rate()*100)
        hits_rate = "{:.2f}%".format(self.get_page_hit_rate() * 100)
        print(f"\n|  \033[91mFault Rate: {fault_rate:>9}\033[0m |", end="")
        print(f"\n+------------------------+", end="")
        print(f"\n|  \033[92mHits  Rate: {hits_rate:>9}\033[0m |", end="")
        print(f"\n+------------------------+", end="")
        print(f"\n")
