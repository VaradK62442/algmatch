"""
Class to read in a file of preferences for the Student Project Allocation with Ties stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.stableMatchings.studentProjectAllocation.ties.entityPreferenceInstance import EntityPreferenceInstance

from algmatch.errors.ReaderErrors import ParticipantQuantityError, CapacityError, IDMisformatError, RepeatIDError, PrefListMisformatError, OffererError

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
        for k in entry:
            if "(" in k and open_bracket:
                raise ValueError("Cannot have tie within a tie")

            elif "(" in k:
                open_bracket = True
                preferences.append([])
                k = k[1:]
                preferences[-1].append(f"{letter}{k}")

            elif ")" in k and not open_bracket:
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

        preferences = [tuple(p) if isinstance(p, list) else p for p in preferences]
        preferences = [EntityPreferenceInstance(p) for p in preferences]

        i = 0
        for p in preferences:
            for elt in p:
                ranks[elt] = i
            i += 1

        return preferences, ranks

    def _read_data(self) -> None:
        self.no_students = 0
        self.no_projects = 0
        self.no_lecturers = 0  # assume number of lecturers <= number of projects
        self.students = {}                
        self.projects = {}
        self.lecturers = {}
        cur_line = 1
        
        with open(self.data, 'r') as file:
            file = file.read().splitlines()

        try: 
            self.no_students, self.no_projects, self.no_lecturers = map(int, file[0].split())
        except ValueError:
            raise ParticipantQuantityError()

        # build students dictionary
        for elt in file[1:self.no_students+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("student", cur_line, line=True)
            student = f"s{entry[0]}"
            if student in self.students:
                raise RepeatIDError("student", cur_line, line=True)

            for i in entry[1:]:
                if not all(j.isdigit() or j in ['(',')'] for j in i):
                    raise PrefListMisformatError("student",cur_line,line=True)

            preferences, rank = self._read_preferences_ranks(entry[1:], letter='p')
            
            self.students[student] = {"list": preferences, "rank": rank}

        # build projects dictionary
        for elt in file[self.no_students+1:self.no_students+self.no_projects+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("project", cur_line, line=True)
            project = f"p{entry[0]}"
            if project in self.projects:
                raise RepeatIDError("project", cur_line, line=True)
            
            if not entry[1].isdigit():
                raise CapacityError("project",cur_line,line=True)
            capacity = int(entry[1])

            if not entry[2].isdigit():
                raise OffererError("project","lecturer",cur_line,line=True)
            offerer = f"l{int(entry[2])}"

            self.projects[project] = {"upper_quota": capacity, "lecturer": offerer}

        # build lecturers dictionary
        for elt in file[self.no_students+self.no_projects+1:self.no_students+self.no_projects+self.no_lecturers+1]:
            cur_line += 1
            entry = elt.split()

            if not entry or not entry[0].isdigit():
                raise IDMisformatError("lecturer", cur_line, line=True)
            lecturer = f"l{entry[0]}"
            if lecturer in self.lecturers:
                raise RepeatIDError("lecturer", cur_line, line=True)
            
            if not entry[1].isdigit():
                raise CapacityError("lecturer",cur_line,line=True)
            capacity = int(entry[1])

            for i in entry[2:]:
                if not all(j.isdigit() or j in ['(',')'] for j in i):
                    raise PrefListMisformatError("lecturer",cur_line,line=True)

            preferences, rank = self._read_preferences_ranks(entry[2:], letter='s')
                        
            self.lecturers[lecturer] = {"upper_quota": capacity, "projects": set(), "list": preferences, "rank": rank, "lkj": {}}