import os
import cv2
import xml.etree.ElementTree as ET
import argparse
from tqdm import tqdm

def parse_voc_annotation(xml_file):
    """Parse a VOC XML file and return the bounding box coordinates and class labels."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    objects = []

    for obj in root.findall('object'):
        label = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        objects.append({'label': label, 'bbox': (xmin, ymin, xmax, ymax)})

    return objects

def visualize_annotations(image_path, annotations):
    """Draw bounding boxes and labels on the image."""
    image = cv2.imread(image_path)
    for obj in annotations:
        label = obj['label']
        xmin, ymin, xmax, ymax = obj['bbox']
        
        # Draw bounding box
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # Put label
        label_text = label
        label_size, _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        label_bg_ymin = max(ymin, label_size[1] + 10)
        cv2.rectangle(image, (xmin, ymin), (xmin + label_size[0], label_bg_ymin), (0, 255, 0), -1)
        cv2.putText(image, label_text, (xmin, ymin + label_size[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    return image

def main(input_dir, output_dir):
    """Main function to visualize VOC annotations."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over annotation files
    annotations_dir = os.path.join(input_dir, 'Annotations')
    images_dir = os.path.join(input_dir, 'JPEGImages')
    
    for annotation_file in tqdm(os.listdir(annotations_dir)):
        if annotation_file.endswith('.xml'):
            # Parse annotation file
            xml_file = os.path.join(annotations_dir, annotation_file)
            annotations = parse_voc_annotation(xml_file)
            
            # Load corresponding image
            image_filename = annotation_file.replace('.xml', '.jpg')
            image_path = os.path.join(images_dir, image_filename)

            if os.path.exists(image_path):
                # Visualize annotations on the image
                image_with_annotations = visualize_annotations(image_path, annotations)
                
                # Save the image with annotations
                output_image_path = os.path.join(output_dir, image_filename)
                cv2.imwrite(output_image_path, image_with_annotations)
                # print(f"Saved: {output_image_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize VOC annotations and save images.")
    parser.add_argument("--input_dir", help="Path to the VOC dataset root directory")
    parser.add_argument("--output_dir", help="Directory to save the output images")
    args = parser.parse_args()

    main(args.input_dir, args.output_dir)
