"""
Student Project Allocation - Abstract class
"""

from copy import deepcopy
import os

from algmatch.stableMatchings.studentProjectAllocation.spaPreferenceInstance import SPAPreferenceInstance


class SPAAbstract:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SPAPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SPAPreferenceInstance(dictionary=dictionary)

        self.students = self._reader.students
        self.projects = self._reader.projects
        self.lecturers = self._reader.lecturers

        # we need original copies of the preference lists to check the stability of solutions
        self.original_students = deepcopy(self.students)
        self.original_lecturers = deepcopy(self.lecturers)

        self.M = {} # provisional matching
        self.stable_matching = {
            "student_sided": {student: "" for student in self.students},
            "lecturer_sided": {lecturer: [] for lecturer in self.lecturers}
        }
        self.blocking_conditions = (self._blockingpair_1bi, self._blockingpair_1bii, self._blockingpair_1biii)
        self.is_stable = False

    # =======================================================================    
    # blocking pair types
    # =======================================================================    
    def _blockingpair_1bi(self, _, project, lecturer):
        #  project and lecturer capacity
        cj, dk = self.projects[project]["upper_quota"], self.original_lecturers[lecturer]["upper_quota"]
        # no of students assigned to project in M
        project_occupancy, lecturer_occupancy = len(self.M[project]["assigned"]), len(self.M[lecturer]["assigned"])
        #  project and lecturer are both under-subscribed
        if project_occupancy < cj and lecturer_occupancy < dk:
            return True
        return False

    
    def _blockingpair_1bii(self, student, project, lecturer):
        # p_j is undersubscribed, l_k is full and either s_i \in M(l_k)
        # or l_k prefers s_i to the worst student in M(l_k)
        cj, dk = self.projects[project]["upper_quota"], self.original_lecturers[lecturer]["upper_quota"]
        project_occupancy, lecturer_occupancy = len(self.M[project]["assigned"]), len(self.M[lecturer]["assigned"])
        #  project is undersubscribed and lecturer is full
        if project_occupancy < cj and lecturer_occupancy == dk:
            Mlk_students = self.M[lecturer]["assigned"]
            if student in Mlk_students: # s_i \in M(lk)
                return True
            student_rank = self.original_lecturers[lecturer]["rank"][student]
            for worst_student in self.M[lecturer]["assigned"]:
                worst_student_rank = self.original_lecturers[lecturer]["rank"][worst_student]
                if student_rank < worst_student_rank:
                    return True              
        return False
    
    
    def _blockingpair_1biii(self, student, project, _):
        # p_j is full and l_k prefers s_i to the worst student in M(p_j)
        cj, project_occupancy = self.projects[project]["upper_quota"], len(self.M[project]["assigned"])
        if project_occupancy == cj:
            student_rank = self.projects[project]["rank"][student]
            for worst_student in self.M[project]["assigned"]:
                worst_student_rank = self.projects[project]["rank"][worst_student]
                if student_rank < worst_student_rank:
                    return True
        return False
    

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_stability(self) -> bool:        
        for student in self.original_students:
            preferred_projects = self.original_students[student]["list"]
            if self.M[student]["assigned"] is not None:
                matched_project = self.M[student]["assigned"]
                rank_matched_project = self.original_students[student]["rank"][matched_project]
                A_si = self.original_students[student]["list"]
                preferred_projects = [pj for pj in A_si[:rank_matched_project]] # every project that s_i prefers to her matched project                                
        
            for project in preferred_projects:
                lecturer = self.projects[project]["lecturer"]
                for condition in self.blocking_conditions:
                    if condition(student, project, lecturer):
                        return False
                    
        return True


    def _while_loop(self):
        raise NotImplementedError("Method _while_loop must be implemented in subclass")
    

    def run(self) -> None:
        self._while_loop()

        for student in self.students:
            project = self.M[student]["assigned"]
            if project is not None:
                lecturer = self.projects[project]["lecturer"]
                self.stable_matching["student_sided"][student] = project
                self.stable_matching["lecturer_sided"][lecturer].append(student)

        self.is_stable = self._check_stability()

        if self.is_stable:
            return f"stable matching: {self.stable_matching}"
        else:
            return f"unstable matching: {self.stable_matching}"