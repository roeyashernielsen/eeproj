from utils.general_general import type_checking
import term
"""
rule (trading rule) is represented by boolean formula of products of sums (POS). Means that the formula is built of
clauses with AND operator between 2 clauses, and evey clauses is built of predicates with OR operator between.
e.g: (p1 OR p2) AND (p3 OR p4 OR p5) AND (p6)

Implementation: Predicate is instance of Term class object. Clause is list of terms and Rule is list of clauses.
So the example from above will look as: [[t1, t2], [t3, t4, t5] [t6]].
"""


class Rule:
    """
    Rule implementation is by list of clauses. The logical operator is implicit- we tread is as between the clauses
    there is AND operator.
    """
    def __init__(self, *clauses):
        type_checking(Clause, *clauses)
        self.clauses = clauses  # this is list of clauses


class Clause:
    """
    Clause is implemented by simple list of Terms. The logical operator between every term is OR (implicitly).
    """
    def __init__(self, *terms):
        type_checking(term.Term, *terms)
        self.terms = terms

