#!/usr/bin/python3
'''
    module for command line interface for AirBnB clone
'''
import cmd
import sys
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.service import Service
from models.hospital import Hospital
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    '''contain the command handlers'''
    classes = {
                'BaseModel': BaseModel,
                'User': User,
                'State': State,
                'City': City,
                'Service': Service,
                'Hospital': Hospital,
                'Review': Review
                }
    commands = ['all', 'count', 'destroy', 'show', 'update']
    prompt = '(hbnb) '
    intro = 'Welcome to my AirBnB command interface, type help to get started'


    def parser(self, line):
        '''parses the functions'''
        my_list = list(filter(None, re.split(r'[\"\(\), .]+', line)))
        return my_list


    def validate(self, line, n):
        '''validates input'''
        if (len(line) == 0):
            print('** class name missing **')
            return None
        if line[0] not in self.classes:
            print('** class doesn\'t exist **')
            return None
        if (n >= 2):
            if (len(line) < 2):
                print('** instance id missing **')
                return None
            key = '{}.{}'. format(line[0], line[1])
            return storage.all().get(key, '** no instance found **')
        return ('valid')


    def do_create(self, line):
        '''creates new object'''

        lines = line.split(' ')
        if len(lines) > 1:
            if lines[0] in self.classes:
                my_dict = {}
                for param in lines[1:]:
                    key_val = param.split('=')
                    val = eval(key_val[1])
                    if type(val) == str:
                        val = key_val[1].strip('"')
                        val = val.rehospital('"', r'\"')
                        val = val.rehospital(' ', '_')
                    my_dict[key_val[0]] = val
                ob = eval(lines[0])(**my_dict)
                storage.new(ob)
                storage.save()
                print(ob.id)
                return
            else:
                print('** class doesn\'t exist **')
                return

        args = self.parser(line)
        obj = self.validate(args, 1)
        if obj:
            ob = eval(args[0])()
            storage.new(ob)
            storage.save()
            print(ob.id)



    def help_create(self):
        print('creates a new object')
        print('Usage: (HBNB) show <class>')


    def do_show(self, line):
        '''prints string representation of an instance'''
        args = self.parser(line)
        obj = self.validate(args, 2)
        if obj is not None:
            print(obj)



    def do_all(self, line):
        '''Prints all string representation of all instances'''
        args = self.parser(line)
        objs = self.validate(args, 1)
        if objs == 'valid':
            my_list = [str(ob) for ob in storage.all(args[0]).values()]
            print(my_list)


    def help_all(self):
        print('Prints all string representation of all instances')
        print('Usage: (HBNB) all <class>')



    def help_show(self):
        print('prints string representation of an instance')
        print('Usage: (HBNB) show <class> <id>')


    def do_update(self, line):
        '''Updates an instance'''
        args = self.parser(line)
        obj = self.validate(args, 5)
        if len(args) < 3:
            print('** attribute name missing **')
            return
        if len(args) < 4:
            print('** value missing **')
            return
        value = eval(args[3])
        exempt = ['id', 'created_at', 'updated_at']
        if args[2] not in exempt:
            setattr(obj, args[2], value)


    def do_destroy(self, line):
        '''Deletes an instance'''
        args = self.parser(line)
        obj = self.validate(args, 2)
        if not obj:
            return
        key = '{}.{}'. format(args[0], args[1])
        del storage.all()[key]


    def help_destroy(self):
        print('Deletes an instance')
        print('Usage: destroy <class name> <id>')


    def help_update(self):
        print('Updates an instance')
        s = 'Usage: update <class name> <id> '
        t = '<attribute name> "<attribute value>"'
        print('{}{}'. format(s, t))


    def execute(self, args):
        '''executes commands for default handler'''
        if len(args) == 1:
            print('** incomplete syntax **')
            print('Enter Help to get Usage')
            return None
        if args[0] not in self.classes:
            print('** class doesn\'t exist **')
            return None
        if args[1] not in self.commands:
            print('         ** unrecognized command **')
            print('Enter Help to get list of commands and usage')
            return None
        if args[1] == 'all':
            print(args[1])
            l = [str(o) for k, o in storage.all().items() if k.find(args[0]) != -1]
            return (l)
        if args[1] == 'count':
            l = [o for k, o in storage.all().items() if k.find(args[0]) != -1]
            return len(l)
        if args[1] == 'show':
            if len(args) != 3:
                print('** id is missing **')
                return None
            key = '{}.{}'. format(args[0], args[2])
            return storage.all().get(key, '** no instance found **')
        if args[1] == 'destroy':
            if len(args) != 3:
                print('** id is missing **')
                return None
            key = '{}.{}'. format(args[0], args[2])
            o = storage.all().get(key)
            if not o:
                print('** no instance found **')
                return None
            del storage.all()[key]
            storage.save()
            return None
        if args[1] == 'update':
            if len(args) < 3:
                print('** id is missing **')
                return None
            key = '{}.{}'. format(args[0], args[2])
            o = storage.all().get(key)
            if not o:
                print('** no instance found **')
                return None
            return (o,)


    def default(self, line):
        '''method to handle unrecognized command prefix'''
        args = self.parser(line)
        string = line.strip(')')
        x = string.find('{')
        if x != -1:
            dic = eval(string[x:])
            if type(dic) != dict:
                print('** wrong dictionary syntax **')
                return
            tup = self.execute(args)
            for key, value in dic.items():
                if key not in ['created_at', 'updated_at', 'id']:
                    setattr(tup[0], key, value)
            return

        obj = self.execute(args)
        if not obj:
            return
        if type(obj) == tuple:
            if len(args) < 4:
                print('** attribute name missing **')
                return None
            if len(args) < 5:
                print('** attribute value missing **')
                return None
            setattr(obj[0], args[3], args[4])
            return
        print(obj)
        return

    def help_default(self):
        print('***** more advanced usage *****')
        print()
        print('* To show all objects of a class *')
        print('Usage: (HBNB) <class name>.all()')
        print()
        print('* To count all objects of a class *')
        print('Usage: (HBNB) <class name>.count()')
        print()
        print('* To show a particular object of a class *')
        print('Usage: (HBNB) <class name>.show(<id>)')
        print()
        print('      * To destroy an object *')
        print('Usage: (HBNB) <class name>.destroy(<id>')
        print()
        print('   * To update an object * ')
        s = '<attribute name>, <attribute value>)'
        print('Usage: (HBNB) <class name>.update(<id>, {}'. format(s))
        print()
        print('         * To update an object with dictionary *')
        j = '(<id>, <dictionary representation>)'
        print('Usage: (HBNB) <class name>.update{}'. format(j))



    def help_EOF(self):
        '''exits the program'''
        print('exits the program')


    def do_EOF(self, line):
        '''exits the program'''
        print('Bye')
        exit()


    def do_quit(self, line):
        '''exits from the interface'''
        print('Bye')
        exit()


    def help_quit(self):
        '''exits from the interface'''
        print('exits the program')


    def emptyline(self):
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
