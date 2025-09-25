import json
import os
import uuid
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple

from PIL import Image
from PySide6.QtWidgets import QApplication

from utils import ensure_data_dirs_exist, load_metadata, save_metadata, pixel_distance
from location_Item import add_location_item, list_all_items


DATA_DIR = os.path.join("data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
METADATA_PATH = os.path.join(DATA_DIR, "metadata.json")
NMH_MAP_PATH = os.path.join("assets", "nmh_map.png")





#TODO make the main window a qt window and put the ui in the main window Henry

def main() -> None:
    return None

if __name__ == "__main__":
    main()


