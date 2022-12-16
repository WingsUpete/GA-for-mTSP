# Genetic Algorithm for Multiple Traveling Salesman Problem

Repository initially forked from https://github.com/Anupal/GA-for-mTSP.

<br>

## Introduction

This is a project from course - Advanced Artificial Intelligence in SUSTech (2021, Fall). The aim is to implement a genetic algorithm design for mTSP (Multiple Traveling Salesman Problem) which is able to beat the [baseline](https://github.com/Anupal/GA-for-mTSP) algorithm subject to various constraints.

<br>

## Formulation

### The Multiple Traveling Salesman Problem (mTSP) - Definition

Given ([reference](https://neos-guide.org/content/multiple-traveling-salesman-problem-mtsp)):

-   a set of `n` cities,
-   `m` salesmen,
-   one depot where the salesmen are located,
-   a cost metric,

the objective of mTSP is to provide a set of routes for `m` salesmen with a minimum total cost.

Additional constraints are as follows:

-   All routes must start and end at the same depot.
-   **Each city must be visited exactly once by only one salesman**.

<br>

### mTSP - Details

Consider a graph `G = (V, A)` where `V` is the set of `n` nodes and `A` is the set of edges. `c(i, j)` is the cost of edge `(i, j)∈A` and `C` is a cost matrix (symmetric) associated with `A`. Here `x(i, j) = 1` if edge `(i, j)` is included in a tour and vice versa. `c(m)` represents the cost of the involvement of one salesman in the solution.

**Let the depot be 1 (the first city)**. The objective function is now formulated as follow:

```math
\min \sum_{i=1}^n \sum_{j=1}^n c_{i, j} x_{i, j} + m c_m
```
<!-- img src="https://render.githubusercontent.com/render/math?math=\min%20\sum_{i=1}^n%20\sum_{j=1}^n%20c_{i,%20j}%20x_{i,%20j}%20%2b%20m%20c_m," alt="objective function" style="zoom:150%;" /-->

subject to:

-   Exactly `m` salesmen depart from the depot (node 1): <img src="https://render.githubusercontent.com/render/math?math=\sum_{j=2}^n x_{1,j} = m," alt="" style="zoom:150%;" />
-   Exactly `m` salesmen return to the depot (node 1): <img src="https://render.githubusercontent.com/render/math?math=\sum_{j=2}^n x_{j,1} = m," alt="" style="zoom:150%;" />
-   Exactly one tour enters each node: <img src="https://render.githubusercontent.com/render/math?math=\sum_{i=1}^n x_{i, j} = 1, j = 2, \dots, n," alt="" style="zoom:150%;" />
-   Exactly one tour exits each node: <img src="https://render.githubusercontent.com/render/math?math=\sum_{j=1}^n x_{i, j} = 1, i = 2, \dots, n," alt="" style="zoom:150%;" />
-   [Subtour elimination constraints](https://how-to.aimms.com/Articles/332/332-Miller-Tucker-Zemlin-formulation.html) (*): define `u(i)` as the position of node `i` in a tour, `p` as the maximum number of nodes that can be visited by any salesman: <img src="https://render.githubusercontent.com/render/math?math=u_i - u_j %2B p \cdot x_{i, j} \le p - 1, \forall 2 \le i \neq j \le n," alt="" style="zoom:150%;" />
-   General constraints for 0-1 binary variable `x`:<img src="https://render.githubusercontent.com/render/math?math=x_{i, j} \in \{0, 1\}, \forall (i,j) \in A." alt="" style="zoom:150%;" />

<br>

## Reference
- https://github.com/Anupal/GA-for-mTSP
- https://link.springer.com/content/pdf/10.1007%2F978-3-642-15220-7.pdf
- https://neos-guide.org/content/multiple-traveling-salesman-problem-mtsp

## Appendix

Notes from the original author are recorded below:

```pseudocode
Here graph is covered using different agents having different routes. Routes only intersect at initial node.
Code is provided for both TSP and mTSP.

  * Nomenclature is different with the terms 'dustbin' and 'route' being used for 'city' and 'tour' respectively.

  - The results are good for large number of nodes
  - Values of numGenerations, numTrucks, mutationRate and populationSize can be tweaked to
    reach satisfactory results.
  - Refer to https://link.springer.com/chapter/10.1007/978-3-642-15220-7_12 for more information.
```
