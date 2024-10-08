import os, json
import argparse
from tqdm import tqdm
from annotation_utils import YoloToXmlConverter

def yolo_to_voc(yolo_input_file, output_file, class_map, image_width, image_height):
    converter = YoloToXmlConverter(class_map, image_width, image_height)
    converter.convert_yolo_to_xml(yolo_input_file, output_file)


def main():
    parser = argparse.ArgumentParser(description="Annotation processing utility")

    # YOLO to VOC
    parser.add_argument("yolo_input_file", type=str, help="YOLO input file path")
    parser.add_argument("output_file", type=str, help="Output XML file path")
    parser.add_argument("--class_map", type=json.loads, help="JSON string of class map", required=True)
    parser.add_argument("--image_width", type=int, help="Image width", required=True)
    parser.add_argument("--image_height", type=int, help="Image height", required=True)

    args = parser.parse_args()
    yolo_to_voc(args.yolo_input_file, args.output_file, args.class_map, args.image_width, args.image_height)