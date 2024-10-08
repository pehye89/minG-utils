import os
import shutil
import argparse
from tqdm import tqdm

def organize_files(dir_path):
    # Define the target directories for each file type
    txt_dir = os.path.join(dir_path, 'txt')
    annotations_dir = os.path.join(dir_path, 'Annotations')
    images_dir = os.path.join(dir_path, 'JPEGImages')

    # Create the target directories if they don't exist
    os.makedirs(txt_dir, exist_ok=True)
    os.makedirs(annotations_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # Iterate over all files in the directory
    for filename in tqdm(os.listdir(dir_path)):
        file_path = os.path.join(dir_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            if filename.endswith('.txt'):
                shutil.move(file_path, os.path.join(txt_dir, filename))
            elif filename.endswith('.xml'):
                shutil.move(file_path, os.path.join(annotations_dir, filename))
            elif filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                shutil.move(file_path, os.path.join(images_dir, filename))

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Organize files in a directory.')
    parser.add_argument('--dir_path', type=str, help='The path to the directory to organize')

    # Parse the arguments
    args = parser.parse_args()

    # Call the organize_files function with the provided directory path
    organize_files(args.dirpath)
