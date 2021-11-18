from typing import Optional

import numpy as np


class SeedMixin:
    """Adds working with ._seed and ._original_seed for reproducibility."""

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value: int):
        self._original_seed = value
        self._seed = value

    def reset_seed(self):
        """Reset the seed to the original seed value, and return self."""
        self._seed = self._original_seed
        return self

    def set_seed(self, seed: Optional[int] = None):
        """Set the current seed and original seed to a new value, and return self.

        Args:
            seed (Optional[int], optional): Seed value. If None, select a random seed. Defaults to None.
        """
        if seed is None:
            seed = np.random.randint(100000)
        self._original_seed = seed
        return self.reset_seed()


class CaseMixin:
    """Adds working with title-, sentence-, upper- and lowercase for random data generation."""

    def lower(self):
        """Switch to lowercase data generation, and return self."""
        self._lowercase = True
        self._sentencecase = False
        self._titlecase = False
        self._uppercase = False
        return self

    def sentence(self):
        """Switch to sentencecase data generation, and return self."""
        self._lowercase = False
        self._sentencecase = True
        self._titlecase = False
        self._uppercase = False
        return self

    def title(self):
        """Switch to titlecase data generation, and return self."""
        self._lowercase = False
        self._sentencecase = False
        self._titlecase = True
        self._uppercase = False
        return self

    def upper(self):
        """Switch to uppercase data generation, and return self."""
        self._lowercase = False
        self._sentencecase = False
        self._titlecase = False
        self._uppercase = True
        return self

    def original(self):
        """Switch to original case data generation, and return self."""
        self._lowercase = False
        self._sentencecase = False
        self._titlecase = False
        self._uppercase = False
        return self

    def apply_case(self, string):
        """Apply the selected case to a string."""
        if not isinstance(string, str) or string.isnumeric():
            return string

        if self._lowercase:
            return string.lower()
        elif self._sentencecase:
            return string.capitalize()
        elif self._titlecase:
            return string.title()
        elif self._uppercase:
            return string.upper()
        return string
