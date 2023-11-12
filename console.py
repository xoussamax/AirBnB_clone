#!/usr/bin/python3
"""
Module that contains the entry point of the command interpreter.
"""
from models.base_model import BaseModel
from models import storage
import cmd


class HBNBCommand(cmd.Cmd):
    """Command Interpreter"""

    prompt = "(hbnb) "
    cls_dict = {
        "BaseModel": BaseModel
    }

    def do_create(self, line):
        """Creates a new instance of a class
        Saves it (to the json file) and prints its id
        Example: (hbnb) create BaseModel
        """
        if line:
            if line in HBNBCommand.cls_dict.keys():
                new = HBNBCommand.cls_dict[line]()
                new.save()
                print(new.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, line):
        """Prints the string representation of an instance"""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        storage.reload()
        objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        if key in objs:
            print(str(objs[key]))
        else:
            print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (and saves the changes to the JSON file)
        """
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.cls_dict.keys():
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        if key in objs:
            del objs[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all
        instances based or not on the class name.
        Ex: $ all BaseModel or $ all.
        """
        args = line.split()

        if args:
            if args[0] not in HBNBCommand.cls_dict.keys():
                print("** class doesn't exist **")
                return

            instances = [
                obj for key, obj in storage.all().items()
                if key.startswith(f"{args[0]}")
            ]
        else:
            instances = list(storage.all().values())

        result = [str(instance) for instance in instances]
        print(str(result))

    def do_update(self, line):
        """
        Updates an instance based on the class name
        and id by adding or updating attribute
        (save the change into the JSON file).

        Usage:
            update <class name> <id> <attribute name> "<attribute value>"

        - Only one attribute can be updated at the time
        """
        args = line.split()

        if len(args) == 0:
            print("** class name missing **")
            return
        else:
            if args[0] not in HBNBCommand.cls_dict.keys():
                print("** class doesn't exist **")
                return
            if len(args) == 1:
                print("** instance id missing **")
                return
            storage.reload()
            objs = storage.all()
            key = f"{args[0]}.{args[1]}"
            if key in objs:
                if len(args) == 2:
                    print("** attribute name missing **")
                    return
                if len(args) == 3:
                    print("** value missing **")
                    return
                instance = objs[key]
                if hasattr(instance, args[2]):
                    origin = type(getattr(instance, args[2]))
                    setattr(instance, args[2], origin(args[3]))
                else:
                    setattr(instance, args[2], args[3])
            else:
                print("** no instance found **")
            storage.save()

    def emptyline(self):
        """Handles empty line input"""
        pass

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF input to exit the program"""
        print()
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
