import os
import matplotlib.pyplot as plt
import numpy as np
from pycocotools.coco import COCO
from PIL import Image
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection

# Set up paths to the dataset (adjust these paths as necessary)
data_dir = '/path/to/coco/'  # Path to the COCO dataset root
ann_file = os.path.join(data_dir, 'annotations', 'instances_train2017.json')
image_dir = os.path.join(data_dir, 'train2017')
output_dir = '/path/to/output/'  # Path where visualized images will be saved

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Initialize COCO API for instance annotations
coco = COCO(ann_file)

# Define the categories of interest
categories_of_interest = ['car', 'bus', 'truck', 'person', 'motorcycle']
category_ids = coco.getCatIds(catNms=categories_of_interest)

# Get all image ids that contain the categories of interest
image_ids = coco.getImgIds(catIds=category_ids)

# Loop through all images containing the relevant categories
for image_id in image_ids:
    # Load image info
    image_info = coco.loadImgs(image_id)[0]
    
    # Load image
    image_path = os.path.join(image_dir, image_info['file_name'])
    image = Image.open(image_path)
    
    # Load annotations for the image
    ann_ids = coco.getAnnIds(imgIds=image_info['id'], catIds=category_ids, iscrowd=None)
    annotations = coco.loadAnns(ann_ids)
    
    # Create a matplotlib figure for each image
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    
    ax = plt.gca()

    # Loop over annotations and visualize only the relevant categories
    for ann in annotations:
        # Draw bounding box
        bbox = ann['bbox']
        x, y, width, height = bbox
        rect = patches.Rectangle((x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        # Draw segmentation if available
        if 'segmentation' in ann:
            seg = ann['segmentation']
            for s in seg:
                poly = np.array(s).reshape((len(s) // 2, 2))
                polygon = patches.Polygon(poly, linewidth=1, edgecolor='b', facecolor='none')
                ax.add_patch(polygon)

        # Get the category name
        category = coco.loadCats(ann['category_id'])[0]['name']
        
        # Place the label
        plt.text(x, y, category, color='white', fontsize=12, bbox=dict(facecolor='blue', alpha=0.5))
    
    # Remove axis for a cleaner look
    plt.axis('off')

    # Save the output to a file in the specified output directory
    output_file = os.path.join(output_dir, f"visualized_{image_info['file_name']}")
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
    plt.close()  # Close the figure after saving to free up memory

    print(f"Visualized image saved as {output_file}")

print("All images with relevant categories have been visualized and saved.")
