from customtkinter import (CTk as Tk, CTkTextbox as Textbox, CTkEntry as Entry, CTkButton as Button, 
                           CTkScrollbar as Scrollbar, CTkCanvas as Canvas, CTkImage as ImageTk,
                           CTkLabel as Label, CTkOptionMenu as OptionMenu, CTkToplevel as Toplevel,
                           StringVar)
from tkinter import ttk
import customtkinter



class SettingsUI(Toplevel):

    def __init__(self, parent, settings):
        customtkinter.deactivate_automatic_dpi_awareness()
        super().__init__(parent.UI)

        
        self.main_window = parent.UI
        self.Tr = parent.Tr

        self.language = parent.language
        self.from_to = f"en-{self.language}"

        self.title(self.Tr.translate("Settings", self.from_to))
        
        self.settings = settings
        self.settings_copy = settings
   
        width = self.main_window.winfo_reqwidth() / 2
        height = int(self.main_window.winfo_reqheight() / 1.25) 

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
    
    
    def add_specific_config_widget(self):
        pass

    
    def set_selected_option(self, selection, module, config_name, options=dict):
        
        try:
            value = self.settings[module][config_name]['options'][selection]
        except KeyError:
            value = self.settings_copy[module][config_name]['options'][selection]
        
        self.settings[module][config_name]['selected_option'] = value
        
  
    def add_config_widgets(self):

        for module, configurations in self.settings.items():
            
            self.settings_copy[module] = configurations
            
            if module == 'MAIN':
                label_text = f"{self.Tr.translate('Main Settings', self.from_to)}"
            else:
                label_text = f"{self.Tr.translate('Module', self.from_to)}: {module}"

            module_label = Label(
                self.canvas, 
                text=label_text,
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

                if cfg_name == 'language':
                    mod = 'MAIN'
                else:
                    mod = module

                cfg_label = Label(
                    self.canvas, 
                    text=self.Tr.translate(cfg['label'], self.from_to, mod),
                    font=self.FONT,
                    )
                cfg_label.grid(row=self.current_row, column=0, sticky='e', padx=(0,10))
               
                if cfg['interact_widget'] == 'OptionMenu': 
                 

                    list_of_options = []
                    options = {}
                    selected_option = ""

                    for key, value in cfg['options'].items():
                        
                        
                        trans = self.Tr.translate(key, self.from_to, mod)
                        options[trans] = value

                        try:
                            self.settings_copy[module][cfg_name]['options'] = {}
                        except KeyError:
                            pass
                        
                        

                        if selected := cfg['selected_option']:
                            pass
                        elif selected := cfg['default_option']:
                            pass
                        if selected == value:
                            selected_option = trans
                    
                    self.settings_copy[module][cfg_name]['options'].update(options)

                    for value_name in options.keys():
                        list_of_options.append(value_name)
                   
                    menu = OptionMenu(
                        self.canvas,
                        values=list_of_options
                    )
                
                    if selected_option:
                        menu.set(selected_option)

                    cmd = (
                        f"menu.configure( \
                            command=lambda selection: self.set_selected_option( \
                                selection, '{module}', '{cfg_name}', {options} \
                            ) \
                        )" 
                    )

                    exec(cmd, locals())

                    if cfg.get("interact_widget_disabled"):
                        menu.configure(state='disabled')
                
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