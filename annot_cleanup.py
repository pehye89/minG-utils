import os, json
import argparse
from tqdm import tqdm
from annotation_utils import AnnotationProcessor

def annotation_cleanup(input_dir, output_dir, rename_map, allowed_annotations):
    processor = AnnotationProcessor(rename_map, allowed_annotations)
    os.makedirs(output_dir, exist_ok=True)
    for xml_file in tqdm(os.listdir(input_dir), desc="Processing XML Annotations"):
        if xml_file.endswith(".xml"):
            input_file_path = os.path.join(input_dir, xml_file)
            output_file_path = os.path.join(output_dir, xml_file)
            processor.process_annotation_file(input_file_path, output_file_path)

def main():
    parser = argparse.ArgumentParser(description="Annotation processing utility")

    # Annotation Cleanup
    parser.add_argument("input_dir", type=str, help="Input directory with XML files")
    parser.add_argument("output_dir", type=str, help="Output directory for cleaned XML files")
    parser.add_argument("--rename_map", type=json.loads, help="JSON string of rename map", required=True)
    parser.add_argument("--allowed_annotations", type=json.loads, help="JSON list of allowed annotations", required=True)

    args = parser.parse_args()
    annotation_cleanup(args.input_file, args.output_file, args.rename_map, args.allowed_annotations)