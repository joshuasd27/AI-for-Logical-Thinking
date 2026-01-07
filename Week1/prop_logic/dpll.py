not_symbol = '~'
import copy
#receives by reference since set and dict are mutable so changes in place
# if literal evaluates to 0 then deleted from clause 
#   as it will not change the truth value of the clause
# if literal evaluates to 1 then returns IS TRUE, so caller can delete clause
# if literal unassigned then moves on to next literal
# if hasn't returned then clause contains 0 or more unassigned's


def look_at_clause(clause: set, assignment: dict ={}) -> tuple[bool]:
    #iterate over literals by using a 'copy' that is a tuple
    for literal in tuple(clause):
        #evaluate literal
        not_symbol_present = ( literal[0] == not_symbol) 
        atom = (literal[1:] if not_symbol_present else literal )

        if atom in assignment:
            truth_value = assignment[atom] ^ not_symbol_present
            if (truth_value==True):
                return (True,False,False)
            else:
                clause.remove(literal)
                continue
        else:
            continue


    num_unassigned = len(clause)
    if num_unassigned==0:
        return (False,True,False)
    elif num_unassigned==1:
        literal = clause.pop()
        not_symbol_present = ( literal[0] == not_symbol) 
        atom = (literal[1:] if not_symbol_present else literal )

        truth_value = not not_symbol_present
        assignment[atom] = truth_value
        return (False,False,True)
    else:
        return (False,False,False)



#assumption: empty clause {} always is False so clauses becomes unsat
#assumption: empty lis of cluases [] is True
def dpll(clauses:list[set], assignment={}):
    """
    clauses: list of sets (e.g. {{'P', '~Q'}, {'Q'}})
    assignment: dict mapping variable -> bool
    Returns: (sat: bool, assignment)
    """ 
    # print('-'*90)
    if len(clauses)==0:
        return (True, assignment)

    while(True):
        # print('*',clauses,'')
        # print('*',assignment,'\n')
        
        restart_clause_checking = False
        # remove clauses which are true under given assignment, 
        # and which are unit clauses(after adding to assignments)
        # check for unsat as well
        clauses_og = tuple(clauses)
        for clause in clauses_og:
            # print('**** starting clause', clause)

            (is_true, is_false, is_unit_clause )= look_at_clause(clause,assignment)
            # print('**** ', '(is_true, is_false, is_unit_clause ):',  (is_true, is_false, is_unit_clause ) )

            if is_true:
                clauses.remove(clause)
            elif is_false:
                return (False, {})
            elif is_unit_clause:
                restart_clause_checking = True
                clauses.remove(clause)
                break
            else:
                continue

        # print('***** clauses', clauses)
        # print('***** assn', assignment)

        if restart_clause_checking:
            # print('* restart clauses','\n')
            continue

        break

    # if clauses now empty 
    if not clauses:
        # print('* clauses empty')
        return (True, assignment)
    
    #clauses not empty, unassigned literals only, take first seen
    literal = next(iter(clauses[0]))
    not_symbol_present = ( literal[0] == not_symbol) 
    atom = (literal[1:] if not_symbol_present else literal )
    lucky_atom = atom

    assignment_lucky = assignment.copy()
    assignment_lucky[lucky_atom] = not not_symbol_present  

    clauses_lucky = copy.deepcopy(clauses)
    clauses_lucky.remove(clauses[0])
    #assume literal is true
    # exit()

    lucky_true_sat, lucky_true_assn = dpll(clauses_lucky, assignment_lucky)

    if lucky_true_sat ==True:
        return (True, lucky_true_assn)
    else:
        # print(lucky_atom,'cant be True, so now false')

        assignment_lucky = assignment.copy()
        assignment_lucky[lucky_atom] = not_symbol_present
        clauses_lucky = copy.deepcopy(clauses)
        #assume literal is false
        lucky_false_sat,lucky_false_assn = dpll(clauses_lucky, assignment_lucky)
        if lucky_false_sat ==True:
            return (True, lucky_false_assn)
        else:        
            return (False, {})

# clauses = [
#         ["A", "B"],
#         ["C", "D"],
#         ["E", "F"],
#         ["G", "H"],
#         ["~A", "~C"],
#         ["~E", "~G"]
#       ]
# #list_of_sets = [set(sublist) for sublist in clauses]
# # clauses=list_of_sets
# print( dpll(clauses))

