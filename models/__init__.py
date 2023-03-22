#!/usr/bin/python3
'''initializing package'''
from os import getenv


if getenv('HLINK_DB') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
