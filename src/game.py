import json
from gui import MainWindow

# loads the json file
def loadjson(): 
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "imagedata.json")
    with open(file_path, "r") as file:
        return json.load(file)

#saves updates to a json file
def savejson(file, data):
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "imagedata.json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent = 4)

#uses the env variable to sort images by difficulty
def load_images_by_difficulty(difficulty):
    images = loadjson()
    if MainWindow.isrunning == 1:
        key_to_find = "difficulty"
        value_to_match = "easy"
        filtered_images = [
            d for d in images
            if key_to_find in d and d[key_to_find] == value_to_match
        ]
    elif MainWindow.isrunning == 2:
        key_to_find = "difficulty"
        value_to_match = "hard"
        filtered_images = [
            d for d in images
            if key_to_find in d and d[key_to_find] == value_to_match
        ]
    return filtered_images

def process_image_path(image_path):
    
    return image_path


def initialize_game_state(difficulty):
    game_state = MainWindow.isrunning
    return game_state


def get_processed_image_path(image_data):

    return None


def save_final_score(score, difficulty):
    
    return []

def get_rankings(difficulty):
  
    return []
