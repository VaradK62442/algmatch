# Data Format Guideline - Stable Marriage Problem

## File

Please use the following format for passing in a text file to specify the preference lists for a Stable Marriage Problem instance.

Let `i` be the number of men and `j` the number of women.

```txt
i j
<man number 1> <preference list of women numbers>
<man number 2> <preference list of women numbers>
...
<man number i> <preference list of women numbers>
<woman number 1> <preference list of men numbers>
<woman number 2> <preference list of men numbers>
...
<woman number j> <preference list of men numbers>
```

An example file could look like this:

```txt
4 4
1 2 4 1 3
2 3 1 4 2
3 2 3 1 4
4 4 1 3 2
1 2 1 4 3
2 4 3 1 2
3 1 4 3 2
4 2 1 4 3
```

which is a case with 4 men and 4 women, where:

- man 1 prefers women 2 to 4 to 1 to 3,
- women 3 prefers man 1 to 4 to 3 to 2,
- and so on for the other six people.

## Dictionary

Please provide the following dictionary to instantiate a preference list for the Stable Marriage stable matching algorithm.

Let `i` be the number of men, and `j` the number of women.

```txt
{
    'men': {
        <man number 1>: <preference list of women numbers>,
        <man number 2>: <preference list of women numbers>,
        ...
        <man number i>: <preference list of women numbers>
    },
    'women': {
        <woman number 1>: <preference list of men numbers>,
        <woman number 2>: <preference list of men numbers>,
        ...
        <woman number j>: <preference list of men numbers>
    }
}
```

An example dictionary could look like this:

```
{
    'men': {
        1: [2, 4, 1, 3],
        2: [3, 1, 4, 2],
        3: [2, 3, 1, 4],
        4: [4, 1, 3, 2]
    },
    'women': {
        1: [2, 1, 4, 3],
        2: [4, 3, 1, 2],
        3: [1, 4, 3, 2],
        4: [2, 1, 4, 3]
    }
}
```

which is the same case with 4 men and 4 women, where:

- man 1 prefers women 2 to 4 to 1 to 3,
- women 3 prefers man 1 to 4 to 3 to 2,
- and so on for the other six people.