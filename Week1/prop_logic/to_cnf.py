# represents node in parse tree
class Expr:
    def __init__(self):
        # self.truth_value = 
        pass

# input = string, output = Var object. 
# represents propositional atom
class Var(Expr):
    def __init__(self, name : str):
        super().__init__()
        self.name = name        

class Not(Expr):
    def __init__(self, expr):
        super().__init__()
        self.child = expr

class And(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

class Or(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

class Implies(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

not_symbol = "~"
and_symbol = "."
or_symbol = "+"
implies_symbol = "→"
def print_expr(expr: Expr, brackets: bool = False) -> str:

    # assumptions: descending order of bindness = Not(~), And,
    # how : looks top and one ahead for human readable and bracket reduction
    #precondition : All Var.name 's are single character
    #postcondition : printed expr with/out surrounding opening and closing brackets     match expr:
    
    match expr:
        case Var(name=name):
            return name

        case Not(child=child):
            match child:
                case Var(name=name):
                    return not_symbol + name
                case Not():
                    return not_symbol * 2 + print_expr(child)
                case And() | Or() | Implies():
                    return not_symbol + print_expr(child, brackets=True)
                case _:
                    raise TypeError("Unknown child expression for Not, matched with Not but ")

        case And(left=left, right=right):
            left_str = print_expr(
                left, brackets=isinstance(left, (Or, Implies))
            )
            right_str = print_expr(
                right, brackets=isinstance(right, (Or, Implies))
            )

            combined = left_str + ' ' + and_symbol + ' ' + right_str
            combined = left_str +  and_symbol + right_str
            return f"({combined})" if brackets else combined

        case Or(left=left, right=right):
            left_str = print_expr(left, brackets=isinstance(left, Implies))
            right_str = print_expr(right, brackets=isinstance(right, Implies))

            combined = left_str + ' ' + or_symbol + ' ' + right_str
            return f"({combined})" if brackets else combined

        case Implies(left=left, right=right):
            left_str = print_expr(left, brackets=True)
            right_str = print_expr(right, brackets=True)

            combined = left_str + ' ' + implies_symbol + ' ' + right_str
            return f"({combined})" if brackets else combined

        case _:
            raise TypeError(f"Unsupported Expr: {expr}, cant match top to anything")

def print_expr_computer(expr: Expr, brackets: bool = True) -> str:
    # assumptions: descending order of bindness = Not(~), And,
    # how : looks top and one ahead for human readable and bracket reduction
    #precondition : All Var.name 's are single character
    #postcondition : printed expr with/out surrounding opening and closing brackets     match expr:
    
    match expr:
        case Var(name=name):
            return name

        case Not(child=child):
            match child:
                case Var(name=name):
                    return not_symbol + name
                case Not():
                    return not_symbol * 2 + print_expr(child)
                case And() | Or() | Implies():
                    return not_symbol + print_expr(child, brackets=True)
                case _:
                    raise TypeError("Unknown child expression for Not, matched with Not but ")

        case And(left=left, right=right):
            left_str = print_expr(
                left, brackets=True
            )
            right_str = print_expr(
                right, brackets=True
            )

            combined = left_str + ' ' + and_symbol + ' ' + right_str
            combined = left_str +  and_symbol + right_str
            return f"({combined})" if brackets else combined

        case Or(left=left, right=right):
            left_str = print_expr(left, brackets=True)
            right_str = print_expr(right, brackets=True)

            combined = left_str + ' ' + or_symbol + ' ' + right_str
            return f"({combined})" if brackets else combined

        case Implies(left=left, right=right):
            left_str = print_expr(left, brackets=True)
            right_str = print_expr(right, brackets=True)

            combined = left_str + ' ' + implies_symbol + ' ' + right_str
            return f"({combined})" if brackets else combined

        case _:
            raise TypeError(f"Unsupported Expr: {expr}, cant match top to anything")

def expr_to_impl_free(expr:Expr):
    # based on topmost node/operator calls itself recursively
    # postcondition: expr with no Implies nodes
    match expr:
        case Var():
            return expr
        
        case (Not(child=child)):
            return Not(expr_to_impl_free(child))
        
        case (And(left=left,right=right)):
            return And(expr_to_impl_free(left),expr_to_impl_free(right))
        
        case (Or(left=left,right=right)):
            return Or(expr_to_impl_free(left),expr_to_impl_free(right))
        
        case (Implies(left=left,right=right)):
            return Or(Not(expr_to_impl_free(left)), expr_to_impl_free(right))

        case _:
            raise TypeError(f"Unsupported Expr: {expr}")

def impl_free_to_nnf(expr:Expr):
    # based on topmost node/operator calls itself recursively
    # precondition: expr with no Implies nodes. Only Var, Not, And, Or
    # postcondition: expr with no Implies nodes or Not nodes of brackets or multipl Nots like ~~~
    match expr:
        case Var():
            return expr
        
        case (Not(child=child)):
            match child:
                case Var():
                    return expr
                
                case (Not(child=child)):
                    return impl_free_to_nnf(child)
                
                case (And(left=left,right=right)):
                    return Or((impl_free_to_nnf(Not(left))),(impl_free_to_nnf(Not(right))))
                
                case (Or(left=left,right=right)):
                    return And((impl_free_to_nnf(Not(left))),(impl_free_to_nnf(Not(right))))
                
                case (Implies(left=left,right=right)):
                    raise TypeError(f"Unsupported Expr: {expr}, imply-free precondition")

                case _:
                    raise TypeError(f"Unsupported Expr: {expr}, cant match Not's child in nnf conversion")

        case (And(left=left,right=right)):
            return And(impl_free_to_nnf(left),impl_free_to_nnf(right))
        
        case (Or(left=left,right=right)):
            return Or(impl_free_to_nnf(left),impl_free_to_nnf(right))
        
        case (Implies(left=left,right=right)):
            raise TypeError(f"Imply-free  precondition, recvd Imply: {print_expr(expr)}")

        case _:
            raise TypeError(f"Unsupported Expr: {print_expr(expr)}")

def distribute_to_get_CNF_or_POS(expr1:Expr, expr2:Expr):
    #  calls itself recursively, distributes over ./AND. 
    # returns CNF of OR(expr1,expr2)
    

    # precondition: expr1 and 2 in CNF or POS form. Top-node is only And, Or. Also Not(Var), Var only.
    # postcondition: computes CNF\POS form for (expr1 OR expr2)

    #check if any of the children are And nodes, if not means that both expr1 and 2 is one maxterm 
    match (expr1,expr2):
        case (And(left=left,right=right), _):
            return And(distribute_to_get_CNF_or_POS(left,expr2),distribute_to_get_CNF_or_POS(right,expr2))
        
        case (_,And(left=left,right=right)):
            return And(distribute_to_get_CNF_or_POS(expr1,left),distribute_to_get_CNF_or_POS(expr1,right))
        case (_,_):
            return Or(expr1,expr2)
        # case (Or(left=left,right=right),Var()):
        #     return Or(distribute_to_get_CNF_or_POS(left,right),expr2)

def nnf_to_cnf(expr:Expr):
    # based on topmost node/operator calls itself recursively, mainly distributes over +/OR

    # precondition: expr with no Implies nodes. Only Var, Not, And, Or as top level
    # postcondition: expr in CNF or POS form
    match expr:
        case Var():
            return expr
        
        case (Not(child=child)):
            match child:
                case Var():
                    return expr
                
                case _:
                    raise TypeError(f"Imply-free and nnf precondition, recvd non-nnf: {print_expr(expr)}")

        case (And(left=left,right=right)):
            return (And((nnf_to_cnf(left)),nnf_to_cnf(right)))
        
        case (Or(left=left,right=right)):
            #get left and right in minimized POS/CNF and then distribute
            return distribute_to_get_CNF_or_POS((nnf_to_cnf(left)),(nnf_to_cnf(right)))
                
        case (Implies(left=left,right=right)):
            raise TypeError(f"Imply-free and nnf precondition, recvd Imply: {print_expr(expr)}")

        case _:
            raise TypeError(f"Unsupported Expr: {print_expr(expr)}")

def order_the_cnf(expr):
    pass

def expr_to_cnf_expr(expr:Expr) -> Expr:
    impl_free = expr_to_impl_free(expr)
    nnf_free_and_impl_free = impl_free_to_nnf(impl_free)
    cnf = nnf_to_cnf(nnf_free_and_impl_free)
    return cnf




def parse_cnf_printed_string(s: str) -> list:
    clauses = []

    # # remove outer parentheses if present
    # while( s.startswith("(") and s.endswith(")")):
    #     s = s[1:-1]

    # split clauses
    for clause in s.split("."):
        literals = set()

        while( clause.startswith("(") and clause.endswith(")")):
            clause = clause[1:-1]

        for lit in clause.split("+"):
            literals.add(lit.strip())

        clauses.append(literals)

    return clauses

def to_cnf(expr:Expr) -> Expr:
    """
    Converts a propositional logic expression to CNF.
    Returns a list_type of clauses, each clause is a set_type of literals.
    """
    cnf_expr = expr_to_cnf_expr(expr)
    cnf_string = print_expr(cnf_expr)
    list_of_clauses = parse_cnf_printed_string(cnf_string)
    return list_of_clauses

#TEST
p = Var('P')
q = Var('Q')
r = Var('R')
s = Var('S')

# expr1 = And(Or(q,Or(r,p)),s)
expr1= Or(And(q,s),Or(And(r,s),And(p,s)))
expr1 = And(Or(Or(p,q),r),s)
# expr2 = Implies(Var("P"), Var("Q"))
expr_og = expr1

def run_test(expr_og:Expr):
    expr = expr_og

    print('OG epxr (below)')
    print(print_expr_computer((expr)) + '\n')

    print('implfree epxr (below)')
    expr = expr_to_impl_free(expr)
    print(print_expr_computer(expr) + '\n')

    print('nnf epxr (below)')
    expr = impl_free_to_nnf(expr)
    print(print_expr_computer(expr) + '\n')

    print('cnf epxr (below)')
    expr = nnf_to_cnf(expr)
    print(print_expr_computer(expr) + '\n')

    print('cnf epxr in one func (below)')
    expr = expr_to_cnf_expr(expr_og)
    print(print_expr_computer(expr) + '\n')

    print('cnf_list epxr (below)')
    expr = to_cnf(expr_og)
    print((expr) )

# run_test(expr_og=expr_og)
