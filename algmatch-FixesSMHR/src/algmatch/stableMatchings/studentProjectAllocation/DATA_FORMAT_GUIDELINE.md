# Data Format Guideline - Student Project Allocation

## File

Please follow the following format for passing in a text file to instantiate a preference list for the Student Project Allocation stable matching algorithm. 

Let `i` be the number of students, `j` the number of projects, and `k` the number of lecturers.

```txt
i j k
<student number 1> <preference list over project numbers>
<student number 2> <preference list over project numbers>
...
<student number i> <preference list over project numbers>
<project number 1> <capacity> <lecturer number>
<project number 2> <capacity> <lecturer number>
...
<project number j> <capacity> <lecturer number>
<lecturer number 1> <capacity> <preference list over student numbers>
<lecturer number 2> <capacity> <preference list over student numbers>
...
<lecturer number k> <capacity> <preference list over student numbers>
```

An example file could look like

```txt
4 4 2
1 1 2
2 2 3
3 3 1
4 4 1
1 1 1
2 1 1
3 1 2
4 1 2
1 2 3 1 2 4
2 2 2 4 3
```

with 4 students, 4 projects and 2 lecturers, where

- student 1 prefers project 1 to project 2
- student 2 prefers project 2 to project 3
- project 3 has capacity 1 and supervised by lecturer 2
- professor 1 has capacity 2 and prefers student 3 to 1 to 2 to 4
- etc.

## Dictionary

Please provide the following dictionary to instantiate a preference list for the Student Project Allocation stable matching algorithm.

Let `i` be the number of students, `j` the number of projects, and `k` the number of lecturers.

```txt
{
    'students': {
        <student number 1>: <preference list over projects>,
        <student number 2>: <preference list over projects>,
        ...
        <student number i>: <preference list over projects>
    },
    'projects': {
        <project number 1>: {
            'capacity': <capacity>,
            'lecturer': <lecturer number>
        },
        <project number 2>: {
            'capacity': <capacity>,
            'lecturer': <lecturer number>
        },
        ...
        <project number j>: {
            'capacity': <capacity>,
            'lecturer': <lecturer number>
        }
    },
    'lecturers': {
        <lecturer number 1>: {
            'capacity': <capacity>,
            'preferences': <preference list over students>
        },
        <lecturer number 2>: {
            'capacity': <capacity>,
            'preferences': <preference list over students>
        },
        ...
        <lecturer number k>: {
            'capacity': <capacity>,
            'preferences': <preference list over students>
        }
    }
}
```

An example dictionary could look like

```txt
{
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
```

with 4 students, 4 projects and 2 lecturers, where

- student 1 prefers project 1 to project 2
- student 2 prefers project 2 to project 3
- project 3 has capacity 1 and supervised by lecturer 2
- professor 1 has capacity 2 and prefers student 3 to 1 to 2 to 4
- etc.