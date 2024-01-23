import importlib
import re
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

from .helpers import Helpers



class Main:

    def __init__(self):
        
        # Regex-triggeri -> funktio
        self.triggers = {
            "r(uu|uo)aksi|ruoka|murkina|syödään|syötiin|syömme|safka|pöperö": "start",
        }

        # Regex-flagit (re.I = ignore case, re.NOFLAG = ei flageja)
        self.re_flags = re.I


    def get_settings(self):
        '''Määritetään asetusikkunaan lisättävät widgetit ja asetukset.'''

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
        '''Asetetaan palautettava output.'''
        
        self.return_value = value

        # Muutetaanko mahdollinen lista stringiksi
        self.return_sanitize = True

        # Jos edeltävään kyllä: merkki, jolla listan arvot erotellaan ('\n' = rivinvaihto) 
        self.return_separator = '\n'

        # Optionaalinen otsikko (False = ei otsikkoa)
        self.message_title = title
        
        
    def check_triggers(self, msg, user_defined_settings=None):
        '''Tutkitaan (Helpers-classin funktiota hyödyntäen), sisältääkö käyttäjän viesti moduulissa 
        asetettuja triggereitä ja palautetaan asiaankuuluva funktio.'''
        
        self.msg = msg
        self.settings, func = Helpers(self).check_triggers(user_defined_settings)
        return func
    
    def get_module_name(self):
        '''Selvitetään moduulin tiedostonimi.'''
        
        return Helpers(self).get_module_name()
       
    
    
    def start(self):
        '''Moduuli tekee tehtävänsä.'''

        # Jäteen huomioimatta tietyt erikoisuudet ruokalistassa
        self.ignore_entries = 'opiskeli|opetus'


        pattern = "maanantai|tiistai|keskiviikko|torstai|perjantai|lauantai|sunnuntai"
        
        # Tarkistetaan, sisältääkö käyttäjän viesti viikonpäivämaininnan
        if match := re.findall(pattern, self.msg, re.I):
            self.weekday = match[0]
        else:
            self.weekday = self.get_day()
        
        if hasattr(self, 'menus') and hasattr(self, 'campus'):
            if self.menus.get(self.campus):
                # Valitun kampuksen menu muistissa, haetaan spesifin päivän menu
                self.get_specific_menu()
        else:
            # Valitun kampuksen menu ei muistissa, KAAVITAAN* kampuksen verkkosivua
            #  * scraping; tietoteknisen sanaston suomentaminen on toisinaan hauska haaste
            if self.get_menus():
                self.get_specific_menu()
        
            

    
    def get_emoji(self, food):
        '''Lisätään murkinalajille sopiva emoji.'''
        
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
        '''Selvitetään viikonpäivä ja konvertoidaan se selvälle suomen kielelle.'''

        conversions = {
            'Monday': 'Maanantai',
            'Tuesday': 'Tiistai',
            'Wednesday': 'Keskiviikko',
            'Thursday': 'Torstai',
            'Friday': 'Perjantai',
            'Saturday': 'Lauantai',
            'Sunday': 'Sunnuntai'
        }
        weekday = datetime.now().strftime("%A")
            
        ret = None
        for weekday_en, weekday_fi in conversions.items():
            if weekday.lower() == weekday_en.lower():
                ret = weekday_fi
                break

        if not ret:
            # Note-to-self: ota logging käyttöön

            print(f"{self.get_module_name()}: Viikonpäivää ei saatu selvitettyä.")

        return ret     
    
    def get_menus(self):
        '''Haetaan ruokalistat.'''

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
        '''Haetaan valitun tai kuluvan päivän ruokalista.'''

        self.menu = []
        
        for day, menu in self.menus[self.campus].items():
            parsed = day.split(" ")[0]
            
            if parsed.lower() == self.weekday.lower():
                for item in menu:
                    if re.findall(self.ignore_entries, item, re.I):
                        continue
                    
                    # Erikoistapaus: kasvisruokavaihtoehto samalla rivillä (separaattorina /)
                    for i in item.split('/'):
                        emoji = self.get_emoji(i)
                        self.menu.append(f"{emoji} {i.lstrip().rstrip()}")
                    
                    

        # Määritellään palautettava data
        if self.menu:
            self.set_return_data(self.menu, title=f'\n{self.weekday.title()}n ruokalista:\n\n')
        else:
            # Päivän menu hukassa
            self.set_return_data("Luvassa saattaa olla laihaa keittoa.")
        

    def print(self):
        '''Terminaalinen ulostus. Placeholder.'''

        for item in self.menu:
            print(item)
        

# Testailu
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
