# Infection

Robert Maratos

Khan Academy Interview Project

## Overview

This was a fun and educational project that helped model how to roll out AB testing within a connected graph of coaches and students.  The project was intended to implement two main methods: total_infection and limited_infection. total_infection takes a user and "infects" that user and all related users with a software version. Users are considered related through either direction in the student/coach relationship. Upon creation of the users, a graph search is performed to partition every connected group of users. I did this to amortize the cost of the graph searches.  By partitioning the network in the beginning, a total_infection can be performed simply by iterating over every user in the group. Further, I map each of these groups in a dictionary that keys on the size of a group. This is useful for limited_infection, in which we specify a limited number of users we would like to infect. My limited_infection algorithm maintains version consistency across every group. To select which groups to infect, I iterate through my dictionary of group sizes and infect the largest ones first. I did this for two reasons, I think it is more important to focus on large networks of users and also finding the most optimum combinations of groups is an N=NP complete problem (subset sum).  Most of my effort went into creating a visualization for this. I will let that speak for itself.

## Requirements
* Python 3
* tkinter (Included with Python 3)

## Running
Visualization
```$ python3 visual.py```

Instructions:
1. Press s to Begin
2. Choose number of users, number of coaches, and maximum number of students.
3. Enjoy the organized chaos. The dalek like suction cup represents a student absorbing information from a coach.
4. Select a color from the gradient to choose the version
5. total_infection: click any node to infect that group
6. limited_infection: specify a number of nodes to infect and press the X

Tests
```$ python3 tests.py```

## TODO
Include instructions in visualization
Improve physics simulation to come to some sort of steady state. Although, it is fun to watch right now.
Visualize graph search by changing one node at a time.
Increase complexity of limited_infection to sometimes split a network if needed.
Write more tests
Improve visualization UI to have help screen, reset nicely
