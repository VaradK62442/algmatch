# Benchmarks

## Device 1

### Specs

RAM: 16 GB
CPU: 12th Gen Intel Core™ i7-12650H  (16 cores)
GPU: Nvidia GeForce RTX 4060
OS: Ubuntu 22.04

### Timing HR:

        Total residents: 75
        Total hospitals: 75
        Preference list length lower bound: 75
        Preference list length upper bound: 75
        
        Repetitions: 1000

        residents-optimal solver:
            average: 0.11 ms
            std.dev.: 0.03 ms
        
        hospitals-optimal solver:
            average: 3.45 ms
            std.dev.: 0.12 ms
    
### Timing SM:

        Total men: 75
        Total women: 75
        Preference list length lower bound: 75
        Preference list length upper bound: 75
        
        Repetitions: 1000

        men-optimal solver:
            average: 2.73 ms
            std.dev.: 0.14 ms
        
        women-optimal solver:
            average: 2.87 ms
            std.dev.: 0.09 ms
    
### Timing SPA:

        Total student: 50
        Lower project bound: 20
        Upper project bound: 25
        
        Repetitions: 1000

        student-optimal solver:
            average: 1.64 ms
            std.dev.: 0.40 ms
        
        lecturer-optimal solver:
            average: 1.14 ms
            std.dev.: 0.23 ms

## Device 2

### Specs

RAM: 16 GB
CPU: AMD Ryzen 9 5900hx (16 cores)
GPU: Nvidia GeForce RTX 3070
OS: Ubuntu 22.04

### Timing HR:

        Total residents: 75
        Total hospitals: 75
        Preference list length lower bound: 75
        Preference list length upper bound: 75
        
        Repetitions: 1000

        residents-optimal solver:
            average: 0.13 ms
            std.dev.: 0.04 ms
        
        hospitals-optimal solver:
            average: 4.03 ms
            std.dev.: 0.11 ms
    
### Timing SM:

        Total men: 75
        Total women: 75
        Preference list length lower bound: 75
        Preference list length upper bound: 75
        
        Repetitions: 1000

        men-optimal solver:
            average: 3.19 ms
            std.dev.: 0.15 ms
        
        women-optimal solver:
            average: 3.39 ms
            std.dev.: 0.11 ms
    
### Timing SPA:

        Total student: 50
        Lower project bound: 20
        Upper project bound: 25
        
        Repetitions: 1000

        student-optimal solver:
            average: 1.88 ms
            std.dev.: 0.43 ms
        
        lecturer-optimal solver:
            average: 1.31 ms
            std.dev.: 0.22 ms

## Device 3

### Specs

RAM: 16 GB
CPU: 12th Gen Intel Code i7-1250U
GPU: Intel Iris XE Graphics
OS: Windows 11 Home

### Timing HR:

        Total residents: 75
        Total hospitals: 75
        Preference list length lower bound: 75
        Preference list length upper bound: 75

        Repetitions: 1000

        residents-optimal solver:
            average: 0.14 ms
            std.dev.: 0.06 ms

        hospitals-optimal solver:
            average: 3.94 ms
            std.dev.: 0.70 ms

### Timing SM:

        Total men: 75
        Total women: 75
        Preference list length lower bound: 75
        Preference list length upper bound: 75

        Repetitions: 1000

        men-optimal solver:
            average: 3.14 ms
            std.dev.: 0.65 ms

        women-optimal solver:
            average: 3.29 ms
            std.dev.: 0.50 ms

### Timing SPA:

        Total student: 50
        Lower project bound: 20
        Upper project bound: 25

        Repetitions: 1000

        student-optimal solver:
            average: 1.92 ms
            std.dev.: 0.56 ms

        lecturer-optimal solver:
            average: 1.17 ms
            std.dev.: 0.30 ms
