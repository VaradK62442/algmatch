# Data Format Guideline - Hospital/Residents Problem with Ties

## File

Please use the following format for passing in a text file to specify the preference lists for a Hospital/Residents Problem instance with ties.

Let `i` be the number of residents, `j` the number of hospitals. Brackets must be round; i.e ().

```txt
i j
<resident number 1> <bracketed preference list over hospital numbers>
<resident number 2> <bracketed preference list over hospital numbers>
...
<resident number i> <bracketed preference list over hospital numbers>
<hospital number 1> <capacity> <bracketed preference list over resident numbers>
<hospital number 2> <capacity> <bracketed preference list over resident numbers>
...
<hospital number j> <capacity> <bracketed preference list over resident numbers>
```

An example file could look like this:

```txt
3 2
1 1 2
2 (1 2)
3 1
1 2 (2 3) 1
2 1 1 2
```

which is a case with 3 students and 2 hospitals, where:

- resident 2 is indifferent between hospitals 1 and 2
- hospital 1 has a capacity of 2 and prefers residents 2 and 3 to 1, and is indifferent between residents 2 and 3
- etc.

## Dictionary

Please use the following format for passing in a dictionary to specify the preference lists for a Hospital/Residents Problem instance.

Let `i` be the number of residents, `j` the number of hospital. By bracketed here we mean the use of a nested list.

```txt
{
    'residents': {
        <resident number 1>: <bracketed preference list over hospital numbers>,
        <resident number 2>: <bracketed preference list over hospital numbers>,
        ...
        <resident number i>: <bracketed preference list over hospital numbers>
    },
    'hospitals': {
        <hospital number 1>: {
            'capacity': <capacity>,
            'preferences': <bracketed preference list over resident numbers>
        },
        <hospital number 2>: {
            'capacity': <capacity>,
            'preferences': <bracketed preference list over resident numbers>
        },...
        <hospital number j>: {
            'capacity': <capacity>,
            'preferences': <bracketed preference list over resident numbers>
        }
    }
}
```

An example file could look like this:

```txt
{
    'residents': {
        1: [1,2],
        2: [[1,2]],
        3: [1]
    },
    'hospitals': {
        1: {
            'capacity': 2,
            'preferences': [[2,3],1]
        },
        2: {
            'capacity': 1,
            'preferences': [1,2]
        }
    }
}
```

which is a case with 3 students and 2 hospitals, where:

- resident 2 is indifferent between hospitals 1 and 2
- hospital 1 has a capacity of 2 and prefers residents 2 and 3 to 1, and is indifferent between residents 2 and 3
- etc.