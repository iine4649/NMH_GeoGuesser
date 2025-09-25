import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas



def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


DATA_DIR = os.path.join("data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
METADATA_PATH = os.path.join(DATA_DIR, "metadata.json")
NMH_MAP_PATH = os.path.join("assets", "nmh_map.png")

