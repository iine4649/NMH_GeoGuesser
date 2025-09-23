from dataclasses import dataclass, asdict
from typing import Optional, List
import os
import uuid
from utils import ensure_data_dirs_exist, load_metadata, save_metadata, IMAGES_DIR

@dataclass
class LocationItem:
    id: str
    image_path: str
    # Local 2D coordinates (integer pixel grid)
    x: int
    y: int
    hint: Optional[str] = None
    spot: Optional[str] = None
    direction: Optional[str] = None


def _clamp_int(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(max_value, value))


def add_location_item(img_bytes: bytes, img_suffix: str, x: float, y: float, hint: Optional[str]) -> None:
    ensure_data_dirs_exist()
    item_id = str(uuid.uuid4())
    filename = f"{item_id}{img_suffix}"
    file_path = os.path.join(IMAGES_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(img_bytes)

    meta = load_metadata()
    xi = int(round(x))
    yi = int(round(y))
    entry = LocationItem(id=item_id, image_path=file_path, x=xi, y=yi, hint=hint)
    meta["items"].append(asdict(entry))
    save_metadata(meta)


def list_all_items() -> List[dict]:
    meta = load_metadata()
    return list(meta.get("items", []))