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
<h1>📚 Codebase Documentation: proj2</h1>
</div>

<div class="project-overview">
<h2>🚀 Project Overview</h2>
<div class="summary-text"></div>
</div>

<div class="toc-container">
<h2>📋 Table of Contents</h2>

- [📄 D:\Projects\demo2\main.py](#d--projects-demo2-main-py)
  - [🏛️ Book](#book)
  - [🏛️ Library](#library)
- [📄 D:\Projects\demo2\main2.py](#d--projects-demo2-main2-py)
  - [🏛️ Vehicle](#vehicle)
  - [🏛️ ElectricVehicle](#electricvehicle)

</div>

<hr class="section-divider">

<h2>🔍 Codebase Details</h2>


<div class="file-section">
<h3><a name="d--projects-demo2-main-py"></a>📄 File: <code>D:\Projects\demo2\main.py</code></h3>


<h4>🏛️ Classes</h4>


<div class="class-container">
<h5><a name="book"></a><span class="badge">CLASS</span>Book</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This Python code defines a `Book` class to represent a book with attributes like title, author, and number of copies. It includes methods to display book information, check availability, borrow a copy (decrementing the count), and return a copy (incrementing the count).
</div>


<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

    def display_info(self):
        print(f"Title: {self.title}, Author: {self.author}, Copies Available: {self.copies}")

    def is_available(self):
        return self.copies > 0

    def borrow(self):
        if self.is_available():
            self.copies -= 1
            print(f"You borrowed '{self.title}'.")
        else:
            print(f"'{self.title}' is not available right now.")

    def return_book(self):
        self.copies += 1
        print(f"You returned '{self.title}'.")
</code></pre>
</div>

</div>


<div class="class-container">
<h5><a name="library"></a><span class="badge">CLASS</span>Library</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This code defines a `Library` class that manages a collection of `Book` objects, allowing users to add books, display the catalog, find books by title, and borrow/return books. It provides basic library functionality such as adding, searching, borrowing, and returning books.
</div>


<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added '{book.title}' to the library.")

    def show_all_books(self):
        print("Library Catalog:")
        for book in self.books:
            book.display_info()

    def find_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def borrow_book(self, title):
        book = self.find_book(title)
        if book:
            book.borrow()
        else:
            print(f"Book '{title}' not found in library.")

    def return_book(self, title):
        book = self.find_book(title)
        if book:
            book.return_book()
        else:
            print(f"Book '{title}' not found in library.")
</code></pre>
</div>

</div>



</div>


<div class="file-section">
<h3><a name="d--projects-demo2-main2-py"></a>📄 File: <code>D:\Projects\demo2\main2.py</code></h3>


<h4>🏛️ Classes</h4>


<div class="class-container">
<h5><a name="vehicle"></a><span class="badge">CLASS</span>Vehicle</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This Python code defines a `Vehicle` class with attributes for brand and model, and methods to start, stop, and display information about the vehicle's engine. It serves as a blueprint for creating vehicle objects with basic engine control and information display functionalities.
</div>


<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def start_engine(self):
        print(f"{self.brand} {self.model}'s engine has started.")

    def stop_engine(self):
        print(f"{self.brand} {self.model}'s engine has stopped.")

    def display_info(self):
        print(f"Vehicle: {self.brand} {self.model}")
</code></pre>
</div>

</div>


<div class="class-container">
<h5><a name="electricvehicle"></a><span class="badge">CLASS</span>ElectricVehicle</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This code defines an `ElectricVehicle` class that inherits from a `Vehicle` class, representing an electric vehicle with attributes like battery capacity and level. It includes methods for charging the battery, simulating driving with battery consumption, and displaying vehicle information including battery details.
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
<td><code>drive()</code></td>
<td>This code defines a `drive` method for an electric vehicle, simulating driving a certain distance and consuming battery power. It checks for sufficient battery, reduces the battery level based on distance driven (at a rate of 0.5 units per km), and prints a status message.</td>
</tr>
</tbody>
</table>
</div>

<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class ElectricVehicle(Vehicle):  # Inherits from Vehicle
    def __init__(self, brand, model, battery_capacity):
        super().__init__(brand, model)  # Call parent constructor
        self.battery_capacity = battery_capacity
        self.battery_level = 100  # Assume full charge

    def charge_battery(self):
        self.battery_level = 100
        print(f"{self.brand} {self.model} is now fully charged.")

    def drive(self, distance):
        if self.battery_level <= 0:
            print(f"{self.brand} {self.model} has no battery left.")
        else:
            used = min(distance * 0.5, self.battery_level)
            self.battery_level -= used
            print(f"Drove {distance} km. Battery now at {self.battery_level:.1f}%.")

    def display_info(self):
        super().display_info()
        print(f"Battery Capacity: {self.battery_capacity} kWh, Battery Level: {self.battery_level:.1f}%")
</code></pre>
</div>

</div>



</div>