## NMH Localized GeoGuesser (Streamlit)

### Setup
1. Requires Python 3.9+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run src/main.py
   ```

### How it works (local 2D coordinates)
- Place your campus map image at `assets/nmh_map.png`.
- In Admin tab: upload a photo, set its answer point as pixel coordinates (x, y). Optional: spot name, direction, hint.
- In Play tab: choose "Canvas guess" to click on the campus map and see pixel distance to the answer. Or use "Multiple choice (images)".

### Data
- Images saved under `data/images/`
- Metadata in `data/metadata.json`

### Notes
- This app is intended for local use. Respect image copyrights.

### Project Structure
```
NMH_GeoGuesser/
  assets/
    nmh_map.png            # Campus base image (you provide)
  data/
    images/                # Uploaded photos (saved at runtime)
    metadata.json          # Item metadata (created at runtime)
  src/
    main.py                # Streamlit app entry
  tests/
    README.md              # Test notes
  .streamlit/
    config.toml            # Streamlit dev config
  .gitignore
  README.md
  requirements.txt
```

