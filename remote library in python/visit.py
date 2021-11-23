from Pyro5.api import Proxy
import sys
import Pyro5.errors

sys.excepthook = Pyro5.errors.excepthook

#Connect to remote class
library = Proxy("PYRONAME:example.library")

#BEGIN TESTING OF REMOTE OBJECT.
#The following code is meant to test the functionality of the remote object as per
#the assessment specification, a description of which can be found in the README file.
library.add_user("Edward")

print(library.return_users())

library.add_author("JK Rowling", "Crime")
library.add_author("Mc", "Drama")

library.add_book_copy("JK Rowling", "Harry Potter 1")
library.add_book_copy("JK Rowling", "Harry Potter 1")
library.add_book_copy("JK Rowling", "Harry Potter 2")
library.add_book_copy("JK Rowling", "Harry Potter 3")
library.add_book_copy("JK Rowling", "Harry Potter 4")
library.add_book_copy("JK Rowling", "Harry Potter 5")

print(library.return_books_not_loan())
library.loan_book("Edward", "Harry Potter 1", 2021, 4, 20)
print(library.return_books_loan())
library.return_book("Edward", "Harry Potter 1", 2021, 5, 20)
print(library.return_books_not_loan())
library.delete_book("Harry Potter 1")
print(library.return_books_not_loan())
library.delete_book("Harry Potter 3")
print(library.return_books_not_loan())

library.add_user("Isobel")
print(library.return_users())
library.delete_user("Isobel")
print(library.return_users())
print(library.user_loans_date("Edward", 2020, 1, 1, 2022, 1, 1))





