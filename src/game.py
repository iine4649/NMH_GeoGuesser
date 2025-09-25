from typing import List, Dict
import os
import random
from utils import (
    ensure_data_dirs_exist,
    load_metadata,
    IMAGES_DIR,
    append_user_data,
    load_all_user_data,
)


_session_total_score = 0
_player_name = ""


def update_total_score(score: int) -> None:
    global _session_total_score
    _session_total_score = _session_total_score + int(score)


def save_final_score(total_score: int, difficulty: str) -> None:
    # Append final score to leaderboard data
    append_user_data({
        "player": _player_name or "Player",
        "score": int(total_score),
        "difficulty": difficulty,
    })


def get_rankings(difficulty: str) -> List[Dict]:
    # Load all entries, filter by difficulty, sort by score desc
    try:
        entries = load_all_user_data()
        filtered = [e for e in entries if e.get("difficulty") == difficulty]
        filtered.sort(key=lambda e: int(e.get("score", 0)), reverse=True)
        return filtered
    except Exception:
        return []



def initialize_game_state(difficulty: str) -> Dict:
    ensure_data_dirs_exist()
    # imagedata.json is an array. Filter by difficulty
    items: List[Dict] = load_metadata()
    if isinstance(items, dict) and "items" in items:
        items = items["items"]

    filtered = [item for item in items if item.get("difficulty") == difficulty]
    if not filtered:
        filtered = items[:]  # Fallback to all items if none match difficulty

    random.shuffle(filtered)
    filtered = filtered[:10]

    current_index = 0
    current_image_data = filtered[current_index] if filtered else None

    global _session_total_score
    _session_total_score = 0

    return {
        "images_list": filtered,
        "current_image_index": current_index,
        "current_score": 0,
        "current_difficulty": difficulty,
        "current_image_data": current_image_data,
    }



def get_processed_image_path(image_data: Dict) -> str:
    if not image_data:
        return ""
    path = image_data.get("impath", "")
    if not path:
        return ""
    # Normalize path: data may store a repo-root-relative path
    # Prefer actual file under assets/Images using the filename
    filename = os.path.basename(path)
    candidate = os.path.join("assets", "Images", filename)
    if os.path.exists(candidate):
        return candidate
    # If original path exists, use it as-is
    if os.path.exists(path):
        return path
    return candidate  # Return candidate; GUI will show failure if it doesn't exist