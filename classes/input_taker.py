class SequenceTaker:
    """
    Represents a class that will take the sequence of page references and the number of frames in physical memory.

    Attributes:
        sequence (list): The sequence of page references.
        frames (int): The number of frames in physical memory.
        process_count (int): The number of processes.
    """

    def __init__(self, file_name):
        self.sequence = []
        self.frames = 0
        self.process_count = 0
        self.file_name = file_name

    def take_sequence(self):
        """
        Takes the sequence of page references and the number of frames in physical memory.
        """
        with open(self.file_name, "r") as file:
            self.process_count = int(file.readline())
            self.sequence = file.readline().split()
            self.frames = int(file.readline())
            self.sequence = [int(i) for i in self.sequence]
        return self.sequence, self.frames, self.process_count

    def take_sequence_from_user(self):
        """
        Takes the sequence of page references and the number of frames in physical memory.
        """
        self.process_count = int(input("Enter the number of processes: "))
        self.sequence = input("Enter the sequence of page references: ").split()
        self.frames = int(input("Enter the number of frames in physical memory: "))
        self.sequence = [int(i) for i in self.sequence]
        return self.sequence, self.frames, self.process_count
    
    def retake_sequence(self, file_name):
        """
        Retakes the inputs with a new file name
        """
        self.file_name = file_name
        self.take_sequence()

    def print_sequence(self):
        """
        Prints the sequence of page references and the number of frames in physical memory.
        """
        print(self.sequence)
        print(self.frames)
        print(self.process_count)