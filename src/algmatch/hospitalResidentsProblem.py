"""
Class to provide interface for the Hospital/Residents Problem algorithm.
"""

import os

from algmatch.stableMatchings.hospitalResidentsProblem.hrResidentOptimal import HRResidentOptimal
from algmatch.stableMatchings.hospitalResidentsProblem.hrHospitalOptimal import HRHospitalOptimal


class HospitalResidentsProblem:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None, optimisedSide: str = "residents") -> None:
        """
        Initialise the Stable Marriage Problem algorithm.

        :param filename: str, optional, default=None, the path to the file to read in the preferences from.
        :param dictionary: dict, optional, default=None, the dictionary of preferences.
        :param optimisedSide: str, optional, default="resident", whether the algorithm is "resident" (default) or "hospital" sided.
        """
        if filename is not None:
            filename = os.path.join(os.getcwd(), filename)

        assert type(optimisedSide) is str, "Param optimisedSide must be of type str"
        optimisedSide = optimisedSide.lower()
        assert optimisedSide in ("residents", "hospitals"), "Optimised side must either be 'residents' or 'hospitals'"

        if optimisedSide == "residents":
            self.hr = HRResidentOptimal(filename=filename, dictionary=dictionary)
        else:
            self.hr = HRHospitalOptimal(filename=filename, dictionary=dictionary)


    def get_stable_matching(self) -> dict | None:
        """
        Get the stable matching for the Hospital/Residents Problem algorithm.

        :return: dict, the stable matching for this instance
        """
        self.hr.run()
        if self.hr.is_stable:
            return self.hr.stable_matching
        return None