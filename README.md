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

backend requirements:
   image location on map
   high score
   use each image only once and randomize(queue all images at start)
   timer
   find point of click on map
   calculate points for each distance