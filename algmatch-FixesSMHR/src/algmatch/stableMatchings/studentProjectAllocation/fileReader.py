"""
Class to read in a file of preferences for the Student Project Allocation stable matching algorithm.
"""

from abstractClasses.abstractReader import AbstractReader


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_data(self) -> None:
        self.no_students = 0
        self.no_projects = 0
        self.no_lecturers = 0  # assume number of lecturers <= number of projects
        self.students = {}                
        self.projects = {}
        self.lecturers = {}
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        self.no_students, self.no_projects, self.no_lecturers = map(int, file[0].split())

        # build students dictionary
        for elt in file[1:self.no_students+1]:
            entry = elt.split()
            student = f"s{entry[0]}"
            preferences = [f"p{k}" for k in entry[1:]]

            rank = {proj: idx for idx, proj in enumerate(preferences)}
            self.students[student] = {"list": preferences, "rank": rank}

        # build projects dictionary
        for elt in file[self.no_students+1:self.no_students+self.no_projects+1]:
            entry = elt.split()
            self.projects[f"p{entry[0]}"] = {"upper_quota": int(entry[1]), "lecturer": f"l{entry[2]}"}

        # build lecturers dictionary
        for elt in file[self.no_students+self.no_projects+1:self.no_students+self.no_projects+self.no_lecturers+1]:
            entry = elt.split()
            lecturer = f"l{entry[0]}"
            capacity = int(entry[1])
            preferences = [f"s{i}" for i in entry[2:]]
            rank = {stud: idx for idx, stud in enumerate(preferences)}
            self.lecturers[lecturer] = {"upper_quota": capacity, "projects": set(), "list": preferences, "rank": rank}

        # update projects
        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]
            project_list = [stu for stu in lecturer_list if project in self.students[stu]["list"]]
            rank = {stud: idx for idx, stud in enumerate(project_list)}
            self.projects[project]["list"] = project_list
            self.projects[project]["rank"] = rank