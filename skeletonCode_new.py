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
        temp_assignment = {}
        for literal in partial_assignment:
            temp_assignment[abs(literal)] = literal > 0
        partial_assignment = temp_assignment

    if not clause_set:
        return [i if partial_assignment[i] else -i for i in partial_assignment]

    if all_clauses_satisfy(clause_set, partial_assignment):
        return [i if partial_assignment[i] else -i for i in partial_assignment]

    variable = find_unassigned_variable(clause_set, partial_assignment)
    if variable is None: 
        return False

    for value in [True, False]:
        new_partial_assignment = copy.deepcopy(partial_assignment)
        new_partial_assignment[variable] = value
        answer = branching_sat_solve(clause_set, new_partial_assignment)
        if answer:
            return answer  

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


def dpll_sat_solve(clause_set,partial_assignment):
    ...



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
sat1 = [[3, -1], [1, 1], [-4, 4], [2, -4, 4]]
#sat1 = load_dimacs("8queens.txt")
print(branching_sat_solve(sat1,[-2]))




