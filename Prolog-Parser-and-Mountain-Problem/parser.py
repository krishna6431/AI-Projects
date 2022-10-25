#import the required things to get
import sys
import re
import enum


class Entity():
    def __init__(self, str, truth):
        """
        :param str: name of entity
        :param truth: bool truth value
        """
        self.name = str
        self.truth = truth

    def evaluate(self):
        return self.truth

    def tostring(self):
        return self.name


class Predicate():
    def __init__(self, str, entity):
        self.name = str
        self.entity = entity


class Expression:
    def __init__(self, pre, op, post):
        """
        :param pre: preceding Expression
        :param op: operation
        :param post: next Expression
        """
        self.pre = pre
        self.op = op
        self.post = post

    # Create text version of expression recursively
    def tostring(self):
        if self.pre is not None:
            pre_value = self.pre.tostring()
        else:
            pre_value = ""
        if self.post is not None:
            post_value = self.post.tostring()
        else:
            post_value = ""

        return "(" + pre_value + " " + self.op.value + " " + post_value + ")"

    # Evaluate statement recursively
    def evaluate(self):
        if self.pre is not None:
            pre_value = self.pre.evaluate()
        else:
            pre_value = None
        if self.post is not None:
            post_value = self.post.evaluate()
        else:
            post_value = None

        # Return boolean function based on type of operation
        if self.op == Op.Neg:
            def res(a, b): return not b
        elif self.op == Op.IncOr:
            def res(a, b): return a or b
        elif self.op == Op.And:
            def res(a, b): return a and b
        elif self.op == Op.Imp:
            def res(a, b): return (not a) or b
        else:
            def res(a, b): return False

        return res(pre_value, post_value)


# Each type of connective
class Op(enum.Enum):
    Neg = "~"
    IncOr = "V"
    And = "^"
    Imp = "->"

    # return Op based on string
    @staticmethod
    def parse(str):
        for connective in Op:
            if str == connective.value:
                return connective


class TruthTable:
    def __init__(self, expression):
        self.expression = expression
        self.entities = []
        self.find_entities(self.expression)

    # Recursively find unique instances of Entity objects in the statement
    def find_entities(self, expression):
        if type(expression.pre) is Entity:
            if not self.in_entities(expression.pre):
                self.entities.append(expression.pre)
        elif type(expression.pre) is Expression:
            self.find_entities(expression.pre)

        if type(expression.post) is Entity:
            if not self.in_entities(expression.post):
                self.entities.append(expression.post)
        elif type(expression.post) is Expression:
            self.find_entities(expression.post)

    # return true iff entity is already in self.entities
    def in_entities(self, entity):
        for e in self.entities:
            if e.name == entity.name:
                return True
        return False

    # return a string of each entity name in self.entities
    def print_entities(self):
        entities = ""
        for e in self.entities:
            entities += e.name + " "
        return entities

    # Create and print truth table from statement
    def construct_table(self):
        # header row
        topRow = self.print_entities() + " | " + self.expression.tostring()
        print(topRow)
        # there are 2^n rows where n is number of entities
        # for each entity, negate truth value using mods and powers of 2
        #     until every true/false combination is evaluated
        mod_counter = len(self.entities)
        for i in range(0, 2**mod_counter):
            for j in range(0, mod_counter):
                if i % 2**(j) == 0:
                    self.entities[mod_counter-1 -
                                  j].truth = not self.entities[mod_counter-1-j].truth
            self.construct_row()

    def construct_row(self):
        first_values = ""
        for e in self.entities:
            first_values += str(e.truth) + " "
        print(first_values + " | " + str(self.expression.evaluate()))


# Finding predicates, not there yet!
# for arg in sys.argv[1:]:
#     matches = re.findall("[A-Z]\([a-z]\)", arg)
#     for e in matches:
#         txt = str(e)
#         entity = Entity(txt[2])
#         obj = Predicate(txt[0] + "()", entity)
#         print(obj.name, obj.entity.name)


# return true iff open bracket count equals close bracket count
def verify_formedness(str):
    open_count = 0
    close_count = 0
    for c in str:
        if c == "(":
            open_count += 1
        elif c == ")":
            close_count += 1

    return open_count == close_count


# Recursively break up string into structure of statement using arrays
def parse_expression(str):
    parts = ["", "", ""]
    index = 0
    num_open = 0
    num_close = 0
    # Add characters to pre-subexpression until number of open parens equals number of close parens
    # Then parse connective to Op
    # Then add characters to post-subexpression and recursively parse both subexpressions
    for i in range(0, len(str)):
        c = str[i]
        if c == "(":
            num_open += 1
            parts[index] += c
        elif c == ")":
            num_close += 1
            parts[index] += c
        elif c == "^" or c == "V" or c == "-":
            if num_open == num_close:
                index += 1
                parts[index] += c
                if c == "-":
                    parts[index] += ">"
                index += 1
            else:
                parts[index] += c
        elif c == "~" and i == 0 and str[1] == "(":
            index += 1
            parts[index] += c
            index += 1
        elif c != ">":
            parts[index] += c

    for i in range(0, 3):
        # parse whole subexpression if negated, otherwise ignore top-level parentheses
        if len(parts[i]) > 2:
            if parts[i][0] == "(":
                elem = parse_expression(parts[i][1:-1])
            else:
                elem = parse_expression(parts[i])
            parts[i] = elem

    return parts


# Take arrays from parse_expression() and construct Expression objects from them
def parse_expression_object(arr):
    parts = ["", "", ""]
    for i in range(0, 3):
        # Create negated entity, entity, connective, or expression from each item in array
        if type(arr[i]) is str:
            if "~" in arr[i] and len(arr[i]) > 1:
                exp = Expression(None, Op.Neg, Entity(arr[i][-1], False))
                parts[i] = exp
            elif re.match("[a-z]", arr[i]) is not None:
                ent = Entity(arr[i], False)
                parts[i] = ent
            else:
                op = Op.parse(arr[i])
                parts[i] = op
        else:
            arr1 = parse_expression_object(arr[i])
            parts[i] = arr1
    return Expression(parts[0], parts[1], parts[2])


# # Make sure there is only one argument when calling LogicParser.py
# if len(sys.argv[1:]) != 1:
#     print("Error: unexpected number of arguments")
# else:
#     statement = sys.argv[1].replace(" ", "")
#     if verify_formedness(statement):
#         # Parse input expression and create truth table
#         parts = parse_expression(statement)
#         exp = parse_expression_object(parts)
#         table = TruthTable(exp)
#         table.construct_table()
#     else:
#         print("Error: check parenthesis count")

# Test Cases:
# 1. (P= > Q) = > ((~Q = > P) = > Q)
# 2. P = > (P V Q)
# 3. (P ^ Q) = > (P V R)


if __name__ == '__main__':
    # stmt = "p->q"
    stmt = "(p->q)->((~q->p)->q)"
    if verify_formedness(stmt):
        # Parse input expression and create truth table
        parts = parse_expression(stmt)
        exp = parse_expression_object(parts)
        table = TruthTable(exp)
        table.construct_table()
    else:
        print("Error: check parenthesis count")

