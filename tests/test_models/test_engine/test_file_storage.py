#!/usr/bin/python3
'''contains the filestorage test classes'''

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class test_FileStorage(unittest.TestCase):

    def test_all_type(self):
        storage = FileStorage()
        self.assertTrue(isinstance(storage.all(), dict))


    def test_all_vals(self):
        storage = FileStorage()
        ob = BaseModel()
        ob.save()
        m_dic = storage.all()
        self.assertTrue(isinstance(m_dict.values()[0], BaseModel))


    def test_all_keys(self):
        storage = FileStorage()
        ob = BaseModel()
        ob.save()
        m_dic = storage.all()
        self.assertEqual(m_dic.keys()[0], 'BaseModel.'+ ob.id)


    def test_get_obs(self):
        storage = FileStorage()
        ob = BaseModel()
        ob.save()
        obj = storage.get(BaseModel, ob.id)
        self.assertTrue(isinstance(obj, BaseModel))


    def test_count(self):
        storage = FileStorage()
        num = storage.count(BaseModel)
        ob = BaseModel()
        ob.save()
        num2 = storage.count(BaseModel)
        self.assertEqual(0, num)
        self.assertEqual(1, num2)
