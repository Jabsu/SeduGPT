import requests
import re
from datetime import datetime

from bs4 import BeautifulSoup as bs

import config

class Food:

    def __init__(self, day=None):

        if not day:
            self.get_day()
        else:
            self.weekday = day

    def get_emoji(self, food):
        '''Lisätään murkinalajille sopiva emoji.'''
        
        default_emoji = '😋'
        patterns = {
            'keitto': '🥣',
            'salaatti': '🥬',
            'kasvi': '🥦',
            'lohi|kala|lohta': '🐟',
            'liha': '🍖',
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
            
        for en, fi in conversions.items():
            if weekday.lower() == en.lower():
                self.weekday = fi
                break     
    
    def get_menu(self):
        '''Haetaan ruokalistat.'''

        r = requests.get(config.campus)
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
        
        for day, menu in self.menus.items():
            parsed = day.split(" ")[0]
            
            if parsed.lower() == self.weekday.lower():
                for item in menu:
                    emoji = self.get_emoji(item)
                    print(f"{emoji} {item}\n")
        


if __name__ == "__main__":
    ruoka = Food()
    ruoka.get_menu()
    ruoka.get_todays_menu()
