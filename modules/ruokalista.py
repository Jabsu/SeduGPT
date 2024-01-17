import importlib
import re
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

# placeholder (testailuun)
try:
    import config
    campus = config.CAMPUS
except ModuleNotFoundError:
    campus = "https://sedu.fi/kampus/sedu-seinajoki-suupohjantie/"

class Main:

    def __init__(self, msg=None):

        self.msg = msg
        
        # Regex-triggeri -> funktio
        self.triggers = {
            "r(uu|uo)aksi|ruoka|murkina|syödään|syötiin|syömme|safka|pöperö": "start",
        }

        # Regex-flagit (re.I = ignore case, re.NOFLAG = ei flageja)
        self.re_flags = re.I

        # Moduulin tiedostonimi
        self.name = self.get_module_name()


        self.settings_UI_configs()

    def settings_UI_configs(self):
        '''Määritetään asetusikkunaan lisättävät widgetit ja asetukset.'''

        self.settings = {
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
            }
        }

   

  
    def set_return_data(self, value, title=False):
        '''Asetetaan palautettava output.'''
        
        self.return_value = value

        # Muutetaanko mahdollinen lista stringiksi
        self.return_sanitize = True

        # Merkki, jolla listan arvot erotellaan ('\n' = rivinvaihto) 
        self.return_separator = '\n'

        # Optionaalinen otsikko (False = ei otsikkoa)
        self.message_title = title
        
        
    def check_triggers(self, msg):
        '''Tutkitaan, sisältääkö käyttäjän viesti __initissä__ asetettuja triggereitä ja 
        palautetaan asiaankuuluva funktio.'''
        
        self.msg = msg
        

        for trigger, func in self.triggers.items():
            if re.findall(trigger, self.msg, self.re_flags):
                
                return func

        return None
    
    def get_module_name(self):
        '''Logging/debug: Selvitetään moduulin tiedostonimi.'''
        
        module = importlib.import_module(self.__module__)
        return os.path.basename(module.__file__)
    
    
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
        
        self.get_menus()
        self.get_todays_menu()

    def get_emoji(self, food):
        '''Lisätään murkinalajille sopiva emoji (yksi tai useampi).'''
        
        default_emoji = '😋'
        patterns = {
            'keitto': '🥣',
            'salaatti': '🥬',
            'kasvi|parsakaal|kaali': '🥦',
            'lohi|kala|lohta': '🐟',
            'liha|härkää': '🍖',
            'broiler|kana': '🍗',
            'peruna|perunoi': '🥔'
        }
        prefix = ''
        for pattern, emoji in patterns.items():

            if re.findall(pattern, food, re.I):
                prefix += emoji

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

            print(f"{self.__class__.__name__}: Viikonpäivää ei saatu selvitettyä.")

        return ret     
    
    def get_menus(self):
        '''Haetaan ruokalistat.'''

        r = requests.get(campus)
        soup = bs(r.content, "html.parser")
        menu_data = soup.find("div", id="ruokalista")
    
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

        self.menus = menus

    
    def get_todays_menu(self):
        '''Haetaan valitun tai (oletuksena) kuluvan päivän ruokalista.'''

        self.menu = []
        
        for day, menu in self.menus.items():
            parsed = day.split(" ")[0]
            
            if parsed.lower() == self.weekday.lower():
                for item in menu:
                    if re.findall(self.ignore_entries, item, re.I):
                        continue
                    emoji = self.get_emoji(item)
                    self.menu.append(f"{emoji} {item}")

        # Määritellään palautettava data
        self.set_return_data(self.menu, title=f'\n{self.weekday.title()}n ruokalista:\n\n')
        

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
