# Data Format Guideline - Stable Marriage Problem

## File

Please use the following format for passing in a text file to specify the preference lists for a Stable Roommates instance.

Let `i` be the number of roommates.

```txt
<roommate number 1> <preference list of other roomates numbers>
<roommate number 2> <preference list of other roomates numbers>
...
<roommate number i> <preference list of other roomates numbers>
```

An example file could look like this:

```txt
1 8 2 9 3 6 4 5 7 10
2 4 3 8 9 5 1 10 6 7
3 5 6 8 2 1 7 10 4 9
4 10 7 9 3 1 6 2 5 8
5 7 4 10 8 2 6 3 1 9
6 2 8 7 3 4 10 1 5 9
7 2 1 8 3 5 10 4 6 9
8 10 4 2 5 6 7 1 3 9
9 6 7 2 5 10 3 4 8 1
10 3 1 6 5 2 9 8 4 7
```

which is a case with 10 roommates, where:

- roommate 1 prefers 8 to 2 to 9 etc.
- roommate 2 prefers 4 to 3 to 8 etc.
- and so on for the other 8 people.

## Dictionary

Please use the following format for passing in a dictionary to specify the preference lists for a Stable Roommates instance.

Let `i` be the number of roommates.

```txt
{
    <roommate number 1>: <preference list of other roomates numbers>,
    <roommate number 2>: <preference list of other roomates numbers>,
    ...
    <roommate number i>: <preference list of other roomates numbers>
}
```

An example file could look like this:

```txt
{
    1: [8, 2, 9, 3, 6, 4, 5, 7, 10],
    2: [4, 3, 8, 9, 5, 1, 10, 6, 7],
    3: [5, 6, 8, 2, 1, 7, 10, 4, 9],
    4: [10, 7, 9, 3, 1, 6, 2, 5, 8],
    5: [7, 4, 10, 8, 2, 6, 3, 1, 9],
    6: [2, 8, 7, 3, 4, 10, 1, 5, 9],
    7: [2, 1, 8, 3, 5, 10, 4, 6, 9],
    8: [10, 4, 2, 5, 6, 7, 1, 3, 9],
    9: [6, 7, 2, 5, 10, 3, 4, 8, 1],
    10: [3, 1, 6, 5, 2, 9, 8, 4, 7]
}
```

which is the same case with 10 roommates, where:

- roommate 1 prefers 8 to 2 to 9 etc.
- roommate 2 prefers 4 to 3 to 8 etc.
- and so on for the other 8 people.