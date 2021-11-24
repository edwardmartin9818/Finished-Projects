This folder contains the Haskell code for a sudoku solver, programmed for an assessment in my MSc Programming Paradigms Module.


Full assessment brief:

Write an efficient Haskell function that can solve this problem. Its input is a matrix, repre-
sented as a list of rows, where each row is a list of the numbers in the grid. The numbers

are either 1, 2, 3, 4 if the field is filled or 0 if the field is empty. The output of the function
should be one solution to the problem, in the same matrix format with the 0 values replaced
by a number 1 to 4 (or an error message if the input has no valid solution). For example, for
the above grid, the input is

input = [[3,4,0,0],
[2,0,3,0],
[0,3,0,2],
[0,0,1,3]]
and one solution is

output = [[3,4,2,1],
[2,1,3,4],
[1,3,4,2],
[4,2,1,3]].

Make sure you clearly document your approach and how to use your function in the com-
ments. Note that you must write your own code to solve this problem and not just call a
library function to solve such problems. You may use the standard libraries listed in the
Haskell 2010 language report, but not any other libraries.