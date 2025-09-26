#!/usr/bin/env python3
"""
NMH GeoGuesser - Main Entry Point

This is the main entry point for the NMH GeoGuesser application.
It can be run from the project root directory.
"""

import sys
import os
from pathlib import Path

# Ensure we're in the project root directory
project_root = Path(__file__).parent.absolute()
os.chdir(project_root)

# Add src directory to Python path
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

# Import and run the application
from main import main

if __name__ == "__main__":
    main()
