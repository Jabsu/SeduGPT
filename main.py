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
        
        self.args = args

        self.user_name = os.getlogin()
        self.bot_name = 'SeduGPT'

        self.settings_file = 'settings.json'
        self.settings = self.read_file()

        self.set_main_defaults()

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
           

    def set_main_defaults(self):
        '''Set or update the default settings for the main program.'''

        if not self.settings.get('MAIN'):
            self.settings['MAIN'] = {}
        
        settings = {
            'language': {
                'label': 'fi:Kieli|en:Language',
                'interact_widget': 'OptionMenu',
                'options': {
                    'Suomi': 'fi',
                    'English': 'en'
                },
                'default_setting': 'Suomi',
                'selected_setting': '',
            }
        }

        if settings.keys() > self.settings['MAIN'].keys():
            self.settings['MAIN'].update(settings)

    def set_cfgs_as_variables(self):
        '''Dynamic creation of config variables.

        Example: VALUE = self.settings['VARIABLE_NAME]['options']['selected'] 
        --> self.VARIABLE_NAME = VALUE
        '''

        for cfg in self.settings['MAIN'].items():
            if selected := cfg['selected_setting']:
                value = cfg['options']['selected_setting']
            else:
                value = cfg['default_setting']

            exec(f"self.{cfg} = {value}", locals())


    def open_settings_window(self):
        
        self.cfgUI = SettingsUI(self.UI, self.settings)
        
        self.cfgUI.add_main_config_widgets()
        self.cfgUI.add_module_config_widgets()

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
            module_main_class = getattr(module, 'Main')()
            module_name = module_main_class.get_module_name()
            module_settings = module_main_class.get_settings()

            # Get module specific settings
            if self.settings.get(module_name):
                # Update imported settings (from settings.json) if Module.settings dict size has 
                # been changed (i.e. new configuration widgets have been added)
                if len(module_settings.keys()) > len(self.settings[module_name].keys()):
                    self.settings[module_name].update(module_settings)
            else:   
                # Add module specific defaults (Module.settings) to configurations
                self.settings[module_name] = module_settings

         
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

            
            self.current_mod = module.Main()
            mod_name = self.current_mod.get_module_name()
            
            
            
            # If triggered by user message, module returns a specific function, which is then called
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
            # Use the module's print function (if implemented) when not using the GUI (placeholder)
            # TO-DO: Finalize the commandline functionalities
            try:
                self.current_mod.print()
            except:
                print(f'{self.current_mod.get_module_name()} does not have a print function.')
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