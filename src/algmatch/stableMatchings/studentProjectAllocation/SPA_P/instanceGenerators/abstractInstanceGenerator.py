"""
Abstract Instance Generators
Student Project Allocation with Lecturer preferences over projects (SPA-P).
"""

from abc import ABC, abstractmethod
import math
import random


class AbstractInstanceGenerator(ABC):
    def __init__(self, num_students, lower_bound, upper_bound, num_projects, num_lecturers, force_project_capacity=0, force_lecturer_capacity=0) -> None:
        assert lower_bound <= upper_bound, "Lower bound must be less than or equal to upper bound."
        assert upper_bound <= num_projects, "Upper bound must be less than or equal to the number of projects."

        self._num_students = num_students
        self._num_projects = num_projects
        self._num_lecturers = num_lecturers

        self._force_project_capacity = force_project_capacity
        self._force_lecturer_capacity = force_lecturer_capacity
        self._total_project_capacity = int(math.ceil(1.1 * self._num_students))

        self._li = lower_bound # lower bound of student preference list
        self._lj = upper_bound # upper bound of student preference list

        self._sp = {f's{i}' : [] for i in range(1, self._num_students+1)} # student -> [project preferences]
        self._plc = {f'p{i}' : [1, ''] for i in range(1, self._num_projects+1)} # project -> [capacity, lecturer]
        self._lp = {f'l{i}' : [0, [], 0, 0] for i in range(1, self._num_lecturers+1)} # lecturer -> [capacity, project preferences, max of all c_j, sum of all c_j]


    def _assign_project_lecturer(self, project, lecturer):
        self._plc[project][1] = lecturer
        self._lp[lecturer][1].append(project)
        self._lp[lecturer][3] += self._plc[project][0] # track sum of all c_j
        if self._plc[project][0] > self._lp[lecturer][2]: # track max of all c_j
            self._lp[lecturer][2] = self._plc[project][0]


    def _generate_projects(self):
        """
        Generates projects for the SPA-P problem.
        """
        project_list = list(self._plc.keys())
        if self._force_project_capacity:
            for project in self._plc:
                self._plc[project][0] = self._force_project_capacity
        else:
            # randomly assign remaining project capacities
            for _ in range(self._total_project_capacity - self._num_projects):
                    self._plc[random.choice(project_list)][0] += 1


    @abstractmethod
    def _generate_students(self):
        """
        Generates students for the SPA-P problem.
        """
        raise NotImplementedError


    @abstractmethod
    def _generate_lecturers(self):
        """
        Generates lecturers for the SPA-P problem.
        """
        raise NotImplementedError

    
    def generate_instance(self) -> None:
        """
        Generates a random instance for the SPA-P problem.
        Stores details in self._sp, self._plc, self._lp.
        """
        self._generate_projects()
        self._generate_students()
        self._generate_lecturers()


    def write_instance_to_file(self, filename: str) -> None:
        """
        Writes instances to filename specified.
        """
        if filename.endswith('.txt'): delim = ' '
        elif filename.endswith('.csv'): delim = ','

        with open (filename, 'w') as f:
            f.write(delim.join(map(str, [self._num_students, self._num_projects, self._num_lecturers])) + '\n')

            # student index, preferences
            for student in self._sp:
                f.write(delim.join(map(str, [student[1:], delim.join([p[1:] for p in self._sp[student]])]))+"\n")

            # project index, capacity, lecturer
            for project in self._plc:
                f.write(delim.join(map(str, [project[1:], self._plc[project][0], self._plc[project][1][1:]])) + "\n")

            # lecturer index, capacity, projects
            for lecturer in self._lp:
                f.write(delim.join(map(str, [lecturer[1:], self._lp[lecturer][0], delim.join([p[1:] for p in self._lp[lecturer][1]])])) + "\n")
