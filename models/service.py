#!/usr/bin/python
'''contains the amanity class'''

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Service(BaseModel, Base):
    '''defines the Service class'''
    if getenv('HLINK_DB') == 'db':
        __tablename__ = 'services'
        name = Column(String(128), nullable=False)
        hospitals = relationship('Hospital',
                                 secondary='hospital_service',
                                 back_populates='services')

    def __init__(self, *args, **kwargs):
        """initializes Service"""
        super().__init__(*args, **kwargs)
