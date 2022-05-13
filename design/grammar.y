
%token NAME
%token NUMBER

%token KEYWORD_FOR
%token KEYWORD_WHILE
%token KEYWORD_IF
%token KEYWORD_CLASS

%%

entry: statement;

block: '{' statements '}';

statement: for_loop | variable_assign | expression;
statements: statement | statements ';' statement

variable_assign: NAME '=' expression;

for_loop: KEYWORD_FOR '('
              variable_assign ';' for_loop_compare ';'
              for_loop_update
          ')' block;

for_loop_compare: NAME for_loop_compare_op expression;
for_loop_update: NAME for_loop_update_op expression;

for_loop_compare_op: '<' | '<''='
                   | '>' | '>''='
                   | '=''=' | '!''=';
for_loop_update_op: '+''=' | '-''='
                  | '*''=' | '/''=' | '%''=';

expression: term '+' term
          | term '-' term;

term: factor '*' factor
    | factor '/' factor
    | factor '%' factor;

factor: '(' expression ')'
      | NUMBER
      | variable
      | '+' factor
      | '-' factor;

variable: NAME | NAME '(' parameters ')' | NAME '(' ')'
parameters: expression | expression ',' parameters

%%
