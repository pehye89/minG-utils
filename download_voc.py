import os, argparse, json
from tqdm import tqdm
from annotation_utils import AnnotationProcessor, VOCDownloader


def download_cleanup_voc(dataset_year, output_dir, rename_map, allowed_annotations):
    voc_downloader = VOCDownloader(dataset_year=dataset_year)
    voc_downloader.download_voc_dataset(output_dir)

    processor = AnnotationProcessor(rename_map, allowed_annotations)
    for xml_file in tqdm(os.listdir(output_dir), desc="Processing VOC XML Annotations"):
        if xml_file.endswith(".xml"):
            processor.process_annotation_file(os.path.join(output_dir, xml_file), os.path.join(output_dir, xml_file))

def main():
    parser = argparse.ArgumentParser(description="Annotation processing utility")
    
    parser.add_argument("--dataset_year", type=str, help="VOC dataset year to download", required=True)
    parser.add_argument("output_dir", type=str, help="Output directory for the dataset")
    parser.add_argument("--rename_map", type=json.loads, help="JSON string of rename map", required=True)
    parser.add_argument("--allowed_annotations", type=json.loads, help="JSON list of allowed annotations", required=True)

    args = parser.parse_args()
    download_cleanup_voc(args.dataset_year, args.output_dir, args.rename_map, args.allowed_annotations)