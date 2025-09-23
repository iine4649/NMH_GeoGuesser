from utils import loadjson, savejson
class image:
    def __init__(self):
        pass
    def imageadd():
        images = loadjson()
        imagename = input("Where is the image taken")
        imagelocationx = int(input("X coordinate"))
        imagelocationy = int(input("Y coordinate"))
        new_image = {
            "imagename" : imagename,
            "imagelocationx" : imagelocationx,
            "imageocationy" : imagelocationy
        }
        images.append(new_image)
        savejson("imagedata.json", images)