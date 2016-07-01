from utils.general_utils import type_checking
from .clause import Clause
"""
rule (trading rule) is represented by boolean formula of sum of products (SOP). Means that the formula is built of
clauses with OR operator between 2 clauses, and evey clauses is built of predicates with AND operator between.
e.g: (p1 AND p2) OR (p3 AND p4 AND p5) OR (p6)

Implementation: Predicate is instance of Term class object. Clause is list of terms and Rule is list of clauses.
So the example from above will look as: [[t1, t2], [t3, t4, t5] [t6]].
"""


class Rule:
    """
    Rule implementation is by list of clauses. The logical operator is implicit- we tread is as between the clauses
    there is AND operator.
    """
    def __init__(self, type, *clauses):
        """
        :param type: open or close rule. Defined in RULE_TYPE enum
        :param clauses: the clauses combined the rule
        """
        type_checking(Clause, *clauses)
        self.type = type
        self.clauses = clauses  # this is list of clauses
        [c.set_index(self.clauses.index(c)+1) for c in clauses]

    def get_clauses(self):
        return self.clauses

    def get_type(self):
        return self.type


