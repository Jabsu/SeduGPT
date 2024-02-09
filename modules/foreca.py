import requests
import re

from bs4 import BeautifulSoup as bs 

from helpers import Helpers



class Module:
    '''Obligatory weather inquiries. WORK IN PROGRESS; no functionality at the moment.'''

    def __init__(self, parent):
        
        # Initialize Helpers class
        self.Help = Helpers(self)
        
        # Default settings
        self.defaults = self.get_defaults()
        
        self.triggers = {
            "(^| )sää( |$)": "start",
            "weather": "start",
        }
        self.re_flags = re.I

        # Module file name
        self.module_name = self.Help.get_module_name()

        # Get module settings from parent class
        if cfg := parent.settings.get(self.module_name):
            self.settings = cfg
        else:
            self.settings = self.defaults

        # Translations dictionary (optional)
        self.translations = {
            "fi-en": {
                "Havaintoasema": "Observation station",
                "Yksiköt": "Units"
            }
        }
        

    def get_defaults(self):
        '''Return UI and/or other settings.'''
        
        settings = {
            "station": {
                "label": "Havaintoasema",
                "interact_widget": "OptionMenu",
                "options": {
                    "Seinäjoki": "100637219",
                },
                "default_option": "100637219",
                "selected_option": "",
            },
            "language": {
                "label": "Language",
                "interact_widget": "OptionMenu",
                "interact_widget_disabled": True,
                "sync_with_main": False,
                "options": {
                    'English': 'en',
                    'Finnish': 'fi',
                },
                "default_option": "fi",
                "selected_option": "",
            },
            "units": {
                "label": "Yksiköt",
                "interact_widget": "OptionMenu",
                "options": {
                    "°C, m/s": "metric",
                    "°C, kmh": "metrickmh",
                    "°C, kn": "metricknots",
                    "°F, mph": "us",
                    "°C, mph": "imperial"
                },
                "default_option": "metric",
                "selected_option": "",
            }
        }

        return settings

    
    def check_triggers(self, msg, user_defined_settings=None):
        '''If triggered by user message, return the specified function.'''
        
        self.msg = msg
        self.settings, func = self.Help.check_triggers(user_defined_settings)
        return func
    

    def get_module_name(self):
        '''Get the module filename.'''
        
        return Helpers(self).get_module_name()
    

    def start(self):
        url_prefix = "https://foreca.mobi/spot.php?l="

        if selected := self.settings['station']['selected_option']:
            station_number = self.settings['station']['options'][selected]
        else:
            default = self.settings['station']['default_option'] 
            station_number = self.settings['station']['options'][default]

        self.url = f"{url_prefix}{station_number}"
        self.get_weather()

    
    def get_weather(self):
        r = requests.get(self.url)
        soup = bs(r.content, 'html.parser')
        # &lang=fi&units=metric&time=24h


    def start(self):
        pass    
