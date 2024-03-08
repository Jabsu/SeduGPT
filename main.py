import sys
import random
import importlib
import os
import traceback

from GUI.main_window import UI
from GUI.settings_window import SettingsUI
from helpers import Helpers
from translations import Translations
from gpt import GPT
from messaging import Messaging

from tkinter.messagebox import showinfo

# Import modules
#for mod in config.MODULES:
#   importlib.import_module(mod)


class Main:

    def __init__(self, args):
        '''Initialize defaults, module configurations, etc.'''

        self.name = 'SeduGPT'
        
        # Init Helpers
        self.Help = Helpers(self)
        
        # Init Translations
        self.Tr = Translations()
        
        # Import settings from a file, if found
        self.settings = self.Help.read_file('settings.json')

        # Update self.settings with missing defaults
        self.update_settings('MAIN', self.get_defaults())
        
        # Define main attributes with values from settings dict
        self.user_name = self.get_val('user_name')
        self.language = self.get_val('language')
        self.modules = self.settings['MAIN']['modules']['options']
        
        # Load modules into memory
        self.module_instances = []
        self.initialize_modules()
        
        self.args = args

        # Placeholder code for upcoming command line argument support
        if args == '--gui':
            # GUI
            self.UI = UI()
            self.UI.send_button.configure(command=lambda: self.send())
            self.UI.settings_button.configure(command=lambda: self.open_settings_window())
            self.UI.bind('<Return>', lambda event=None: self.send())

            self.GPT = GPT(self.settings, self.UI.status)
            
            self.UI.mainloop()
        elif args == '--debug':
            pass
        elif args:
            pass
            # self.msg = args
            # msg_handler = Messaging(self)
            # msg_handler.start()

       
    def get_defaults(self):
        # Return default settings
        
        try:
            files = {f: 1 for f in os.listdir("modules") if os.path.isfile(os.path.join("./modules", f))}
        except FileNotFoundError:
            print("The 'modules' directory does not exist.")
            files = {}
        else:
            if not files:
                print("No modules found in 'modules' directory.")

        settings = {
            'modules': {
                'label': 'Modules',
                'interact_widget': 'Checkbox',
                'options': files,
            },
            'user_name': {
                'label': 'Username',
                'interact_widget': 'Entry',
                'default_value': os.getlogin().split(' ')[0],
                'selected_value': '',
            },
            'language': {
                'label': 'Language',
                'interact_widget': 'OptionMenu',
                'options': {
                    'Finnish': 'fi',
                    'English': 'en'
                },
                'default_value': 'en',
                'selected_value': '',
            },
            'gpt_model': {
                'label': 'GPT Model',
                'interact_widget': 'Combobox',
                'options': [
                    'mistral-7b-openorca.Q4_0.gguf',
                    'mistral-7b-instruct-v0.1.Q4_0.gguf',
                    'gpt4all-falcon-newbpe-q4_0.gguf',
                    'orca-2-7b.Q4_0.gguf',
                    'wizardlm-13b-v1.2.Q4_0.gguf',
                ],
                'default_value': 'mistral-7b-openorca.Q4_0.gguf',
                'selected_value': '',
            },
            'gpt_model_path': {
                'label': 'GPT Model Path',
                'interact_widget': 'Entry',
                'default_value': './GPT4All',
                'selected_value': '',
                'extra_widget': {
                    'text': '...',
                    'interact_widget': 'Button',
                    'function': 'filedialog',
                    'modify_value_of': 'gpt_model_path', 
                },
            },
            'gpt_system_prompt': {
                'label': 'GPT System Prompt',
                'interact_widget': 'OptionMenu',
                'options': {
                    'Detailed (slower)': 1,
                    'Short (faster)': 2,
                },
                'default_value': 2,
                'selected_value': ''
            },
            'gpt_device': {
                'label': 'GPT Device',
                'interact_widget': 'OptionMenu',
                'options': {
                    'CPU': 'cpu',
                    'GPU': 'gpu',
                },
                'default_value': 'cpu',
                'selected_value': '',
            },
            'gpt_threads': {
                'label': 'GPT CPU Threads',
                'interact_widget': 'Entry',
                'default_value': str(os.cpu_count()),
                'selected_value': '',
                'extra_widget': {
                    'text': 'Set to default',
                    'interact_widget': 'Button',
                    'function': 'set_default',
                    'modify_value_of': 'gpt_threads', 
                },
            },
        }

        return settings
           

    def get_val(self, var):
        '''Shortener for Helpers.get_selected_value()'''
        return self.Help.get_selected_value(var, self.settings['MAIN'])[1]
    

    def update_attributes(self):
        self.user_name = self.get_val('user_name')
        self.language = self.get_val('language')
        self.modules = self.settings['MAIN']['modules']['options']


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


    def create_attribute(self, cfg, value):
        '''Create an attribute and optionally apply special function/method.'''
        
        # This method is not used anymore, but I like it, so I'll leave it here for posterity.
        
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

        # This method is not used anymore, but I like it, so I'll leave it here for posterity.

        for cat, contents in self.settings['MAIN'].items():
            if contents.get('interact_widget'):
                # Create attributes from UI settings
                if value := contents['selected_value']:
                    pass
                else:
                    value = contents['default_value']
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

        reinitialize_GPT = False
        # reinitialize_mods = False
        gpt_init_list = ['gpt_model', 'gpt_model', 'gpt_device', 'gpt_threads']

        # Update settings with values from Entry widgets
        for widget, data in self.cfgUI.entry_widgets.items():

            value = widget.get()
            module = data['module']
            category = data['category']
            previous_value = self.settings[module][category]['selected_value']
            
            if previous_value and previous_value != value and category in gpt_init_list:
                reinitialize_GPT = True
                

            self.settings[module][category]['selected_value'] = value

        '''
        # Were modules activated/deactivated?
        for module, previous_state in self.modules.items():
            current_state = self.cfgUI.settings_copy['MAIN']['modules']['options'][module]
 
            if current_state != previous_state:
                reinitialize_mods = True
        '''

        self.cfgUI.destroy()
        self.Help.save_file('settings.json', self.settings)
        self.update_attributes()
        
        if reinitialize_GPT:
            showinfo(f"My mind went blank!", 
                     "GPT4All model needs to be re-initialized.")
            self.GPT = GPT(self.settings, self.UI.status)
        
        self.initialize_modules()
        
    
    def initialize_modules(self):
        '''Create a list of Module objects, get their settings and translations.'''  

        for mod, activated in self.modules.items():
            
            skip = False
            
            if not activated:
                for instance in self.module_instances:
                    # Remove existing instances of deactivated modules
                    if mod == os.path.basename(instance.__file__):
                        self.module_instances.remove(instance)
                continue
            
            for instance in self.module_instances:
                if mod == os.path.basename(instance.__file__):
                    skip = True

            if skip:
                continue

            print(f"Module \033[1m{mod}\033[0m initialization", end="")
            try:
                module = importlib.import_module('modules.' + mod.split('.')[0])
            except ModuleNotFoundError:
                print(" didn't quite succeed, because it does not exist ☹️")
                continue
            except Exception as e:
                print(" resulted in an error: {e}")
                continue
            else:
                word = random.choice(['quite', 'relatively', 'pretty', 'super'])
                print(f" was {word} successful ✔️")
            
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
            
            self.module_instances.append(module)

    
    def send(self, event=None):
        '''Start the message handler.'''
        
        self.GPT.update_attributes(self.settings)
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