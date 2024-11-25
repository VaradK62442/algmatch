import random
from math import ceil

class SPAInstanceGenerator:
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
        self.students = {i+1 : {"list": []} for i in range(self.no_students)}
        # in order to do a trick on this dictionary below, we need them to start at 0
        self.projects = {i: {"upper_quota": 1, "lecturer": ""} for i in range(self.no_projects)}
        self.lecturers = {i+1: {"upper_quota": 0, "projects": [], "list": [], "max_proj_uquota": 0, "sum_proj_uquota": 0} for i in range(self.no_lecturers)}
        
        # ====== STUDENTS ======
        for student in self.students:
            length = random.randint(self.li, self.lj)
            # we provide this many preferred projects at random
            random.shuffle(self.available_projects)
            self.students[student]["list"] = self.available_projects[:length]

        # ====== PROJECT QUOTAS ======
        # randomly assign the remaining project capacities
        for i in range(self.tpc - self.no_projects):
            # we can get a random value, and just update that inner dictionary.
            # Testing with perf_counter_ns in IDLE suggests that this is faster.
            # This is the line than need the projects to start at zero.
            random.choice(self.projects)["upper_quota"] += 1

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
            quota = self.projects[project]["upper_quota"]
            offerer = project_lecturer_map[project]
            if quota > self.lecturers[offerer]["max_proj_uquota"]:
                self.lecturers[offerer]["max_proj_uquota"] = quota
            self.lecturers[offerer]["sum_proj_uquota"] += quota

        for lecturer in self.lecturers:
            lecturer_info = self.lecturers[lecturer]
            max_q = lecturer_info["max_proj_uquota"]
            sum_q = lecturer_info["sum_proj_uquota"]
            lecturer_info["upper_quota"] = random.randint(max_q, sum_q)
            random.shuffle(self.available_students)
            lecturer_info["list"] = self.available_students[:]

    def write_instance_no_ties(self, filename):  # writes to txt file
        if type(filename) is not str:
            raise ValueError("Filename is not a string.")

        with open(filename, 'w') as Instance:

            # write the numbers of each participant type as the header
            Instance.write(f"{self.no_students} {self.no_projects} {self.no_lecturers}\n")
            
            # write indexes, capacities and preferences, 
            # see the DATA_FORMAT_GUIDELINE.md
            for n in range(1, self.no_students + 1):
                preferences = self.students[n]["list"]
                Instance.write(f"{n} {' '.join([str(h) for h in preferences])}\n")

            for n in range(self.no_projects):                
                # the dictionary start at 0, see above
                uquota = self.projects[n]["upper_quota"]
                offerer = self.projects[n]["lecturer"]
                Instance.write(f"{n+1} {uquota} {offerer}\n")

            for n in range(1, self.no_lecturers + 1):
                uquota = self.lecturers[n]["upper_quota"]
                preferences = self.lecturers[n]["list"]
                Instance.write(f"{n} {uquota} {' '.join([str(r) for r in preferences])}\n")

            Instance.close()