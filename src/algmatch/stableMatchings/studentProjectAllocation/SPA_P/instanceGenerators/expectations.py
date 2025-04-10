"""
Program to generate an instance of SPA-P - Expectations Euclidean
Student Project Allocation with Student and Lecturer preferences over projects
"""

import numpy as np

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.euclidean import SPAPIG_Euclidean


class SPAPIG_ExpectationsEuclidean(SPAPIG_Euclidean):
    def __init__(
            self,
            num_dimensions: int = 5,
            stdev: float = 0.5,
            **kwargs,
    ):
        super().__init__(num_dimensions=num_dimensions, **kwargs)
        self._stdev = stdev


    def sample_all_points(self):
        super().sample_all_points()

        self._project_points = np.random.normal(
            loc=self._project_points,
            scale=self._stdev,
        )
