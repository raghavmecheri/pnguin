from enum import Enum

operations = {
    "<": lambda lhs, rhs: lhs < rhs,
    ">": lambda lhs, rhs: lhs > rhs,
    "<=": lambda lhs, rhs: lhs <= rhs,
    ">=": lambda lhs, rhs: lhs >= rhs,
    "==": lambda lhs, rhs: lhs == rhs,
    "IN": lambda lhs, rhs: lhs in rhs,
}

sql_map = {"<": "<", ">": ">", "<=": "<=", ">=": ">=", "==": "=", "IN": "IN"}


def perform_filter(lhs, operator, rhs):
    operation = operations[operator]
    return operation(lhs, rhs)


class FilterOp(str, Enum):
    le = "<"
    ge = ">"
    eq = "=="
    leq = "<="
    geq = ">="
    contains = "IN"

    @classmethod
    def fetch_sql(cls, op):
        return sql_map[op]
