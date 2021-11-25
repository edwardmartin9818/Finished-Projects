The code presented here is the implementation of a resource allocation problem using Answer Set Programming (ASP), a type of logic programming.
The program uses the Clingo language to achieve this. 

How the program works:

In terms of guess-and-test methodology, my program is designed to minimise unnecessary
candidate model generation (guessing) such that the search of the model space and subsequent reduction of it through candidate elimination (testing) is as small as possible. To this
end, model generation must be structured such to include implicit constraints that would
otherwise need to be explicit in the testing phase.
Model generation in my program is performed through this line of code: ”{at(D, C, T) :
team(C, T)} = N : −district(D), need(D, N).”
Using ”district/1” as a global variable means that for each district a new choice rule is
instantiated. Using ”team/2” as a local variable ensures that no ’team’ can be assigned more
than once per choice rule, as a given instance of ”team/2” can only exist once. Thus, no
team can be assigned more than once per district. Next, using the global variable ”need/2”
we obtain the required number of teams N for our given district, and bound the cardinality
of the choice rule with it. This is justified given that no stable model in our desired final
solution would assign more teams than is necessary (as this would increase cost) or less than
required. These implicit design constraints remove the need for multiple explicit constraints
and greatly improves the performance of the program.
The constraint, ”D1 = D2 : −at(D1, C, T), at(D2, C, T).”, ensures no team can be
used in multiple districts. Combined with the result of our model generation this ensures
each team is never used more than once. the constraint, ”: −district(D), #count{T :
at(D, C, T), exp(C, 1)} = 0.”, eliminates candidate solutions in which no experienced teams
are assigned to a given district, as a minimum of 1 is required at each.
Finally, the optimisation statement,
”#minimize{X, D, C, T : at(D, C, T), cost(C, D, X)}.”, attempts to minimise the total cost
of all assigned teams (instances of ”at/3” and corresponding ”cost/3”).


A full description of the task is given below.


Consider the following situation:
The public works division in a region has the responsibility to subcontract
work to private companies. There are several types of tasks. Each task is carried
out by a team, but each team is capable of carrying out all different types of tasks.
The region is divided into districts, and the amount of tasks to be done in each
district is known. In particular, the following information is available:
• The region is divided into n districts.
• There are m private companies such that 1 . . . k are experienced and
k + 1 . . . m are non-experienced.
• Each company i has ti

teams available, for all 1 ≤ i ≤ m.
• Each district j requires aj many teams, for all 1 ≤ j ≤ n.
• The yearly cost of allocating a team from a company i to a district j is (the
integer) ci,j , for all 1 ≤ i ≤ m, 1 ≤ j ≤ n.

The goal is to write a logic program for helping the public works division with this process.
Using the information above, the program should determine the number of teams from each
company to allocate to each district such that the following constraints are satisfied.
• At least one experienced company must be allocated to each district (as precaution in
case some difficult task arises in that district).
• Enough teams must be allocated to meet the demand in each district.
• No company can be asked to provide more teams than it still has available.
• The cost must be minimised.


Task:
1. Write a logic program in ASP (problem encoding.lp) which finds all solutions to the
problem, given n, m, k, ti , aj , ci,j for all 1 ≤ i ≤ m, 1 ≤ j ≤ n. Document your code
so the following is clear.
(a) How it should be used.
(b) What the approach to solving the problem is. In particular, you need to explain
what each rule achieves and how the rule achieves it.
Include your name and student id in the comments.
2. Write three problem instances (problem instancei.lp, for all i ∈ {1, 2, 3}) to test your
program. Document your code so it is clear what the instance is modeling.