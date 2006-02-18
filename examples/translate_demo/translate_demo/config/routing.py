"""
Setup your Routes options here
"""
import sys, os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from routes.base import Mapper

map = Mapper(directory=root_path+'/controllers')
map.connect(':controller/:action/:id')
map.connect('*url', controller='template', action='view')
