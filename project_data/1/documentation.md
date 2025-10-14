<style>
/* Custom CSS for beautiful documentation */
.header-main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.project-overview {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 3px 10px rgba(245, 87, 108, 0.3);
}

.toc-container {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 3px 10px rgba(79, 172, 254, 0.3);
}

.toc-container h2 {
    color: white;
    margin-top: 0;
}

.toc-container ul {
    color: white;
}

.toc-container a {
    color: #ffffff;
    text-decoration: none;
    font-weight: 500;
}

.toc-container a:hover {
    text-decoration: underline;
}

.file-section {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
}

.file-section h3 {
    color: white;
    margin-top: 0;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.class-container {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 1.2rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 5px solid #667eea;
    box-shadow: 0 2px 8px rgba(168, 237, 234, 0.4);
}

.class-container h5 {
    color: #2d3748;
    margin-top: 0;
}

.function-container {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    padding: 1.2rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 5px solid #f093fb;
    box-shadow: 0 2px 8px rgba(252, 182, 159, 0.4);
}

.function-container h5 {
    color: #2d3748;
    margin-top: 0;
}

.summary-text {
    background: rgba(255, 255, 255, 0.9);
    padding: 1rem;
    border-radius: 6px;
    color: #2d3748;
    font-style: italic;
    border-left: 4px solid #4facfe;
    margin: 0.5rem 0;
}

.methods-table {
    background: white;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.methods-table table {
    width: 100%;
    border-collapse: collapse;
}

.methods-table th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px;
    text-align: left;
}

.methods-table td {
    padding: 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #2d3748;
}

.methods-table tr:nth-child(even) {
    background-color: #f8fafc;
}

.code-block {
    background: #2d3748;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    overflow-x: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    border: 1px solid #4a5568;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 9999px;
    margin-right: 0.5rem;
}

.section-divider {
    height: 3px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border: none;
    border-radius: 2px;
    margin: 2rem 0;
}
</style>

<div class="header-main">
<h1>📚 Codebase Documentation: Proj11</h1>
</div>

<div class="project-overview">
<h2>🚀 Project Overview</h2>
<div class="summary-text"></div>
</div>

<div class="toc-container">
<h2>📋 Table of Contents</h2>

- [📄 C:\Desktop\projtrial\demo.py](#c--desktop-projtrial-demo-py)
  - [🏛️ Book](#book)
  - [🏛️ Member](#member)
  - [🏛️ Library](#library)

</div>

<hr class="section-divider">

<h2>🔍 Codebase Details</h2>


<div class="file-section">
<h3><a name="c--desktop-projtrial-demo-py"></a>📄 File: <code>C:\Desktop\projtrial\demo.py</code></h3>


<h4>🏛️ Classes</h4>


<div class="class-container">
<h5><a name="book"></a><span class="badge">CLASS</span>Book</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This Python code defines a `Book` class to represent a book with attributes like title, author, ISBN, and availability status. It includes an `__init__` method to initialize book objects and a `__str__` method to provide a user-friendly string representation of the book's details and availability.
</div>

<div class="methods-table">
<table>
<thead>
<tr>
<th>🔧 Method</th>
<th>📝 Summary</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>__init__()</code></td>
<td>This code defines the constructor (`__init__`) for a class, likely representing a book. It initializes the book's title, author, ISBN, and sets its availability status to True by default.</td>
</tr>
<tr>
<td><code>__str__()</code></td>
<td>This code defines the string representation of an object, likely a book. It returns a formatted string containing the book's title, author, ISBN, and availability status ("Available" or "Checked Out").</td>
</tr>
</tbody>
</table>
</div>

<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Checked Out"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"
</code></pre>
</div>

</div>


<div class="class-container">
<h5><a name="member"></a><span class="badge">CLASS</span>Member</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This code defines a `Member` class to represent a library member, allowing them to borrow books (updating book availability and due dates), return books, and view their currently borrowed books. It manages the member's borrowed books as a list of tuples containing the book object and its due date.
</div>

<div class="methods-table">
<table>
<thead>
<tr>
<th>🔧 Method</th>
<th>📝 Summary</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>borrow_book()</code></td>
<td>This code defines a `borrow_book` method that allows a user to borrow a book if it's available. It marks the book as unavailable, sets a due date 14 days from the borrowing date, and adds the book and due date to the user's list of borrowed books, also printing a confirmation message.</td>
</tr>
<tr>
<td><code>return_book()</code></td>
<td>This code defines a `return_book` method that allows a patron to return a borrowed book to the library. It checks if the patron has borrowed the book, updates the book's availability, removes it from the patron's borrowed books list, and prints a confirmation message.</td>
</tr>
<tr>
<td><code>show_borrowed_books()</code></td>
<td>This code snippet defines a function `show_borrowed_books` that displays the books borrowed by a member, along with their due dates. If the member has no borrowed books, it prints a message indicating that; otherwise, it iterates through the borrowed books and prints each book's title and due date.</td>
</tr>
</tbody>
</table>
</div>

<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Member:
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
</code></pre>
</div>

</div>


<div class="class-container">
<h5><a name="library"></a><span class="badge">CLASS</span>Library</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This code defines a `Library` class to manage a collection of books and members. It provides methods to add books and members, list all books in the catalog, and find a specific book by its ISBN.
</div>

<div class="methods-table">
<table>
<thead>
<tr>
<th>🔧 Method</th>
<th>📝 Summary</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>add_book()</code></td>
<td>This Python code defines a method `add_book` that adds a `book` object to a list called `books` (presumably a library's collection) and then prints a confirmation message to the console indicating the title of the added book.</td>
</tr>
<tr>
<td><code>add_member()</code></td>
<td>This Python code defines a method `add_member` that adds a new `member` object to a list called `members` within the class instance. It also prints a confirmation message to the console indicating the name of the member that was added.</td>
</tr>
<tr>
<td><code>list_books()</code></td>
<td>This code snippet defines a method `list_books` that iterates through a list of `book` objects stored in `self.books` and prints each book's information to the console, effectively displaying the library's catalog.</td>
</tr>
<tr>
<td><code>find_book_by_isbn()</code></td>
<td>This code snippet defines a function `find_book_by_isbn` that searches a list of `books` for a book with a matching ISBN. If a book with the given ISBN is found, it is returned; otherwise, the function returns `None`.</td>
</tr>
</tbody>
</table>
</div>

<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Library:
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
</code></pre>
</div>

</div>



</div>