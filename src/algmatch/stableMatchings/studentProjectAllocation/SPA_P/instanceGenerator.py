"""
Program to generate an instance of SPA-P
Student Project Allocation with Student and Lecturer preferences over projects
"""

import random
import math
import sys


class SPAPIG:
    def __init__(self, num_students, lower_bound, upper_bound) -> None:
        self._num_students = num_students
        self._num_projects = int(math.ceil(self._num_students / 2))
        self._num_lecturers = int(math.ceil(self._num_students / 5)) # assume |lecturers| < |projects|

        self._total_project_capacity = int(math.ceil(1.1 * self._num_students))
        self._li = lower_bound # lower bound of student preference list
        self._lj = upper_bound # upper bound of student preference list

        self._sp = {'s'+str(i) : [] for i in range(1, self._num_students+1)} # student -> [project preferences]
        self._plc = {'p'+str(i) : [1, ''] for i in range(1, self._num_projects+1)} # project -> [capacity, lecturer]
        self._lp = {'l'+str(i) : [0, [], 0, 0] for i in range(1, self._num_lecturers+1)} # lecturer -> [capacity, project preferences, max of all c_j, sum of all c_j]


    def _assign_project_lecturer(self, project, lecturer):
        self._plc[project][1] = lecturer
        self._lp[lecturer][1].append(project)
        self._lp[lecturer][3] += self._plc[project][0] # track sum of all c_j
        if self._plc[project][0] > self._lp[lecturer][2]: # track max of all c_j
            self._lp[lecturer][2] = self._plc[project][0]


    def generate_instance(self):
        """
        Generates a random instance for the SPA-P problem.
        """
        # PROJECTS
        project_list = list(self._plc.keys())
        # randomly assign remaining project capacities
        for _ in range(self._total_project_capacity - self._num_projects):
            self._plc[random.choice(project_list)][0] += 1

        # STUDENTS
        for student in self._sp:
            length = random.randint(self._li, self._lj) # randomly decide length of preference list
            projects_copy = project_list[:]
            for _ in range(length):
                p = random.choice(projects_copy)
                projects_copy.remove(p) # avoid picking same project twice
                self._sp[student].append(p)

        # LECTURERS
        lecturer_list = list(self._lp.keys())
        
        # number of projects lecturer can offer is between 1 and ceil(|projects| / |lecturers|)
        # done to ensure even distribution of projects amongst lecturers
        upper_bound = math.floor(self._num_projects / self._num_lecturers)
        projects_copy = project_list[:]

        for lecturer in self._lp:
            num_projects = random.randint(1, upper_bound)
            for _ in range(num_projects):
                p = random.choice(projects_copy)
                projects_copy.remove(p)
                self._assign_project_lecturer(p, lecturer)

        # while some projects are unassigned
        while projects_copy:
            p = random.choice(projects_copy)
            projects_copy.remove(p)
            lecturer = random.choice(lecturer_list)
            self._assign_project_lecturer(p, lecturer)

        # decide ordered preference and capacity
        for lecturer in self._lp:
            random.shuffle(self._lp[lecturer][1])
            self._lp[lecturer][0] = random.randint(self._lp[lecturer][2], self._lp[lecturer][3])


    def write_instance_to_file(self, filename: str) -> None:
        with open (filename, 'w') as f:
            f.write(f"{self._num_students} {self._num_projects} {self._num_lecturers}\n")

            # student index, preferences
            for student in self._sp:
                f.write(f"{student[1:]} {' '.join([p[1:] for p in self._sp[student]])}\n")

            # project index, capacity, lecturer
            for project in self._plc:
                f.write(f"{project[1:]} {self._plc[project][0]} {self._plc[project][1][1:]}\n")

            # lecturer index, capacity, projects
            for lecturer in self._lp:
                f.write(f"{lecturer[1:]} {self._lp[lecturer][0]} {' '.join([p[1:] for p in self._lp[lecturer][1]])}\n")


def main():
    try:
        students = int(sys.argv[1])
        lower_bound = int(sys.argv[2])
        upper_bound = int(sys.argv[3])
        output_file = sys.argv[4]

    except (IndexError, ValueError):
        print("Usage: python instanceGenerator.py <num_students[int]> <lower_bound[int]> <upper_bound[int]> <output_file>")
        sys.exit(1)

    S = SPAPIG(students, lower_bound, upper_bound)
    S.generate_instance()
    S.write_instance_to_file(output_file)

if __name__ == "__main__":
    main()