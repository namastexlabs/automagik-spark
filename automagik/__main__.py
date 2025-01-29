"""
Main entry point for automagik CLI.
"""

from dotenv import load_dotenv

# Load environment variables before importing any other modules
load_dotenv()

from automagik.cli.cli import main

if __name__ == "__main__":
    main()
