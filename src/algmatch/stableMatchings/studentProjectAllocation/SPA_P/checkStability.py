"""
Given a solved instance of a SPA-P problem, check for blocking pairs and coalitions.
"""

from algmatch.stableMatchings.studentProjectAllocation.SPA_P.SPAPSolver import GurobiSPAP


class StabilityChecker:
    def __init__(self, solver: GurobiSPAP) -> None:
        self.G = solver

        self._students = {student: self.G._students[student][0] for student in self.G._students}
        self._projects = self.G._projects
        self._lecturers = self.G._lecturers

        self._directed_graph = dict()

        self.blocking_pair = False
        self.coalition = False


    # blocking pair types
    def _typea(self, project, current_project):
        """
        s_i in M(l_k) and l_k prefers p_j to M(s_i)
        """
        current_lecturer = self._projects[current_project][1]
        preferred_lecturer = self._projects[project][1]

        if current_lecturer == preferred_lecturer:
            preference = self._lecturers[current_lecturer][1]
            if preference.index(project) < preference.index(current_project):
                self.blocking_pair = True

    def _typeb(self, project):
        """
        s_i not in M(l_k) and l_k is undersubscribed in M
        """
        lecturer = self._projects[project][1]
        if self._lecturers[lecturer][2] < self._lecturers[lecturer][0]:
            self.blocking_pair = True

    def _typec(self, project):
        """
        s_i not in M(l_k) and l_k prefers p_j to his worst non-empty project
        """
        lecturer = self._projects[project][1]
        worst_project = self._lecturers[lecturer][3]
        preference = self._lecturers[lecturer][1]
        if preference.index(project) < preference.index(worst_project):
            self.blocking_pair = True


    def check_blocking_pairs(self) -> None:
        for student in self.G.matching:
            current_project = self.G.matching[student]
            # blocking pair (i)
            if current_project == '':
                preferred_projects = self._students[student]
                for project in preferred_projects:
                    # blocking pair (ii)
                    if self._projects[project][2] < self._projects[project][0]:
                        self._typeb(project)
                        if self.blocking_pair:
                            break

                        self._typec(student, project)
                        if self.blocking_pair:
                            break

            # blocking pair (i)
            else:
                index_of_current_project = self._students[student].index(current_project)
                preferred_projects = self._students[student][:index_of_current_project]
                for project in preferred_projects:
                    # blocking pair (ii)
                    if self._projects[project][2] < self._projects[project][0]:
                        self._typea(project, current_project)
                        if self.blocking_pair:
                            break

                        current_lecturer = self._projects[current_project][1]
                        preferred_lecturer = self._projects[project][1]

                        if current_lecturer != preferred_lecturer:
                            self._typeb(project)
                            if self.blocking_pair:
                                break

                            self._typec(project)
                            if self.blocking_pair:
                                break

            if self.blocking_pair:
                break


    def _dfs(self, u, colour, found_cycle) -> None:
        if found_cycle[0]:
            return
        
        colour[u] = "grey" # nodes in current path are grey
        for v in self._directed_graph[u]:
            if colour[v] == "grey": # cycle exists
                found_cycle[0] = True
                return
            
            if colour[v] == "white":
                self._dfs(v, colour, found_cycle)

        colour[u] = "black" # nodes is completely visited


    def _check_cycle(self) -> bool:
        # source -- https://algocoding.wordpress.com/2015/04/02/detecting-cycles-in-a-directed-graph-with-dfs-python/
        
        colour = {u: "white" for u in self._directed_graph} # all nodes initially white (unvisited)
        found_cycle = [False]

        for u in self._directed_graph:
            if colour[u] == "white":
                self._dfs(u, colour, found_cycle)
            if found_cycle[0]:
                break

        return found_cycle[0]


    def check_coalitions(self) -> None:
        for s1 in self._students:
            self._directed_graph[s1] = []
            for s2 in self._students:
                if s1 != s2 and self.G.matching[s1] != '' and self.G.matching[s2] != '':
                    current_project = self.G.matching[s1]
                    preferred_project = self.G.matching[s2]
                    prefence = self._students[s1]

                    if preferred_project in prefence and (prefence.index(preferred_project) < prefence.index(current_project)):
                        self._directed_graph[s1].append(s2)

        self.coalition = self._check_cycle()

    
    def check_stability(self) -> bool:
        self.check_blocking_pairs()
        self.check_coalitions()

        return not self.blocking_pair and not self.coalition