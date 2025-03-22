"""
Using Gurobi Integer Programming solver to solve the SPA-ST problem.
"""

import gurobipy as gp
from gurobipy import GRB

from algmatch.stableMatchings.studentProjectAllocation.ties.fileReaderIPModel import FileReaderIPModel as FileReader

from collections import defaultdict
from pprint import pprint


class GurobiSPAST:
    def __init__(self, filename: str, output_flag=1) -> None:
        self.filename = filename
        r = FileReader(filename)

        self._students = r.students
        self._projects = r.projects
        self._lecturers = r.lecturers

        self.J = gp.Model("SPAST")
        self.J.setParam('OutputFlag', output_flag)

        self.matching = defaultdict(str)


    def _matching_constraints(self) -> None:
        """
        Matching contraints

        x_{ij} \in {0, 1} s.t. (1 <= i <= |S|, 1 <= j <= |P|)
        x_{ij} indicates whether s_i is assigned to p_j in a solution or not

        \sum_{p_j \in A_i}(x_{ij}) <= 1 for all i in {1, 2, ..., |S|} # student can be assigned to at most one project
        \sum_{i=1}^{|S|}(x_{ij}) <= c_j for all j in {1, 2, ..., |P|} # project does not exceed capacity
        \sum_{i=1}^{|S|} \sum_{p_j \in P_k} x_{ij} <= d_k for all k in {1, 2, ..., |L|} # lecturer does not exceed capacity
        """

        for student in self._students:
            sum_student_variables = gp.LinExpr()
            for project in self._students[student][1]:
                xij = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{student} is assigned {project}")
                self._students[student][1][project] = xij
                sum_student_variables += xij

            # CONSTRAINT: student can be assigned to at most one project
            self.J.addConstr(sum_student_variables <= 1, f"Constraint (4.5) for {student}")

        for project in self._projects:
            total_project_capacity = gp.LinExpr()
            for student in self._students:
                if project in self._students[student][1]:
                    total_project_capacity += self._students[student][1][project]

            # CONSTRAINT: project does not exceed capacity
            self.J.addConstr(total_project_capacity <= self._projects[project][0], f"Total capacity constraint (4.6) for {project}")

        for lecturer in self._lecturers:
            total_lecturer_capacity = gp.LinExpr()
            for student in self._students:
                for project in self._students[student][1]:
                    if lecturer == self._projects[project][1]:
                        total_lecturer_capacity += self._students[student][1][project]

            # CONSTRAINT: lecturer does not exceed capacity
            self.J.addConstr(total_lecturer_capacity <= self._lecturers[lecturer][0], f"Total capacity constraint (4.7) for {lecturer}")


    def _get_outranked_entities(self, preference_list, entity, strict=False) -> list:
        """
        Get entities that outrank entity in preference list

        :param strict: if True, only return entities that strictly outrank entity
        """
        idx = 0
        p = preference_list[idx]
        outranked_projects = []
        while entity not in p:
            outranked_projects += p
            idx += 1
            p = preference_list[idx]
        
        outranked_projects += p if not strict else []
        return outranked_projects


    def _get_equal_entities(self, preference_list, entity) -> list:
        """
        Get entities that are equal to entity in preference list
        """
        for p in preference_list:
            if entity in p:
                return p
            

    def _P_k(self, lecturer) -> list:
        """
        Return list of projects offered by lecturer l_k
        """
        return [
            project for project in self._projects if self._projects[project][1] == lecturer
        ]
    

    def _L_k_j(self, lecturer, project) -> list:
        """
        Return projected preference list of lecturer l_k for project p_j
        """
        return [
            s for students in self._lecturers[lecturer][1] for s in students if project in self._students[s][1]
        ]


    def _theta(self, student, project) -> gp.LinExpr:
        """
        theta_{ij} = 1 - (sum of x_{ij'} over projects p_{j'} equal or higher than p_j in student's preference list)
        theta_{ij} = 1 iff student is unassigned or prefers p_j to M(s_i)
        """
        theta_ij = gp.LinExpr()
        sum_outranked_projects = gp.LinExpr()

        for p_jprime in self._get_outranked_entities(self._students[student][1], project):
            sum_outranked_projects += self._students[student][1][p_jprime]

        theta_ij.addConstant(1)
        theta_ij.add(sum_outranked_projects, -1)

        return theta_ij
    

    def _theta_star(self, student, project) -> gp.LinExpr:
        """
        theta_{ij} = (sum of x_{ij'} over projects p_{j'} equal to p_j in student's preference list) - x_{ij}
        theta_{ij} = 1 iff student is indifferent between p_j and M(s_i), where p_j != M(s_i)
        """
        theta_star_ij = gp.LinExpr()
        sum_equal_projects = gp.LinExpr()

        for p_jprime in self._get_equal_entities(self._students[student][0], project):
            sum_equal_projects += self._students[student][1][p_jprime]

        theta_star_ij.add(sum_equal_projects)
        theta_star_ij.add(self._students[student][1][project], -1)

        return theta_star_ij
    

    def _get_project_occupancy(self, project) -> gp.LinExpr:
        """
        Get the occupancy of project p_j defined as
        sum_{i=1}^{|S|} x_{ij}
        """
        project_occupancy = gp.LinExpr()
        for student in self._students:
            if project in self._students[student][0]:
                project_occupancy += self._students[student][1][project]

        return project_occupancy
    

    def _alpha(self, project) -> gp.Var:
        """
        alpha_j \in {0, 1} s.t. (1 <= j <= |P|)
        alpha_j = 1 <= project p_j is undersubscribed
        """
        alpha_j = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{project} is undersubscribed")
        c_j = self._projects[project][0]
        project_occupancy = self._get_project_occupancy(project)

        # CONSTRAINT: ensures p_j is not oversubscribed
        self.J.addConstr(c_j * alpha_j >= c_j - project_occupancy, f"Constraint (4.8) for {project}")
        return alpha_j
    

    def _get_lecturer_occupancy(self, lecturer) -> gp.LinExpr:
        """
        Get the occupancy of lecturer l_k defined as
        sum_{i=1}^{|S|} sum_{p_j \in P_k} x_{ij}
        """
        lecturer_occupancy = gp.LinExpr()
        for project in self._P_k(lecturer):
            for student in self._students:
                if project in self._students[student][0]:
                    lecturer_occupancy += self._students[student][1][project]

        return lecturer_occupancy
    

    def _beta(self, lecturer) -> gp.Var:
        """
        beta_k \in {0, 1} s.t. (1 <= k <= |L|)
        beta_k = 1 <= lecturer l_k is undersubscribed
        """
        lecturer_capacity = self._lecturers[lecturer][0]
        beta_k = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{lecturer} is undersubscribed")
        lecturer_occupancy = self._get_lecturer_occupancy(lecturer)

        # CONSTRAINT: if l_k is undersubscribed in M, beta_k = 1
        self.J.addConstr(lecturer_capacity * beta_k >= lecturer_capacity - lecturer_occupancy, f"Constraint (4.9) for {lecturer}")
        return beta_k

    
    def _eta(self, lecturer) -> gp.Var:
        """
        eta_k \in {0, 1} s.t. (1 <= k <= |L|)
        eta_k = 1 <= lecturer l_k is full
        """
        eta_k = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{lecturer} is full")
        d_k = self._lecturers[lecturer][0]
        lecturer_occupancy = self._get_lecturer_occupancy(lecturer)
        lecturer_occupancy.addConstant(1)

        # CONSTRAINT: if l_k is full in M, eta_k = 1
        self.J.addConstr(d_k * eta_k >= lecturer_occupancy - d_k, f"Constraint (4.11) for {lecturer}")
        return eta_k
    

    def _delta(self, student, lecturer) -> gp.Var:
        """
        delta_{ik} \in {0, 1} s.t. (1 <= i <= |S|, 1 <= k <= |L|)
        delta_{ik} = 1 <= s_i \in M(l_k) or l_k prefers s_i to a worst student in M(l_k) or l_k is indifferent between them
        """
        delta_ik = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{student} is assigned to {lecturer}")
        d_k = self._lecturers[lecturer][0]
        lecturer_occupancy = self._get_lecturer_occupancy(lecturer)

        lecturer_preferred_occupancy = gp.LinExpr()
        D_ik = self._get_outranked_entities(self._lecturers[lecturer][1], student, strict=True)

        for student in D_ik:
            for project in self._P_k(lecturer):
                if project in self._students[student][0]:
                    lecturer_preferred_occupancy += self._students[student][1][project]

        # CONSTRAINT: if s_i \in M(l_k) or l_k prefers s_i to a worst student in M(l_k)
        # or l_k is indifferent between them, delta_{ik} = 1
        self.J.addConstr(d_k * delta_ik >= lecturer_occupancy - lecturer_preferred_occupancy, f"Constraint (4.12) for {student}, {lecturer}")
        return delta_ik
    

    def _gamma(self, project) -> gp.Var:
        """
        gamma_j \in {0, 1} s.t. (1 <= j <= |P|)
        gamma_j = 1 <= p_j is full
        """
        gamma_j = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{project} is full")
        c_j = self._projects[project][0]
        project_occupancy = self._get_project_occupancy(project)

        # CONSTRAINT: if p_j is full in M, gamma_j = 1
        self.J.addConstr(c_j * gamma_j >= 1 + project_occupancy - c_j, f"Constraint (4.14) for {project}")
        return gamma_j
    

    def _lambda(self, student, project, lecturer) -> gp.Var:
        """
        lambda_{ijk} \in {0, 1} s.t. (1 <= i <= |S|, 1 <= j <= |P|, 1 <= k <= |L|)
        lambda_{ijk} = 1 <= l_k prefers s_i to a worst student in M(p_j) or l_k is indifferent between them
        """
        lambda_ijk = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{lecturer} prefers / indifferent to {student} to a worst student in M({project})")
        c_j = self._projects[project][0]
        project_occupancy = self._get_project_occupancy(project)

        project_preferred_occupancy = gp.LinExpr()
        T_ijk = self._get_outranked_entities(self._L_k_j(lecturer, project), student, strict=True)
        for student in T_ijk:
            project_preferred_occupancy += self._students[student][1][project]

        # CONSTRAINT: if l_k prefers s_i to a worst student in M(p_j)
        # or l_k is indifferent between them, lambda_{ijk} = 1
        self.J.addConstr(c_j * lambda_ijk >= project_occupancy - project_preferred_occupancy, f"Constraint (4.15) for {student}, {project}, {lecturer}")
        return lambda_ijk
    

    def _mu(self, student, lecturer) -> gp.Var:
        """
        mu_{ik} \in {0, 1} s.t. (1 <= i <= |S|, 1 <= k <= |L|)
        mu_{ik} = 1 <= s_i in M(l_k) or l_k prefers s_i to a worst student in M(l_k)
        """
        mu_ik = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{lecturer} assigned to / prefers {student} to a worst student in M({lecturer})")
        d_k = self._lecturers[lecturer][0]
        lecturer_occupancy = self._get_lecturer_occupancy(lecturer)

        omega_ik = gp.LinExpr()
        for project in self._P_k(lecturer):
            if project in self._students[student][0]:
                omega_ik += self._students[student][1][project]

        lecturer_preferred_occupancy = gp.LinExpr()
        D_star_ik = self._get_outranked_entities(self._lecturers[lecturer][1], student)
        for student in D_star_ik:
            for project in self._P_k(lecturer):
                if project in self._students[student][0]:
                    lecturer_preferred_occupancy += self._students[student][1][project]

        # CONSTRAINT: if s_i \in M(l_k) or l_k prefers s_i to a worst student in M(l_k), mu_{ik} = 1
        self.J.addConstr(d_k * mu_ik >= omega_ik + lecturer_occupancy - lecturer_preferred_occupancy, f"Constraint (5.15) for {student}, {lecturer}")
        return mu_ik
    

    def _tau(self, student, project, lecturer) -> gp.Var:
        """
        tau_{ijk} \in {0, 1} s.t. (1 <= i <= |S|, 1 <= j <= |P|, 1 <= k <= |L|)
        tau_{ijk} = 1 <= l_k prefers s_i to a worst student in M(p_j)
        """
        tau_ijk = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{lecturer} prefers {student} to a worst student in M({project})")
        c_j = self._projects[project][0]
        project_occupancy = self._get_project_occupancy(project)

        T_star_ijk = self._get_outranked_entities(self._L_k_j(lecturer, project), student)
        project_preferred_occupancy = gp.LinExpr()
        for student in T_star_ijk:
            project_preferred_occupancy += self._students[student][1][project]

        # CONSTRAINT: if l_k prefers s_i to a worst student in M(p_j), tau_{ijk} = 1
        self.J.addConstr(c_j * tau_ijk >= project_occupancy - project_preferred_occupancy, f"Constraint (5.17) for {student}, {project}, {lecturer}")
        return tau_ijk

    
    def _blocking_pair_constraints(self) -> None:
        for student in self._students:
            for project in self._students[student][1]:
                lecturer = self._projects[project][1]

                theta_ij = self._theta(student, project)
                theta_star_ij = self._theta_star(student, project)
                alpha_j = self._alpha(project)
                beta_k = self._beta(lecturer)

                eta_k = self._eta(lecturer)
                delta_ik = self._delta(student, lecturer)

                gamma_j = self._gamma(project)
                lambda_ijk = self._lambda(student, project, lecturer)

                mu_ik = self._mu(student, lecturer)

                tau_ijk = self._tau(student, project, lecturer)

                # blocking pair 1i
                self.J.addConstr(theta_ij + alpha_j + beta_k <= 2, f"Blocking pair 1i for {student} and {project} (5.11)")
                # blocking pair 1ii
                self.J.addConstr(theta_ij + alpha_j + eta_k + delta_ik <= 3, f"Blocking pair 1ii for {student} and {project} (5.12)")
                # blocking pair 1iii
                self.J.addConstr(theta_ij + gamma_j + lambda_ijk <= 2, f"Blocking pair 1iii for {student} and {project} (5.13)")

                # blocking pair 2i
                self.J.addConstr(theta_star_ij + alpha_j + beta_k <= 2, f"Blocking pair 2i for {student} and {project} (5.14)")
                # blocking pair 2ii
                self.J.addConstr(theta_star_ij + alpha_j + eta_k + mu_ik <= 3, f"Blocking pair 2ii for {student} and {project} (5.16)")
                # blocking pair 2iii
                self.J.addConstr(theta_star_ij + gamma_j + tau_ijk <= 2, f"Blocking pair 2iii for {student} and {project} (5.18)")


    def _objective_function(self) -> None:
        all_xij = gp.quicksum(self._students[student][1][project] for student in self._students for project in self._students[student][1])
        self.J.setObjective(all_xij, GRB.MAXIMIZE)


    def _construct_matching(self) -> None:
        """
        Construct matching after optimising.
        Stored in self.matching
        """
        for student in self._students:
            for project in self._students[student][1]:
                if self._students[student][1][project].x == 1.0:
                    lecturer = self._projects[project][1]
                    self.matching[student] = project
                    
                    break


    def solve(self) -> None:
        self._matching_constraints()
        self._blocking_pair_constraints()
        self._objective_function()

        self.J.optimize()
        self._construct_matching()


if __name__ == "__main__":
    G = GurobiSPAST("instance.txt")
    G.solve()
    print(G.matching)