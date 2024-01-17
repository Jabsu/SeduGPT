from customtkinter import (CTk as Tk, CTkTextbox as Textbox, CTkEntry as Entry, CTkButton as Button, 
                           CTkScrollbar as Scrollbar, CTkCanvas as Canvas, CTkImage as ImageTk,
                           CTkLabel as Label, CTkOptionMenu as OptionMenu)
from tkinter import ttk

import customtkinter

class SettingsUI(Tk):
    def __init__(self, master=None):
        customtkinter.deactivate_automatic_dpi_awareness()
        self.master = Tk.__init__(self, master)

        self.title(f"Asetukset")

        self.configurations = {}

        width = self.winfo_screenwidth() / 2
        height = self.winfo_screenheight() / 2
        
        self.CANVAS_COLOR = "#2C2C2C"
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.FONT = ('Helvetica', 14)
        self.FONT_BOLD = ('Helvetica', 14, 'bold')
        
        self.current_row = 0

        
        self.create_widgets()
      

    def create_widgets(self):
        self.canvas = Canvas(
            self,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bd=0,
            bg=self.CANVAS_COLOR,
            highlightthickness=0,
        )
        self.canvas.grid(row=1, column=0, padx=20, pady=20)
        self.scrollbar = Scrollbar(self.canvas)
    
    def add_main_config_widgets(self, settings):
        pass

    
    def add_specific_config_widget(self):
        pass

    
    def change_value(self, selection, module, config_name, options=dict):
        value = options[selection]
        self.settings[module][config_name]['selected'] = value
        
  
    def add_module_config_widgets(self, settings):
        
        self.settings = settings

        for module, configurations in settings.items():
            label = Label(
                self.canvas, 
                text=f"Moduuli: {module}",
                text_color='white',
                font=self.FONT_BOLD,
            )
            label.grid(row=self.current_row, column=0)
            separator = ttk.Separator(self.canvas, orient='horizontal')
            separator.grid(row=self.current_row+1, column=0, columnspan=2, sticky='ew')
            self.current_row += 2
            for cfg_name, cfg in configurations.items():
                label = Label(
                    self.canvas, 
                    text=cfg['label'],
                    font=self.FONT,
                    )
                label.grid(row=self.current_row, column=0)
               
                if cfg['interact_widget'] == 'OptionMenu': 
                 

                    list_of_options = []
                    
                    for value_name, value in cfg['options'].items():
                        list_of_options.append(value_name)
                   

                    menu = OptionMenu(
                        self.canvas, 
                        values=list_of_options,
                        command=lambda selection: self.change_value(
                            selection, module, cfg_name, cfg['options']),
                        
                    )
                    
                    if default := cfg['default_option']:
                        menu.set(default)           
                
                    menu.grid(row=self.current_row, column=1)
                
                self.current_row += 1
            
            Label(self.canvas, text="").grid(row=self.current_row, column=0)
            self.current_row += 1

        




    '''
    Layout:

    MODUULIN NIMI
    -------------
    LABEL         WIDGET
                + OPTIONAALINEN WIDGET
                + OPTIONAALINEN WIDGET
    '''