#const n = 3. %Num. districts
#const m = 2. %Num. Companies
#const k = 1. %Num. Experienced Companies

%Instantiate experience
exp(1..k, 1).
exp(k+1..m, 0).

%Instantiate
district(1..n).
company(1..m).

%Company teams
team(1, 1..t1).
team(2, 1..t2).

%Num. teams per company
#const t1 = 3.
#const t2 = 3. 

%Instantiate number of teams needed
need(1,1).
need(2,2).
need(3,1).

%Cost of teams
cost(1,1,1).
cost(1,2,2).
cost(1,3,4).

cost(2,1,3).
cost(2,2,6).
cost(2,3,2).