from pydantic import validate_arguments, ValidationError
from pnguin.models import FilterOp, perform_filter


class Filter:
    """A representaton of a FrameFilter object.

    FrameFilters may be used to filter out specific datapoints from both DataFrames and RemoteFrames.


    """

    @validate_arguments
    def __init__(self, column: str, operation: FilterOp, target):
        self.column = column
        self.operation = operation
        self.target = target
        self._validate_params()

    @validate_arguments
    def does_conform(self, row: dict):
        target_value = row[self.column]
        try:
            res = perform_filter(target_value, self.operation, self.target)
            return res
        except Exception as e:
            raise "Filter operation failed with error: {}".format(e)
        return False

    @validate_arguments
    def to_sql(self):
        def _fix_if_needed(op, target):
            if op == FilterOp.contains:
                return "({})".format(",".join(['"{0}"'.format(x) for x in target]))
            return '"{}"'.format(target) if isinstance(target, str) else target

        return "{}{}{}".format(
            self.column,
            FilterOp.fetch_sql(self.operation),
            _fix_if_needed(self.operation, self.target),
        )

    def _validate_params(self):
        def _op_check(op, target):
            if op == FilterOp.contains:
                if not isinstance(target, list):
                    return False, "be of type list for the IN operator"
                else:
                    return True, ""
            elif op == FilterOp.eq:
                if isinstance(target, list):
                    return False, "not be of type list for the equality operator"
                else:
                    return True, ""
            else:
                if isinstance(target, list):
                    return False, "not be of type list for a logical operator"
                else:
                    return True, ""

        if not isinstance(self.column, str):
            raise "Invalid parameter! The column parameter must be a column name"

        does_conform, e = _op_check(self.operation, self.target)

        if not does_conform:
            raise "Invalid parameter! The target parameter must {}".format(e)
