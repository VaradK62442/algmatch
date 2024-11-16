"""
Class to read in a file of preferences for the Student Project Allocation with Ties stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.stableMatchings.studentProjectAllocation.ties.entityPreferenceInstance import EntityPreferenceInstance

from pprint import pprint as pp


class FileReader(AbstractReader):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self._read_data()

    def _read_preferences_ranks(self, entry: list[str], letter: str):
        """
        Returns preferences and ranks from an entry in the file.
        """
        preferences = []
        ranks = {}

        open_bracket = False

        for i, k in enumerate(entry):
            if "(" in k and open_bracket:
                # cannot have tie within a tie
                raise ValueError("Cannot have tie within a tie")

            elif "(" in k:
                open_bracket = True
                preferences.append([])
                k = k[1:]
                preferences[-1].append(f"{letter}{k}")

            elif ")" in k and not open_bracket:
                # cannot have closing bracket without an opening bracket
                raise ValueError("Cannot have closing bracket without an opening bracket")

            elif ")" in k:
                open_bracket = False
                k = k[:-1]
                preferences[-1].append(f"{letter}{k}")

            else:
                if not open_bracket:
                    # not inside tie
                    preferences.append(f"{letter}{k}")
                else:
                    # inside tie
                    preferences[-1].append(f"{letter}{k}")

            ranks[f"p{k}"] = i

        preferences = [tuple(p) if isinstance(p, list) else p for p in preferences]
        preferences = [EntityPreferenceInstance(p) for p in preferences]

        return preferences, ranks

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

            preferences, rank = self._read_preferences_ranks(entry[1:], letter='p')
            
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

            preferences, rank = self._read_preferences_ranks(entry[2:], letter='s')

            # preferences = [f"s{i}" for i in entry[2:]]
            # rank = {stud: idx for idx, stud in enumerate(preferences)}
                        
            self.lecturers[lecturer] = {"upper_quota": capacity, "projects": set(), "list": preferences, "rank": rank}

        # update projects
        for project in self.projects:
            lec = self.projects[project]["lecturer"]
            self.lecturers[lec]["projects"].add(project)
            lecturer_list = self.lecturers[lec]["list"]
            
            # TODO: beautify?
            project_list = []
            for epi in lecturer_list:
                if epi.isTie:
                    for stu in epi.values:
                        for elt in self.students[stu.values]["list"]:
                            if project in elt:
                                project_list.append(stu.values)
                
                else:
                    for elt in self.students[epi.values]["list"]:
                        if project in elt:
                            project_list.append(epi.values)
            
            rank = {stud: idx for idx, stud in enumerate(project_list)}
            self.projects[project]["list"] = project_list
            self.projects[project]["rank"] = rank