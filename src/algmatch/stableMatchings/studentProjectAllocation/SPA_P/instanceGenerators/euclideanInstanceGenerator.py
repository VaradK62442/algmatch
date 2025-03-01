"""
Program to generate an instance of SPA-P
Student Project Allocation with Student and Lecturer preferences over projects
"""

import numpy as np
import random

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.abstractInstanceGenerator import AbstractInstanceGenerator


class SPAPIG_Euclidean(AbstractInstanceGenerator):
    def __init__(
            self,
            num_dimensions=5,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self._num_dimesions = num_dimensions
        self.to_project_string = lambda x: f'p{x+1}'


    def _sample_points(self, num_points: int):
        return np.random.uniform(0, 1, (num_points, self._num_dimesions))


    def _generate_students(self):
        for i, student_point in enumerate(self._student_points):
            self._sp[f's{i+1}'] = list(map(
                self.to_project_string,
                np.argsort(
                    np.linalg.norm(
                        self._project_points - student_point,
                        axis=1
                    )
                )[:random.randint(self._li, self._lj)]
            ))


    def _generate_lecturers(self):
        lecturer_list = list(self._lp.keys())

        upper_bound_lecturers = self._num_projects // self._num_lecturers
        project_list = list(self._plc.keys())

        for lecturer in self._lp:
            num_projects = random.randint(1, upper_bound_lecturers)
            for _ in range(num_projects):
                p = random.choice(project_list)
                project_list.remove(p)
                self._assign_project_lecturer(p, lecturer)

        # while some projects are unassigned
        while project_list:
            p = random.choice(project_list)
            project_list.remove(p)
            lecturer = random.choice(lecturer_list)
            self._assign_project_lecturer(p, lecturer)

        # decide ordered preference and capacity
        for i, lecturer in enumerate(self._lp):
            ordered_project_list = list(map(
                self.to_project_string,
                np.argsort(
                    np.linalg.norm(
                        self._project_points - self._lecturer_points[i],
                        axis=1
                    )
                )
            ))
            self._lp[lecturer][1] = [p for p in ordered_project_list if p in self._lp[lecturer][1]]

            if self._force_lecturer_capacity:
                self._lp[lecturer][0] = self._force_lecturer_capacity
            else:
                self._lp[lecturer][0] = random.randint(self._lp[lecturer][2], self._lp[lecturer][3])


    def generate_instance(self):
        self._student_points = self._sample_points(self._num_students)
        self._project_points = self._sample_points(self._num_projects)
        self._lecturer_points = self._sample_points(self._num_lecturers)

        super().generate_instance()
