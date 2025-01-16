from algmatch.studentProjectAllocation import StudentProjectAllocation

from tests.abstractTestClasses.abstractVerifier import AbstractVerifier
from tests.SPATests.utils.instanceGenerator import SPAInstanceGenerator
from tests.SPATests.utils.minmaxSMs import MMSMS
from tests.SPATests.utils.enumerateSMs import ESMS

class SPASAbstractVerifier(AbstractVerifier):
    def __init__(self, total_students,
                 lower_project_bound, upper_project_bound):
        """
        It takes argument as follows (set in init):
            number of men
            number of women
            lower bound of the preference list length
            upper bound of the preference list length
        """

        self._total_students = total_students
        self._lower_project_bound = lower_project_bound
        self._upper_project_bound = upper_project_bound

        generator_args = (total_students,
                          lower_project_bound,
                          upper_project_bound)

        AbstractVerifier.__init__(
            self,
            StudentProjectAllocation,
            ("students", "lecturers"),
            SPAInstanceGenerator,
            generator_args,
            ESMS
        )