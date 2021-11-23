from Pyro5.api import expose, behavior, serve, Daemon
from datetime import date
@expose
@behavior(instance_mode="single")

#Initialise library class containing all information
class library(object):
    #INITIALISE BASE DATA STRUCTURES
    def __init__(self):
        self.users = [] #List of library users
        self.authors = [] #List of authors who have books in the library
        self.books = [] #List of books available in library 
        self.loans = [] #List of book loan histories
        self.returns = [] #List of book return histories

    #ADD USER TO THE LIBRARY SYSTEM
    #Input(s) - Username: string
    #Output(s) - None
    def add_user(self, user_name):
        #Check to ensure user_name not already in the system
        if user_name not in self.users:
            self.users.append(user_name) #Append user_name to list of all users
            print("User , ", user_name, " added to system.") 
        else: print("Username already in system.")
        
    #RETURN LIST OF ALL USERS IN SYSTEM
    #Input(s) - None
    #Output(s) - List of all users: string
    def return_users(self):
        base1 = "All system users:\n" #Beginning of returned string
        base2 = "{0}) {1}\n" #Placeholder string
        for i, user in enumerate(self.users): #Loop through all users
            base1 += base2.format(i, user) #Append formatted placeholder to base string
        return base1

    #ADD AUTHOR TO SYSTEM
    #Input(s) - Authors name: string, Authors genre: string
    #Output(s) - None
    def add_author(self, author_name, author_genre):
        self.authors.append((author_name, author_genre)) #Append author and genre to list
        print(self.authors)

    #RETURN LIST OF ALL AUTHORS IN SYSTEM
    #Input(s) - None
    #Output(s) - List of all users: string
    def return_authors(self):
        base1 = "All authors in system:\n" #Beginning of returned string
        base2 = "{0}) Name:{1}, Genre:{2}\n" #Placeholder string
        for i, pair in enumerate(self.authors): #Loop through all authors
            base1 += base2.format(i, pair[0], pair[1]) #Append formatted placeholder to base string
        return base1
    
    #ADD COPY OF BOOK TO SYSTEM
    #Input(s) - Authors name: string, Title of book: string
    #Output(s) - None
    def add_book_copy(self, author_name, book_title):
        #Below, 'True' indicates that the book is available to be loaned (not currently loaned out)
        self.books.append([book_title, author_name, True]) #Append book title and author to list
        print(("Copy of {0} by author {1} added to library").format(book_title,author_name))

    #LOAN BOOK FROM SYSTEM
    #Input(s) - Name of user: string, Title of book: string, year/time/day of loan: int
    #Output(s) - 1: if loan successfully completed, 0: if loan failed
    def loan_book(self, user_name, book_title, year, month, day):
        #Chek if user exists in system
        if user_name not in self.users:
            print("username not recognised.")
            return 0 #If user not in system, return 0
        #If user in system, loop through all books
        for i, entry in enumerate(self.books):
            #If book title found and loanable
            if (book_title == entry[0]) & entry[-1]:
                print(("Loaning book {0} to {1}").format(book_title, user_name))
                self.loans.append([user_name, book_title, year, month, day]) #Append to loan history
                self.books[i][-1] = False #Set book to not loanable
                return 1 #Return 1 to indicate successful loan
        return 0 #If no available book found, return 0

    #RETURN BOOK FROM SYSTEM
    #Input(s) - Name of user: string, Title of book: string, year/time/day of return: int
    #Output(s) - 1: if return successfully completed, 0: if loan failed
    def return_book(self, user_name, book_title, year, month, day):
        if user_name not in self.users: #Check if username in system
            print("username not recognised.")
            return 0 #If username not in system, return 0
        for i, entry in enumerate(self.books): #If username in systen, loop through all books
            if (book_title == entry[0]) & (not entry[-1]):
                print(("Returning book {0} from {1}").format(book_title, user_name))
                self.returns.append([user_name, book_title, year, month, day]) #Append to return history
                self.books[i][2] = True #Set returned book to loanable
                return 1 #return 1 to indicate successful return
        return 0 #Return 0 if book not foudn in system

    #RETURN LIST OF ALL BOOKS NOT ON LOAN IN SYSTEM
    #Input(s) - None
    #Output(s) - List of all available books to loan: string    
    def return_books_not_loan(self):
        base1 = "All books not on loan in system:\n" #Beginning of returned string
        base2 = "Title:{0}, Author:{1}\n" #Placeholder string
        for entry in self.books: #Loop through all books
            if entry[-1]: base1 += base2.format(entry[0], entry[1]) #Append formatted placeholder to base string
        return base1
    
    #RETURN LIST OF ALL BOOKS ON LOAN IN SYSTEM
    #Input(s) - None
    #Output(s) - List of all books on loan: string   
    def return_books_loan(self):
        base1 = "All books on loan in system:\n" #Beginning of returned string
        base2 = " Title:{0}, Author:{1}\n" #Placeholder string
        for entry in self.books: #Loop through all books
            if not entry[-1]: base1 += base2.format(entry[0], entry[1]) #Append formatted placeholder to base string
        return base1         


    #DELETE ALL COPYS OF A GIVEN BOOK FROM WHICH ARE LOANABLE (in the library)
    #Input(s) - Title of book: string
    #Outputs - None
    def delete_book(self, book_title):
        to_delete = [] #Initialise buffer of books to delete
        
        for i, pair in enumerate(self.books): #Enumerate through books
            if (pair[0] == book_title) & pair[2]: #If book exists and NOT on loan
                to_delete.append(i) #Add book to delete buffer
                print(("Deleting {0} from system.").format(book_title))

        for i in to_delete[::-1]: #Loop through delete buffer
            del self.books[i] #Delete book in buffer

            
    #DELETE USER 
    #Input(s) - Username: string
    #Outputs - None
    def delete_user(self, user_name):
        if user_name not in self.users: #If user not in system
            print("Username not found, could not delete.") 
            return 0 #Return 0 if user not in system
        for loan in self.loans: #Loop through books currently on loan
            if user_name in loan: #If user currently has book on loan
                print(user_name, " has loaned books previously, cannot delete user.")
                return 0 #If user has book on loan, return 0 canot delete user
        for i, user in enumerate(self.users): #Enumerate through all usersin system
            if user == user_name: #If user in system
                del self.users[i] #Delete the user
                print(("Deleting user {0}.").format(user_name))
        

    #RETURN ALL LOAN/RETURN PAIRS FROM WITHIN A SPECIFIC DATE BOUNDS
    #Input(s) - Username: string, start/end year/day/month of loaned+returned book: string
    #Outputs - All loan/return pairs which fall inbetween given dates: int
    def user_loans_date(self, user_name, start_year, start_month, start_day, end_year, end_month, end_day):

        #Check if user in system
        if user_name not in self.users: return "Username not found."

        #Convert date inputs to python 'date'
        start_date = date(start_year, start_month, start_day)
        end_date= date(end_year, end_month, end_day)

        #Create base strings to be formated and concatenated together
        base1 = "Books loaned and returned between, Year:{0}, Month:{1}, Day:{2} and Year:{3}, Month:{4}, Day:{5}\n".format(start_year, start_month, start_day, end_year, end_month, end_day)
        base2 = "Username: {0}\n"
        base3 = "Loaned - Year: {0}, Month: {1}, Day: {2}\n"
        base4 = "Returned - Year: {0}, Month: {1}, Day: {2}\n"
        final = "" #Create final string to be appended to
        list_loans = [] #Initiated loans buffer
        list_returns = [] #Initialise returns buffer
        for loan in self.loans: #Loop through all loans
            if (user_name in loan): #Check if user loaned this book
                temp_loan_date = date(loan[2], loan[3], loan[4]) #Store dates of loan found
                if (start_date <= temp_loan_date <= end_date): #Check if dates of loan fall between input dates 
                    for r in self.returns: #Loop through returns
                        temp_return_date = date(r[2], r[3], r[4]) #Store dates of return
                        if (start_date <= temp_loan_date <= temp_return_date <= end_date): #Check if return if within input dates
                            #Format output strings
                            final += base3.format(loan[2],loan[3],loan[4]) 
                            final += base4.format(r[2],r[3],r[4])
                            break #Break out of loop through returns as pair found

        if final != "": #Check if formatted string is 'empty'
            final = base1 + base2.format(user_name) + final #Perform final string formatting
            return final
        else:
            return "No books loaned and returned within these dates."
            
                                
    
daemon = Daemon() 
serve({library: "example.library"}, daemon=daemon, use_ns=True)
