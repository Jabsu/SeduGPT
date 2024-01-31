import sys
import random
import importlib
import time
import os
import json


from GUI.main_window import UI
from GUI.settings_window import SettingsUI
import config

# Import modules
for mod in config.MODULES:
    importlib.import_module(mod)


class Main:
    def __init__(self, args):
        '''Initialize the main program with important variables.'''
        
        # Default settings
        defaults = {
            'language': {
                'label': 'Language',
                'interact_widget': 'OptionMenu',
                'options': {
                    'Suomi': 'fi',
                    'English': 'en'
                },
                'default_option': 'Suomi',
                'selected_option': '',
            },
            'internal': {
                'bot_name': 'SeduGPT', 
                'user_name': '', # if empty, username will be set to OS username
                'start_with_args': '--gui',
                'settings_file': 'settings.json'
            }
        }
        
        
        
        self.set_internal_cfgs_as_attributes()

        # Import settings from a file
        self.settings = self.read_file()
        
        # Update imported settings, if needed
        self.update_settings('MAIN', defaults)

        
       
        
        self.args = args
        
        self.settings_file = 'settings.json'
        
        
        

        self.initialize_modules()
        
        if args == '--gui':
            # GUI
            self.UI = UI()
            self.UI.send_button.configure(command=lambda: self.send())
            self.UI.settings_button.configure(command=lambda: self.open_settings_window())
            self.UI.bind('<Return>', lambda event=None: self.send())
        
            self.UI.mainloop()

        elif args == '--debug':
            # gudeb
            pass

        elif args:
            self.msg = args
            self.iterate_module_triggers()
           

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

        

    def set_internal_cfgs_as_attributes(self):
        '''Dynamic creation of config attributes.

        Example: VALUE = self.settings['VARIABLE_NAME]['options']['selected'] 
        --> self.VARIABLE_NAME = VALUE
        '''
         
        for cfg, value in self.settings['MAIN']['internal'].items():
            if not f'self.{cfg}' in locals():
                exec(f"self.{cfg} = {value}", locals())

    def set_UI_cfgs_as_attributes(self):
        '''Set attributes for specific UI configurations, for convenience.'''

        # Unless specified, user name defaults to OS user
        # TO-DO: Make this non-internal (i.e. configurable on the UI)
        if custom_user := self.settings['MAIN']['internal']['user_name']:
            self.user_name = custom_user
        else:
            self.user_name = os.getlogin()

        
        


    def open_settings_window(self):
        
        self.cfgUI = SettingsUI(self.UI, self.settings)
        
        self.cfgUI.add_config_widgets()

        self.cfgUI.protocol("WM_DELETE_WINDOW", lambda: self.settings_window_closed())
        
        self.cfgUI.mainloop()



    def settings_window_closed(self):
        self.settings = self.cfgUI.settings
        self.save_file(self.settings)
        self.cfgUI.destroy()

    
    def read_file(self):
        
        data = {}
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
            except:
                data = {}
        
            if type(data) != dict:
                data = {}

        return data
            
    def save_file(self, settings):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

    
    def initialize_modules(self):
        
        self.modules = []

        for mod in config.MODULES:
            module = importlib.import_module(mod)
            module_main_class = getattr(module, 'Module')()
            module_name = module_main_class.get_module_name()
            module_settings = module_main_class.get_settings()

            self.update_settings(module_name, module_settings)
            
            self.modules.append(module)

    
    def iterate_module_triggers(self):
        '''Iterates through module triggers. 
        
        TO-DO: 
        Load the triggers into memory instead of iterating through them repeatedly, so that 
        a quarter of a millisecond would be saved on a 386 SX (@ 12 MHz, 4 MB RAM, less than 640 kB 
        of conventional memory).'''
        
        triggered = False

        for module in self.modules:
            
            config = None

            
            self.current_mod = module.Module()
            mod_name = self.current_mod.get_module_name()
            
            
            
            # If triggered by user message, module returns a specific method, which is then called
            if module_func := self.current_mod.check_triggers(self.msg, self.settings[mod_name]):
                
                triggered = True
                
                func = getattr(self.current_mod, module_func)
                func()
                
                self.bot_output(True)

        if not triggered:
            # Not triggered by any module; bot outputs the default text
            self.bot_output(False)

    
    def send(self, event=None):
        '''Add user input to chat (with formattings) and iterate through module triggers.'''
        
        self.msg = self.UI.entry.get()
        
        if not self.msg:
            return
        
        self.UI.entry.delete(0, 'end')
        
        self.send_prefix('user') 
        self.UI.text_insert(self.msg+'\n', tag='msg')
        
        self.iterate_module_triggers()


    def sanitize(self, content):
        '''Convert List to String. 
        
        TO-DO: Other conversions.'''

        ret = content

        if type(content) == list:
            # Use the separator defined in the module for joining the values
            ret = self.current_mod.return_separator.join(content)

        if type(content) == dict:
            pass

        return ret
    

    def send_prefix(self, user):
        '''Format and send a prefix to chat (HH:MM <user>); tags (prefix, prefix2) point to colors
        configured in main_window.py. 
        
        TO-DO: More dynamic/modular tag support.'''
        
        clock = time.strftime("%H:%M ")
        self.UI.text_insert(clock, 'prefix')      
        self.UI.text_insert('<', 'prefix2')
     
        if user == 'bot':
            user_name = self.bot_name
            self.UI.text_insert('@', 'prefix2')
        else:
            user_name = self.user_name
            self.UI.text_insert('+', 'prefix2')

        self.UI.text_insert(user_name, user)      
        self.UI.text_insert('> ' , 'prefix2')

        


    def random_output(self):
        '''The user message did not trigger any module, display random output instead.'''

        outputs = [
            'Opettelen vielä, ymmärrän tuonnempana.',
            'Pahus, menin ihan solmuun.',
            'Pahoittelen, opettelen parhaillaan ymmärtämään toista asiaa.',
            'Ymmärrän kyllä yskäsi, mutta en juuri muuta.',
        ]
        
        return random.choice(outputs)
            
    
    def bot_output(self, triggered_by_module=False):
        '''Bot's output to chat.'''
        
        if not triggered_by_module:
            bot_msg = self.random_output()
        else:
            bot_msg = self.current_mod.return_value
            
            # If the return value set in a module is not String and 'sanitize' is set to True, 
            # the value will be converted to String
            if type(bot_msg) != 'str' and self.current_mod.return_sanitize:
                bot_msg = self.sanitize(bot_msg)

     
        self.send_prefix('bot') 

        if self.args != "--gui":
            # Use the module's print method (if implemented) when not using the GUI
            # TO-DO: Finalize the command line functionalities
            try:
                self.current_mod.print()
            except:
                print(f'{self.current_mod.get_module_name()} does not have a print method.')
        else:
            if triggered_by_module:
                
                # If set by module, add a title to the output
                if title := self.current_mod.message_title:
                    self.UI.text_insert(title, tag='title')
                   
            
            self.UI.text_insert(bot_msg+'\n', tag='msg')
            

if __name__ == '__main__':
    
    # Incomplete command line functionality
    args = '--gui'

    if len(sys.argv) > 1:
        args = ' '.join(sys.argv[1:])
    
    Main(args)