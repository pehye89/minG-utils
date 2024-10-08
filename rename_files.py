import os
import re
import argparse
from tqdm import tqdm

"""
This script renames files in a specified directory by performing the following operations:

- Replaces all occurrences of '.' (period) with '_' (underscore) in the filename, except for the file extension.
- Replaces parentheses '(' and ')' with '_' (underscore).
- Removes all spaces from the filename.
"""

def rename_files(directory):
    # Loop through all files in the directory
    for root, _, files in os.walk(directory):
        for file in tqdm(files, desc="Renaming files", unit="file"):
            # Construct old file path
            old_path = os.path.join(root, file)

            # Replace '.' with '_', replace parentheses with '_', and remove spaces
            new_filename = re.sub(r'[()]', '_', file)
            new_filename = new_filename.replace('.', '_').replace(' ', '')

            # Ensure file extension is maintained properly
            if '.' in file:
                file_extension = file.split('.')[-1]
                new_filename = new_filename.rsplit('_', 1)[0] + '.' + file_extension

            # Construct new file path
            new_path = os.path.join(root, new_filename)

            # Rename the file
            os.rename(old_path, new_path)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Rename files in a directory by replacing specific characters.")
    parser.add_argument("--input_dir", type=str, help="Path to the directory containing files to rename")
    args = parser.parse_args()

    # Call rename function
    rename_files(args.input_dir)