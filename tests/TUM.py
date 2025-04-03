from itertools import combinations
import numpy as np

from algmatch.stableMatchings.studentProjectAllocation.ties.spastSolver import (
    GurobiSPAST,
)


G = GurobiSPAST("instance.txt", output_flag=0)
G.solve()
G.display_assignments()

constr_mat = G.J.getA().toarray()


def is_TUM(A):
    rows, cols = A.shape
    for size in range(1, min(rows, cols) + 1):
        for row_indices in combinations(range(rows), size):
            for col_indices in combinations(range(cols), size):
                submatrix = A[np.ix_(row_indices, col_indices)]
                det = np.linalg.det(submatrix)
                if det not in {0, 1, -1}:
                    print(submatrix)
                    return False
    return True


print(f"Result: {is_TUM(constr_mat)}")
