from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import evaluate, RuntimeEvaluationError
import unittest

# Test cases are specifically designed to test every possible branch in evaluator and in the process
# This will also mean that the parser and lexer will be tested, since code being able to evaluate the code will also mean tokenizing and parsing it
# Mainly involves testing branches that my user stories do not cover


def run_test(input: str):
    lexer: Lexer = Lexer(input)
    parser: Parser = Parser(lexer)
    statements = parser.run()
    return evaluate(statements)


class FunctionTester(unittest.TestCase):
    # testing float and float usage
    def test1(self):
        self.assertEqual(run_test("return 5.0;"), 5.0)

    # testing characters
    def test2(self):
        self.assertEqual(run_test("return 'a';"), "a")

    # here on its all about testing functions that are built into our language
    # testing square root and its errors
    def test3(self):
        self.assertEqual(run_test("return sqrt(9);"), 3)

    def test4(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return sqrt(9, 5);")

    # power
    def test5(self):
        self.assertEqual(run_test("return pow(3, 2);"), 9)

    def test6(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return pow(3, 2, 4);")

    # ceil
    def test7(self):
        self.assertEqual(run_test("return ceil(1.3);"), 2)

    def test8(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return ceil();")

    # floor
    def test9(self):
        self.assertEqual(run_test("return floor(1.3);"), 1)

    def test10(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return floor();")

    # abs
    def test11(self):
        self.assertEqual(run_test("return abs(-5);"), 5)

    def test12(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("return abs();")

    # println, print has been tested but println hasnt
    def test13(self):
        run_test("println(5);")

    # isInt
    def test14(self):
        self.assertTrue(run_test('isInt("5");'))

    def test15(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("isInt(1, 5);")

    # toInt
    def test16(self):
        self.assertEqual(run_test('toInt("5");'), 5)

    def test17(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("toInt();")

    def test18(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test('toInt("jim");')

    # isFloat
    def test19(self):
        self.assertTrue(run_test('isFloat("5");'))

    def test20(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("isFloat(1, 5);")

    def test21(self):
        self.assertFalse(run_test('return isFloat("thing");'))

    # toFloat
    def test22(self):
        self.assertEqual(run_test('toFloat("5");'), 5)

    def test23(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("toFloat();")

    def test24(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test('toFloat("jim");')

    # toStr
    def test25(self):
        self.assertEqual(run_test("return toStr(5);"), "5")

    def test26(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("toStr();")

    # concat
    def test27(self):
        variable = 'return concat("5", "3");'
        self.assertEqual(run_test(variable), "53")

    def test28(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("concat();")

    def test29(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("concat(5, 12);")

    # trim
    def test30(self):
        self.assertEqual(run_test('return trim(" a ");'), "a")

    def test31(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("trim();")

    def test32(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("trim(5);")

    # hasPrefix
    def test33(self):
        self.assertTrue('return hasPrefix("a", "ab");')

    def test34(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("hasPrefix();")

    def test35(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("hasPrefix(5, 8);")

    # hasSuffix
    def test37(self):
        self.assertTrue('return hasSuffix("b", "ab");')

    def test38(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("hasSuffix();")

    def test39(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("hasSuffix(5, 8);")

    # length
    def test40(self):
        self.assertEqual(run_test('return length("slap");'), 4)

    def test41(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("length();")

    def test42(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("length(5);")

    # exit
    def test43(self):
        self.assertEqual(run_test("exit(5);"), 5)

    def test44(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("exit();")

    # type
    def test45(self):
        self.assertEqual(run_test('return type("thing");'), "string")

    def test46(self):
        self.assertEqual(run_test("return type(5);"), "integer")

    def test47(self):
        self.assertEqual(run_test("return type(3.1);"), "float")

    def test48(self):
        self.assertEqual(run_test("return type(true);"), "boolean")

    def test49(self):
        self.assertEqual(run_test("return type(null);"), "null")

    def test50(self):
        self.assertEqual(run_test("fn thing(){}; return type(thing);"), "function")

    def test51(self):
        with self.assertRaises(RuntimeEvaluationError):
            run_test("type();")

    # if statemetns
    def test52(self):
        output = run_test("""
                if(true){
                    return 1; 
                }else{
                    return 0;
                };""")
        self.assertEqual(output, 1)

    def test53(self):
        output = run_test("""
            if(false){
                return 1; 
            }else{
                return 0;
            };""")
        self.assertEqual(output, 0)

    # for loops
    def test54(self):
        output = run_test("""
            for(let i = 1; i < 3; i = i + 1){
                continue;
                return 0;
            }
            return 1;
        """)
        self.assertEqual(output, 1)

    def test55(self):
        output = run_test("""
            for(let i = 1; i < 3; i = i + 1){
                break;
                return 0;
            }
            return 1;
        """)
        self.assertEqual(output, 1)

    def test56(self):
        output = run_test("""
            for(let i = 1; i < 3; i = i + 1){
            }
            return 1;
        """)
        self.assertEqual(output, 1)

    # while loops
    def test57(self):
        output = run_test("""
            let i = 0;
            while(i < 3){
                i = i + 1;
                continue;
                return 0;
            }
            return 1;
        """)
        self.assertEqual(output, 1)

    def test58(self):
        output = run_test("""
            let i = 0;
            while(i < 3){
                i = i + 1;
                break;
                return 0;
            }
            return 1;
        """)
        self.assertEqual(output, 1)
