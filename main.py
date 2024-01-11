import sys
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
            inited_mod = module.Main()
            if module_func := inited_mod.check_triggers(self.msg):
                
                # Käynnistetään triggerin asettama funktio
                func = getattr(inited_mod, module_func)
                func()
                inited_mod.print()

    def send(self, event=None):
        '''Käsitellään lähetetty viesti.'''
        
        self.msg = self.UI.entry.get().lower()
        
        if not self.msg:
            return
        
        self.iterate_module_triggers()
        
        return

        send = f"{self.UI.USERNAME} {self.UI.SEPARATOR} " + self.UI.entry.get()
        self.UI.txt.insert(END, "\n" + send)
    
        user_msg = self.UI.entry.get().lower()
    
        if user_msg == "testi":
            self.UI.txt.insert(END, "\n" + f"{self.UI.BOT_NAME} {self.UI.SEPARATOR} Toimii.")

        else:
            self.UI.txt.insert(END, "\n" + f"{self.UI.BOT_NAME} {self.UI.SEPARATOR} Pahoittelen, mutta ymmärrykseni on rajallinen.")
        self.UI.entry.delete(0, END)

if __name__ == '__main__':
    
    # Oletusparametri (--gui = lataa pääikkunan)
    args = '--gui'

    if len(sys.argv) > 1:
        args = ' '.join(sys.argv[1:])
    
    Main(args)