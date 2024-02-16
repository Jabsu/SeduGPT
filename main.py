import sys
import random
import importlib
import time
import os

from GUI.main_window import UI
from GUI.settings_window import SettingsUI
from helpers import Helpers
from translations import Translations
from gpt import GPT
from messaging import Messaging

import config

# Import modules
for mod in config.MODULES:
    importlib.import_module(mod)


class Main:

    def __init__(self, args):
        '''Initialize defaults, module configurations, etc.'''

        self.Help = Helpers(self)
        self.Tr = Translations()
        
        # Default settings (main)
        defaults = {
            'language': {
                'label': 'Language',
                'interact_widget': 'OptionMenu',
                'options': {
                    'Finnish': 'fi',
                    'English': 'en'
                },
                'default_option': 'en',
                'selected_option': '',
            },
            'internal': {
                'bot_name': 'SeduGPT',
                'user_name': '', # if empty, username will be set to OS username
                'start_with_args': '--gui', # placeholder
            }
        }

        # Import settings from a file
        self.settings = self.Help.read_file(config.SETTINGS_FILE)

        # Update imported settings, if needed
        self.update_settings('MAIN', defaults)
        
        # Dynamic attribute creation
        self.set_settings_as_attributes()
        
        self.args = args
        
        self.initialize_modules()
        
        
        if args == '--gui':
            # GUI
            self.UI = UI()
            self.UI.send_button.configure(command=lambda: self.send())
            self.UI.settings_button.configure(command=lambda: self.open_settings_window())
            self.UI.bind('<Return>', lambda event=None: self.send())

            self.GPT = GPT(self.user_name, self.UI.status)
            self.UI.mainloop()

        elif args == '--debug':
            # gudeb
            pass

        elif args:
            self.msg = args
            self.iterate_module_triggers()

       


           
    def language(self):
        
        self.language = 'en'
        
        option, value = self.Help.get_selected_option('MAIN', 'language')
  
        if value:
            self.language = value
       

    def update_settings(self, module, defaults):
        '''Update the settings dictionary with new or renamed keys.'''
              
        settings = self.settings
        
        if not settings.get(module):
            self.settings[module] = defaults
            return
        
        for container, cfgs in defaults.items():
            if not container in settings[module].keys():
                settings[module][container] = defaults[container]

            for cfg, value in cfgs.items():
                if not settings[module][container].get(cfg):
                    settings[module][container][cfg] = value

        # Finally, rearrange the dict so that it starts with the 'MAIN' key
        self.settings = {
            'MAIN': settings['MAIN'], 
            **{key: settings[key] for key in settings if key != 'MAIN'}
        }


    def _get_selected(self, cfg):
      
        if selected := cfg['selected_option']:
            return selected 
        else:
            return cfg['default_option']
    

    def create_attribute(self, cfg, value):
        '''Create attributes and apply special functions/methods for certain settings.'''
        
        # create_attr: creates the attribute with the defined value, unless set to:
        #        False — skip attribute creation
        #   'func_ret' — create the attribute with the value returned by 'function'
        
        # rename_attr: If not '', use a defined name for the attribute

        special_operations = {
            'user_name': {
                'condition_satisfied': value == '',
                'function': lambda: os.getlogin(),
                'create_attr': 'func_ret',
                'rename_attr': '',
            },
        }
    
        create_attribute = True
        
        for attr, ops in special_operations.items():
            if cfg == attr and ops['condition_satisfied']:
                special = True
                if ops['function']:
                    function_return = ops['function']()
                if value_container := ops['create_attr']:
                    if value_container == 'func_ret':
                        value = function_return
                    else:
                        value = value_container
                    if renamed := ops['rename_attr']:
                        cfg = renamed
                else:
                    create_attribute = False
                break
        
        if create_attribute:
            exec(f"self.{cfg} = '{value}'", locals())
                

    def set_settings_as_attributes(self):
        '''Dynamic attribute creation with keys and values used in main settings.'''
         
        for cat, contents in self.settings['MAIN'].items():
            if contents.get('interact_widget'):
                # Create attributes from UI settings
                value = self._get_selected(contents)
                self.create_attribute(cat, value)
            else:
                # Create attributes from non-UI settings (such as "internal")
                for cfg, value in contents.items():
                    self.create_attribute(cfg, value.replace("'", "\\'"))


    def open_settings_window(self):
        
        self.cfgUI = SettingsUI(self, self.settings)
        self.cfgUI.add_config_widgets()
        self.cfgUI.protocol("WM_DELETE_WINDOW", lambda: self.settings_window_closed())
        self.cfgUI.mainloop()



    def settings_window_closed(self):
        self.settings = self.cfgUI.settings_copy
        self.Help.save_file(config.SETTINGS_FILE, self.settings)
        self.cfgUI.destroy()
        self.set_settings_as_attributes()

    
    def initialize_modules(self):
        
        self.modules = []

        for mod in config.MODULES:
            module = importlib.import_module(mod)
            module_main_class = getattr(module, 'Module')(self)
            module_name = module_main_class.module_name
            module_defaults = module_main_class.defaults
            
            self.update_settings(module_name, module_defaults)
            
            try: 
                dict = getattr(module_main_class, 'translations')
            except AttributeError:
                pass
            else:
                self.Tr.update_dictionary(module_name, dict)

            
            
            self.modules.append(module)

    
    def iterate_module_triggers(self):
        '''Iterates through module triggers. 
        
        TO-DO: 
        Load the triggers into memory instead of iterating through them repeatedly, so that 
        a quarter of a millisecond would be saved on a 386 SX (@ 12 MHz, 4 MB RAM, less than 640 kB 
        of conventional memory).'''
        
        triggered = False

        for module in self.modules:
            
            
            self.current_mod = module.Module(self)
            # mod_name = self.current_mod.get_module_name()
            
            # If triggered by user message, module returns a specific method, which is then called
            if module_func := self.current_mod.check_triggers(self.msg):
                
                triggered = True
                
                func = getattr(self.current_mod, module_func)
                func()
                
                self.bot_output(True)

        if not triggered:
            # Not triggered by any module; bot outputs the default text
            self.bot_output(False)

    
    def send(self, event=None):
        '''Start the message handler.'''
        
        msg_handler = Messaging(self)
        msg_handler.start()
        

if __name__ == '__main__':
    
    # Append current directory to system path (top-level package import hack)
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Incomplete command line functionality
    args = '--gui'
    if len(sys.argv) > 1:
        args = ' '.join(sys.argv[1:])
    
    Main(args)