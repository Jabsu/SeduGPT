import importlib
import json
import os
import re
import time

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
            return_settings = self.parent.settings

        return_func = None
        
        for trigger, func in self.parent.triggers.items():
            if re.findall(trigger, self.parent.msg, self.parent.re_flags):
                return_func = func

        return [return_settings, return_func]
    

    def convert_to_dict(self, items) -> dict:
            '''Convert list object to dict object (where key name equals value name).'''

            ret = {}
            
            if type(items) == list:
                for item in items:
                    ret[item] = item
            else:
                print(f"convert_to_dict(): Conversion not supported: {type(items).__name__} -> dict")
            
            return ret

    def get_selected_value(self, category, settings) -> tuple:
        '''Returns a selected/default option and its value from provided settings dict.'''

        if cfg := settings.get(category):
            pass
        else: 
            print(f"get_selected_value(): Provided settings do not have '{category}' category")
            print(f"Provided settings: {settings}")
            return (None, None)
    
        selected_key = None
        selected_value = None
        
        if options := cfg.get('options'):
            pass
        else:
            options = {}

        if selected_value := cfg.get('selected_value'):
            pass
        else:
            selected_value = cfg.get('default_value')
        
        
        if options:
            if type(options) == list:
                options = self.convert_to_dict(options)
            
            for key, value in options.items():
                if selected_value == value:
                    selected_key = key
            

        return (selected_key, selected_value) 


    def get_module_name(self):
        '''Returns the filename of the parent class.'''
        
        module = importlib.import_module(self.parent.__module__)
        return os.path.basename(module.__file__)
    

    def timer(self):
        '''Timer, utilizing time.perf_counter(). First call: start, second call: stop.'''
        
        if hasattr(self, 'start'):
            ret = time.perf_counter() - self.start
            del self.start
        else:
            self.start = time.perf_counter()
            ret = self.start
        
        return ret
