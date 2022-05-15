
%token IDENTIFIER

%token INCREMENT
%token DECREMENT

%token PLUS_EQUALS
%token MINUS_EQUALS
%token STAR_EQUALS
%token SLASH_EQUALS

%token KWD_FOR
%token KWD_WHILE
%token KWD_IF
%token KWD_CLASS

%token KWD_AUTO
%token KWD_CONST
%token KWD_FINAL
%token KWD_NONLOCAL

%%

program        : program statement
               | statement
               ;

statement      : IDENTIFIER IDENTIFIER '=' expr ';'
               | IDENTIFIER IDENTIFIER ';'
               | KWD_CONST IDENTIFIER IDENTIFIER '=' expr ';'
               | KWD_AUTO IDENTIFIER '=' expr ';'
               | KWD_CONST KWD_AUTO IDENTIFIER '=' expr ';'
               | IDENTIFIER '=' expr ';'
               | operator_assign ';'
               | expr ';'
               | '{' program '}'
               ;

operator_assign: IDENTIFIER PLUS_EQUALS expr
               | IDENTIFIER MINUS_EQUALS expr
               | IDENTIFIER STAR_EQUALS expr
               | IDENTIFIER SLASH_EQUALS expr
               ;

access_expr    : expr '.' expr
               ;

expr           : access_expr
               | expr '+' expr
               | expr '-' expr
               | expr '*' expr
               | expr '/' expr
               | INCREMENT IDENTIFIER
               | DECREMENT IDENTIFIER
               | '+' expr
               | '-' expr
               | '(' expr ')'
               | IDENTIFIER
               ;

%%
