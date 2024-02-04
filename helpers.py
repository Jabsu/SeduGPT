import importlib
import json
import os
import re

class Helpers:
    '''Important helper methods for both Main and Module classes.'''
    
    def __init__(self, parent=None):
        if parent:
            self.parent = parent

    def read_file(self, file) -> dict: 
        '''Import .json file and return it as a dict.'''
        
        data = {}
        if os.path.exists(file):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
            except:
                data = {}
        
            if type(data) != dict:
                data = {}

        return data
            
    
    def save_file(self, file, data=dict):
        '''Export dict to .json file.'''
        
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)


    def check_triggers(self, user_defined_settings=None):
        '''If triggered by user message, return the method specified in the module.'''
        
        if user_defined_settings:
            return_settings = user_defined_settings
        else:
            return_settings = self.parent.module_settings

        return_func = None
        
        for trigger, func in self.parent.triggers.items():
            if re.findall(trigger, self.parent.msg, self.parent.re_flags):
                return_func = func

        return [return_settings, return_func]
    

    def get_module_name(self):
        '''Returns the filename of the parent class.'''
        
        module = importlib.import_module(self.parent.__module__)
        return os.path.basename(module.__file__)