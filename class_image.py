from jsonutils import loadjson, savejson
class image:
    def __init__(self):
        pass
    def imageadd():
        images = loadjson()
        imagename = input("What is the picture of? ")
        imagelocationx = int(input("X coordinate"))
        imagelocationy = int(input("Y coordinate"))
        imagedifficulty = input("Easy or Hard difficulty (case sensitive)? ")
        new_image = {
            "imagename" : imagename,
            "imagelocationx" : imagelocationx,
            "imageocationy" : imagelocationy,
            "imagedifficulty" : imagedifficulty
        }
        images.append(new_image)
        savejson("imagedata.json", images)
    