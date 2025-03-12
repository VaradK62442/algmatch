"""
Class to provide interface for the Hospital/Residents Problem With Ties algorithm.
"""

import os

from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtSuperResidentOptimal import (
    HRTSuperResidentOptimal,
)
from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtSuperHospitalOptimal import (
    HRTSuperHospitalOptimal,
)
from algmatch.stableMatchings.hospitalResidentsProblem.ties.hrtAbstract import (
    HRTAbstract,
)


class HospitalResidentsProblemWithTies:
    def __init__(
        self,
        filename: str | None = None,
        dictionary: dict | None = None,
        optimised_side: str = "residents",
        stability_type: str = None,
    ) -> None:
        """
        Initialise the Hospital Residents Problem With Ties algorithms.

        :param filename: str, optional, default=None, the path to the file to read in the preferences from.
        :param dictionary: dict, optional, default=None, the dictionary of preferences.
        :param optimised_side: str, optional, default="resident", whether the algorithm is "resident" (default) or "hospital" sided.
        """
        if filename is not None:
            filename = os.path.join(os.getcwd(), filename)

        self._validate_and_save_parameters(
            filename, dictionary, optimised_side, stability_type
        )
        self._set_algorithm()

    def _assert_valid_optimised_side(self, optimised_side):
        assert type(optimised_side) is str, "Param optimised_side must be of type str"
        optimised_side = optimised_side.lower()
        assert optimised_side in ("residents", "hospitals"), (
            "Optimised side must either be 'residents' or 'hospitals'"
        )

    def _validate_and_save_parameters(
        self, filename, dictionary, optimised_side, stability_type
    ):
        self._assert_valid_optimised_side(optimised_side)
        self.optimised_side = optimised_side.lower()

        HRTAbstract._assert_valid_stability_type(stability_type)
        self.stability_type = stability_type.lower()

        self.filename = filename
        self.dictionary = dictionary

    def _set_algorithm(self):
        if self.stability_type == "super":
            if self.optimised_side == "residents":
                self.hr_alg = HRTSuperResidentOptimal(
                    filename=self.filename, dictionary=self.dictionary
                )
            else:
                self.hr_alg = HRTSuperHospitalOptimal(
                    filename=self.filename, dictionary=self.dictionary
                )
        elif self.stability_type == "strong":
            raise NotImplementedError("Strong algorithms are not yet available.")
        else:
            raise ValueError('stability_type must be either "strong" or "super".')

    def get_stable_matching(self) -> dict | None:
        """
        Get the stable matching for the Hospital/Residents Problem With Ties algorithm.

        :return: dict, the stable matching for this instance
        """
        self.hr_alg.run()
        if self.hr_alg.is_stable:
            return self.hr_alg.stable_matching
        return None
