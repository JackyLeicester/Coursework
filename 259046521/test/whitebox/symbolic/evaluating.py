from z3 import *

# symbolic testing will only be used on code with branching paths
# only code with if statements were tested using this, the following is about the evaluate file
# important to mention that there are a lot of if statements in the _eval function, so the first layer of the if statement is ignored as its only ever a type check
# mainly looking for dead code
# the reason why booleans are used for variable types is because in many cases we will be checking things like enums, which z3 regards as integers and therefore creates non existent enums


# tests the _env_stack function, uses a boolean for if the value is an env, since z3 will not handle class types well
def test_env_stack1():
    is_env = Bool("is_env")
    s = Solver()
    s.add(is_env == True)
    print(s.check())
    print(s.model())


def test_env_stack2():
    is_env = Bool("is_env")
    s = Solver()
    s.add(is_env == False)
    print(s.check())
    print(s.model())


test_env_stack1()
test_env_stack2()


def test_declare_var1():
    declared = Bool("already_declared")
    s = Solver()
    s.add(declared == False)
    print(s.check())
    print(s.model())


def test_declare_var2():
    declared = Bool("already_declared")
    s = Solver()
    s.add(declared == False)
    print(s.check())
    print(s.model())


test_declare_var1()
test_declare_var2()


def test_assign_var1():
    is_const = Bool("is_const")
    s = Solver()
    s.add(is_const == False)
    print(s.check())
    print(s.model())


def test_assign_var2():
    is_const = Bool("is_const")
    s = Solver()
    s.add(is_const == True)
    print(s.check())
    print(s.model())


test_assign_var1()
test_assign_var2()

# this isnt testing a function, rather a branch of the _eval function, specifically the section about call expressions
def test_call_expression_base(identifier: str, args: int):
    identifier_s = String("node")
    identifier_length = Int("parameters_length")
    s = Solver()
    s.add(identifier_s == identifier)
    s.add(identifier_length == args)
    print(s.check())
    print(s.model())


def test_call_expression1():
    test_call_expression_base("sqrt", 1)


def test_call_expression2():
    test_call_expression_base("pow", 2)


def test_call_expression3():
    test_call_expression_base("ceil", 1)


def test_call_expression4():
    test_call_expression_base("floor", 1)


def test_call_expression5():
    test_call_expression_base("abs", 1)


# this one is a special case as there is no limit to the amount of parameters passed
def test_call_expression6():
    identifier_s = String("node")
    s = Solver()
    s.add(identifier_s == "print")
    print(s.check())
    print(s.model())


def test_call_expression7():
    identifier_s = String("node")
    s = Solver()
    s.add(identifier_s == "println")
    print(s.check())
    print(s.model())


def test_call_expression8():
    identifier_s = String("node")
    identifier_length = Int("parameters_length")
    parameter_type = String("type")
    s = Solver()
    s.add(identifier_s == "input")
    s.add(identifier_length == 1)
    s.add(parameter_type == "str")
    print(s.check())
    print(s.model())


def test_call_expression9():
    identifier_s = String("node")
    identifier_length = Int("parameters_length")
    s = Solver()
    s.add(identifier_s == "input")
    s.add(identifier_length == 0)
    print(s.check())
    print(s.model())


def test_call_expression10():
    test_call_expression_base("isInt", 1)


def test_call_expression11():
    test_call_expression_base("isFloat", 1)


def test_call_expression12():
    test_call_expression_base("toFloat", 1)


def test_call_expression13():
    test_call_expression_base("toStr", 1)


def test_call_expression14():
    test_call_expression_base("concat", 2)


def test_call_expression15():
    test_call_expression_base("trim", 1)


def test_call_expression16():
    test_call_expression_base("hasPrefix", 2)


def test_call_expression17():
    test_call_expression_base("hasSuffix", 2)


def test_call_expression18():
    test_call_expression_base("length", 1)


def test_call_expression19():
    identifier_s = String("node")
    identifier_length = Int("parameters_length")
    parameter_type = String("type")
    s = Solver()
    s.add(identifier_s == "ifExists")
    s.add(identifier_length == 1)
    s.add(parameter_type == "str")
    print(s.check())
    print(s.model())


def test_call_expression20():
    test_call_expression_base("exit", 1)


def test_call_expression21():
    identifier_s = String("node")
    parameter_count = Int("parameter_count")
    user_defined_parameters = Int("user_parameter_count")
    s = Solver()
    s.add(identifier_s != "ANY_KEYWORD")
    s.add(parameter_count == user_defined_parameters)
    print(s.check())
    print(s.model())


test_call_expression1()
test_call_expression2()
test_call_expression3()
test_call_expression4()
test_call_expression5()
test_call_expression6()
test_call_expression7()
test_call_expression8()
test_call_expression9()
test_call_expression10()
test_call_expression11()
test_call_expression12()
test_call_expression13()
test_call_expression14()
test_call_expression15()
test_call_expression16()
test_call_expression17()
test_call_expression18()
test_call_expression19()
test_call_expression20()
test_call_expression21()


def test_prefix_expression():
    operation_s = String("operation")
    for operation in ["MINUS", "PLUS", "NOT"]:
        s = Solver()
        s.add(operation_s == operation)
        print(s.check())
        print(s.model())


test_prefix_expression()

# operation is a string in place of enum
def test_infix_expression():
    operation_s = String("operation")
    for operation in [
        "PLUS",
        "MINUS",
        "ASTERISK",
        "SLASH",
        "EQUAL",
        "NOTEQUAL",
        "LESS",
        "GREATER",
        "GREATEREQUAL",
        "AND",
        "OR",
    ]:
        s = Solver()
        s.add(operation_s == operation)
        print(s.check())
        print(s.model())


test_infix_expression()

# we cant really do a type check so instead its a string check
def test_assign_expression1():
    left = String("left")
    s = Solver()
    s.add(left == "identifier")
    print(s.check())
    print(s.model())


def test_assign_expression2():
    left = String("left")
    s = Solver()
    s.add(left != "identifier")
    print(s.check())
    print(s.model())


test_assign_expression1()
test_assign_expression2()


def test_expression1():
    expression = String("expression")
    s = Solver()
    s.add(expression != "None")
    print(s.check())
    print(s.model())


def test_expression2():
    expression = String("expression")
    s = Solver()
    s.add(expression == "None")
    print(s.check())
    print(s.model())


test_expression1()
test_expression2()


def test_if1():
    if_s = Bool("if")
    s = Solver()
    s.add(if_s == True)
    print(s.check())
    print(s.model())


def test_if2():
    if_s = Bool("if")
    s = Solver()
    s.add(if_s == False)
    print(s.check())
    print(s.model())


test_if1()
test_if2()


# the following is about the parser
