"""
Program to generate an instance of SPA-P
Student Project Allocation with Student and Lecturer preferences over projects
"""

import random
import math
import sys

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.instanceGenerators.abstractInstanceGenerator import AbstractInstanceGenerator


class SPAPIG_Random(AbstractInstanceGenerator):
    def _generate_students(self):
        for student in self._sp:
            length = random.randint(self._li, self._lj) # randomly decide length of preference list
            project_list = list(self._plc.keys())
            for _ in range(length):
                p = random.choice(project_list)
                project_list.remove(p) # avoid picking same project twice
                self._sp[student].append(p)


    def _generate_lecturers(self):
        lecturer_list = list(self._lp.keys())

        # number of projects lecturer can offer is between 1 and ceil(|projects| / |lecturers|)
        # done to ensure even distribution of projects amongst lecturers
        upper_bound = math.floor(self._num_projects / self._num_lecturers)
        project_list = list(self._plc.keys())

        for lecturer in self._lp:
            num_projects = random.randint(1, upper_bound)
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
        for lecturer in self._lp:
            random.shuffle(self._lp[lecturer][1])
            if self._force_lecturer_capacity:
                self._lp[lecturer][0] = self._force_lecturer_capacity
            else:
                self._lp[lecturer][0] = random.randint(self._lp[lecturer][2], self._lp[lecturer][3])


def main():
    try:
        students = int(sys.argv[1])
        lower_bound = int(sys.argv[2])
        upper_bound = int(sys.argv[3])
        output_file = sys.argv[4]

    except (IndexError, ValueError):
        print("Usage: python instanceGenerator.py <num_students[int]> <lower_bound[int]> <upper_bound[int]> <output_file>")
        sys.exit(1)

    S = SPAPIG_Random(students, lower_bound, upper_bound)
    S.generate_instance()
    S.write_instance_to_file(output_file)


if __name__ == "__main__":
    main()
