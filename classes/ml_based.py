import page as p
import frames as f
from EventType import EventType
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from collections import Counter


class MLBased(p.Page):
    def __init__(self, page_sequence, frame_count, page_count):  # Fixed method name and parameters
        super().__init__(page_sequence, frame_count, page_count)
        self.frames = []
        for i in range(frame_count):
            self.frames.append(ML_Frame(i, page_count))

        self.k = 3  # Window size for prediction
        self.model = DecisionTreeClassifier()

        # Only train if we have enough data
        if len(page_sequence) > self.k:
            self.train_model()
        self.ml_based()

    def train_model(self):
        X = []
        y = []
        for i in range(len(self.page_sequence) - self.k):
            X.append(self.page_sequence[i:i+self.k])
            y.append(self.page_sequence[i+self.k])
        
        # Reshape X if necessary
        X = np.array(X)
        y = np.array(y)
        self.model.fit(X, y)

    def predict_next_page(self, context):
        if len(context) < self.k:
            return None
        context = context[-self.k:]
        try:
            context_array = np.array([context])
            return self.model.predict(context_array)[0]
        except:
            return None

    def ml_based(self):
        index = 0
        history = []

        for page in self.page_sequence:
            history.append(page)

            if self.check_for_page(page):
                self.page_hit_events(index)
            elif self.check_for_empty_frame():
                self.page_fault_events(index)
                self.add_page_to_empty_frame(page, index)
            else:
                self.page_fault_events(index)

                if len(history) > self.k:
                    predicted_next = self.predict_next_page(history[:-1])
                else:
                    predicted_next = None

                if predicted_next is None:
                    frame_id = self.find_oldest_page()
                else:
                    frame_id = self.least_similar_to_prediction(predicted_next)

                self.page_replacement_event(index, page, frame_id)

            index += 1

        self.calculate_rates()
        self.print_ml_table()

    def least_similar_to_prediction(self, predicted_next):
        similarities = {}
        for frame in self.frames:
            page = frame.get_frame_current_page()
            similarities[frame.get_frame_id()] = int(page == predicted_next)

        return min(similarities, key=similarities.get)

    def print_ml_table(self):
        print(f"+------------------------+")
        print(f"| ML-Based Prediction    |")
        self.print_sequence()
        self.print_frames()
        self.print_rates()


class ML_Frame(f.Frame):
    def __init__(self, frame_id, event_count):  # Fixed method name
        super().__init__(frame_id, event_count)

    def replace_page(self, page, index):
        self.frame_current_page = page
        self.frame_current_page_age = 0
        self.frame_current_page_birth = index
        self.set_current_event(index, EventType.PAGE_REPLACEMENT, page)


def main():
    # This is just for testing
    page_sequence = [7, 0, 1, 2, 0, 3, 0, 4,
                     2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3
    page_count = len(page_sequence)
    ml_algo = MLBased(page_sequence, frame_count, page_count)


if __name__ == "__main__":
    main()