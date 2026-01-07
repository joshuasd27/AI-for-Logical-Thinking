"""
First-Order Logic - Robinson's Resolution Algorithm
Implement the Robinson resolution algorithm for FOL theorem proving.
"""

from typing import List, Tuple, Dict, Optional
import itertools


# ---------- Term / Literal Utilities ----------

def is_variable(t: str) -> bool:
    return t[0].islower()

def split_args(s: str):
    args = []
    depth = 0
    start = 0

    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(s[start:i].strip())
            start = i + 1

    args.append(s[start:].strip())
    return args


def parse_literal(lit):
    sign = True
    if lit.startswith("~"):
        sign = False
        lit = lit[1:]

    # split predicate from arguments at FIRST '('
    idx = lit.find("(")
    if idx == -1:
        raise ValueError(f"Invalid literal: {lit}")

    pred = lit[:idx]
    args_str = lit[idx+1:-1]  # strip outer parentheses

    args = split_args(args_str)
    return (sign, pred, tuple(args))


def literal_to_string(sign, predicate, args):
    s = f"{predicate}({', '.join(args)})"
    return s if sign else "~" + s


def substitute_term(t, subst: Dict[str, str]) -> str:
    while t in subst:
        t = subst[t]
    return t


def apply_substitution_literal(lit, subst):
    sign, pred, args = lit
    new_args = tuple(substitute_term(a, subst) for a in args)
    return (sign, pred, new_args)



def unify_terms(t1: str, t2: str, subst: Dict[str, str]) -> Optional[Dict[str, str]]:
    t1 = substitute_term(t1, subst)
    t2 = substitute_term(t2, subst)

    if t1 == t2:
        return subst

    if is_variable(t1):
        if occurs_check(t1, t2, subst):
            return None
        subst[t1] = t2
        return subst

    if is_variable(t2):
        if occurs_check(t2, t1, subst):
            return None
        subst[t2] = t1
        return subst

    return None


def occurs_check(v: str, t: str, subst: Dict[str, str]) -> bool:
    if v == t:
        return True
    if t in subst:
        return occurs_check(v, subst[t], subst)
    return False


def unify_literals(lit1, lit2) -> Optional[Dict[str, str]]:
    s1, p1, a1 = lit1
    s2, p2, a2 = lit2

    if p1 != p2 or s1 == s2 or len(a1) != len(a2):
        return None

    subst: Dict[str, str] = {}
    for x, y in zip(a1, a2):
        subst = unify_terms(x, y, subst)
        if subst is None:
            return None
    return subst



def robinson_resolution(
    clauses: List[List[str]],
    max_iterations: int = 1000
) -> Tuple[str, List]:

    # Parse clauses
    parsed_clauses = [
        [parse_literal(lit) for lit in clause]
        for clause in clauses
    ]

    clause_set = [tuple(c) for c in parsed_clauses]
    seen = set(clause_set)

    proof = []
    iterations = 0

    while iterations < max_iterations:
        iterations += 1
        new_clauses = []

        for c1, c2 in itertools.combinations(clause_set, 2):
            for lit1 in c1:
                for lit2 in c2:
                    subst = unify_literals(lit1, lit2)
                    if subst is None:
                        continue

                    # Build resolvent
                    resolvent = []

                    for l in c1:
                        if l != lit1:
                            resolvent.append(apply_substitution_literal(l, subst))

                    for l in c2:
                        if l != lit2:
                            resolvent.append(apply_substitution_literal(l, subst))

                    # Remove duplicates
                    resolvent = list(set(resolvent))


                    if not resolvent:
                        proof.append({
                            "parents": (c1, c2),
                            "resolved": (lit1, lit2),
                            "substitution": subst,
                            "resolvent": []
                        })
                        return "UNSAT", proof

                    resolvent_tuple = tuple(resolvent)
                    if resolvent_tuple not in seen:
                        seen.add(resolvent_tuple)
                        new_clauses.append(resolvent_tuple)
                        proof.append({
                            "parents": (c1, c2),
                            "resolved": (lit1, lit2),
                            "substitution": subst,
                            "resolvent": resolvent
                        })

        if not new_clauses:
            return "TIMEOUT", []

        clause_set.extend(new_clauses)

    return "TIMEOUT", []


clauses = [
        ["P(f(g(x)))"],
        ["~P(f(g(a)))"]
      ]
result, proof = robinson_resolution(clauses, max_iterations=50)
print(result)
print(proof)
