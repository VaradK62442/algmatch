# Algmatch

A package containing various matching algorithms. 
- All algorithms check for blocking pairs and return a stable matching if no blocking pair is found, and None otherwise

The following algorithms are implemented so far:
- SM: Stable Marriage (both man and woman optimal)
  - SMI: Stable Marriage with incomplete lists
- HR: Hospital Residents (both residents and hospital optimal)
- SPA-S: Student Project Allocation with lecturer preferences over students (both student and lecturer optimal)
  - With verification testing
    - Tested by producing random instances
    - File to brute force all stable matchings
    - Check algorithm is generating correct stable matchings

Requires Python 3.10 or later.

TEMP:
For testing, do the following steps to build and install the package.
In the `algmatch` package, run `python3 -m build` to build the package and put build files in the `dist/` folder.
Then, run `pip install dist/*.tar.gz --force-reinstall` to install the package.
Then, from any file, you can do `import algmatch` to use the package.
