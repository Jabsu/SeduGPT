import importlib
import os
import re

class Helpers:
    '''Helper functions for modules.'''
    
    def __init__(self, parent):
        self.parent = parent


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
        '''Get the module filename.'''
        
        module = importlib.import_module(self.parent.__module__)
        return os.path.basename(module.__file__)