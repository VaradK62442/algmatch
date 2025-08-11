"""
Instance Generator for SPA-ST
Student Project Allocation with Ties in student's list
"""

import random
import math


class SPASTGen:
    def __init__(self, num_students, lower_bound, upper_bound, num_projects, num_lecturers, student_tie_density=0, lecturer_tie_density=0):
        """
        A program that writes to a .txt file, a randomly-generated instance of the student project allocation problem 
        with students preferences over projects, lecturers preferences over students, and with ties.
        
        * the density of tie in the preference lists is a number between 0 and 1 (inclusive)
            - if the tie density is 0 on both sides, then the program writes an instance of SPA-S
            without ties
            - if the tie density is 1 on both sides, then the program writes an instance of SPA-ST,
            where each preference list is a single tie of length 1
        
        * the tie density given is the probability (decided at random) that a project (or student) will be tied
        with its successor.

        :param num_students: int, number of students
        :param lower_bound: int, lower bound of the students' preference list length
        :param upper_bound: int, upper bound of the students' preference list length
        :param num_projects: int, number of projects
        :param num_lecturers: int, number of lecturers
        :param student_tie_density: float, [0, 1], the density of tie in the students preference list 
        :param lecturer_tie_density: float, [0, 1], the density of tie in the lecturers preference list
        """

        self._num_students: int = num_students
        self._num_projects: int = num_projects
        self._num_lecturers: int = num_lecturers
        
        self._li: int = lower_bound  # lower bound of the student's preference list
        self._lj: int = upper_bound  # upper bound of the student's preference list
        self._total_project_capacity: int = int(math.ceil(1.1*self._num_students))

        self.student_tie_density = student_tie_density
        self.lecturer_tie_density = lecturer_tie_density

        self._reset_instance()


    def _reset_instance(self):
        self._sp = {f's{i}': [] for i in range(1, self._num_students + 1)}  # student -> [project preferences]
        self._plc = {f'p{i}': [1, '', []] for i in range(1, self._num_projects + 1)}  # project -> [capacity, lecturer, student]
        self._lp = {f'l{i}': [0, [], [], 0, 0] for i in range(1, self._num_lecturers + 1)}  # lecturer -> [capacity, projects, students, max of all c_j, sum of all c_j]


    def _assign_project_lecturer(self, project, lecturer):
        self._plc[project][1] = lecturer
        self._lp[lecturer][1].append(project)
        self._lp[lecturer][2] += self._plc[project][2] # track all students
        self._lp[lecturer][4] += self._plc[project][0] # track sum of all c_j
        if self._plc[project][0] > self._lp[lecturer][3]: # track max of all c_j
            self._lp[lecturer][3] = self._plc[project][0]


    def _generate_projects(self):
        project_list = list(self._plc.keys())
        for _ in range(self._total_project_capacity - self._num_projects):
            self._plc[random.choice(project_list)][0] += 1


    def _generate_students(self):
        for student in self._sp:
            length = random.randint(self._li, self._lj)
            project_list = list(self._plc.keys())
            for i in range(length):
                p = random.choice(project_list)
                project_list.remove(p)
                if i == 0 or random.uniform(0, 1) > self.student_tie_density:
                    self._sp[student].append([p])
                else:
                    self._sp[student][-1].append(p)
                self._plc[p][2].append(student)


    def _generate_lecturers(self):
        upper_bound = math.floor(self._num_projects / self._num_lecturers)
        project_list = list(self._plc.keys())

        for lecturer in self._lp:
            num_projects = random.randint(1, upper_bound)
            for _ in range(num_projects):
                p = random.choice(project_list)
                project_list.remove(p)
                self._assign_project_lecturer(p, lecturer)

        lecturer_list = list(self._lp.keys())
        while project_list:
            p = random.choice(project_list)
            project_list.remove(p)
            lecturer = random.choice(lecturer_list)
            self._assign_project_lecturer(p, lecturer)

        for lecturer in self._lp:
            pref = list(set(self._lp[lecturer][2][:]))
            if not pref: continue
            random.shuffle(pref)
            pref_with_ties = [[pref[0]]]

            for student in pref[1:]:
                if random.uniform(0, 1) <= self.lecturer_tie_density:
                    pref_with_ties[-1].append(student)
                else:
                    pref_with_ties.append([student])
            self._lp[lecturer][2] = pref_with_ties

            self._lp[lecturer][0] = random.randint(self._lp[lecturer][3], self._lp[lecturer][4])
                

    def generate_instance(self):
        self._reset_instance()
        self._generate_projects()
        self._generate_students()
        self._generate_lecturers()


    def _tied_list_to_string(self, l: list[list[str]], delim: str = ' ') -> str:
        """
        Take in a list of lists of strings that represents a tied preference list,
        and return a string representation of the list

        :param l: a list of lists of strings
        :return: a string representation of the list
        """
        return delim.join(
            list(map(
                lambda s: str(s).replace(',', ''),
                [
                    x
                    if len(x := tuple(map(lambda x: int(x[1:]), p))) > 1
                    else x[0] for p in l
                ]
            ))
        )


    def write_instance_to_file(self, filename: str):
        if filename.endswith('.txt'): delim = ' '
        elif filename.endswith('.csv'): delim = ','

        with open(filename, 'w') as f:
            f.write(delim.join(map(str, [self._num_students, self._num_projects, self._num_lecturers])) + '\n')

            # student index, preferences
            for student in self._sp:
                f.write(f"{student[1:]}{delim}{self._tied_list_to_string(self._sp[student], delim)}\n")

            # project index, capacity, lecturer
            for project in self._plc:
                f.write(delim.join(map(str, [project[1:], self._plc[project][0], self._plc[project][1][1:]])) + "\n")

            # lecturer index, capacity, preferences
            for lecturer in self._lp:
                f.write(f"{lecturer[1:]}{delim}{self._lp[lecturer][0]}{delim}{self._tied_list_to_string(self._lp[lecturer][2], delim)}\n")


if __name__ == '__main__':
    s = SPASTGen(
        5, 1, 2,
        3, 1,
        0.5, 0.5
    )
    s.generate_instance()
    s.write_instance_to_file('instance.txt')