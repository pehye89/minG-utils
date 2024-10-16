import os
import xml.etree.ElementTree as ET
import requests
from zipfile import ZipFile
import tarfile
from tqdm import tqdm

# Step 1: Download the VOC dataset (you can use VOC 2012)
def download_voc_dataset(url, dataset_dir):
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
    tar_file_path = os.path.join(dataset_dir, "voc2012.tar")

    # Download the dataset
    if not os.path.exists(tar_file_path):
        print("Downloading VOC dataset...")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(tar_file_path, "wb") as f:
            for data in tqdm(response.iter_content(1024), total=total_size // 1024, unit='KB'):
                f.write(data)
    
    # Extract the downloaded dataset
    with tarfile.open(tar_file_path, 'r') as tar_ref:
        print("Extracting dataset...")
        tar_ref.extractall(dataset_dir)
    print("Dataset downloaded and extracted.")


# Step 2: Process annotations
def process_annotations(annotations_dir, output_dir, target_classes):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse each annotation file
    for annotation_file in os.listdir(annotations_dir):
        if annotation_file.endswith(".xml"):
            tree = ET.parse(os.path.join(annotations_dir, annotation_file))
            root = tree.getroot()

            # Filter objects by target classes and modify bus to car
            for obj in root.findall("object"):
                cls = obj.find("name").text
                if cls == "bus":
                    obj.find("name").text = "car"  # Merge bus into car

                if cls not in target_classes:
                    root.remove(obj)

            # Check if there are remaining valid objects in the annotation
            if len(root.findall("object")) > 0:
                # Save the updated annotation file
                tree.write(os.path.join(output_dir, annotation_file))


# Step 3: Copy corresponding images
def copy_images(image_dir, output_image_dir, annotations_dir):
    if not os.path.exists(output_image_dir):
        os.makedirs(output_image_dir)

    # Copy only images that have corresponding annotation files
    for annotation_file in os.listdir(annotations_dir):
        if annotation_file.endswith(".xml"):
            image_filename = annotation_file.replace(".xml", ".jpg")
            source_image_path = os.path.join(image_dir, image_filename)
            if os.path.exists(source_image_path):
                destination_image_path = os.path.join(output_image_dir, image_filename)
                if not os.path.exists(destination_image_path):
                    os.link(source_image_path, destination_image_path)

# Function to remove all <part> elements from annotations
def remove_part_elements(annotations_dir):
    # Loop through all annotation files
    for annotation_file in os.listdir(annotations_dir):
        if annotation_file.endswith(".xml"):
            # Parse the XML annotation file
            annotation_path = os.path.join(annotations_dir, annotation_file)
            tree = ET.parse(annotation_path)
            root = tree.getroot()

            # Find and remove all <part> elements from the XML
            for obj in root.findall('object'):
                parts = obj.findall('part')
                for part in parts:
                    obj.remove(part)  # Remove each <part> element

            # Write the updated annotation back to the file
            tree.write(annotation_path)
    print("Removed all <part> elements from annotations.")

    
# Step 4: Main function to download, filter, and save the dataset
def download_and_filter_voc(dataset_dir='VOCdevkit'):
    voc_url = "http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar"
    download_voc_dataset(voc_url, dataset_dir)

    voc_base_dir = os.path.join(dataset_dir, "VOCdevkit", "VOC2012")
    annotations_dir = os.path.join(voc_base_dir, "Annotations")
    image_dir = os.path.join(voc_base_dir, "JPEGImages")

    output_annotations_dir = os.path.join(dataset_dir, "Annotations")
    output_image_dir = os.path.join(dataset_dir, "JPEGImages")

    # Step 2: Process annotations and filter classes
    process_annotations(annotations_dir, output_annotations_dir, target_classes=["car", "bus", "person", "motorbike"])

    # Step 3: Remove all <part> elements from annotations
    remove_part_elements(output_annotations_dir)

    # Step 4: Copy corresponding images
    copy_images(image_dir, output_image_dir, output_annotations_dir)

    print("Filtered dataset saved to:", dataset_dir)


# Run the function to download, filter and save the dataset
download_and_filter_voc()
