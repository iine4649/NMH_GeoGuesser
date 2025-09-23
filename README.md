Roles:
Backend: Shun & Eben
Frontend: Henry & Ethan
Chief Photographer and Location Services: Georgii Panasenko

file structure:
- \src
- \ - \backend.py
- \ - \gui.py
- \ - \main.py
- \ data
- \ - \imagedata.json
- \ - \userdata.json
- \ - \ photos
- \ - \ - \ photo0.jpg

User will be able to:
   click a point on the map and get returned a score
   see a map
   see a photo
   see a timer
   show the next image after an image is clicked or the timer runs out
   see their score
   see number of images left
   When the file is run they will choose easy or hard
### Project Structure

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
backend requirements:
   image location on map
   high score
   use each image only once and randomize(queue all images at start)
   timer
   find point of click on map
   calculate points for each distance