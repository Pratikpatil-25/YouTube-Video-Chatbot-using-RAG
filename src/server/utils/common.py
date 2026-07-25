import os
from box.exceptions import BoxValueError  # This exception occurs when converting an empty dictionary or invalid data into a ConfigBox.
import yaml
from logger import logger
import json  
from ensure import ensure_annotations # This is a decorator that checks whether function arguments match their type hints.
from box import ConfigBox  # ConfigBox converts a dictionary into an object. So that we can access dictionary items using '.' notation. Eg. dict = {"k1":"val1","k2":"val2"} we can only access 'val1' using dict['k1'] but it is easy using this syntax : "dict.k1". ConfigBox allows us this as it converts the dictionary into an object.
from pathlib import Path 


    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):  # if verbose == True then the function prints diagnostic info such as which dir is being created or noting if already exists. if verbose == False then the function runs silently, providing no output unless an error occurs.
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data

    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """
    with open(path, "w") as file:
        json.dump(data, file, indent=4)  # indent parameter specifies the number of spaces to use for indentation, making the JSON output human-readable.

    logger.info(f"json file saved at: {path}")




@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data

    Args:
        path (Path): path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"json file loaded succesfully from: {path}")
    return ConfigBox(content)



@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"