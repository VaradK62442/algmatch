"""
Using Gurobi Integer Programming to solve the SPA-P problem.
"""

import sys
import gurobipy as gp
from gurobipy import GRB

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.fileReader import FileReader

from collections import defaultdict


class GurobiSPAP:
    def __init__(self, filename: str, output_flag=1) -> None:
        self.filename = filename
        r = FileReader(filename)

        # self._students originally has the form: student -> [project preferences, {project: assigned?}]
        # after running _avoid_coalition, it will have the form: student -> [project preferences, {project: assigned?}, vertex label, {envy edge values}]
        self._students = r.students
        self._projects = r.projects
        self._lecturers = r.lecturers

        self.J = gp.Model("SPAP")
        self.J.setParam('OutputFlag', output_flag)

        self.matching = defaultdict(str)

    
    def _assignment_constraints(self) -> None:
        """
        Variable constraints

        x_{ij} \in {0, 1} s.t. (1 <= i <= |S|, 1 <= j <= |P|)
        x_{ij} indicates whether s_i is assigned to p_j in a solution or not

        \sum_{p_j \in A_j}(x_{ij}) <= 1 for all i in {1, 2, ..., |S|} # student can be assigned to at most one project
        \sum_{i=1}^{|S|}(x_{ij}) <= c_j for all j in {1, 2, ..., |P|} # project does not exceed capacity
        \sum_{i=1}^{|S|} \sum_{p_j \in P_k} x_{ij} <= d_k for all k in {1, 2, ..., |L|} # lecturer does not exceed capacity
        """

        for student in self._students:
            sum_student_variables = gp.LinExpr()
            for project in self._students[student][0]:
                xij = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{student} is assigned {project}")
                self._students[student][1][project] = xij
                sum_student_variables += xij

            # CONSTRAINT: student can be assigned to at most one project
            self.J.addConstr(sum_student_variables <= 1, f"Constraint for {student}")

        for project in self._projects:
            total_project_capacity = gp.LinExpr()
            for student in self._students:
                if project in self._students[student][0]:
                    total_project_capacity += self._students[student][1][project]

            # CONSTRAINT: project does not exceed capacity
            self.J.addConstr(total_project_capacity <= self._projects[project][0], f"Total capacity constraint for {project}")

        for lecturer in self._lecturers:
            total_lecturer_capacity = gp.LinExpr()
            for student in self._students:
                for project in self._students[student][0]:
                    if lecturer == self._projects[project][1]:
                        total_lecturer_capacity += self._students[student][1][project]

            # CONSTRAINT: lecturer does not exceed capacity
            self.J.addConstr(total_lecturer_capacity <= self._lecturers[lecturer][0], f"Total capacity constraint for {lecturer}")


    def _theta(self, student, project) -> gp.LinExpr:
        """
        theta_{ij} = 1 - (sum of x_{ij'} over projects p_{j'} equal or higher than p_j in student's preference list)    
        theta_{ij} = 1 iff student unassigned or prefers p_j to the project she is assigned to
        """

        theta_ij = gp.LinExpr()
        sum_outranked_projects = gp.LinExpr()

        student_preferences = self._students[student][0]
        project_index = student_preferences.index(project)

        for p_jprime in student_preferences[:project_index+1]:
            sum_outranked_projects += self._students[student][1][p_jprime]

        theta_ij.addConstant(1.0)
        theta_ij.add(sum_outranked_projects, -1.0)

        return theta_ij
    

    def _alpha(self, project) -> gp.Var:
        """
        alpha_j \in {0, 1} s.t. (1 <= j <= |P|)
        alpha_j indicates whether p_j is undersubscribed or not
        """
        alpha_j = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{project} is undersubscribed")
        c_j = self._projects[project][0]
        project_occupancy = gp.LinExpr()

        for student in self._students:
            if project in self._students[student][0]:
                project_occupancy += self._students[student][1][project]

        # CONSTRAINT: ensures p_j is not oversubscribed
        # i.e. if undersubscribed, c_j - project_occupancy = remaining_space <= c_j
        # if not, c_j - project_occupancy = remaining_space = 0
        self.J.addConstr(c_j * alpha_j >= c_j - project_occupancy, f"Constraint for {project}")
        return alpha_j
    

    def _gamma(self, student, project) -> gp.LinExpr:
        """
        gamma_{ijk} = sum of x_{ij'} over projects p_{j'} strictly worse than p_j in lecturer's preference list
        gamma_{ijk} = 1 implies student is assigned to a project p_j' where lecturer prefers p_j to p_j'
        """
        lecturer = self._projects[project][1]
        lecturer_preferences = self._lecturers[lecturer][1]
        student_preferences = self._students[student][0]

        index_of_project = lecturer_preferences.index(project)
        strictly_worse_projects = lecturer_preferences[index_of_project+1:]
        intersection = set(strictly_worse_projects).intersection(set(student_preferences)) # projects that s_i has in common with l_k

        gamma_ijk = gp.LinExpr()
        gamma_ijk = gp.quicksum(self._students[student][1][p_jprime] for p_jprime in intersection)

        return gamma_ijk
    

    def _beta(self, student, project) -> gp.LinExpr:
        """
        beta_{ik} = sum of x_{ij'} over projects p_{j'} offered by lecturer l_k
        beta_{ik} = 1 iff s_i is assigned to a project offered by l_k
        """
        lecturer = self._projects[project][1]
        lecturer_preferences = self._lecturers[lecturer][1]
        student_preferences = self._students[student][0]

        intersection = set(lecturer_preferences).intersection(set(student_preferences))
        beta_ik = gp.LinExpr()
        beta_ik = gp.quicksum(self._students[student][1][p_jprime] for p_jprime in intersection)

        return beta_ik
    

    def _eta(self, project) -> gp.Var:
        """
        eta_{jk} \in {0, 1} s.t. (1 <= j <= |P|, 1 <= k <= |L|)
        eta_{jk} indicates whether l_k is undersubscribed or prefers p_j to his worst non-empty project

        D_{kj} = set of projects p_j' offered by l_k that are equal or higher than p_j in l_k's preference list
        """
        lecturer = self._projects[project][1]
        d_k, lecturer_preferences, _, _ = self._lecturers[lecturer]
        index_of_project = lecturer_preferences.index(project)
        D_kj = lecturer_preferences[:index_of_project+1]

        eta_jk = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{lecturer} prefers {project} to his worst non-empty project")
        lecturer_occupancy = gp.LinExpr()

        for p_jprime in D_kj:
            for student in self._students:
                if p_jprime in self._students[student][0]:
                    lecturer_occupancy += self._students[student][1][p_jprime]

        # CONSTRAINT: ensures l_k is not oversubscribed
        # similar logic to alpha_j
        self.J.addConstr(d_k * eta_jk >= d_k - lecturer_occupancy, f"Constraint for {lecturer}")
        return eta_jk


    def _avoid_blocking_pair(self) -> None:
        """
        Blocking pair constraints
        """

        for student in self._students:
            for project in self._students[student][0]:
                alpha_j = self._alpha(project)
                beta_ik = self._beta(student, project)
                gamma_ijk = self._gamma(student, project)
                eta_jk = self._eta(project)
                theta_ij = self._theta(student, project)

                # blocking pair 3a
                self.J.addConstr(theta_ij + alpha_j + gamma_ijk <= 2, "Avoid blocking pair 3a")
                # blocking pair 3b and 3c
                self.J.addConstr(theta_ij + alpha_j + (1 - beta_ik) + eta_jk <= 3, "Avoid blocking pair 3b and 3c")


    def _avoid_coalition(self) -> None:
        """
        Coalition constraints

        envy graph: (s_i, s_i') => s_i prefers the project that s_i' is assigned to over what s_i is assigned to
        envy graph contains directed cycle iff there exists a coalition
        envy graph is acyclic iff it admits a topological ordering

        hence, we add constraints to ensure J admits a topological ordering

        e_{i i'} = 1 iff (s_i, s_i') in envy graph for s_i != s_i'
        """
        
        # construct vertex labels for students
        for student in self._students:
            label = self.J.addVar(lb=1.0, ub=len(self._students), obj=0.0, vtype=GRB.INTEGER, name=f"Vertex label for {student}")
            self._students[student].append(label)

        for s1 in self._students:
            self._students[s1].append(dict()) # entries for envy edge values
            s1_preferences = self._students[s1][0]
            for s2 in self._students:
                if s1 != s2:
                    envy_edge = self.J.addVar(lb=0.0, ub=1.0, obj=0.0, vtype=GRB.BINARY, name=f"{s1} envies {s2}")
                    self._students[s1][3][s2] = envy_edge

                    s2_preferences = self._students[s2][0]
                    # for every p_jprime that s1 prefers to p_j s.t. s2 finds p_jprime acceptable
                    for p_j in s1_preferences:
                        index_of_p_j = s1_preferences.index(p_j)
                        acceptable_projects = s1_preferences[:index_of_p_j]
                        intersection = set(acceptable_projects).intersection(set(s2_preferences))

                        for p_jprime in intersection:
                            # CONSTRAINT: if s_i envies s_i', then e_{i i'} = 1
                            self.J.addConstr(self._students[s1][3][s2] + 1 >= (self._students[s1][1][p_j] + self._students[s2][1][p_jprime]), "Construct envy arc")

                    # construct integer variable v_i to label topological ordering
                    # if e_{i i'} = 1, then v_i < v_i'
                    topological_ordering_LHS = gp.LinExpr() # v_i corresponding to s1
                    topological_ordering_LHS.add(self._students[s1][2], 1.0)

                    topological_ordering_RHS = gp.LinExpr() # v_i' corresponding to s2
                    topological_ordering_RHS.add(self._students[s2][2], 1.0)

                    # CONSTRAINT: following inequality is true iff graph does not admit a directed cycle
                    # v_i < v_i' + |S| ( 1 - e_{i i'} )
                    self.J.addConstr(topological_ordering_LHS + 1 <= topological_ordering_RHS + len(self._students) * (1 - self._students[s1][3][s2]), "Avoid coalition")
                    # gurobi does not support strict inequalities, hence the +1 and +|S|


    def _objective_function(self) -> None:
        """
        Objective function
        Maximise number of matched student-project pairs
        """
        total_x_ij_variables = gp.LinExpr()
        for student in self._students:
            for project in self._students[student][0]:
                total_x_ij_variables += self._students[student][1][project]

        self.J.setObjective(total_x_ij_variables, GRB.MAXIMIZE)


    def solve(self) -> None:
        self._assignment_constraints()
        self._avoid_blocking_pair()
        self._avoid_coalition()
        self._objective_function()

        self.J.optimize()
        
        for student in self._students:
            for project in self._students[student][0]:
                if self.J.getVarByName(f"{student} is assigned {project}").x == 1.0:
                    lecturer = self._projects[project][1]

                    self.matching[student] = project
                    self._projects[project][2] += 1
                    self._lecturers[lecturer][2] += 1

                    l_k_worst_project = self._lecturers[lecturer][3]
                    if l_k_worst_project is None:
                        self._lecturers[lecturer][3] = project
                    else:
                        if self._lecturers[lecturer][1].index(l_k_worst_project) < self._lecturers[lecturer][1].index(project):
                            self._lecturers[lecturer][3] = project

                    break


    def display_assignments(self) -> None:
        # assumes model has been solved
        for student in self._students:
            for project in self._students[student][0]:
                if self._students[student][1][project].x == 1: 
                    print(f"{student} -> {project}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 GurobiSPAP.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    G = GurobiSPAP(filename)
    G.solve()
    G.display_assignments()


if __name__ == "__main__":
    main()