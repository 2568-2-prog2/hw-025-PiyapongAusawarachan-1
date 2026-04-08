import random

class Dice:
    def __init__(self, probabilities):
        self._validate_probabilities(probabilities)
        self.probabilities = probabilities
        self.faces = [1, 2, 3, 4, 5, 6]

    def _validate_probabilities(self, probabilities):
        if not isinstance(probabilities, list):
            raise TypeError("Probabilities must be a list")

        if len(probabilities) != 6:
            raise ValueError("Must have exactly 6 probabilities")

        if any(p < 0 for p in probabilities):
            raise ValueError("Probabilities cannot be negative")

        if abs(sum(probabilities) - 1.0) > 1e-6:
            raise ValueError("Probabilities must sum to 1")

    def roll_once(self):
        return random.choices(self.faces, weights=self.probabilities, k=1)[0]

    def roll(self, n):
        if not isinstance(n, int):
            raise TypeError("Number of rolls must be an integer")

        if n < 0:
            raise ValueError("Number of rolls must be non-negative")

        return random.choices(self.faces, weights=self.probabilities, k=n)

    def get_probabilities(self):
        return self.probabilities