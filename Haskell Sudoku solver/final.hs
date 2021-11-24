import Data.Array
import Data.List

-- HOW TO USE:
-- 	Run this file and call function: "solveSudo"
-- 	You will be prompted to enter a your sudo problem to solve
-- 	The program will return an print the solution to the screen


-- Detailed program breakdown:
-- 	1) calling "solveSudo" prompts an input.
-- 	2) The input is converted into a Board and checked to ensure it's
--	   validity using "checkboard" before attemping to solve it. If not valid, an error will be 
--	   printed and the function terminates.
--	3) "solveSudo" calls "sudo" and attempts only to retrieve the first solution.
-- 	4) "sudo" calls "generator" which takes a Board an Int as arguements. This
--	   Int is the number of zeros in the Board which need to be filled.
--	5) "generator" calls itself recursively. With each call it calls the following functions:
-- 		"allchoices" - generates a list of type [((Int,Int),Int)], a pair of coordinates and 
--				values which could validly be placed in them.
--		"checkoptions" - checks if the [((Int,Int),Int)] list is empty. If so, no valid moves 
--				remain and the problem is impossible to solve. Reports an error message
--				and exits the function.
-- 		"getsmallest" - calls a series of other functions that sorts and selects the 'simplest'
--				possible set of choices. For example, if in the set of all choices
--				there is only one possible assignment for some given coordinates, then if a solution 
--				exists for this problem this assigment must be part of it. Therefore, for
--				efficiency this assignment should be performed before other options are explored.
--				In other words, "getsmallest" attempts to find the next SHORTEST STEP toward the solution,
--				improving it's performance by reducing the number of iterative calls necessary.
-- 		"replacer" - takes coordinates, a value and Board, and using "replace" it returns a new Board
--				in which the cordinates of the Board now hold the given value. If multiple
--				options (coordinate value pairs) are given it will return multiple new boards,
--				splitting the programs search along different paths.
--	These Boards (new problem states) generted by the generator are fed into the next recursive call of 
--	"genertor", and this continues until either a solution is found (the Board fed into a "generator" call
--	contains no zeros and thus the base case is satisfied) or until "checkoptions" throws an error, in 
--	which case no solution exists.

--	Other functions:
--	"getsmallest" - Takes the list of all choices for a given problem state and uses: "groupchoices"
-- 		to turn it into a list of lists, in which each sub-list is associated with a given coordinate
--		in the problem (e.g. (0,0)). Then, calls "sortchoices" which sorts this list of lists so that
--		the smallest sublist is at it's head. Then, calls "firstchoice" which returns the head of the 
--		list of lists.
--	"check" - Takes a coordinate pair and value and calls functions "checkrow", "checkcol" and "checkbox" to 
--		check if placing the value in the coordinate position would constitute a valid move given
--		the values in it's row, colum and sub-square respectively. Returns true if the move it valid.
--	"getsquare" - used by "checkbox" in "check" to return coordinates needed for checking if a move is valid
--		relative to the square it is in.
--	"countzeros" - returns the number of zeros left in the problem state. Used to trigger the base case of 
--		"generator" and return the found solution to the problem. 
--	"getInput" - function to retrieve input from the user and casts it to type [[Int]]
--	"matrixToBoard" - takes the given matrix input [[Int]] and converts it to the type Board so it is 
--		usable by the rest of the program.
--	"boardToMatrix" - takes the given Board and convert it to a type [[Int]] to be returned and displayed
--		to the user.

				




-- Solver
-- This function "sudo" takes a board and and generates a list of solutions by calling "generator"
type Board = Array (Int,Int) Int
sudo :: Board -> [Board]
sudo matrix = [solution | solution <- generator matrix (countzeros matrix)]


-- "generator" takes a board and recursively generates boards taking the simplest next move(s). 
generator :: Board -> Int -> [Board]
generator matrix 0 = [matrix] -- If no zeros left, solution is complete
generator matrix z = [solution | option <- getsmallest $ checkoptions $ allchoices matrix, board <- [replacer option matrix], solution <- generator board (countzeros board)]
 where allchoices matrix = [(xy,i) | xy <- indices matrix, matrix ! xy == 0,i <- choices xy matrix]
       choices xy matrix = [i | i <- [1..4], check xy i matrix]

-- Replacer function creates new board with replaced value
replacer :: ((Int,Int),Int) -> Board -> Board
replacer (xy,n) matrix = listArray ((0,0),(3,3)) [replace xy n coord matrix |  coord <- indices matrix]
 where replace target n coord matrix
        | target == coord = n
        | otherwise = matrix ! coord

checkoptions :: [a] -> [a]
checkoptions [] = error "No valid solutions exist"
checkoptions x = x

-- SORTER
getsmallest :: [((Int,Int), Int)] -> [((Int,Int), Int)]
getsmallest allchoices = firstchoice $ sortchoices $ groupchoices allchoices
 where groupchoices choices = groupBy (\a b -> fst a == fst b) choices
       sortchoices listchoices = sortBy (\list1 list2 -> compare (length list1) (length list2)) listchoices
       firstchoice listchoices = head listchoices


check :: (Int,Int) -> Int -> Board -> Bool
check xy n matrix = or [(checkcol xy n matrix && checkrow xy n matrix && checkbox xy n matrix), n==0]
 where checkbox xy n matrix = all (/=n) [matrix ! coord | coord <- getsquare xy matrix, coord /= xy]
       checkcol (x,y) n matrix = all (/=n) [matrix !(i,y) | (i,j) <- (indices matrix), j == y, (i,y) /= (x,y)]
       checkrow (x,y) n matrix = all (/=n) [matrix !(x,j) | (i,j) <- (indices matrix), i == x, (x,j) /= (x,y)]
       

getsquare :: (Int,Int) -> Board -> [(Int,Int)]
getsquare xy matrix
 | elem xy [(0,0),(0,1),(1,0),(1,1)] = [(0,0),(0,1),(1,0),(1,1)]
 | elem xy [(0,2),(0,3),(1,2),(1,3)] = [(0,2),(0,3),(1,2),(1,3)] 
 | elem xy [(2,0),(2,1),(3,0),(3,1)] = [(2,0),(2,1),(3,0),(3,1)]
 | elem xy [(2,2),(2,3),(3,2),(3,3)] = [(2,2),(2,3),(3,2),(3,3)]
 | otherwise = []

-- Count number of zeros in input Board
countzeros :: Board -> Int
countzeros matrix = length (filter (==0) (elems matrix))

-- Check all elements of input Board are in valid position
checkboard :: Board -> Bool
checkboard board = all (==True) [check xy i board| (xy, i) <- zip (indices board) (elems board)]

getInput :: IO [[Int]]
getInput = readLn

-- Convert input [[Int]] to type Board
matrixToBoard :: [[Int]] -> Board
matrixToBoard xs = listArray ((0,0),(3,3)) (concat xs)

-- Convert input Board to type [[Int] or output
boardToMatrix :: Board -> [[Int]]
boardToMatrix board = split (elems board)
 where split xs = [take 4 xs, take 4 $ drop 4 xs, take 4 $ drop 8 xs, take 4 $ drop 12 xs]
 

-- IO controller

solveSudo :: IO [[Int]]
solveSudo = do 
 putStrLn "Enter sudoku puzzle to be solved:"
 matrix <- getInput 
 let start = matrixToBoard matrix
 if (checkboard start)
  then return ((boardToMatrix $ (sudo start) !! 0))
  else error "Input has no valid solution"

