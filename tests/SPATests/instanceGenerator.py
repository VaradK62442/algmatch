import random
import math
import os


class SPAS:
    def __init__(self, students, lower_bound, upper_bound):
        self.no_students = students
        self.no_projects = int(math.ceil(0.5*self.no_students))
        self.no_lecturers = int(math.ceil(0.2*self.no_students))  # assume number of lecturers <= number of projects
        self.tpc = int(math.ceil(1.2*self.no_students))  # assume total project capacity >= number of projects
        self.li = lower_bound  # lower bound of the student's preference list
        self.lj = upper_bound  # upper bound of the student's preference list

        self.students = {} # student dictionary
        self.projects = {} # project dictionary
        self.lecturers = {} # lecturer dictionary

        
    def instance_generator_no_tie(self):
        """
        A program that generates a random instance for the student project allocation problem 
        with student preferences over projects and lecturer preferences over students (without ties!).
        return: a random instance of SPA-S

        
        It takes argument as follows:
            number of students
            lower bound of the students' preference list length
            upper bound of the students' preference list length
        """
        # -----------------------------------------------------------------------------------------------------------------------------------------
        # ---------------------------------------        ====== PROJECTS =======                    -----------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------------------------------
        # projects have [at least capacity 1, empty string to assign lecturer, empty list to store students]
        self.projects = {f"p{i}": {"upper_quota": 1, "lec": "", "list": []} for i in range(1, self.no_projects+1)}
        project_list = list(self.projects.keys())
        # randomly assign the remaining project capacities
        for i in range(self.tpc - self.no_projects):  # range(9 - 8) = range(1) = 1 iteration. Okay!
            self.projects[random.choice(project_list)]["upper_quota"] += 1
        # -----------------------------------------------------------------------------------------------------------------------------------------
        # ---------------------------------------        ====== STUDENTS =======                    -----------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------------------------------
        self.students = {f"s{i}": {"list": []} for i in range(1, self.no_students + 1)}  # stores randomly selected projects
        for student in self.students:
            length = random.randint(self.li, self.lj)  # randomly decide the length of each student's preference list
            #  based on the length of their preference list, we provide projects at random
            projects_copy = project_list[:] # deep copy of list so that deletion only happens in the copy
            for i in range(length):
                p = random.choice(projects_copy)
                projects_copy.remove(p)  # I did this to avoid picking the same project 2x. This could also be achieved by shuffling and popping?
                self.students[student]["list"].append(p)
                self.projects[p]["list"].append(student)

        # -----------------------------------------------------------------------------------------------------------------------------------------
        # ---------------------------------------        ====== LECTURERS =======                    ----------------------------------------------
        # -----------------------------------------------------------------------------------------------------------------------------------------
        # lecturers have [capacity set to 0, empty list to store projects, empty list to store students, max c_j: p_j \in P_K, \sum_{p_j \in P_k} c_j]
        self.lecturers = {f"l{i}": {"upper_quota": 0, "projects": [], "list": [], "max_proj_uquota": 0, "sum_proj_uquota": 0} for i in range(1, self.no_lecturers + 1) }
        lecturer_list = list(self.lecturers.keys())
        upper_bound = math.floor(self.no_projects / self.no_lecturers)
        projects_copy = project_list[:]  # deep copy all the projects
        for lecturer in self.lecturers:
            # the number of projects a lecturer can offer is firstly bounded below by 1 and above by floor(total_projects/total_lecturers)
            # to ensure projects are evenly distributed among lecturers
            number_of_projects = random.randint(1, upper_bound)
            for i in range(number_of_projects):
                p = random.choice(projects_copy)
                projects_copy.remove(p)  # I did this to avoid picking the same project 2x. This could also be achieved by shuffling and popping?
                self.projects[p]["lec"] = lecturer  # take note of the lecturer who is offering the project
                self.lecturers[lecturer]["projects"].append(p)
                self.lecturers[lecturer]["list"].extend(self.projects[p]["list"])  # keep track of students who have chosen this project for the lecturer
                self.lecturers[lecturer]["sum_proj_uquota"] += self.projects[p]["upper_quota"]  # increment the total project capacity for each lecturer
                if self.projects[p]["upper_quota"] > self.lecturers[lecturer]["max_proj_uquota"]:  # keep track of the project with the highest capacity
                    self.lecturers[lecturer]["max_proj_uquota"] = self.projects[p]["upper_quota"]
        # -----------------------------------------------------------------------------------------------------------------------------------------
        # if at this point some projects are still yet to be assigned to a lecturer
        while projects_copy:
            p = projects_copy.pop()  # remove a project from end of the list
            lecturer = random.choice(lecturer_list)  # pick a lecturer at random
            self.projects[p]["lec"] = lecturer  # take note of the lecturer who is offering the project
            self.lecturers[lecturer]["projects"].append(p)
            self.lecturers[lecturer]["list"].extend(self.projects[p]["list"])  # keep track of students who have chosen this project for the lecturer
            self.lecturers[lecturer]["sum_proj_uquota"] += self.projects[p]["upper_quota"]  # increment the total project capacity for each lecturer
            if self.projects[p]["upper_quota"] > self.lecturers[lecturer]["max_proj_uquota"]:
                self.lecturers[lecturer]["max_proj_uquota"] = self.projects[p]["upper_quota"]
        # -----------------------------------------------------------------------------------------------------------------------------------------
        #  Now we decide the ordered preference for each lecturer. We convert to set and back to list because set removes duplicate.
        #  There will be duplicates in the lecture --> students list since we add a student to a lecturer's list for every project the student
        #  has in common with the lecturer, which could be more than 1.
        # capacity for each lecturer can also be decided here..
        for lecturer in self.lecturers:
            self.lecturers[lecturer]["list"] = list(set(self.lecturers[lecturer]["list"]))
            random.shuffle(self.lecturers[lecturer]["list"])  # this line shuffles the final preference list for each lecturer. Hence ordered!
            self.lecturers[lecturer]["upper_quota"] = random.randint(self.lecturers[lecturer]["max_proj_uquota"], self.lecturers[lecturer]["sum_proj_uquota"])  # capacity for each lecturer


    def write_instance_no_ties(self, filename):  # writes the SPA-S instance to a txt file

        with open(filename, 'w') as Instance:

            # ---------------------------------------------------------------------------------------------------------------------------------------
            #  ...write number of student (n) number of projects (m) number of lecturers (k) ---- for convenience, they are all separated by space
            Instance.write(str(self.no_students) + ' ' + str(self.no_projects) + ' ' + str(self.no_lecturers) + '\n')
            # ---------------------------------------------------------------------------------------------------------------------------------------

            # ---------------------------------------------------------------------------------------------------------------------------------------
            # .. write the students index and their corresponding preferences ---- 1 2 3 1 7
            for n in range(1, self.no_students + 1):
                preference = self.students[f"s{n}"]["list"]
                sliced = [p[1:] for p in preference] # this only grabs the project index, e.g., p20 becomes 20 and p100 becomes 100
                Instance.write(str(n) + ' ')
                Instance.writelines('%s ' % p for p in sliced)
                Instance.write('\n')
            # ---------------------------------------------------------------------------------------------------------------------------------------

            # ---------------------------------------------------------------------------------------------------------------------------------------
            #  ..write each project's index, its capacity and the lecturer who proposed it ------- 1 5 1
            for m in range(1, self.no_projects + 1):
                project = f"p{m}"                    
                upper_quota = self.projects[project]["upper_quota"]
                lecturer = self.projects[project]["lec"][1:] # index of the lecturer that offers the project
                Instance.write(str(m) + ' ' + str(upper_quota) + ' ' + str(lecturer))
                
                Instance.write('\n')
            # ---------------------------------------------------------------------------------------------------------------------------------------

            # ---------------------------------------------------------------------------------------------------------------------------------------
            # .. write each lecturer's index, their capacity and their corresponding preferences ---- 1 2 3 1 7
            for k in range(1, self.no_lecturers + 1):
                lecturer = f"l{k}"
                upper_quota = self.lecturers[lecturer]["upper_quota"]
                preference = self.lecturers[lecturer]["list"]
                sliced = [s[1:] for s in preference] # this only grabs the student index, e.g., s20 becomes 20 and s100 becomes 100
                Instance.write(str(k) + ' ' + str(upper_quota) + ' ')
                Instance.writelines('%s ' % s for s in sliced)
                Instance.write('\n')
            # ---------------------------------------------------------------------------------------------------------------------------------------
            Instance.close()
    

def main():
    total_students = 6
    # total_projects =0.5*(total_students)
    # total_lecturers = 0.2*(total_students)
    lower_bound, upper_bound = 2, 3 # make sure this does not exceed the total number of projects
    for k in range(1, 11):
        S = SPAS(total_students, lower_bound, upper_bound)
        S.instance_generator_no_tie()
        file = 'instance'+str(k)+'.txt'
        # check if instances dir exists
        if not os.path.exists('instances'):
            os.makedirs('instances')    
        filename = 'instances/'+ file
        S.write_instance_no_ties(filename)


if __name__ == "__main__":
    main()