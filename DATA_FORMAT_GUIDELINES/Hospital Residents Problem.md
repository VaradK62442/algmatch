# Data Format Guideline - Hospital/Residents Problem

## File

Please use the following format for passing in a text file to specify the preference lists for a Hospital/Residents Problem instance.

Let `i` be the number of residents, `j` the number of hospital.

```txt
i j
<resident number 1> <preference list over hospital numbers>
<resident number 2> <preference list over hospital numbers>
...
<resident number i> <preference list over hospital numbers>
<hospital number 1> <capacity> <preference list over resident numbers>
<hospital number 2> <capacity> <preference list over resident numbers>
...
<hospital number j> <capacity> <preference list over resident numbers>
```

An example file could look like this:

```txt
3 2
1 1 2
2 2 1
3 1
1 2 3 2 1
2 1 1 2
```

which is a case with 2 students and 2 hospitals, where:

- resident 2 prefers hospital 2 to 1
- hospital 1 has a capacity of 2 and prefers resident 3 to 2 to 1
- etc.

## Dictionary

Please use the following format for passing in a dictionary to specify the preference lists for a Hospital/Residents Problem instance.

Let `i` be the number of residents, `j` the number of hospital.

```txt
{
    'residents': {
        <resident number 1>: <preference list over hospital numbers>,
        <resident number 2>: <preference list over hospital numbers>,
        ...
        <resident number i>: <preference list over hospital numbers>
    },
    'hospitals': {
        <hospital number 1>: {
            'capacity': <capacity>,
            'preferences': <preference list over resident numbers>
        },
        <hospital number 2>: {
            'capacity': <capacity>,
            'preferences': <preference list over resident numbers>
        },...
        <hospital number j>: {
            'capacity': <capacity>,
            'preferences': <preference list over resident numbers>
        }
    }
}
```

An example file could look like this:

```txt
{
    'residents': {
        1: [1,2],
        2: [2,1],
        3: [1]
    },
    'hospitals': {
        1: {
            'capacity': 2,
            'preferences': [3,2,1]
        },
        2: {
            'capacity': 1,
            'preferences': [1,2]
        }
    }
}
```

which is a case with 2 students and 2 hospitals, where:

- resident 2 prefers hospital 2 to 1
- hospital 1 has a capacity of 2 and prefers resident 3 to 2 to 1
- etc.