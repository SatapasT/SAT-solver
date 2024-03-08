import time

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

            #branch True
            if literal not in partial_assignment and -literal not in partial_assignment:
                simplified_clause_set = try_literal(clause_set, literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer

                #branch False
                simplified_clause_set = try_literal(clause_set, -literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(-literal)
                    answer = branching_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    
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
    
    if not clause_set:
        for literal in unique_literals:
            if literal not in partial_assignment and -literal not in partial_assignment:
                partial_assignment.append(literal)
        return sorted(partial_assignment, key=abs)

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

    for clause in clause_set:
        if not clause:
            return False

    for clause in clause_set:
        for literal in clause:

            if literal not in partial_assignment and -literal not in partial_assignment:
                simplified_clause_set = try_literal(clause_set, literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(literal)
                    answer = dpll_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer

                simplified_clause_set = try_literal(clause_set, -literal)
                if simplified_clause_set is not None:
                    partial_assignment.append(-literal)
                    answer = dpll_sat_solve(simplified_clause_set, partial_assignment, unique_literals)
                    if answer:
                        return answer
                    
                return False  
            
    return False 

# Testing the branching_sat_solve function
print("Testing branching_sat_solve")
try:
    sat1 = [[1],[1,-1],[-1,-2]]
    check = branching_sat_solve(sat1,[])
    assert check == [1,-2] or check == [-2,1], f"Returned: {check}"
    print("Test (SAT) passed")
except Exception as e:
    print("branching_sat_solve did not work correctly for a SAT instance:", e)

try:
    unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
    check = branching_sat_solve(unsat1,[])
    assert (not check), f"Returned: {check}"
    print("Test (UNSAT) passed")
except Exception as e:
    print("branching_sat_solve did not work correctly for an UNSAT instance:", e)


clause_set = [[1],[3, -1], [1, 1], [-4, 4], [2, -4, 4],[2],[5],[-5,2,3],[-6],[6,1,2],[1,2,3,4,5,6,7,8,9],[-8],[-1,-2,-3,-4,-5,-6,-7,-8,-9],]

# Measure runtime for branching_sat_solve with an empty initial partial assignment
start_time = time.time()
for i in range(1000):
    branching_sat_result = branching_sat_solve(clause_set, [])
end_time = time.time()
branching_sat_runtime = end_time - start_time

print("simple_sat_solve runtime: ", branching_sat_runtime, branching_sat_result)

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

# Measure runtime for branching_sat_solve with an empty initial partial assignment
start_time = time.time()
for i in range(1000):
    dpll_sat_solve_result = dpll_sat_solve(clause_set, [])
end_time = time.time()
dpll_sat_solve_runtime = end_time - start_time

print("dpll_sat_solve runtime: ", dpll_sat_solve_runtime,dpll_sat_solve_result )
