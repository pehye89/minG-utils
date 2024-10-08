import xml.etree.ElementTree as ET
import os
import json
import requests
import zipfile

class AnnotationProcessor:
    def __init__(self, rename_map, allowed_annotations):
        self.rename_map = rename_map
        self.allowed_annotations = allowed_annotations

    def rename_annotations(self, xml_root):
        # Rename annotations as specified in rename_map
        for obj in xml_root.findall(".//object/name"):
            if obj.text in self.rename_map:
                obj.text = self.rename_map[obj.text]

    def remove_unwanted_annotations(self, xml_root):
        # Remove all annotations except those in allowed_annotations
        for obj in xml_root.findall(".//object"):
            name = obj.find("name").text
            if name not in self.allowed_annotations:
                xml_root.find("annotation").remove(obj)

    def retain_only_bounding_box(self, xml_root):
        # Retain only the bounding box for each object
        for obj in xml_root.findall(".//object"):
            for child in list(obj):
                if child.tag != "bndbox" and child.tag != "name":
                    obj.remove(child)

    def process_annotation_file(self, input_path, output_path):
        tree = ET.parse(input_path)
        root = tree.getroot()
        
        # Perform operations
        self.rename_annotations(root)
        self.remove_unwanted_annotations(root)
        self.retain_only_bounding_box(root)

        # Write modified XML to output file
        tree.write(output_path)

class YoloToXmlConverter:
    def __init__(self, class_map, image_width, image_height):
        self.class_map = class_map
        self.image_width = image_width
        self.image_height = image_height

    def convert_yolo_to_xml(self, yolo_file_path, output_xml_path):
        annotation = ET.Element("annotation")
        with open(yolo_file_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                class_id = int(parts[0])
                class_name = self.class_map.get(class_id, "unknown")

                x_center = float(parts[1]) * self.image_width
                y_center = float(parts[2]) * self.image_height
                width = float(parts[3]) * self.image_width
                height = float(parts[4]) * self.image_height

                xmin = int(x_center - width / 2)
                ymin = int(y_center - height / 2)
                xmax = int(x_center + width / 2)
                ymax = int(y_center + height / 2)

                obj = ET.SubElement(annotation, "object")
                name = ET.SubElement(obj, "name")
                name.text = class_name
                bndbox = ET.SubElement(obj, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(xmin)
                ET.SubElement(bndbox, "ymin").text = str(ymin)
                ET.SubElement(bndbox, "xmax").text = str(xmax)
                ET.SubElement(bndbox, "ymax").text = str(ymax)

        tree = ET.ElementTree(annotation)
        tree.write(output_xml_path)

class CocoToXmlConverter:
    def __init__(self, class_map):
        self.class_map = class_map

    def convert_coco_to_xml(self, coco_file_path, output_dir):
        with open(coco_file_path, 'r') as file:
            coco_data = json.load(file)

        images = {image['id']: image for image in coco_data['images']}
        annotations = coco_data['annotations']

        for image_id, image_info in images.items():
            annotation = ET.Element("annotation")
            ET.SubElement(annotation, "filename").text = image_info['file_name']
            width = image_info['width']
            height = image_info['height']

            for ann in annotations:
                if ann['image_id'] == image_id:
                    class_id = ann['category_id']
                    class_name = self.class_map.get(class_id, "unknown")

                    xmin = int(ann['bbox'][0])
                    ymin = int(ann['bbox'][1])
                    xmax = int(xmin + ann['bbox'][2])
                    ymax = int(ymin + ann['bbox'][3])

                    obj = ET.SubElement(annotation, "object")
                    name = ET.SubElement(obj, "name")
                    name.text = class_name
                    bndbox = ET.SubElement(obj, "bndbox")
                    ET.SubElement(bndbox, "xmin").text = str(xmin)
                    ET.SubElement(bndbox, "ymin").text = str(ymin)
                    ET.SubElement(bndbox, "xmax").text = str(xmax)
                    ET.SubElement(bndbox, "ymax").text = str(ymax)

            output_xml_path = os.path.join(output_dir, f"{os.path.splitext(image_info['file_name'])[0]}.xml")
            tree = ET.ElementTree(annotation)
            tree.write(output_xml_path)

class CocoDownloader:
    def __init__(self, dataset_type="train"):
        self.dataset_type = dataset_type
        self.base_url = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
        if dataset_type == "test":
            self.base_url = "http://images.cocodataset.org/annotations/image_info_test2017.zip"

    def download_coco_dataset(self, output_dir):
        zip_file_path = os.path.join(output_dir, "coco_annotations.zip")
        response = requests.get(self.base_url)
        with open(zip_file_path, "wb") as file:
            file.write(response.content)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        os.remove(zip_file_path)

class VOCDownloader:
    def __init__(self, dataset_year="2012"):
        self.dataset_year = dataset_year
        self.base_url = f"http://host.robots.ox.ac.uk/pascal/VOC/voc{dataset_year}/VOCtrainval_{dataset_year}.tar"

    def download_voc_dataset(self, output_dir):
        tar_file_path = os.path.join(output_dir, "voc_annotations.tar")
        response = requests.get(self.base_url)
        with open(tar_file_path, "wb") as file:
            file.write(response.content)

        with zipfile.ZipFile(tar_file_path, 'r') as tar_ref:
            tar_ref.extractall(output_dir)

        os.remove(tar_file_path)
