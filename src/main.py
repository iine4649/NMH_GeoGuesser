import json
import os
import uuid
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple

from PIL import Image
from PySide6.QtWidgets import QApplication

from utils import ensure_data_dirs_exist, load_metadata, save_metadata, pixel_distance



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


def sidebar_controls_local() -> dict:
    st.sidebar.subheader("NMH Local Coordinate Settings")
    if not os.path.exists(NMH_MAP_PATH):
        st.sidebar.warning("Please place assets/nmh_map.png.")
        width = int(st.sidebar.number_input("Campus image width (px)", value=1200, step=10, min_value=100))
        height = int(st.sidebar.number_input("Campus image height (px)", value=800, step=10, min_value=100))
    else:
        with Image.open(NMH_MAP_PATH) as im:
            width, height = im.size
        st.sidebar.caption(f"Campus image size: {width}x{height} px")
    return {"width": width, "height": height}


def page_admin_local(canvas_meta: dict) -> None:
    st.header("Admin: Upload photos and register coordinates")
    st.write("Register locations using campus image pixel coordinates (x, y).")

    uploaded = st.file_uploader("Select image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input("X (px)", value=float(canvas_meta["width"] // 2), step=1.0, format="%.0f")
    with col2:
        y = st.number_input("Y (px)", value=float(canvas_meta["height"] // 2), step=1.0, format="%.0f")
    hint = st.text_input("Hint (optional)")
    spot = st.text_input("Spot name (optional, e.g., Library, Gym)")
    direction = st.selectbox("Direction (optional)", ["", "N", "NE", "E", "SE", "S", "SW", "W", "NW"], index=0)

    if uploaded is not None:
        image = Image.open(uploaded)
        st.image(image, caption="Preview", use_column_width=True)

    if st.button("Save"):
        if uploaded is None:
            st.warning("Please select an image.")
            return
        suffix = os.path.splitext(uploaded.name)[1].lower()
        if suffix not in [".png", ".jpg", ".jpeg"]:
            st.warning("Only PNG/JPG are supported.")
            return
        xi = _clamp_int(int(round(float(x))), 0, int(canvas_meta["width"]) - 1)
        yi = _clamp_int(int(round(float(y))), 0, int(canvas_meta["height"]) - 1)
        add_location_item(uploaded.getvalue(), suffix, xi, yi, hint if hint else None)
        # Save additional metadata
        meta = load_metadata()
        last_id = meta["items"][-1]["id"] if meta.get("items") else None
        if last_id is not None:
            for item in meta["items"]:
                if item["id"] == last_id:
                    if spot:
                        item["spot"] = spot
                    if direction:
                        item["direction"] = direction
                    break
            save_metadata(meta)
        st.success("Saved.")

    st.divider()
    st.subheader("Current total items")
    items = list_all_items()
    st.write(f"Total: {len(items)}")


def canvas_click_get_point(bg_image_path: str, display_width: int) -> Optional[Tuple[int, int]]:
    if not os.path.exists(bg_image_path):
        st.warning("Campus image not found: assets/nmh_map.png")
        return None
    bg_image = Image.open(bg_image_path)
    orig_width, orig_height = bg_image.size
    ratio = display_width / orig_width
    display_height = int(orig_height * ratio)

    c = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=2,
        background_image=bg_image,
        update_streamlit=True,
        height=display_height,
        width=display_width,
        drawing_mode="point",
        point_display_radius=6,
        key="nmh_canvas",
    )

    if c.json_data and c.json_data.get("objects"):
        # Use the last point
        last_obj = c.json_data["objects"][-1]
        x = float(last_obj.get("left", 0))
        y = float(last_obj.get("top", 0))
        # Convert display coords back to original image coords and snap to integer pixel grid
        xi = int(round(x / ratio))
        yi = int(round(y / ratio))
        xi = _clamp_int(xi, 0, orig_width - 1)
        yi = _clamp_int(yi, 0, orig_height - 1)
        return (xi, yi)
    return None


def page_play_local(canvas_meta: dict) -> None:
    st.header("NMH Local GeoGuesser (2D pixels)")
    items = list_all_items()
    if not items:
        st.info("No images yet. Please add some in the Admin tab.")
        return

    mode = st.radio("Mode", ["Canvas guess", "Multiple choice (images)"] , index=0, horizontal=True)

    import random

    if mode == "Canvas guess":
        if "current_item_id" not in st.session_state:
            st.session_state.current_item_id = None

        if st.button("Random question") or st.session_state.current_item_id is None:
            st.session_state.current_item_id = random.choice(items)["id"]

        current = next((i for i in items if i["id"] == st.session_state.current_item_id), None)
        if not current:
            st.warning("Item not found. Please try again.")
            return

        caption = current.get("hint") or (current.get("spot") or "")
        st.image(current["image_path"], caption=caption, use_column_width=True)

        guessed = canvas_click_get_point(NMH_MAP_PATH, display_width=int(min(900, canvas_meta["width"])))

        if guessed:
            gx, gy = guessed
            tx, ty = int(current["x"]), int(current["y"])
            dist = pixel_distance((gx, gy), (tx, ty))
            st.success(f"Pixel distance: {dist:.0f} px (guess: {gx},{gy} / answer: {tx},{ty})")

    else:
        if len(items) < 4:
            st.info("Multiple choice requires at least 4 images.")
            return

        if st.button("New question") or "mc_current" not in st.session_state:
            correct = random.choice(items)
            distractors = random.sample([i for i in items if i["id"] != correct["id"]], 3)
            choices = distractors + [correct]
            random.shuffle(choices)
            st.session_state.mc_current = {
                "correct_id": correct["id"],
                "choices": [c["id"] for c in choices],
            }

        state = st.session_state.get("mc_current")
        if not state:
            return

        id_to_item = {i["id"]: i for i in items}
        choices_ids = state["choices"]

        cols = st.columns(2)
        selected_id: Optional[str] = None
        for idx, cid in enumerate(choices_ids):
            item = id_to_item[cid]
            with cols[idx % 2]:
                st.image(item["image_path"], caption=f"Choice {idx+1}  " + (item.get("direction") or ""), use_column_width=True)
                if st.button(f"Choose this image", key=f"pick_{cid}"):
                    selected_id = cid

        if selected_id:
            correct_id = state["correct_id"]
            if selected_id == correct_id:
                st.success("Correct!")
            else:
                st.error("Incorrect")

            correct_item = id_to_item[correct_id]
            st.write("Answer x,y and info:")
            st.write(f"Spot: {correct_item.get('spot') or '-'} / Direction: {correct_item.get('direction') or '-'}")
            st.write(f"x={correct_item['x']:.0f}, y={correct_item['y']:.0f}")


def main() -> None:
    st.set_page_config(page_title="NMH Localized GeoGuesser (2D)", layout="wide")
    ensure_data_dirs_exist()

    st.sidebar.title("Menu")
    canvas_meta = sidebar_controls_local()
    page = st.sidebar.radio("Page", ["Play", "Admin"], index=0)

    if page == "Admin":
        page_admin_local(canvas_meta)
    else:
        page_play_local(canvas_meta)


if __name__ == "__main__":
    main()


