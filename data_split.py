import os
import argparse
import random
from tqdm import tqdm

def get_image_annotation_pairs(dirpath):
    image_annotation_pairs = []

    # Walk through directories and display progress using tqdm
    for root, dirs, files in tqdm(os.walk(dirpath), desc="Scanning directories", unit="dir"):
        if 'JPEGImages' in dirs and 'Annotations' in dirs:
            jpeg_dir = os.path.join(root, 'JPEGImages')
            annotation_dir = os.path.join(root, 'Annotations')

            # List files in the JPEGImages directory and match them with Annotations
            for image_file in tqdm(os.listdir(jpeg_dir), desc=f"Processing {os.path.basename(jpeg_dir)}", unit="file", leave=False):
                if image_file.endswith('.jpg'):
                    image_name = os.path.splitext(image_file)[0]
                    annotation_file = os.path.join(annotation_dir, f'{image_name}.xml')

                    if os.path.exists(annotation_file):
                        # Relative paths
                        image_rel_path = os.path.relpath(os.path.join(jpeg_dir, image_file), dirpath)
                        annotation_rel_path = os.path.relpath(annotation_file, dirpath)

                        image_annotation_pairs.append((image_rel_path, annotation_rel_path))
    
    return image_annotation_pairs

def split_data(pairs, train_ratio=0.8, test_ratio=0.1, val_ratio=0.1):
    random.shuffle(pairs)
    
    total = len(pairs)
    train_size = int(train_ratio * total)
    test_size = int(test_ratio * total)
    val_size = total - train_size - test_size

    train_pairs = pairs[:train_size]
    test_pairs = pairs[train_size:train_size + test_size]
    val_pairs = pairs[train_size + test_size:]
    
    return train_pairs, test_pairs, val_pairs

def save_split_to_file(pairs, filename):
    with open(filename, 'w') as f:
        for image, annotation in pairs:
            f.write(f'{image} {annotation}\n')

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Match JPEG images with XML annotations and split into train/test/val.")
    parser.add_argument('dirpath', type=str, help="Directory containing subdirectories with 'JPEGImages' and 'Annotations'.")
    args = parser.parse_args()

    # Get the list of image and annotation pairs
    print("Gathering image-annotation pairs...")
    pairs = get_image_annotation_pairs(args.dirpath)

    # Split the data into train/test/val
    print("Splitting data into train/test/val sets...")
    train_pairs, test_pairs, val_pairs = split_data(pairs)

    # Save to files
    print("Saving splits to files...")
    save_split_to_file(train_pairs, 'train.txt')
    save_split_to_file(test_pairs, 'test.txt')
    save_split_to_file(val_pairs, 'val.txt')

if __name__ == "__main__":
    main()
