# Software Measurement and Quality Assurance Coursework

Team Members:
- [Vatsal Chaudhari](https://github.com/vrc4)
- [Myrza Danike](https://github.com/wawatashi)
- [Jacky Liang Xu](https://github.com/JackyLeicester)
- [Syed Fasiuddin](https://github.com/sf403)

## Getting Started

The `smqa.zip` file can be uncompressed on Linux file systems using the default
file manager on Percy Gee Linux labs.

The github repository for this project is located at: <https://github.com/JackyLeicester/Coursework>

The video demonstration of this project is upload on YouTube as well: <https://youtu.be/Q0FbzMhAotE>

To get started with the project, install the dependencies using:
```bash
pip install -r requirements.txt
```

The project can then be ran in two ways:
1. Make a new file with test program in it and pass the name of the file to the
   interpreter as follows:
   ```bash
   ./main.py name-of-file
   ```
   Checkout the `examples/` folder or refer to [this](#ebnf-of-language-that-is-developed)
   section for the grammar of the language.
2. Run the interpreter in interactive mode as follows:
   ```bash
   ./main.py
   ```

## Testing and coverage

For running the test cases and generating a coverage report for overall project
and all the test cases written by all team members run:
```bash
coverage erase
python -m coverage run --branch --source=src -a -m unittest discover -s 249039503/test -t . -p "*.py"
python -m coverage run --branch --source=src -a -m unittest discover -s 249053812/test -t . -p "*.py"
python -m coverage run --branch --source=src -a -m unittest discover -s 259045253/test -t . -p "*.py"
python -m coverage run --branch --source=src -a -m unittest discover -s 259046521/test -t . -p "*.py"

python -m coverage report -m
python -m coverage html
open htmlcov/index.html
```

In order to generate individual test reports for blackbox and whitebox tests for
each team member run the following commands by changing the `student_id` and
`test_type`:
```bash
coverage erase
python -m coverage run --branch --source=src -a -m unittest discover -s <student_id>/test/<test_type> -t . -p "*.py"

python -m coverage report -m
python -m coverage html
open htmlcov/index.html
```

## EBNF of Language that is developed

```
program         = { statement } ;
statement       = assignment
                | while_stmt
                | for_stmt
                | function
                | call_expr
                | return_stmt
                | if_stmt
                | while_stmt
                | for_stmt
                | break_stmt
                | continue_stmt
                | initialiazation
                ;

break_stmt      = "break" ";" ;
continue_stmt   = "continue" ";" ;

while_stmt      = "while" "(" expression ")" block ;
for_stmt        = "for" "(" initialization ";" condition ";" update ")" block ;

initialization  = variable_decl | "" ;
variable_decl   = ( "let" | "const" ) lhs_var_decl "=" expression ;
lhs_var_decl    = identifier ;
assignment      = variable_decl ";" ;

condition       = expression | "" ;
update          = expression | "" ;

return_stmt     = "return" expression ";" ;
identifier      = letter { letter | digit } ;
expression      = identifier
                | literal
                | call_expr
                | infix_expr
                | negation_expr
                | comparision_expr ;
if_stmt         = "if" expression block [ "else" block ] ;
infix_expr      = expression ( "+" | "-" | "*" | "/" ) expression ;
comparision_expr = expression ( "<=" | "<" | ">" | ">=" | "==" | "!=" ) expression ;
negation_expr   = "!" expression ;
function        = "fn" identifier "(" [ identifier { "," identifier } ] ")" block ;
call_expr       = identifier "(" [ identifier { "," identifier } ] ")" ;
block           = "{" { statement } "}" ;
literal         = integer
                | float
                | boolean
                | string
                | char
                | null ;

integer         = [ "-" ] digit { digit } ;
float           = [ "-" ] digit { digit } "." digit { digit } ;
boolean         = "true" | "false" ;
char            = "'" ? any character ? "'" ;
string          = '"' { ? any character ? } '"' ;
letter          = ? a-z | A-Z ? ;
digit           = ? 0..9 ? ;
null            = "null" ;
```
