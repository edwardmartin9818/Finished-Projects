%--------------------------------
%PROBLEM
%asign teams to districts
{at(D,C,T) : district(D)} :- company(C), team(C,T).

%Team can only be in one place at a time
D1 = D2 :- at(D1,C,T), at(D2,C,T). 

%At least 1 experienced team at every district
:- district(D), #count{T : at(D,C,T), exp(C, 1)} < 1.

%Each district has required number of teams
:- district(D), need(D,N), #count{T : at(D,_,T)} < N.

%Sum total of cost
total(S) :- S = #sum{X, T : at(D,C,T), cost(C,T,X)}.

#minimize{X, T : at(D,C,T), cost(C,T,X)}.

#show at/3.
#show total/1.




