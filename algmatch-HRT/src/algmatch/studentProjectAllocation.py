"""
Class to provide interface for the Student Project Allocation stable matching algorithm.
"""

import os

from stableMatchings.studentProjectAllocation.spaStudentOptimal import SPAStudentOptimal
from stableMatchings.studentProjectAllocation.spaLecturerOptimal import SPALecturerOptimal


class StudentProjectAllocation:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None, studentSided: bool = True) -> None:
        """
        Initialise the Student Project Allocation algorithm.

        :param filename: str, optional, default=None, the path to the file to read in the preferences from.
        :param dictionary: dict, optional, default=None, the dictionary of preferences.
        :param studentSided: bool, optional, default=True, whether the algorithm is student (default) or lecturer sided.        
        """
        if filename is not None:
            filename = os.path.join(os.path.dirname(__file__), filename)

        self.spa = SPAStudentOptimal(filename=filename, dictionary=dictionary) if studentSided else SPALecturerOptimal(filename=filename, dictionary=dictionary)


    def get_stable_matching(self) -> dict:
        """
        Get the stable matching for the Student Project Allocation algorithm.

        :return: dict, the stable matching.
        """
        self.spa.run()
        return self.spa.stable_matching