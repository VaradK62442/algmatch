import random
from math import ceil

from tests.abstractTestClasses.abstractInstanceGenerator import AbstractInstanceGenerator

class SPAInstanceGenerator(AbstractInstanceGenerator):
    def __init__(self, students, lower_bound, upper_bound):
        if type(students) is not int or students <= 0:
            raise ValueError("number of residents must be a postive integer")
        
        self.no_students = students
        self.no_projects = int(ceil(0.5*self.no_students))
        self.no_lecturers = int(ceil(0.2*self.no_students))  # assume number of lecturers <= number of projects

        if type(lower_bound) is not int or type(upper_bound) is not int:
            raise ValueError("Bound must be integers.")
        if lower_bound < 0:
            raise ValueError("Lower bound is negative.")
        if upper_bound > self.no_projects:
            raise ValueError("Upper bound is greater than the number of projects.")
        if lower_bound > upper_bound:
            raise ValueError("Lower bound is greater than upper bound")

        
        self.tpc = int(ceil(1.2*self.no_students))  # assume total project capacity >= number of projects
        self.li = lower_bound  # lower bound of the student's preference list
        self.lj = upper_bound  # upper bound of the student's preference list

        self.students = {}
        self.projects = {}
        self.lecturers = {}

        # lists of numbers that will be shuffled to get preferences
        self.available_students = [i+1 for i in range(self.no_students)]
        self.available_projects = [i+1 for i in range(self.no_projects)]
        
    def generate_instance_no_ties(self):
        # ====== BLANKS ======
        self.students = {i+1 : [] for i in range(self.no_students)}
        # in order to do a trick on this dictionary below, we need project ids to start at 0
        self.projects = {i: {"capacity": 1, "lecturer": ""} for i in range(self.no_projects)}
        self.lecturers = {i+1: {"capacity": 0, "preferences": [], "max_proj_uquota": 0, "sum_proj_uquota": 0} for i in range(self.no_lecturers)}
        
        # ====== STUDENTS ======
        for student in self.students:
            length = random.randint(self.li, self.lj)
            # we provide this many preferred projects at random
            random.shuffle(self.available_projects)
            self.students[student] = self.available_projects[:length]

        # ====== PROJECT QUOTAS ======
        # randomly assign the remaining project capacities
        for i in range(self.tpc - self.no_projects):
            # we can get a random value, and just update that inner dictionary.
            # Testing with perf_counter_ns in IDLE suggests that this is faster.
            # This is the line that needs the projects to start at zero.
            random.choice(self.projects)["capacity"] += 1

        # ====== PROJECT-LECTURER ======
        project_lecturer_map = {p: 0 for p in self.projects}
        # give all lecturers one project
        for i, lecturer in enumerate(self.lecturers):
            project_lecturer_map[i] = lecturer
        random.shuffle(project_lecturer_map)

        # assign remaining projects    
        lecturer_list = list(self.lecturers.keys())
        for project in project_lecturer_map:
            if project_lecturer_map[project] == 0:
                offerer = random.choice(lecturer_list)
                project_lecturer_map[project] = offerer

        # now save
        for project in self.projects:
            self.projects[project]["lecturer"] = project_lecturer_map[project]

        # ====== LECTURERS =======
        # calculate quota bounds
        for project in self.projects:
            quota = self.projects[project]["capacity"]
            offerer = project_lecturer_map[project]
            if quota > self.lecturers[offerer]["max_proj_uquota"]:
                self.lecturers[offerer]["max_proj_uquota"] = quota
            self.lecturers[offerer]["sum_proj_uquota"] += quota

        for lecturer in self.lecturers:
            lecturer_info = self.lecturers[lecturer]
            max_q = lecturer_info["max_proj_uquota"]
            sum_q = lecturer_info["sum_proj_uquota"]
            lecturer_info["capacity"] = random.randint(max_q, sum_q)
            random.shuffle(self.available_students)
            lecturer_info["preferences"] = self.available_students[:]

        return self.pack_dictionary()

    def pack_dictionary(self):
        self.instance = {}

        # clean up extra variables
        for l_data in self.lecturers.values():
            del l_data["max_proj_uquota"]
            del l_data["sum_proj_uquota"]

        # shift projects back up one
        for i in range(self.no_projects,0,-1):
            self.projects[i] = self.projects[i-1].copy()
        del self.projects[0]

        self.instance["students"] = self.students
        self.instance["projects"] = self.projects
        self.instance["lecturers"] = self.lecturers

        return self.instance