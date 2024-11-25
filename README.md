# Algmatch

A package containing various matching algorithms. 
- All algorithms check for blocking pairs and return a stable matching if no blocking pair is found, and None otherwise
- All algorithms implemented have verification testing
  - Tested by producing random instances
  - File to brute force all stable matchings
  - Check algorithm is generating correct stable matchings

The following algorithms are implemented so far:
- SM: Stable Marriage (both man and woman optimal)
  - SMI: Stable Marriage with incomplete lists
- HR: Hospital Residents (both residents and hospital optimal)
- SPA-S: Student Project Allocation with lecturer preferences over students (both student and lecturer optimal)

Requires Python 3.10 or later.
