import cv2
import numpy as np
from setup import setup
from metadata import read_metadata_from_video, parse_metadata
from video import generate_overlay

video = "GX010104.MP4"

if __name__ == "__main__":

    setup()
    
    raw_metadata = read_metadata_from_video(video)

    metadata = parse_metadata(raw_metadata)

    generate_overlay(metadata)
