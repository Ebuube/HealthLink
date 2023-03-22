#!/usr/bin/python3
'''test module for the baseclass and all its methods'''
import unittest
from models.base_model import BaseModel
from models import storage


class test_BaseClass(unittest.TestCase):
    '''test the methods of the base class'''
    def test_init_no_args(self):
        ob = BaseModel()
        self.assertTrue(isinstance(ob, BaseModel))


    def test_init_args(self):
        ob = BaseModel('James', 'Apple', 'Beans')
        self.assertIs(hasattr(ob, 'name'), False)
        self.assertIs(hasattr(ob, 'Apple'), False)


    def test_init_dic(self):
        m_dict = {'name': 'James'}
        ob = BaseModel(**m_dict)
        self.assertIs(hasattr(ob, 'name'), True)
        self.assertEqual(ob.name, 'James')


    def test_init_tup(self):
        name = 'james'
        m_tup = ('name', name)
        ob = BaseModel(m_tup)
        self.assertIs(hasattr(ob, 'name'), False)


    def test_str_meth(self):
        ob = BaseModel()
        s = '[BaseModel] ({}) {}'. format(ob.id, ob.__dict__)
        self.assertEqual(s, str(ob))


    def test_to_dict(self):
        ob = BaseModel()
        self.assertTrue(isinstance(ob.to_dict(), dict))


    def test_to_dict_cls(self):
        ob = BaseModel()
        m_dict = ob.to_dict()
        self.assertIn('__class__', m_dict)


    def test_to_dict_cls_cont(self):
        ob = BaseModel()
        m_dic = ob.to_dict()
        self.assertEqual('BaseModel', m_dic['__class__'])

if __name__ == '__main__':
    unittest.main()
