# tests/conftest.py
import os
import sys

# Add the project root (one level above tests/) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
