from customtkinter import (CTk as Tk, CTkTextbox as Textbox, CTkEntry as Entry, CTkButton as Button, 
                           CTkScrollbar as Scrollbar, CTkCanvas as Canvas, CTkImage as ImageTk,
                           CTkLabel as Label, CTkOptionMenu as OptionMenu, CTkToplevel as Toplevel,
                           StringVar)
from tkinter import ttk

import customtkinter

class SettingsUI(Toplevel):
    def __init__(self, main_window, settings):
        customtkinter.deactivate_automatic_dpi_awareness()
        super().__init__(main_window)
        
        self.main_window = main_window

        self.title(f"Asetukset")
        self.settings = settings
        
        width = self.main_window.winfo_reqwidth() / 2
        height = self.main_window.winfo_reqheight() / 2

        self.minsize(width, height)

        
        self.grab_set()
        self.resizable(False, False)
        
        self.configure(background='#2C2C2C')
        
        self.CANVAS_COLOR = "#2C2C2C"
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.FONT = ('Helvetica', 14)
        self.FONT_BOLD = ('Helvetica', 14, 'bold')
        
        self.current_row = 0

        self.create_widgets()
        

    def center_window(self):
        '''Keskitetään asetusikkuna suhteessa pääikkunaan.'''

        main_width = self.main_window.winfo_reqwidth()
        main_height = self.main_window.winfo_reqheight()

        main_x = self.main_window.winfo_x()
        main_y = self.main_window.winfo_y()

        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        x = main_x + (main_width // 2) - (window_width // 2)
        y = main_y + (main_height // 2) - (window_height // 2)

        self.geometry(f'{window_width}x{window_height}+{x}+{y}')   

    
    def create_widgets(self):
        self.canvas = Canvas(
            self,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bd=0,
            # bg=self.CANVAS_COLOR,
            bg=self['bg'],
            highlightthickness=0,
        )
        self.canvas.pack(fill='both', padx=20, pady=20)
        self.scrollbar = Scrollbar(self.canvas)
    
    def add_main_config_widgets(self):
        pass

    
    def add_specific_config_widget(self):
        pass

    
    def set_selected_option(self, selection, module, config_name, options=dict):
        self.settings[module][config_name]['selected_option'] = selection
        
  
    def add_module_config_widgets(self):

        for module, configurations in self.settings.items():
            
            if module == 'MAIN':
                # Not a module, skip
                continue

            module_label = Label(
                self.canvas, 
                text=f"Moduuli: {module}",
                text_color='white',
                font=self.FONT_BOLD,
            )
            
            module_label.grid(row=self.current_row, column=0, sticky='w')
            separator = ttk.Separator(self.canvas, orient='horizontal')
            separator.grid(row=self.current_row+1, column=0, columnspan=2, sticky='ew', pady=(2,10))
            self.current_row += 2
            for cfg_name, cfg in configurations.items():
                
                if not cfg.get('interact_widget'):
                    # Interactable widget not defined, jump to next configuration 
                    continue

                
                cfg_label = Label(
                    self.canvas, 
                    text=cfg['label'],
                    font=self.FONT,
                    )
                cfg_label.grid(row=self.current_row, column=0, sticky='e', padx=(0,10))
               
                if cfg['interact_widget'] == 'OptionMenu': 
                 

                    list_of_options = []
                    
                    for value_name, value in cfg['options'].items():
                        list_of_options.append(value_name)
                   
                    menu = OptionMenu(
                        self.canvas,
                        values=list_of_options
                    )
          
                    if default := cfg['default_option']:
                        menu.set(default)
                    if selected := cfg['selected_option']:
                        menu.set(selected)

                    cmd = (
                        f"menu.configure( \
                            command=lambda selection: self.set_selected_option( \
                                selection, '{module}', '{cfg_name}', {cfg['options']} \
                            ) \
                        )" 
                    )

                    exec(cmd, locals())
                
                    menu.grid(row=self.current_row, column=1, sticky='ew')
                    
                self.current_row += 1
            
            Label(self.canvas, text="").grid(row=self.current_row, column=0)
            self.current_row += 1

        
        self.canvas.columnconfigure(0, weight=0)
        self.canvas.columnconfigure(1, weight=1)
        
        self.center_window()   
        




    '''
    Layout:

    MODUULIN NIMI
    -------------
    LABEL         WIDGET
                + OPTIONAALINEN WIDGET
                + OPTIONAALINEN WIDGET
    '''