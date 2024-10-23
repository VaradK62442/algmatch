"""
Class to provide interface for the Stable Marriage Problem algorithm.
"""

import os

from stableMatchings.stableMarriageProblem.smManOptimal import SMManOptimal
from stableMatchings.stableMarriageProblem.smWomanOptimal import SMWomanOptimal


class StableMarriageProblem:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None, optimisedSide: str = "men") -> None:
        """
        Initialise the Stable Marriage Problem algorithm.

        :param filename: str, optional, default=None, the path to the file to read in the preferences from.
        :param dictionary: dict, optional, default=None, the dictionary of preferences.
        :param optimisedSide: str, optional, default="men"
        """
        if filename is not None:
            filename = os.path.join(os.path.dirname(__file__), filename)

        assert type(optimisedSide) == str, "Param optimisedSide must be of type str"
        optimisedSide = optimisedSide.lower()
        assert optimisedSide == "men" or optimisedSide == "women", "Optimised side must either be 'men' or 'women'"
        if optimisedSide == "men":
            self.sm = SMManOptimal(filename=filename, dictionary=dictionary)
        else:
            self.sm = SMWomanOptimal(filename=filename, dictionary=dictionary)


    def get_stable_matching(self) -> dict:
        """
        :return: dict, the stable matching.
        """
        self.sm.run()
        return self.sm.stable_matching