import itertools
import copy
import random
import time


def load_dimacs(file_name):
    with open(file_name, "r") as file:
        clauses_array = []
        for line in file:
            if not line.startswith("p"):
                clause_list = []
                for clause in line.split()[:-1]:
                    clause_list.append(int(clause))
                clauses_array.append(clause_list)
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
            for literal in all_literals:
                if not assignment[literal]:
                    answer.append(-literal)
                else:
                    answer.append(literal)
            return answer
    
    return False

def branching_sat_solve(clause_set, partial_assignment, unique_literals=None):
    if unique_literals is None:
        unique_literals = set()
        for clause in clause_set:
            for literal in clause:
                unique_literals.add(abs(literal))
        
    if not clause_set:
        for literal in unique_literals:
            if literal not in partial_assignment and -literal not in partial_assignment:
                partial_assignment.append(literal)
        return sorted(partial_assignment, key=abs)

    for clause in clause_set:
        for literal in clause:
            
            #True Branch
            if literal not in partial_assignment and -literal not in partial_assignment:
                simplified_clause_set = try_literal(clause_set, literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(literal)

            #False Branch
                simplified_clause_set = try_literal(clause_set, -literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(-literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(-literal)
                    
                return False  
            
    return False  

def try_literal(clause_set, literal):
    new_clause_set = []
    for clause in clause_set:
        if literal in clause:
            continue

        if -literal in clause:
            new_clause = []
            for i in clause:
                if i != -literal:
                    new_clause.append(i)

            if not new_clause:
                return None  
            new_clause_set.append(new_clause)
        else:
            new_clause_set.append(clause)
    return new_clause_set


def unit_propagate(clause_set):
    unit_clauses = set()
    for clause in clause_set:
        if len(clause) == 1:
            literal = clause[0]
            if -literal in unit_clauses:
                return False 
            
            unit_clauses.add(literal)

    while unit_clauses:
        unit = unit_clauses.pop()
        new_clause_set = []
        for clause in clause_set:
            if unit in clause:
                continue  

            elif -unit in clause:
                new_clause = []
                for x in clause:
                    if x != -unit:
                        new_clause.append(x)
                if len(new_clause) == 0:
                    return False

                elif len(new_clause) == 1:
                    new_unit = new_clause[0]
                    if -new_unit in unit_clauses:
                        return False 
                    unit_clauses.add(new_unit)
                    
                else:
                    new_clause_set.append(new_clause)

            else:
                new_clause_set.append(clause)
        clause_set = new_clause_set

    return clause_set


def dpll_sat_solve(clause_set, partial_assignment, unique_literals=None):
    if unique_literals is None:
        unique_literals = set()
        for clause in clause_set:
            for literal in clause:
                unique_literals.add(abs(literal))

    unit_clauses = set()
    for clause in clause_set:
        if len(clause) == 1:
            literal = clause[0]
            if -literal in unit_clauses:
                return False 
            unit_clauses.add(literal)

    while unit_clauses:
        unit = unit_clauses.pop()
        new_clause_set = []
        partial_assignment.append(unit)
        
        for clause in clause_set:
            if unit in clause:
                continue  

            elif -unit in clause:
                new_clause = []
                for x in clause:
                    if x != -unit:
                        new_clause.append(x)
                if len(new_clause) == 0:
                    return False

                elif len(new_clause) == 1:
                    new_unit = new_clause[0]
                    if -new_unit in unit_clauses:
                        return False 
    
                    unit_clauses.add(new_unit)
                    
                else:
                    new_clause_set.append(new_clause)

            else:
                new_clause_set.append(clause)
        
        clause_set = new_clause_set
        
    if not clause_set:
        for literal in unique_literals:
            if literal not in partial_assignment and -literal not in partial_assignment:
                partial_assignment.append(literal)
        return sorted(partial_assignment, key=abs)

    for clause in clause_set:
        for literal in clause:

            #True Branch
            if literal not in partial_assignment and -literal not in partial_assignment:
                simplified_clause_set = try_literal(clause_set, literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(literal)

            #False Branch
                simplified_clause_set = try_literal(clause_set, -literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(-literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(-literal)
                    
                return False  
            
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