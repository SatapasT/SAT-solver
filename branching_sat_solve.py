import time
import copy
import itertools


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
        if not clause:
            return False

    for clause in clause_set:
        for literal in clause:

            if literal not in partial_assignment and -literal not in partial_assignment:
                simplified_clause_set = try_literal(clause_set, literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(literal)

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


def dpll_sat_solve(clause_set, partial_assignment, unique_literals=None):
    if unique_literals is None:
        unique_literals = set()
        for clause in clause_set:
            for literal in clause:
                unique_literals.add(abs(literal))

    unit_clauses = set()
    for clause in clause_set:
        if len(clause) == 1:
            unit_clauses.add(tuple(clause))

    while unit_clauses:
        unit = list(unit_clauses.pop())
        partial_assignment.append(unit[0])
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

    if not clause_set:
        for literal in unique_literals:
            if literal not in partial_assignment and -literal not in partial_assignment:
                partial_assignment.append(literal)
        return sorted(partial_assignment, key=abs)

    for clause in clause_set:
        for literal in clause:

            if literal not in partial_assignment and -literal not in partial_assignment:

                simplified_clause_set = try_literal(clause_set, literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(literal)
                    answer = dpll_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(literal)

                simplified_clause_set = try_literal(clause_set, -literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(-literal)
                    answer = dpll_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    partial_assignment.remove(-literal)
                    
                return False  
            
    return False 


def load_dimacs(file_name):
    with open(file_name, "r") as file:
        clauses_array = [
            [int(clause) for clause in line.split()[:-1]]
            for line in file if not line.startswith("p") and not line.startswith("c")
        ]
    return clauses_array


def simple_sat_solve(clause_set):
    unique_literals = set()
    for clause in clause_set:
        for literal in clause:
            unique_literals.add(abs(literal))

    all_literals = list(unique_literals)
    literals_to_indices = {}
    for index, literal in enumerate(all_literals):
        literals_to_indices[literal] = index

    possible_assignment = [True, False]
    for truth_assignment in itertools.product(possible_assignment, repeat=len(all_literals)):
        clause_set_truth = []

        for clause in clause_set:
            clause_truth = False
            for literal in clause:
                literal_index = literals_to_indices[abs(literal)]
                if literal > 0 and truth_assignment[literal_index] == True or literal < 0 and not truth_assignment[literal_index]:
                    clause_truth = True
                    break
                
            clause_set_truth.append(clause_truth)
                    
        if all(clause_set_truth):
            answer = []
            for i, literal in enumerate(all_literals):
                if not truth_assignment[i]:
                    answer.append(-literal)
                else:
                    answer.append(literal)
            return answer
        
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

clause_set =  [[1],[3, -1], [1, 1], [-4, 4], [2, -4, 4],[2],[5],[-5,2,3],[-6],[6,1,2],[1,2,3,4,5,6,7,8,9,10,11,12,12],[-8]]
print(clause_set)

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
print(simple_sat_result == branching_sat_result)
print(simple_sat_result == dpll_sat_solve_result)

def validate_solution(clause_set, solution):
    if not solution:
        return True
    for clause in clause_set:
        if not any((lit in solution) or (-lit not in solution) for lit in clause):
            return False
    return True

print(validate_solution(clause_set,simple_sat_result))
print(validate_solution(clause_set,branching_sat_result))
print(validate_solution(clause_set,dpll_sat_solve_result))
print("----------------------------------------------------------------------------------------")
clause_set = load_dimacs("8queens.txt")
clause_set = [[1],[1,-1],[-1,-2]]
print(dpll_sat_solve(clause_set,[]))
print(branching_sat_solve(clause_set,[]))
#print(simple_sat_solve(sat1), "simple")

# Measure runtime for branching_sat_solve with an empty initial partial assignment
start_time = time.time()
for i in range(10):
    dpll_sat_solve_result = dpll_sat_solve(clause_set, [])
end_time = time.time()
dpll_sat_solve_runtime = end_time - start_time


# Measure runtime for branching_sat_solve with an empty initial partial assignment
start_time = time.time()
for i in range(1):
    branching_sat_result = branching_sat_solve(clause_set, [])
end_time = time.time()
branching_sat_runtime = end_time - start_time


print("branching_sat_solve runtime: ", branching_sat_runtime,branching_sat_result )
print("dpll_sat_solve runtime: ", dpll_sat_solve_runtime,dpll_sat_solve_result )
print(validate_solution(clause_set,branching_sat_result))
print(validate_solution(clause_set,dpll_sat_solve_result))




