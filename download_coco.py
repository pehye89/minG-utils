import os, json
import argparse
from tqdm import tqdm
from annotation_utils import AnnotationProcessor, CocoDownloader
from coco_voc import coco_to_voc

def download_and_convert_coco(dataset_type, output_dir, class_map, rename_map, allowed_annotations):
    coco_downloader = CocoDownloader(dataset_type=dataset_type)
    coco_downloader.download_coco_dataset(output_dir)

    coco_input_file = os.path.join(output_dir, "annotations", f"instances_{dataset_type}2017.json")
    coco_output_dir = os.path.join(output_dir, "coco_converted")
    os.makedirs(coco_output_dir, exist_ok=True)

    coco_to_voc(coco_input_file, coco_output_dir, class_map)

    processor = AnnotationProcessor(rename_map, allowed_annotations)
    for xml_file in tqdm(os.listdir(coco_output_dir), desc="Processing COCO XML Annotations"):
        if xml_file.endswith(".xml"):
            processor.process_annotation_file(os.path.join(coco_output_dir, xml_file), os.path.join(coco_output_dir, xml_file))

def main():
    parser = argparse.ArgumentParser(description="Annotation processing utility")
    
    # Download and Convert COCO then Cleanup
    parser.add_argument("--dataset_type", type=str, choices=["train", "test"], help="COCO dataset type to download", required=True)
    parser.add_argument("output_dir", type=str, help="Output directory for the dataset")
    parser.add_argument("--class_map", type=json.loads, help="JSON string of class map", required=True)
    parser.add_argument("--rename_map", type=json.loads, help="JSON string of rename map", required=True)
    parser.add_argument("--allowed_annotations", type=json.loads, help="JSON list of allowed annotations", required=True)

    args = parser.parse_args()
    download_and_convert_coco(args.dataset_type, args.output_dir, args.class_map, args.rename_map, args.allowed_annotations)