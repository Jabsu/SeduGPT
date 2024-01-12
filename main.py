import sys
import random
import importlib

from tkinter import *

from GUI.main_window import UI
import config

# Ladataan moduulit
for mod in config.MODULES:
    importlib.import_module(mod)


class Main:
    def __init__(self, args):
        
        self.args = args

        self.initialize_modules()
        
        if args == '--gui':
            # GUI
            self.UI = UI()
            self.UI.send_button.config(command=lambda: self.send())
            self.UI.bind('<Return>', lambda event=None: self.send())
        
            self.UI.mainloop()

        elif args == '--debug':
            # gudeb
            pass

        elif args:
            # Testiviesti (parametri)
            self.msg = args
            self.iterate_module_triggers()

            

    '''
    def create_list_of_modules(self):
        
        self.module_list = []

        for lib in sys.modules.keys():
            if lib.startswith('modules.'):
                self.module_list.append(lib)
    '''

    def initialize_modules(self):
        
        # self.modules = {}
        self.modules = []

        for mod in config.MODULES:
            module = importlib.import_module(mod)
            # module_main_class = getattr(module, 'Main')
            # self.modules[module] = module_main_class
            self.modules.append(module)

    
    def iterate_module_triggers(self):
        for module in self.modules:
            self.current_mod = module.Main()

            triggered = False
            
            # Moduuli palauttaa spesifin funktion, mikäli viestistä löytyy triggerivastaavuus 
            if module_func := self.current_mod.check_triggers(self.msg):
                
                triggered = True
                
                # Käynnistetään triggerin asettama funktio
                func = getattr(self.current_mod, module_func)
                func()
                
                # Botin output
                self.bot_output(True)

        if not triggered:
            # Ei triggeriä, botti oksentaa default-tekstin
            self.bot_output(False)

    
    def send(self, event=None):
        '''Käsitellään GUI:ssa lähetetty viesti.'''
        
        self.msg = self.UI.entry.get()
        
        if not self.msg:
            return
        
        self.UI.entry.delete(0, END)
        
        # Placeholder-formatointi (funktio näille myöhemmin)
        formatted_msg = f"{self.UI.USER_PREFIX}{self.UI.USERNAME}{self.UI.USER_SUFFIX}{self.UI.SEPARATOR}{self.msg}\n" 
        self.UI.txt.insert('end', '\n' + formatted_msg)
        
        # Tarkistetaan, triggeröikö viesti jonkin moduulin
        self.iterate_module_triggers()


    def sanitize(self, content):
        '''Muutetaan listat ja dictionaryt stringeiksi.'''

        ret = content

        if type(content) == list:
            # Käytetään moduulin määrittelemää separaattoria listan arvoja yhdistäessä
            ret = self.current_mod.return_separator.join(content)

        if type(content) == dict:
            pass

        return ret
    
    def random_output(self):
        outputs = [
            'Opettelen vielä, ymmärrän kohta.',
            'Pahus, menin ihan solmuun.',
            'Pahoittelen, opettelen parhaillaan ymmärtämään toista asiaa.',
            'Ymmärrän kyllä yskäsi, mutta en juuri muuta.',
        ]
        
        return random.choice(outputs)
            
    def bot_output(self, triggered_by_module=False):
        '''Botti oksentaa tekstiwidgettiin.'''
        
        if not triggered_by_module:
            bot_msg = self.random_output()
        else:
            bot_msg = self.current_mod.return_value
            
            # Jos moduulin palauttama arvo ei ole string ja sanitize = True, muutetaan arvo stringiksi
            if type(bot_msg) != 'str' and self.current_mod.return_sanitize:
                bot_msg = self.sanitize(bot_msg)

        
        if self.args != "--gui":
            # Mikäli GUI ei käytössä, käytetään moduulin print-funktiota (placeholder)
            self.current_mod.print()
        else:
            # Placeholder-formatointi (funktio näille myöhemmin)
            formatted_msg =  f"{self.UI.USER_PREFIX}{self.UI.BOT_NAME}{self.UI.USER_SUFFIX}{self.UI.SEPARATOR}{bot_msg}\n"
            self.UI.txt.insert('end', '\n' + formatted_msg)




if __name__ == '__main__':
    
    # Oletusparametri (--gui = lataa pääikkunan)
    args = '--gui'

    if len(sys.argv) > 1:
        args = ' '.join(sys.argv[1:])
    
    Main(args)