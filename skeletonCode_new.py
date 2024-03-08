import itertools
import copy
import random
import time


def load_dimacs(file_name):
    with open(file_name, "r") as file:
        clauses_array = [
            [int(clause) for clause in line.split()[:-1]]
            for line in file if not line.startswith("p")
        ]
    return clauses_array


def simple_sat_solve(clause_set):
    unique_literals = set()
    for clause in clause_set:
        for literal in clause:
            unique_literals.add(abs(literal))

    all_literals = list(unique_literals)

    possible_assignment = [True, False]
    for truth_assignment in itertools.product(possible_assignment, repeat=len(all_literals)):
        assignment = dict(zip(all_literals, truth_assignment))
        clause_set_truth = []

        for clause in clause_set:
            clause_truth = False
            for literal in clause:
                if literal > 0 and assignment[literal] == True or literal < 0 and assignment[abs(literal)] == False:
                    clause_truth = True
                    break
                
            clause_set_truth.append(clause_truth)
                    
        if all(clause_set_truth):
            answer = []
            for i in all_literals:
                if not assignment[i]:
                    answer.append(-i)
                else:
                    answer.append(i)
            return answer
        
    return False

def branching_sat_solve(clause_set, partial_assignment):
    if isinstance(partial_assignment, list):
        new_assignment = {}
        for literal in partial_assignment:
            new_assignment[abs(literal)] = literal > 0
        partial_assignment = new_assignment
    
    if len(clause_set) == 0 and len(partial_assignment) == 0 :
        return []
    elif len(clause_set) == 0 and len(partial_assignment) > 0:
        return False

    if all_clauses_satisfy(clause_set, partial_assignment):

        unique_literals = set()
        for clause in clause_set:
            for literal in clause:
                unique_literals.add(abs(literal))
        
        for literal in unique_literals:
            if literal not in partial_assignment:
                partial_assignment[literal] = True

        result = []

        for i in sorted(partial_assignment.keys()):
            if partial_assignment.get(i, False):
                result.append(i)
            else:
                result.append(-i)
                
        return result 

    variable = find_unassigned_variable(clause_set, partial_assignment)
    if variable is None:
        return False

    for value in [True, False]:
        partial_assignment[variable] =  value
        answer = branching_sat_solve(clause_set, partial_assignment)
        if answer:
            return answer
        del partial_assignment[variable]

    return False


def all_clauses_satisfy(clause_set,partial_assignment):
    for clause in clause_set:
        clause_satisfy = False
        for literal in clause:
            if literal in partial_assignment and partial_assignment[abs(literal)] == True:
                clause_satisfy = True
                break
            elif -literal in partial_assignment and partial_assignment[abs(literal)] == False:
                clause_satisfy = True
                break
        
        if not clause_satisfy:
            return False
        
    return True


def find_unassigned_variable(clause_set, partial_assignment):
    for clause in clause_set:
        for literal in clause:
            if abs(literal) not in partial_assignment:
                return abs(literal)
    return None


def unit_propagate(clause_set):
    unit_clauses = set()
    for clause in clause_set:
        if len(clause) == 1:
            unit_clauses.add(tuple(clause))

    while unit_clauses:
        unit = list(unit_clauses.pop())
        new_clause_set = []
        for clause in clause_set:
            if unit[0] in clause:
                continue 
            elif -unit[0] in clause:
                new_clause = [x for x in clause if x != -unit[0]] 
                if len(new_clause) == 1:
                    unit_clauses.add(tuple(new_clause))
                elif len(new_clause) > 0:
                    new_clause_set.append(new_clause)
            else:
                new_clause_set.append(clause)

        clause_set = new_clause_set

    return clause_set


