"""
Setup your Routes options here
"""
import sys, os

from routes.base import Mapper

def make_map():
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    map = Mapper(directory=root_path+'/controllers')
    
    # Define your routes
    map.connect(':controller/:action/:id')
    map.connect('*url', controller='template', action='view')

    return map