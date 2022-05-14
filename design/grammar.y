
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

entry: statement;

statement : IDENTIFIER IDENTIFIER '=' expr ';'
          | IDENTIFIER IDENTIFIER ';'
          | IDENTIFIER '=' expr ';'
          | expr ';'
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
