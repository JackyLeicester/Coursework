from z3 import *

# we only care about what is inside the loop in this case
# we do not need a test case about what goes on after the loop since there are no branches after the loop
def test_run1():
    s = Solver()
    curr_token = String("curr_token")
    expression = String("expression")
    start_number = Int("start_number")
    token_number = Int("token_number")
    s.add(curr_token != "None")
    s.add(expression != "None")
    s.add(start_number > token_number)
    print(s.check())
    print(s.model())
    

def test_run2():
    s = Solver()
    curr_token = String("curr_token")
    expression = String("expression")
    start_number = Int("start_number")
    token_number = Int("token_number")
    s.add(curr_token != "None")
    s.add(expression != "None")
    s.add(start_number == token_number)
    print(s.check())
    print(s.model())

def test_run3():
    s = Solver()
    curr_token = String("curr_token")
    expression = String("expression")
    start_number = Int("start_number")
    token_number = Int("token_number")
    s.add(curr_token == "None")
    s.add(expression != "None")
    s.add(start_number > token_number)
    print(s.check())
    print(s.model())
    

def test_run4():
    s = Solver()
    curr_token = String("curr_token")
    expression = String("expression")
    start_number = Int("start_number")
    token_number = Int("token_number")
    s.add(curr_token == "None")
    s.add(expression != "None")
    s.add(start_number == token_number)
    print(s.check())
    print(s.model())

test_run1()
test_run2()
test_run3()
test_run4()

def test_parse_function():
    s = Solver()
    s.add(String("function") == "fn")
    s.add(String("lpar") == "(")
    s.add(Int("parameter") >= 0)
    s.add(String("rpar") == ")")
    print(s.check())
    print(s.model())

test_parse_function()

def test_parse_identifier_or_callexpression():
    s = Solver()
    s.add(String("next") == "(")
    print(s.check())
    print(s.model())

test_parse_identifier_or_callexpression()

def test_callexpression():
    s = Solver()
    s.add(String("rpar") == ")")
    print(s.check())
    print(s.model())

test_callexpression()

def test_accept_token1():
    s = Solver()
    s.add(String("current_token") == String("expected_token"))
    print(s.check())
    print(s.model())

def test_accept_token2():
    s = Solver()
    s.add(String("current_token") == String("expected_token"))
    print(s.check())
    print(s.model())

test_accept_token1()
test_accept_token2()