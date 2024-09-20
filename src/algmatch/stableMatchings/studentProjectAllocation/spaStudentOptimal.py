"""
Student Project Allocation - Student Optimal version
"""

import os
from copy import deepcopy

from stableMatchings.studentProjectAllocation.spaPreferenceInstance import SPAPreferenceInstance


class SPAStudentOptimal:
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

        self.delete = {}
        self.unassigned = set()
        self.M = {} # provisional matching

        for student in self.students:
            self.unassigned.add(student)
            self.M[student] = {"assigned": None}
            self.delete[student] = deepcopy(self.students[student]["list"])

        for project in self.projects:
            self.M[project] = {"assigned": set(), "worst_student": None}
            self.delete[project] = deepcopy(self.projects[project]["list"])

        for lecturer in self.lecturers:
            self.M[lecturer] = {"assigned": set(), "worst_student": None}
            self.delete[lecturer] = deepcopy(self.lecturers[lecturer]["list"])

        self.found_blocking_pair = False
        self.stable_matching = {}


    # =======================================================================
    # provisionally assign s_i to p_j (and to l_k)
    # =======================================================================    
    def _provisionally_assign(self, student, project, lecturer):
        self.M[student]["assigned"] = project
        self.M[project]["assigned"].add(student)
        self.M[lecturer]["assigned"].add(student)

        # keep track of worst_student assigned to p_j
        if self.M[project]["worst_student"] is None: 
            self.M[project]["worst_student"] = student
        else:
            # if the new student has a rank worse than that of the current worst_student
            # then update this student as the worst_student assigned to the project
            current_worst_student = self.M[project]["worst_student"]
            rank_current_worst_student = self.projects[project]["rank"][current_worst_student]
            rank_student = self.projects[project]["rank"][student]
            if rank_student > rank_current_worst_student:
                self.M[project]["worst_student"] = student

        # keep track of worst_student assigned to l_k
        if self.M[lecturer]["worst_student"] is None: 
            self.M[lecturer]["worst_student"] = student
        else:
            current_worst_student = self.M[lecturer]["worst_student"]
            rank_current_worst_student = self.lecturers[lecturer]["rank"][current_worst_student]
            rank_student = self.lecturers[lecturer]["rank"][student]
            if rank_student > rank_current_worst_student:
                self.M[lecturer]["worst_student"] = student
         
    # =======================================================================
    # break provisional assignment between s_r and p_j (and l_k)
    # =======================================================================       
    def _break_assignment(self, student, project, lecturer):

        self.M[student]["assigned"] = None 
        self.M[project]["assigned"].remove(student)
        self.M[lecturer]["assigned"].remove(student)        
        # if student has a non-empty list, add her to the list of unassigned students
        if len(self.delete[student]) > 0:
            self.unassigned.add(student) 
        
        self._update_worst_student(student, project, lecturer)
        
    # =======================================================================
    # update worst student assigned to project and lecturer
    # ======================================================================= 
    def _update_worst_student(self, student, project, lecturer):
        
        # if this student is also the worst_student assigned to project, 
        # then we need to update the project's worst_student
        if student == self.M[project]["worst_student"]:
            if self.M[project]["assigned"] == set(): # possible at this point, M(p_j) is empty 
                self.M[project]["worst_student"] = None
            else:
                worst_student_rank = self.projects[project]["rank"][student]
                preferences = self.projects[project]["list"]
                # find the student who is currently assigned to pj and who is close in rank to the current worst_student
                worst_student_rank -= 1 # this moves the pointer to the next best student
                while worst_student_rank >= 0:
                    if preferences[worst_student_rank] in self.M[project]["assigned"]:
                        self.M[project]["worst_student"] = preferences[worst_student_rank]
                        break
                    worst_student_rank -= 1

        # if this student is also the worst_student assigned to lecturer, 
        # then we need to update the lecturer's worst_student
        # print(student, self.M[lecturer]["worst_student"])
        if student == self.M[lecturer]["worst_student"]:
            worst_student_rank = self.lecturers[lecturer]["rank"][student]
            preferences = self.lecturers[lecturer]["list"]
            # find the student who is currently assigned to lk and who is close in rank to the current worst_student
            worst_student_rank -= 1 # this moves the pointer to the next best student
            while worst_student_rank >= 0:
                #print(preferences[worst_student_rank])
                if preferences[worst_student_rank] in self.M[lecturer]["assigned"]:
                    self.M[lecturer]["worst_student"] = preferences[worst_student_rank]
                    break
                worst_student_rank -= 1

    # =======================================================================
    # delete (s_i, p_j) from A(s_i)  -------- (but not from L_k^j)
    # =======================================================================
    def _delete_pair(self, student, project, lecturer):         
        self.delete[student].remove(project)
        self.delete[project].remove(student)
        #self.delete[lecturer].remove(student)
        #print(f"successfully deleted {student} from {project} and {lecturer} ")
    
    # =======================================================================
    # while loop that constructs M from students preference lists
    # =======================================================================    
    def _while_loop(self):
        while self.unassigned:                     
            student = self.unassigned.pop()
            # if the student has a non-empty preference list
            if len(self.delete[student]) > 0:                      
                project = self.delete[student][0]
                lecturer = self.projects[project]["lecturer"]  
                self._provisionally_assign(student, project, lecturer)
                # ----------- if project is oversubscribed -----------
                if len(self.M[project]["assigned"]) > self.projects[project]["upper_quota"]:
                    worst_student = self.M[project]["worst_student"]  
                    self._break_assignment(worst_student, project, lecturer) 
                # ----------- elif lecturer is oversubscribed -----------
                elif len(self.M[lecturer]["assigned"]) > self.lecturers[lecturer]["upper_quota"]:
                    worst_student = self.M[lecturer]["worst_student"]
                    # print(f"{worst_student}: {self.M[worst_student]} : {self.delete[worst_student]}")
                    # print(f"{lecturer}: {self.M[lecturer]} : {self.delete[lecturer]} \n")
                    worst_student_project = self.M[worst_student]["assigned"]
                    self._break_assignment(worst_student, worst_student_project, lecturer)   
                # ----------- if project is full ----------- 
                if len(self.M[project]["assigned"]) == self.projects[project]["upper_quota"]:
                    worst_student = self.M[project]["worst_student"] 
                    rank_worst_student = self.projects[project]["rank"][worst_student] 
                    # now we get the strict successors of worst student from the deletions list of Lkj 
                    strict_successors = [sr for sr in self.projects[project]["list"][rank_worst_student+1:] if sr in self.delete[project]]
                    for st in strict_successors:
                        #print(self.M)
                        #print(st, project, lecturer)
                        self.delete[st].remove(project)
                        self.delete[project].remove(st)
                        #print(f"successfully deleted {st} from {project} and {lecturer} ---- project full ")
                # ----------- if lecturer is full -----------
                if len(self.M[lecturer]["assigned"]) == self.lecturers[lecturer]["upper_quota"]:
                    worst_student = self.M[lecturer]["worst_student"]
                    rank_worst_student = self.lecturers[lecturer]["rank"][worst_student]
                    # now we get the strict successors of worst student from the deletions list of Lkj
                    strict_successors = [sr for sr in self.lecturers[lecturer]["list"][rank_worst_student+1:] if sr in self.delete[lecturer]]
                    P_k = self.lecturers[lecturer]["projects"] # this is a set
                    for st in strict_successors:
                        st_preference = set(self.delete[st])
                        intersect_projects = P_k.intersection(st_preference)
                        for pu in intersect_projects:
                            #print(f"{st}: {self.delete[st]}\n {pu}: {self.delete[pu]} \n {lecturer}: {self.delete[lecturer]}")
                            self.delete[st].remove(pu)
                            self.delete[pu].remove(st)
                            #print(f"successfully deleted {st} from {pu} and {lecturer} ---- lecturer full")
                        self.delete[lecturer].remove(st)
            # !* if the current student is unassigned in the matching, with a non-empty preference list, we re-add the student to the unassigned list --- this cannot happen in the strict preference case (only in the ties case)
            if self.M[student]["assigned"] is None and student not in self.unassigned and len(self.delete[student]) > 0:  
                self.unassigned.append(student)


    # =======================================================================    
    # blocking pair types
    # =======================================================================    
    def _blockingpair_1bi(self, student, project, lecturer):
        #  project and lecturer capacity
        cj, dk = self.projects[project]["upper_quota"], self.lecturers[lecturer]["upper_quota"]
        # no of students assigned to project in M
        project_occupancy, lecturer_occupancy = len(self.M[project]["assigned"]), len(self.M[lecturer]["assigned"])
        #  project and lecturer are both under-subscribed
        if project_occupancy < cj and lecturer_occupancy < dk:
            return True
        return False
    
    def _blockingpair_1bii(self, student, project, lecturer):
        # p_j is undersubscribed, l_k is full and either s_i \in M(l_k)
        # or l_k prefers s_i to the worst student in M(l_k)
        cj, dk = self.projects[project]["upper_quota"], self.lecturers[lecturer]["upper_quota"]
        project_occupancy, lecturer_occupancy = len(self.M[project]["assigned"]), len(self.M[lecturer]["assigned"])
        #  project is undersubscribed and lecturer is full
        if project_occupancy < cj and lecturer_occupancy == dk:
            Mlk_students = self.M[lecturer]["assigned"]
            if student in Mlk_students: # s_i \in M(lk)
                return True
            student_rank = self.lecturers[lecturer]["rank"][student]
            worst_student = self.M[lecturer]["worst_student"]
            worst_student_rank = self.lecturers[lecturer]["rank"][worst_student]
            if student_rank < worst_student_rank: # lk prefers s_i to her worst student in M(l_k)
                return True                
        return False
    
    def _blockingpair_1biii(self, student, project, lecturer):
        # p_j is full and l_k prefers s_i to the worst student in M(p_j)
        cj, project_occupancy = self.projects[project]["upper_quota"], len(self.M[project]["assigned"])
        if project_occupancy == cj:
            student_rank = self.projects[project]["rank"][student]
            worst_student = self.M[project]["worst_student"]
            worst_student_rank = self.projects[project]["rank"][worst_student]
            if student_rank < worst_student_rank: # lk prefers s_i to her worst student in M(p_j)
                return True    
        return False

    # =======================================================================    
    # Is M stable? Check for blocking pair
    # self.found_blocking_pair is set to True if blocking pair exists
    # =======================================================================
    def _check_stability(self):        
        for student in self.students:
            preferred_projects = self.students[student]["list"]
            if self.M[student]["assigned"] is not None:
                matched_project = self.M[student]["assigned"]
                rank_matched_project = self.students[student]["rank"][matched_project]
                A_si = self.students[student]["list"]
                preferred_projects = [pj for pj in A_si[:rank_matched_project]] # every project that s_i prefers to her matched project                                
        
            for project in preferred_projects:
                lecturer = self.projects[project]["lecturer"]
                if not self.found_blocking_pair:
                    self.found_blocking_pair = self._blockingpair_1bi(student, project, lecturer)
                if not self.found_blocking_pair:
                    self.found_blocking_pair = self._blockingpair_1bii(student, project, lecturer)
                if not self.found_blocking_pair:
                    self.found_blocking_pair = self._blockingpair_1biii(student, project, lecturer)
                
                if self.found_blocking_pair:
                #    print(student, project, lecturer)
                   break
            
            if self.found_blocking_pair:
                # print(student, project, lecturer)
                break
 
        
    def run(self):
        self._while_loop()
        self._check_stability()

        # construct stable matching with only students as keys
        for student in self.students:
            if self.M[student]["assigned"] is None:
                self.stable_matching[student] = ""
            else: 
                self.stable_matching[student] = self.M[student]["assigned"]

        if not self.found_blocking_pair: return f"student-optimal stable matching: {self.stable_matching}"
        else: return f"Unstable matching: {self.stable_matching}"       