#!/usr/bin/python3
"""
models/__init__.py - Package Initialization Module

Usage:
    - Import the package using 'import models' in your application.
    - Access the 'storage' variable to interact with the FileStorage instance.
    - Optionally, call 'storage.reload()' to load data from the JSON file.
"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
