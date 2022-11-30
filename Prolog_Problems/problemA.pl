/* 

Assignment-7
Name: Krishna Kant Verma (2211cs19)
Name: Gourab Chatterji(2211cs08)
Name: Aditi Marathe(2211cs01)

Write a program in Prolog to represent the following knowledge and find the answer to
the given questions.
a. Knowledge
Smith, Baker, Carpenter, and Tailor have each a profession (smith, baker,
carpenter, and tailor) but not shown by their names. Each of them has a son. But
the sons also do not have the profession shown by their name.
If you know that:
1) No son has the same profession as his father has and
2) Baker has the same profession as Carpenter's son has and
3) Smith's son is a baker.
Question: find the professions of the parents and sons.

*/

 % list of professions 
professions([smith,baker,carpenter,tailor]).
/* S = Smith's profession 	   			
   B = Baker's profession 
   C = Carpenter's profession	   		
   T = Taylor's profession
   S_Son = Smith son's profession 		
   B_Son = Baker son's profession 
   C_Son = Carpenter son's profession	
   T_Son = Taylor son's profession
*/


solve([S,B,C,T],[S_Son,B_Son,C_Son,T_Son]):-
	professions(L),
	member(S,L),S\=smith,
	member(B,L),B\=baker,
	member(C,L),C\=carpenter,
	member(T,L),T\=taylor,
	
/* The sons do not have the same profession as their name shows */
	member(S_Son,L),S_Son\=smith,	
	member(B_Son,L),B_Son\=baker,
	member(C_Son,L),C_Son\=carpenter,
	member(T_Son,L),T_Son\=taylor,
/* The sons do not have the same profession as their fathers either */
	S\= F_Son,
	B\= B_Son,
	C\= T_Son,
	T\= C_Son,
	
	% Baker has the same profession as Carpenters son.
        B=C_Son, 
        	
        % Smiths son is a baker	 
   	S_Son=baker. 	
   	
% solve([S,X,C,T],[baker,B_Son,X,T_Son]).
% Thank You So Much
