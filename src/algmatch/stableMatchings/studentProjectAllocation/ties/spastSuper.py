"""
Student Project Allocation with Ties - Super Stable Matching
"""

import os
from collections import defaultdict

from algmatch.stableMatchings.studentProjectAllocation.ties.spastPreferenceInstance import SPASTPreferenceInstance
from algmatch.stableMatchings.studentProjectAllocation.ties.entityPreferenceInstance import EntityPreferenceInstance as EPI

class SPASTSuper:
    def __init__(self, filename: str | None = None, dictionary: dict | None = None) -> None:
        assert filename is not None or dictionary is not None, "Either filename or dictionary must be provided"
        assert not (filename is not None and dictionary is not None), "Only one of filename or dictionary must be provided"

        if filename is not None:    
            assert os.path.isfile(filename), f"File {filename} does not exist"
            self._reader = SPASTPreferenceInstance(filename=filename)

        if dictionary is not None:
            self._reader = SPASTPreferenceInstance(dictionary=dictionary)

        self.students = self._reader.students
        self.projects = self._reader.projects
        self.lecturers = self._reader.lecturers

        self.lkj_dict = {}
        self.rejected_students = defaultdict(list) # project -> list of students rejected

        self.initial_student_preferences = {s: self.students[s]["list"] for s in self.students.keys()}

        # self.sp = self._reader.sp # student preference information
        # self.sp_copy = self._reader.sp_copy
        # self.sp_no_tie = self._reader.sp_no_tie
        # self.sp_no_tie_deletions = self._reader.sp_no_tie_deletions

        # self.plc = self._reader.plc # project information
        # self.lp = self._reader.lp # lecturer preference information
        # self.lp_copy = self._reader.lp_copy

        self.unassigned = list(self.students.keys()) # keeps track of unassigned students
        # self.super_stable_matching = {}
        # self.M = {} #provisional assignment graph

        for student in self.students:
            self.M[student] = set() # set of p_j's adjacent to s_i
        for project in self.projects:
            self.M[project] = [set(), self.projects[project]["upper_quota"]] # [students assigned to p_j, remnant of c_j] 
        for lecturer in self.lecturers:
            self.M[lecturer] = [set(), set(), self.lecturers[lecturer]["upper_quota"]] # [students assigned to l_k, non-empty p_j's in G offered by l_k, remnant of d_k]

        self.full_projects = set()
        self.blocking_pair = False
        self.found_super_stable_matching = False
        self.restart_extra_deletions = False

    
    def _provisionally_assign(self, s_i, p_j, l_k):
        self.M[s_i].add(p_j) # assign s_i to p_j

        self.M[p_j][0].add(s_i) # assign p_j to s_i
        self.M[p_j][1] -= 1 # decrement quota

        self.M[l_k][0].add(s_i) # assign l_k to s_i
        self.M[l_k][1].add(p_j) # p_j is now non-empty
        self.M[l_k][2] -= 1 # decrement quota


    def _remove_from_EPI_list(value, EPI_list):
        for epi in EPI_list:
            if value in epi:
                if epi.isTie:
                    epi._remove_from_tied(value)
                else:
                    EPI_list.remove(epi)
                break


    def _delete(self, s_i, p_j, l_k):
        """
        delete(s_i, p_j, l_k):
            1. remove p_j from s_i preference list
            2. remove s_i from L_k^j
            3. if s_i provisionally assigned to p_j, 
                - break assignment
            4. if s_i deleted from every projected preference list of l_k, 
                - remove s_i from l_k preference list
        """
        self._remove_from_EPI_list(p_j, self.students[s_i]['list'])

        if s_i in self.lecturers[l_k]["lkj"][p_j]:
            self._remove_from_EPI_list(s_i, self.lecturers[l_k]["lkj"][p_j])

        if p_j in self.M[s_i]:
            # almost inverse of _provisionally_assign
            self.M[s_i].remove(p_j)

            self.M[p_j][0].remove(s_i)
            self.M[p_j][1] += 1

            self.M[l_k][0].remove(s_i)
            if self.M[p_j][0] == set(): self.M[l_k][1].remove(p_j)
            self.M[l_k][2] += 1

            self.rejected_students[p_j].append(s_i) # we keep track of students rejected from p_j

            # if s_i no longer has any project in common with lecturer in M
            if s_i in self.M[l_k][0] and self.M[s_i].intersection(self.M[l_k][1]) == set():
                self.M[l_k][0].remove(s_i)

        for proj in self.lecturers[l_k]["projects"]:
            if s_i not in set([x for x in self.lecturers[l_k]["lkj"][proj]]):
                self._remove_from_EPI_list(s_i, self.lecturers[l_k]["lkj"][proj])

        # if s_i is not paired with a project in M and has a non-empty list, s_i is unassigned
        if self.M[s_i] == set() and s_i not in self.unassigned and len(self.students[s_i]["list"]) > 0:
            self.unassigned.append(s_i)


    def _unpack_EPI_list(self, EPI_list) -> set[str]:
        res = set()
        for epi in EPI_list:
            if epi.isTie:
                res.update([str(x) for x in epi.values])
            else:
                res.add(str(epi.values))

        return res
    

    def _strict_successors(self, entity, L_subset) -> set:
        """
        Find strict successors of either 
        - p_j in Lkj or
        - l_k in Lk
        """
        assigned_students = self.M[entity][0]
        if L_subset[-1] in assigned_students: return []

        for i, elt in enumerate(L_subset[::-1]):
            if elt in assigned_students:
                return L_subset[-i:]


    # while some student s_i is unassigned and has a non-empty preference list
    def while_loop(self):
        while self.unassigned:
            student = self.unassigned.pop(0)
            head = self.students[student]['list'][0]

            for project in head:
                lecturer = self.projects[project]['lecturer']

                # student applies to project
                self._provisionally_assign(student, str(project), lecturer)

                # if project is oversubscribed:
                if self.M[project][1] < 0:
                    Lkj = self.lecturers[lecturer]["lkj"][project]
                    tail_students: EPI = Lkj[-1] # EPI - either tie or single value

                    for st in tail_students:
                        self._delete(st, project, lecturer)

                # elif l_k is oversubscribed:
                elif self.M[lecturer][2] < 0:
                    Lk = self.lecturers[lecturer]["list"]
                    tail_students = Lk[-1]

                    self.lecturers[lecturer]["list"] = Lk[:-1]

                    P_k = self.lecturers[lecturer]["projects"] # all projects offered by lecturer
                    for st in tail_students:
                        A_t = self._unpack_EPI_list(self.students[st]["list"]) # student's altered preference list without ties
                        intersection = A_t.intersection(P_k)
                        for p in intersection:
                            self._delete(st, p, lecturer)

                # if project is full
                if self.M[project][1] == 0:
                    self.full_projects.add(project)

                    Lkj = self.lecturers[lecturer]["lkj"][project]
                    successors_of_worst_assigned = self._strict_successors(project, Lkj) # successors of worst student assigned to project p_j in Lkj

                    for s_t in successors_of_worst_assigned:
                        self._delete(s_t, project, lecturer)

                # if lecturer is full
                if self.M[lecturer][2] == 0:
                    Lk = self.lecturers[lecturer]["list"]
                    P_k = self.lecturers[lecturer]["projects"] # all projects offered by lecturer
                    successors_of_worst_assigned = self._strict_successors(lecturer, Lk) # successors of worst student assigned to lecturer l_k in Lk

                    for s_t in successors_of_worst_assigned:
                        A_t = self._unpack_EPI_list(self.students[s_t]["list"])
                        intersection = A_t.intersection(P_k)

                        for p_u in intersection:
                            self._delete(s_t, p_u, lecturer)


    def for_loop(self):
        self.restart_extra_deletions = False
        for p_j in self.projects:
            if p_j in self.full_projects and self.M[p_j][1] > 0:
                l_k = self.projects[p_j]['lecturer']
                s_r = self.rejected_students[p_j][-1]
                Lk_students = self.lecturers[l_k]["list"]
                pointer = len(Lk_students)

                found = False
                while pointer >= 0:
                    if s_r in Lk_students[pointer]:
                        found = True
                        if pointer < len(Lk_students):
                            self.restart_extra_deletions = True
                        break
                    pointer -= 1

                if found:
                    Lk_tail = Lk_students.pop(-1) # TODO: why last element?
                    P_k = self.lecturers[l_k]["projects"]

                    for s_t in Lk_tail:
                        A_t = self._unpack_EPI_list(self.students[s_t]["list"])
                        intersection = A_t.intersection(P_k)
                        for p_u in intersection:
                            self._delete(s_t, p_u, l_k)


    def _every_unassigned_student_has_empty_preference_list(self) -> bool:
        return all([len(self.students[student]['list']) == 0 for student in self.unassigned])


    # terminates when every unassigned student has an empty preference list
    def outer_repeat(self):
        while not self._every_unassigned_student_has_empty_preference_list() or self.restart_extra_deletions:
            self.while_loop()
            self.for_loop()


    def check_stability(self):
        # self.blocking_pair is set to true if blocking pair exists
        for student in self.students:
            if self.M[student] == set():
                preferred_projects = self.initial_student_preferences[student]

        
    def run(self):
        self.outer_repeat()
        self.check_stability()