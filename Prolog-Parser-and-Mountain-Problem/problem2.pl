/*
Assignment-6 Solution
Name : Krishna Kant Verma (2211cs19)
Name : Gourab Chatterjee (2211cs08)
Name : Aditi Marathe (2211cs01)

Problem-2:
Q. Write a program in Prolog to represent the following knowledge and find
the answer to the given questions
a. Knowledge
A, B and C belong to Himalayan club. Every member in the club is
either a mountain climber or skier or both. A likes whatever B dislikes
and dislikes whatever B likes. A likes rain and snow. No mountain
climber likes rain. Every skiers likes snow.

Question : Is there a member who is a mountain climber but not a
skier?

*/

:- style_check(-singleton).
/* a ,b, c belongs to Himalayan Club*/
belongsToHimalayanClub(a).
belongsToHimalayanClub(b).
belongsToHimalayanClub(c).



/*if not a mountain climber and not skier then not belongs to himalayan club*/
belongsToHimalayanClub(X):-notMntClimber(X),notSkier(X),!,fail.
belongsToHimalayanClub(X).

/* a likes Rain and Snow*/
likes(a,rain).
likes(a,snow).
 
/*A likes whatever B dislikes and dislikes whatever B likes*/
likes(a,X):-dislikes(b,X).

/* if a likes something b dislikes and viceversa  */
/*using cut and fail */
likes(b,X):-likes(a,X),!,fail.
likes(b,X).

/*if someone likes rain then it is not mountain climber*/ 
/*negation as a failure*/
mntClimber(X):-likes(X,rain),!,fail. 
mntClimber(X). 

/*if someone dislikes snow they are not skier*/
notSkier(X):-dislikes(X,snow).

/*not mountain climber clause*/
notMntClimber(X):-mntClimber(X),!,fail.
notMntClimber(X).

/*if p likes q is not true than p dislikes q*/
dislikes(P,Q):-likes(P,Q),!,fail.
dislikes(P,Q).

/*Given Question in the Query)*/
solveGivenQuery(X):-belongsToHimalayanClub(X),mntClimber(X),notSkier(X),!.
