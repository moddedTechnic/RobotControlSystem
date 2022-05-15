
%token IDENTIFIER

%token KWD_FOR
%token KWD_WHILE
%token KWD_IF
%token KWD_CLASS

%token KWD_AUTO
%token KWD_CONST
%token KWD_FINAL
%token KWD_NONLOCAL

%%

program   : program statement
          | statement
          ;

statement : IDENTIFIER IDENTIFIER '=' expr ';'
          | IDENTIFIER IDENTIFIER ';'
          | KWD_CONST IDENTIFIER IDENTIFIER '=' expr ';'
          | KWD_AUTO IDENTIFIER '=' expr ';'
          | KWD_CONST KWD_AUTO IDENTIFIER '=' expr ';'
          | IDENTIFIER '=' expr ';'
          | expr ';'
          | '{' program '}'
          ;

expr      : expr '.' expr
          | expr '+' expr
          | expr '-' expr
          | expr '*' expr
          | expr '/' expr
          | '+' expr
          | '-' expr
          | '(' expr ')'
          | IDENTIFIER
          ;

%%
