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
<h1>📚 Codebase Documentation: proj1</h1>
</div>

<div class="project-overview">
<h2>🚀 Project Overview</h2>
<div class="summary-text"></div>
</div>

<div class="toc-container">
<h2>📋 Table of Contents</h2>

- [📄 D:\Projects\demo\banking.py](#d--projects-demo-banking-py)
  - [🏛️ BankAccount](#bankaccount)
- [📄 D:\Projects\demo\studenttClass.py](#d--projects-demo-studenttclass-py)
  - [🏛️ Student](#student)

</div>

<hr class="section-divider">

<h2>🔍 Codebase Details</h2>


<div class="file-section">
<h3><a name="d--projects-demo-banking-py"></a>📄 File: <code>D:\Projects\demo\banking.py</code></h3>


<h4>🏛️ Classes</h4>


<div class="class-container">
<h5><a name="bankaccount"></a><span class="badge">CLASS</span>BankAccount</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This Python code defines a `BankAccount` class that simulates a simple bank account, allowing users to deposit, withdraw, and check their balance. It initializes with an owner and optional initial balance, and provides methods to modify and view the account's financial status.
</div>


<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class BankAccount:
    """Simple bank account simulation"""
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        """Add money to the account"""
        self.balance += amount
        print(f"Deposited ₹{amount}. New balance: ₹{self.balance}")
    
    def withdraw(self, amount):
        """Withdraw money if enough balance"""
        if amount <= self.balance:
            self.balance += amount
            print(f"Withdrew ₹{amount}. Remaining balance: ₹{self.balance}")
        else:
            print("Insufficient balance!")
    
    def check_balance(self):
        """Check account balance"""
        print(f"Account holder: {self.owner} | Balance: ₹{self.balance}")
</code></pre>
</div>

</div>



</div>


<div class="file-section">
<h3><a name="d--projects-demo-studenttclass-py"></a>📄 File: <code>D:\Projects\demo\studenttClass.py</code></h3>


<h4>🏛️ Classes</h4>


<div class="class-container">
<h5><a name="student"></a><span class="badge">CLASS</span>Student</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> This Python code defines a `Student` class to represent a student's information, including their name and a list of marks. It provides methods to calculate the average mark, determine the grade based on the average, and display the student's information.
</div>


<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">class Student:
    """Represents a student with marks and grade calculation"""
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks  # List of marks for subjects
    
    def calculate_average(self):
        """Calculates average marks"""
        return sum(self.marks) / len(self.marks)
    
    def get_grade(self):
        """Determines grade based on average"""
        avg = self.calculate_average()
        if avg >= 90:
            return "A=="
        elif avg >= 75:
            return "WW"
        elif avg >= 60:
            return "B"
        elif avg >= 40:
            return "C"
        else:
            return "m"
    
    def display_info(self):
        """Prints student details"""
        print(f"Student: {self.name}")
        print(f"Average Marks: {self.calculate_average():.2f}")
        print(f"Grade: {self.get_grade()}")
</code></pre>
</div>

</div>



</div>