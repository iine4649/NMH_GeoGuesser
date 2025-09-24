import json
def loadjson(): 
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "imagedata.json")
    with open(file_path, "r") as file:
        return json.load(file)
def savejson(file, data):
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "imagedata.json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent = 4)