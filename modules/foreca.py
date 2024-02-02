import requests
import re

from bs4 import BeautifulSoup as bs 

from helpers import Helpers



class Module:
    '''Obligatory weather inquiries. WORK IN PROGRESS; no functionality at the moment.'''

    def __init__(self):
        
        self.triggers = {
            "(^| )sää( |$)": "start",
            "weather": "start",
        }
        self.re_flags = re.I

    def get_settings(self):
        settings = {
            "station": {
                "label": "Havaintoasema",
                "interact_widget": "OptionMenu",
                "options": {
                    "Seinäjoki": "100637219",
                },
                "default_option": "Seinäjoki",
                "selected_option": "",
            },
            "language": {
                "label": "Kieli",
                "interact_widget": "OptionMenu",
                "options": {
                    "Englanti": "en",
                    "Suomi": "fi",
                },
                "default_option": "Suomi",
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
                "default_option": "°C, m/s",
                "selected_option": "",
            }
        }
 
        return settings
    
    
    def check_triggers(self, msg, user_defined_settings=None):
        '''If triggered by user message, return the specified function.'''
        
        self.msg = msg
        self.settings, func = Helpers(self).check_triggers(user_defined_settings)
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
