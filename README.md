# Software Measurement and Quality Assurance Coursework

Team Members:
- [Vatsal Chaudhari](https://github.com/vrc4)
- [Myrza Danike](https://github.com/wawatashi)
- [Jacky Liang Xu](https://github.com/JackyLeicester)
- [Syed Fasiuddin](https://github.com/sf403)

## EBNF of Language to be developed

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
                | array ;

integer         = [ "-" ] digit { digit } ;
float           = [ "-" ] digit { digit } "." digit { digit } ;
boolean         = "true" | "false" ;
char            = "'" ? any character ? "'" ;
string          = '"' { ? any character ? } '"' ;
letter          = ? a-z | A-Z ? ;
digit           = ? 0..9 ? ;
```
