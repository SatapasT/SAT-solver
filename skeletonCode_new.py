import itertools
import timeit

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
    

def branching_sat_solve(clause_set,partial_assignment):
    ...


def unit_propagate(clause_set):
    
    unit_clauses = set() 
    for clause in clause_set:
        if len(clause) == 1:
            unit_clauses.add(tuple(clause))

    while unit_clauses:
        unit = list(unit_clauses.pop())
        clause_set.remove(unit)
        #print(clause_set)


        for clause in clause_set:
            if unit in clause:
                continue
            elif -unit[0] in clause and len(clause) > 1:
                clause.remove(-unit[0])
            
            if len(clause) == 1:
                    unit_clauses.add(tuple(clause))
                
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
#sat1 = load_dimacs("8queens.txt")
sat1 = [[1], [2], [-1,3], [3,-2]]
print(simple_sat_solve(sat1))



