from .hospitalResidentsProblem import HospitalResidentsProblem
from .stableMarriageProblem import StableMarriageProblem
from .studentProjectAllocation import StudentProjectAllocation
from .studentProjectAllocationProjects import StudentProjectAllocationProjectsSingle
from .studentProjectAllocationProjects import StudentProjectAllocationProjectsMultiple

from .hospitalResidentsProblem import HospitalResidentsProblem as HR
from .stableMarriageProblem import StableMarriageProblem as SM
from .studentProjectAllocation import StudentProjectAllocation as SPA
from .studentProjectAllocationProjects import StudentProjectAllocationProjectsSingle as SPAP_Single
from .studentProjectAllocationProjects import StudentProjectAllocationProjectsMultiple as SPAP_Multiple
from .studentProjectAllocationProjects import instance_to_numpy as SPAP_instance_to_numpy, solution_to_numpy as SPAP_solution_to_numpy