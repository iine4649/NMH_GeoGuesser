"""Utils.py

This module provides helper constants and functions used across the
application for data storage and simple geometry operations.

Constants
- DATA_DIR: base data directory ("data/")
- IMAGES_DIR: directory where image files are stored ("data/images/")
- METADATA_PATH: JSON file path storing image metadata ("data/metadata.json")
- NMH_MAP_PATH: bundled map image used by the clickable map widget

Functions
- load_metadata() / save_metadata(data): read/write the metadata JSON.
- is_within_bbox(lat, lon, bbox): check whether a coordinate is inside a
    bounding box (min_lat, min_lon, max_lat, max_lon).
- pixel_distance(p1, p2): Distance between two pixel coordinates.

Metadata format (expected)
The metadata file is a JSON object with an "items" list. Each entry is a
dictionary describing an image and may contain fields like:
    {
        "filename": "images/photo_1.jpg",
        "imlocationx": 123,
        "imlocationy": 456,
        "difficulty": "easy"
    }

"""

import os
import json
from typing import Tuple


DATA_DIR = os.path.join("data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
METADATA_PATH = os.path.join(DATA_DIR, "metadata.json")
NMH_MAP_PATH = os.path.join("assets", "nmh_map.png")


def ensure_data_dirs_exist() -> None:
    os.makedirs(IMAGES_DIR, exist_ok=True)
    if not os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump({"items": []}, f, ensure_ascii=False, indent=2)


def load_metadata() -> dict:
    ensure_data_dirs_exist()
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metadata(data: dict) -> None:
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_within_bbox(lat: float, lon: float, bbox: Tuple[float, float, float, float]) -> bool:
    min_lat, min_lon, max_lat, max_lon = bbox
    return (min_lat <= lat <= max_lat) and (min_lon <= lon <= max_lon)


def pixel_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    from math import sqrt
    return float(sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2))


