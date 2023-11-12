#!/usr/bin/python3
"""
Module defining the BaseModel class.

Provides a base class, that serves as a foundation for other classes.
It defines common attributes and methods to be inherited.
"""
import datetime
import uuid


class BaseModel():
    """
    Base class for other classes to inherit from.
    Defines all common attributes/methods for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Class instantiation method.

        Public instance attributes:
            - `id` (str): Unique identifier.
            - `created_at` (datetime): Instance creation timestamp.
            - `updated_at` (datetime): Instance update timestamp.
        """
        from models import storage
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    if k in ['created_at', 'updated_at']:
                        setattr(self, k, datetime.datetime.fromisoformat(v))
                    else:
                        setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.today()
            self.updated_at = datetime.datetime.today()
            storage.new(self)

    def save(self):
        """
        Updates the public instance attribute `updated_at`
        with the current datetime.
        """
        from models import storage
        self.updated_at = datetime.datetime.today()
        storage.save()

    def __str__(self):
        """
        Human-readable string representation.

        Returns:
            str: Formatted string "[<class name>] (<self.id>) <self.__dict__>".
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of `__dict__` of
        the instance, + class name + string representation of the dates.

        Returns:
            dict: Dictionary representation of the instance.
        """
        result_dict = self.__dict__.copy()
        result_dict['__class__'] = self.__class__.__name__
        result_dict['created_at'] = self.created_at.isoformat()
        result_dict['updated_at'] = self.updated_at.isoformat()
        return result_dict
