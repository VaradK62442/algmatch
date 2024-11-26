# Algmatch

A package containing various two-sided matching algorithms. 
- SM: Stable Marriage (both man and woman optimal)
- HR: Hospital Residents (both residents and hospital optimal)
- SPA-S: Student Project Allocation with lecturer preferences over students (both student and lecturer optimal)

Requires Python 3.10 or later.

Format data according to the guidelines in [this](DATA_FORMAT_GUIDELINES/) folder.

# Installation

Simply run `pip install algmatch`.

# Usage

To import a specific algorithm, use `from algmatch import <algorithm>`, e.g. `from algmatch import SPA` or `from algmatch import StudentProjectAllocation`.
Create a file or dictionary with your instance, following the guidelines in the [`DATA_FORMAT_GUIDELINES`](DATA_FORMAT_GUIDELINES/) folder.
For example, 

Importing data:

```python
from algmatch import HR, SM, SPA

spa_instance = {
    'students': {
        1: [1, 2],
        2: [2, 3],
        3: [3, 1],
        4: [4, 1]
    },
    'projects': {
        1: {
            'capacity': 1,
            'lecturer': 1
        },
        2: {
            'capacity': 1,
            'lecturer': 1
        },
        3: {
            'capacity': 1,
            'lecturer': 2
        },
        4: {
            'capacity': 1,
            'lecturer': 2
        }
    },
    'lecturers': {
        1: {
            'capacity': 2,
            'preferences': [3, 1, 2, 4]
        },
        2: {
            'capacity': 2,
            'preferences': [2, 4, 3]
        }
    }
}

spa_student = SPA(dictionary=spa_instance, optimisedSide="student")
spa_lecturer = SPA(dictionary=spa_instance, optimisedSide="lecturer")
```

Getting the stable matchings:

```python
spa_student_stable_matching = spa_student.get_stable_matching()
spa_lecturer_stable_matching = spa_lecturer.get_stable_matching()

print("SPA student stable matching:")
print(spa_student_stable_matching)

print("SPA lecturer stable matching:")
print(spa_lecturer_stable_matching)
```

```
SPA 2 student stable matching:
{'student_sided': {'s1': 'p1', 's2': 'p2', 's3': 'p3', 's4': 'p4'}, 'lecturer_sided': {'l1': ['s1', 's2'], 'l2': ['s3', 's4']}}
SPA 2 lecturer stable matching:
{'student_sided': {'s1': 'p2', 's2': 'p3', 's3': 'p1', 's4': 'p4'}, 'lecturer_sided': {'l1': ['s1', 's3'], 'l2': ['s2', 's4']}}
```

See more example usage [here](examples.ipynb).

# Further details

- All algorithms check for blocking pairs and return a stable matching if no blocking pair is found, and None otherwise
- All algorithms implemented have verification testing
  - Tested by producing random instances
  - File to brute force all stable matchings
  - Check algorithm is generating correct stable matchings
