class MovingAverage:
    def __init__(self, size):
        self.size = size
        self.data = []

    def add(self, value):
        self.data.append(value)
        if len(self.data) > self.size:
            self.data.pop(0)  # remove oldest value

    def average(self):
        return sum(self.data) / len(self.data)
