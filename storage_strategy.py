# storage.py

from abc import ABC, abstractmethod
import os
import json

from cache import RedisCache

"""
 # storage_strategy.py

This module defines the storage strategy for saving data and images.

The Storage class is an abstract base class that defines the interface for 
saving data and images.
Any concrete storage implementation should inherit from this class and 
implement the save_data and save_image methods.

The LocalFileStorage class is a concrete implementation of the Storage class 
that saves data and images locally.
It takes a filename as a parameter and saves the data as a JSON file and the 
image as a binary file.

To add a new storage strategy, create a new class that inherits from the 
Storage class and implement the save_data and save_image methods.
"""


class Storage(ABC):

    @staticmethod
    def get_storage_technique(technique):
        if technique == "local":
            return LocalFileStorage
        elif technique == "redis":
            return RedisStorage
        else:
            raise ValueError(f"Unknown storage technique: {technique}")

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def save_data(self, data):
        pass

    @abstractmethod
    def save_image(self, image_url, image_path):
        pass


class LocalFileStorage(Storage):
    def __init__(self, filename):
        assert filename, "Filename cannot be empty"
        self.filename = filename

    def save_data(self, data: list):
        file_path = os.getcwd() + "/data/"
        os.makedirs(file_path, exist_ok=True)
        # Read the existing data from the file
        existing_data = self.get_data()
        existing_data.extend(data)
        file_path = file_path + self.filename

        # Write the data back to the file
        with open(file_path, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)

    def save_image(self, image_content):
        file_path = os.getcwd() + "/images/"
        os.makedirs(file_path, exist_ok=True)
        file_path = file_path + self.filename
        with open(file_path + self.filename, "wb") as f:
            f.write(image_content)
        return file_path

    def get_data(self):
        file_path = os.getcwd() + "/data/" + self.filename
        # Read the existing data from the file
        existing_data = []
        try:
            with open(file_path, 'r') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []
        return existing_data


class RedisStorage(Storage):
    def __init__(self, key, expiration=None):
        self.redis_client = RedisCache()
        self.key = key
        self.expiry_time = expiration

    def save_data(self, data):
        self.redis_client.write_to_cache(self.key, data, self.expiry_time)

    def get_data(self):
        return self.redis_client.read_from_cache(self.key)

    def save_image(self, image_content):
        pass
