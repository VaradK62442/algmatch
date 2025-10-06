from random import shuffle

from tests.abstractTestClasses.genericGeneratorInterface import (
    GenericGeneratorInterface,
)


class SRInstanceGenerator(GenericGeneratorInterface):
    def __init__(self, no_roommates):
        self.no_roommates = no_roommates
        assert isinstance(self.no_roommates, int) and self.no_roommates > 0, (
            "Number of men must be a postive integer."
        )

        self.instance = dict()

        # lists of numbers that will be shuffled to get preferences
        self.available_roommates = [i + 1 for i in range(self.no_roommates)]

    def _reset_instance(self):
        self.instance = {r: [] for r in self.available_roommates}

    def generate_instance(self):
        self._reset_instance()
        self._generate_lists()
        return self.instance

    def _generate_lists(self):
        for r, r_list in self.instance.items():
            shuffle(self.available_roommates)
            r_list.extend(self.available_roommates.copy())
            r_list.remove(r)
