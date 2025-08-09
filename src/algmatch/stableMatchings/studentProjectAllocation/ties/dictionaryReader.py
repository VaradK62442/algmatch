"""
Class to read in a dictionary of preferences for the Student Project Allocation with Ties stable matching algorithm.
"""

from algmatch.abstractClasses.abstractReader import AbstractReader
from algmatch.stableMatchings.studentProjectAllocation.ties.entityPreferenceInstance import EntityPreferenceInstance

from algmatch.errors.ReaderErrors import ParticipantQuantityError, CapacityError, IDMisformatError, RepeatIDError, PrefListMisformatError, OffererError

class DictionaryReader(AbstractReader):
    def __init__(self, dictionary: dict) -> None:
        super().__init__(dictionary)
        self._read_data()

    def _read_data(self) -> None:
        self.students = {}
        self.projects = {}
        self.lecturers = {}

        for key, value in self.data.items():
            match key:
                case "students":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("student",k)
                        student = f"s{k}"
                        if student in self.students:
                            raise RepeatIDError("student",k)
                        
                        for i in v:
                            if type(i) is not int and not all(type(j) is int for j in i):
                                raise PrefListMisformatError("student",k,i)

                        preferences = []
                        rank = {}
                        for i, elt in enumerate(v):
                            if isinstance(elt, int):
                                epi = EntityPreferenceInstance(f"p{elt}")
                                rank[f"p{elt}"] = i
                            else:
                                epi = EntityPreferenceInstance(tuple(f"p{j}" for j in elt))
                                for j in elt:
                                    rank[f"p{j}"] = i

                            preferences.append(epi)

                        self.students[student] = {"list": preferences, "rank": rank}

                case "projects":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("project",k)
                        project = f"p{k}"
                        if project in self.projects:
                            raise RepeatIDError("project",k)
                        
                        if type(v["capacity"]) is not int:
                            raise CapacityError("project",k)
                        capacity = v["capacity"]

                        if type(v["lecturer"]) is not int:
                            raise OffererError("project","lecturer",k)
                        lecturer = f"l{v['lecturer']}"

                        self.projects[project] = {"upper_quota": capacity, "lecturer": lecturer}

                case "lecturers":
                    for k, v in value.items():
                        if type(k) is not int:
                            raise IDMisformatError("lecturer",k)
                        lecturer = f"l{k}"
                        if lecturer in self.lecturers:
                            raise RepeatIDError("lecturer",k)
                        
                        if type(v["capacity"]) is not int:
                            raise CapacityError("project",k)
                        capacity = v["capacity"]

                        for i in v["preferences"]:
                            if type(i) is not int and not all(type(j) is int for j in i):
                                raise PrefListMisformatError("lecturer",k,i)

                        preferences = []
                        rank = {}

                        for i, elt in enumerate(v["preferences"]):
                            if isinstance(elt, int):
                                epi = EntityPreferenceInstance(f"s{elt}")
                                rank[f"s{elt}"] = i
                            else:
                                epi = EntityPreferenceInstance(tuple(f"s{j}" for j in elt))
                                for j in elt:
                                    rank[f"s{j}"] = i

                            preferences.append(epi)

                        self.lecturers[lecturer] = {"upper_quota": capacity, "projects": set(), "list": preferences, "rank": rank, "lkj": {}}