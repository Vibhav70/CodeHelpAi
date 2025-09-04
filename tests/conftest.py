import sys
import os

# Add the project root directory to the Python path before tests are collected.
# This file is automatically discovered by pytest. By placing the path
# modification here, we ensure that all test files and the test runner
# itself can correctly locate the 'backend', 'parser', and 'summarizer' modules.
# We go up one directory ('..') from the 'tests' folder to reach the project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