def dpll_sat_solve(clause_set, partial_assignment, unique_literals=None):

    if isinstance(partial_assignment, list):
        new_assignment = {}
        for literal in partial_assignment:
            new_assignment[abs(literal)] = literal > 0
        partial_assignment = new_assignment
    
    if unique_literals is None:
        unique_literals = set()
        for clause in clause_set:
            for literal in clause:
                unique_literals.add(abs(literal))
    
    if len(clause_set) == 0 and len(partial_assignment) == 0 :
        return []
    elif len(clause_set) == 0 and len(partial_assignment) > 0:
        return False

    unit_clauses = set()
    for clause in clause_set:
        if len(clause) == 1:
            unit_clauses.add(tuple(clause))

    while unit_clauses:
        unit = list(unit_clauses.pop())
        partial_assignment[abs(unit[0])] = unit[0] > 0
        new_clause_set = []
        for clause in clause_set:
            if unit[0] in clause:
                continue 
            elif -unit[0] in clause:
                new_clause = [x for x in clause if x != -unit[0]] 
                if len(new_clause) == 1:
                    unit_clauses.add(tuple(new_clause))
                elif len(new_clause) > 0:
                    new_clause_set.append(new_clause)
            else:
                new_clause_set.append(clause)

        clause_set = new_clause_set

    if all_clauses_satisfy(clause_set, partial_assignment):
        
        for literal in unique_literals:
            if literal not in partial_assignment:
                partial_assignment[literal] = True

        result = []

        for i in sorted(partial_assignment.keys()):
            if partial_assignment.get(i, False):
                result.append(i)
            else:
                result.append(-i)
                
        return result 

    variable = find_unassigned_variable(clause_set, partial_assignment)
    if variable is None:
        return False

    for value in [True, False]:
        partial_assignment[variable] = value
        answer = dpll_sat_solve(clause_set, partial_assignment,unique_literals)
        if answer:
            return answer
        del partial_assignment[variable]

    return False

def test():
    print("Testing load_dimacs")
    try:
        dimacs = load_dimacs("sat.txt")
        assert dimacs == [[1],[1,-1],[-1,-2]]
        print("Test passed")
    except:
        print("Failed to correctly load DIMACS file")

    print("Testing simple_sat_solve")
    try:
        sat1 = [[1],[1,-1],[-1,-2]]
        check = simple_sat_solve(sat1)
        assert check == [1,-2] or check == [-2,1]
        print("Test (SAT) passed")
    except:
        print("simple_sat_solve did not work correctly a sat instance")

    try:
        unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
        check = simple_sat_solve(unsat1)
        assert (not check)
        print("Test (UNSAT) passed")
    except:
        print("simple_sat_solve did not work correctly an unsat instance")

    print("Testing branching_sat_solve")
    try:
        sat1 = [[1],[1,-1],[-1,-2]]
        check = branching_sat_solve(sat1,[])
        assert check == [1,-2] or check == [-2,1]
        print("Test (SAT) passed")
    except:
        print("branching_sat_solve did not work correctly a sat instance")

    try:
        unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
        check = branching_sat_solve(unsat1,[])
        assert (not check)
        print("Test (UNSAT) passed")
    except:
        print("branching_sat_solve did not work correctly an unsat instance")

    print("Testing unit_propagate")
    try:
        clause_set = [[1],[-1,2]]
        check = unit_propagate(clause_set)
        assert check == []
        print("Test passed")
    except:
        print("unit_propagate did not work correctly")

    print("Testing DPLL") #Note, this requires load_dimacs to work correctly
    problem_names = ["sat.txt","unsat.txt"]
    for problem in problem_names:
        try:
            clause_set = load_dimacs(problem)
            check = dpll_sat_solve(clause_set,[])
            if problem == problem_names[1]:
                assert (not check)
                print("Test (UNSAT) passed")
            else:
                assert check == [1,-2] or check == [-2,1]
                print("Test (SAT) passed")
        except:
            print("Failed problem " + str(problem))
    print("Finished tests")

test()
clause_set = [[1],[3, -1], [1, 1], [-4, 4], [2, -4, 4],[2],[5],[-5,2,3],[-6],[6,1,2],[1,2,3,4,5,6,7,8,9],[-8],[-1,-2,-3,-4,-5,-6,-7,-8,-9]]
#sat1 = load_dimacs("LNP-6.txt")
#print(dpll_sat_solve(clause_set,[]))

# Measure runtime for simple_sat_solve
start_time = time.time()
for i in range(1000):
    simple_sat_result = simple_sat_solve(clause_set)
end_time = time.time()
simple_sat_runtime = end_time - start_time

# Measure runtime for branching_sat_solve with an empty initial partial assignment
start_time = time.time()
for i in range(1000):
    dpll_sat_solve_result = dpll_sat_solve(clause_set, [])
end_time = time.time()
dpll_sat_solve_runtime = end_time - start_time


# Measure runtime for branching_sat_solve with an empty initial partial assignment
start_time = time.time()
for i in range(1000):
    branching_sat_result = branching_sat_solve(clause_set, [])
end_time = time.time()
branching_sat_runtime = end_time - start_time


print("simple_sat_solve runtime: ", simple_sat_runtime, simple_sat_result)
print("branching_sat_solve runtime: ", branching_sat_runtime,branching_sat_result )
print("dpll_sat_solve runtime: ", dpll_sat_solve_runtime,dpll_sat_solve_result )