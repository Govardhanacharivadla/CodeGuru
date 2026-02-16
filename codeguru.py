#!/usr/bin/env python
"""CodeGuru - AI Coding Mentor Command Line Tool."""

import sys
from pathlib import Path

# Add src to path if running directly
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.cli import cli

if __name__ == "__main__":
    cli()
