from datetime import datetime, timedelta

# Book class to represent a book in the library
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Checked Out"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"


# Member class to represent a library member
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.is_available:
            book.is_available = False
            due_date = datetime.now() + timedelta(days=14)
            self.borrowed_books.append((book, due_date))
            print(f"{self.name} borrowed '{book.title}'. Due on {due_date.date()}.")
        else:
            print(f"Sorry, '{book.title}' is already borrowed.")

    def return_book(self, book):
        for borrowed, due_date in self.borrowed_books:
            if borrowed.isbn == book.isbn:
                book.is_available = True
                self.borrowed_books.remove((borrowed, due_date))
                print(f"{self.name} returned '{book.title}'. Thank you!")
                return
        print(f"{self.name} did not borrow '{book.title}'.")

    def show_borrowed_books(self):
        if not self.borrowed_books:
            print(f"{self.name} has not borrowed any books.")
        else:
            print(f"{self.name}'s Borrowed Books:")
            for book, due_date in self.borrowed_books:
                print(f" - {book.title} (Due: {due_date.date()})")


# Library class to manage books and members
class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added book: {book.title}")

    def add_member(self, member):
        self.members.append(member)
        print(f"Added member: {member.name}")

    def list_books(self):
        print("\nLibrary Catalog:")
        for book in self.books:
            print(book)

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None


# Example usage
if __name__ == "__main__":
    library = Library()

    # Add books
    book1 = Book("1984", "George Orwell", "1234567890")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")
    library.add_book(book1)
    library.add_book(book2)

    # Add members
    member1 = Member("Alice", "M001")
    library.add_member(member1)

    # List available books
    library.list_books()

    # Member borrows a book
    member1.borrow_book(book1)

    # List available books after borrowing
    library.list_books()

    # Show borrowed books by the member
    member1.show_borrowed_books()

    # Member returns the book
    member1.return_book(book1)

    # Final state of the library
    library.list_books()
