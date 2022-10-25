/*
Assignment-6 Solution
Name : Krishna Kant Verma (2211cs19)
Name : Gourab Chatterjee (2211cs08)
Name : Aditi Marathe (2211cs01)

Problem-1:
Given an expression, write a program to decide whether it's a theorem or not.
Steps:
1. Write a parser to isolate the clauses around the implication in the
expressions

Test Cases :
1. (P => Q ) => ((~Q => P) => Q)
2. P => (P V Q)
3. (P ^ Q) => (P V R)


isValid((v(P)->v(Q))->((v(not(Q))->v(P))-> v(Q))). (true)
isValid(v(P)->v(P);v(Q)). (true)
isValid((v(P),v(Q))->(v(P);v(R))).  (true)
isValid((v(P)->v(Q)),(v(P);v(Q))).

*/

% check whether the premise and conclusion are satisfiable
isValid(Premise, Conclusion) :- isValid(Premise->Conclusion).

isValid(Prop) :- unsatisfiable(\+Prop).

% checking unsatisfiability
unsatisfiable(Prop) :- \+ true(Prop).

true(v(true)).

% not true if Proposition is false
true(\+ Prop) :- false(Prop).

% X or Y    
true((X;Y)) :- (true(X);true(Y)).

% X and Y
true((X,Y)) :- (true(X),true(Y)).

% X -> Y
true((X->Y)) :- (false(X);true(Y)).

%(X->Y)and(Y->X)
true((X=:=Y)) :- (true(X),true(Y);false(X),false(Y)).

% negation of above clauses

false(v(false)).
false(\+ Prop) :- true(Prop).

false((X;Y)) :- false(X), false(Y).

false((X,Y)) :- (false(X) ; false(Y)).

false((X->Y)) :- (true(X),false(Y)).

false((X=:=Y)) :- (true(X),false(Y);false(X),true(Y)).

