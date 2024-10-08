import os, json
import argparse
from tqdm import tqdm
from annotation_utils import AnnotationProcessor, YoloToXmlConverter, CocoToXmlConverter, CocoDownloader, VOCDownloader

def coco_to_voc(coco_input_file, output_dir, class_map):
    os.makedirs(output_dir, exist_ok=True)
    converter = CocoToXmlConverter(class_map)
    converter.convert_coco_to_xml(coco_input_file, output_dir)

def main():
    parser = argparse.ArgumentParser(description="Annotation processing utility")

    # COCO to VOC
    parser.add_argument("coco_input_file", type=str, help="COCO input JSON file path")
    parser.add_argument("output_dir", type=str, help="Output directory for XML files")
    parser.add_argument("--class_map", type=json.loads, help="JSON string of class map", required=True)

    args = parser.parse_args()
    coco_to_voc(args.coco_input_file, args.output_dir, args.class_map)