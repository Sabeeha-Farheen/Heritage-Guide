import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    ".env",
    "requirements.txt",
    "setup.py",
    "app.py",
    "research/trials.ipynb"
]

for filepath in list_of_files:
    filepath = Path(filepath)  # Convert string to Path object
    filedir = filepath.parent  # Get directory path
    filename = filepath.name   # Get file name

    if filedir != Path("."):  # Ensure we don't create "." as a directory
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()  # Creates an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
