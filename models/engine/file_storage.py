#!/usr/bin/python3
"""
Module defining the FileStorage class.

The class is responsible for serializing instances  to a JSON file,
and deserializing JSON files back to instances.
"""
from models.base_model import BaseModel
import json
import os


class FileStorage(BaseModel):
    """
    Class responsible for file storage using JSON.
    """
    def __init__(self):
        """
        Class instantiation method.

        Private class attributes:
            - `__file_path` (str): path to the JSON file.
            - `__objects` (dict): empty in the beginning.
                stores all objects by <class name>.id
                (ex: BaseModel object with id=12121212,
                    the key will be BaseModel.12121212)
        """
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self):
        """
        Returns: the dictionary `__objects`.
        """
        return self.__objects

    def new(self, obj):
        """
        Adds an object to `__objects`.
        with key <class name>.id

        Args:
            obj (object): the object to be added
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects.update({key: obj})

    def save(self):
        """
        Serializes `__objects` to the JSON file.
        """
        with open(self.__file_path, 'w') as f:
            if self.__objects is None:
                f.write("{}")
            else:
                serialized = {
                    key: obj.to_dict()
                    for key, obj in self.__objects.items()
                }
                f.write(json.dumps(serialized))

    def reload(self):
        """
        Deserializes the JSON file to __objects if the JSON file exists.
        No exception is raised if the file doesn't exist.
        """
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, 'r') as f:
                    loaded = json.load(f)
                    if loaded:
                        self.__objects = {
                            key: BaseModel(**value)
                            for key, value in loaded.items()
                        }
            except json.decoder.JSONDecodeError:
                pass
