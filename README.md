# Simple SAT Solver Using DPLL

This project is a simple implementation of a SAT (Satisfiability) solver that uses the **DPLL (Davis-Putnam-Logemann-Loveland)** algorithm, along with some basic backtracking and branching techniques. The solver takes as input a set of clauses in DIMACS format and outputs a solution if the formula is satisfiable, or indicates if the formula is unsatisfiable.

## Features

- **DIMACS Loader:** The solver supports loading problems in the standard DIMACS format.
- **Brute-force SAT Solver:** A simple SAT solver that tries all possible assignments.
- **Branching Solver:** A more efficient solver that explores the search space with backtracking.
- **DPLL Algorithm:** The main algorithm that leverages unit propagation and branching to solve the SAT problem.
- **Unit Propagation:** Simplifies the formula by propagating unit clauses (single-literal clauses).
- **Test Suite:** Includes basic tests for different solving methods and DIMACS file loading.
