import importlib
import re
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

from .helpers import Helpers



class Main:

    def __init__(self):
        
        # Regex trigger -> function
        self.triggers = {
            "r(uu|uo)aksi|ruoka|murkina|syödään|syötiin|syömme|safka|pöperö|sapuska": "start",
        }

        # Regex flags (re.I = ignore case, re.NOFLAG = no flags)
        self.re_flags = re.I


    def get_settings(self):
        '''Default settings, widgets and labels to be shown on settings window.'''

        settings = {
            "campus": {
                "label": "Kampus",
                "interact_widget": "OptionMenu",
                "options": {
                   "Sedu Ilmajoki":
                        "https://sedu.fi/kampus/sedu-ilmajoki-ilmajoentie/",
                    "Sedu Kurikka": 
                        "https://sedu.fi/kampus/sedu-kurikka/",
                    "Sedu Lappajärvi":
                        "https://sedu.fi/kampus/lappajarvi/",
                    "Sedu Lapua":
                        "https://sedu.fi/kampus/sedu-lapua/",
                    "Sedu Seinäjoki, Rastaantaival":
                        "https://sedu.fi/kampus/sedu-seinajoki-rastaantaival/",
                    "Sedu Seinäjoki, Suupohjantie": 
                        "https://sedu.fi/kampus/sedu-seinajoki-suupohjantie/",    
                    "Sedu Seinäjoki, Törnäväntie":
                        "https://sedu.fi/kampus/sedu-seinajoki-tornavantie/",
                    "Sedu Vaasa":
                        "https://sedu.fi/kampus/sedu-vaasa-runsorintie/",
                    "Sedu Ähtäri, Koulutie":
                        "https://sedu.fi/kampus/sedu-ahtari-koulutie/",
                    "Sedu Ähtäri, Tuomarniementie":
                        "https://sedu.fi/kampus/sedu-ahtari-tuomarniementie/",
                },
                "default_option": "Sedu Seinäjoki, Suupohjantie",
                "selected_option": "",
            }
        }
        return settings
   
  
    def set_return_data(self, value, title=False):
        '''Preparing the output for Textbox.'''
        
        self.return_value = value

        # If the output is a list, will it be converted to a string?
        self.return_sanitize = True

        # If True in above: separator character for list values ('\n' = enter) 
        self.return_separator = '\n'

        # Optional title (False = no title)
        self.message_title = title
        
        
    def check_triggers(self, msg, user_defined_settings=None):
        '''If triggered by user message, return the specified function.'''
        
        self.msg = msg
        self.settings, func = Helpers(self).check_triggers(user_defined_settings)
        return func
    
    def get_module_name(self):
        '''Get the module filename.'''
        
        return Helpers(self).get_module_name()
       
    
    
    def start(self):
        '''The module does it job.'''

        # Ignore non-food related listings
        self.ignore_entries = 'opiskeli|opetus'


        pattern = "maanantai|tiistai|keskiviikko|torstai|perjantai|lauantai|sunnuntai"
        
        # Set the day of week to today or the one used as a parameter 
        if match := re.findall(pattern, self.msg, re.I):
            self.weekday = match[0]
        else:
            self.weekday = self.get_day()
        
        if hasattr(self, 'menus') and hasattr(self, 'campus'):
            if self.menus.get(self.campus):
                # Campus' menu is stored in memory; retrieve the menu for a specific day  
                self.get_specific_menu()
        else:
            # Campus' menu is not stored in memory; scrape the web page and retrieve the menu
            if self.get_menus():
                self.get_specific_menu()
        
            

    
    def get_emoji(self, food):
        '''Add a corresponding emoji for certain food categories.'''
        
        default_emoji = '😋'
        patterns = {
            'keitto': '🥣',
            'salaatti': '🥬',
            'kasvi|parsakaal|kaali': '🥦',
            'lohi|kala|lohta': '🐟',
            'liha|härkää': '🍖',
            'broiler|^kana': '🍗',
            'peruna|perunoi': '🥔'
        }
        prefix = ''
        for pattern, emoji in patterns.items():

            if re.findall(pattern, food, re.I):
                if not prefix:
                    prefix = emoji

        if not prefix:
            prefix = default_emoji
        
        return prefix


    def get_day(self):
        '''Return the current day of week in Finnish.'''

        weekdays = {
            '1': 'Maanantai',
            '2': 'Tiistai',
            '3': 'Keskiviikko',
            '4': 'Torstai',
            '5': 'Perjantai',
            '6': 'Lauantai',
            '7': 'Sunnuntai'
        }
        weekday = datetime.now().strftime("%w")
        return weekdays[weekday]
            
     
    def get_menus(self):
        '''Get the menu for the week from a specified campus.'''

        if selected := self.settings['campus']['selected_option']:
            campus = self.settings['campus']['options'][selected]
        else:
            default = self.settings['campus']['default_option'] 
            campus = self.settings['campus']['options'][default]

        self.campus = campus    
        
        r = requests.get(campus)
        soup = bs(r.content, "html.parser")
        menu_data = soup.find("div", id="ruokalista")

        if not menu_data:
             self.set_return_data(
                 f'Valitun kampuksen ruokalista ei ole saatavilla. Kuinkas nyt suu pannaan?')
             return

    
        menus = {}

        day = None
   
            

        for entry in menu_data.find_all('p'):
        
            if day:
                if not entry.find("strong"):
                    if entry.get_text():
                        menu.append(entry.get_text())
                        menus[day] = menu
                
        
            if entry.find("strong"):
                day = entry.get_text().replace("  ", " ")
                menu = []
                menus[day] = menu

        self.menus = {self.campus: menus}
        return True


    def get_specific_menu(self):
        '''Gets the menu for today or the day specified by the user.'''

        self.menu = []
        
        for day, menu in self.menus[self.campus].items():
            parsed = day.split(" ")[0]
            
            if parsed.lower() == self.weekday.lower():
                for item in menu:
                    if re.findall(self.ignore_entries, item, re.I):
                        continue
                    
                    # Special case for irregular formatting: Make vegetarian option as a separate 
                    # list item if it's listed on the same line as the non-vegetarian option 
                    # (and separated with '/')
                    for i in item.split('/'):
                        emoji = self.get_emoji(i)
                        self.menu.append(f"{emoji} {i.lstrip().rstrip()}")
                    
                    

        # Make return data configurations
        if self.menu:
            self.set_return_data(self.menu, title=f'\n{self.weekday.title()}n ruokalista:\n\n')
        else:
            # No menu found
            self.set_return_data("Luvassa saattaa olla laihaa keittoa.")
        

    def print(self):
        '''Terminaalinen ulostus. Placeholder.'''

        for item in self.menu:
            print(item)
        

# For testing
if __name__ == "__main__":
    import sys
    
    msg = "ruoka"
    if len(sys.argv) > 1:
        msg = ' '.join(sys.argv[1:])

    ruoka = Main()
    
    if func := ruoka.check_triggers(msg):
        trigger_function = getattr(ruoka, func)
        trigger_function()
        ruoka.print()
