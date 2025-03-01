"""
Program to generate an instance of SPA-P
Student Project Allocation with Student and Lecturer preferences over projects
"""

import numpy as np
import random
import math

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.abstractInstanceGenerator import AbstractInstanceGenerator


class SPAPIG_Euclidean(AbstractInstanceGenerator):
    def __init__(
            self,
            num_students,
            lower_bound,
            upper_bound,
            num_projects,
            num_lecturers,
            num_dimensions=5,
    ):
        super().__init__(num_students, lower_bound, upper_bound, num_projects, num_lecturers)
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
                )
            ))
    

    def _generate_lecturers(self):
        upper_bound_lecturers = math.floor(self._num_projects / self._num_lecturers)
        project_list = list(self._plc.keys())

        lecturer_num_projects = {}
        total_projects = 0

        for lec in self._lp:
            num_projects = random.randint(1, upper_bound_lecturers)
            lecturer_num_projects[lec] = num_projects
            total_projects += num_projects

        # while some projects are unassigned
        while total_projects < self._num_projects:
            lec = random.choice(self._lp.keys())
            lecturer_num_projects[lec] += 1
            total_projects += 1

        for i in range(self._num_lecturers):
            for p in list(map(
                self.to_project_string,
                np.argsort(
                    np.linalg.norm(
                        self._project_points - self._lecturer_points[i],
                        axis=1
                    )
                )[:lecturer_num_projects[lec]]
            )):
                p = random.choice(project_list)
                project_list.remove(p)
                self._assign_project_lecturer(p, f'l{i+1}')

        # decide capacity
        for i, lecturer in enumerate(self._lp):
            if self._force_lecturer_capacity:
                self._lp[lecturer][0] = self._force_lecturer_capacity
            else:
                self._lp[lecturer][0] = random.randint(self._lp[lecturer][2], self._lp[lecturer][3])


    def generate_instance(self):
        self._student_points = self._sample_points(self._num_students)
        self._project_points = self._sample_points(self._num_projects)
        self._lecturer_points = self._sample_points(self._num_lecturers)

        super().generate_instance()
