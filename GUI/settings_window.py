from customtkinter import (CTk as Tk, CTkTextbox as Textbox, CTkEntry as Entry, CTkButton as Button, 
                           CTkScrollbar as Scrollbar, CTkCanvas as Canvas, CTkImage as ImageTk,
                           CTkLabel as Label, CTkOptionMenu as OptionMenu, CTkToplevel as Toplevel,
                           StringVar, CTkFrame as Frame, CTkComboBox as Combobox, CTkCheckBox as 
                           Checkbox)
from tkinter import ttk, filedialog 
from tkinter.font import Font
import customtkinter

from helpers import Helpers

class SettingsUI(Toplevel):

    def __init__(self, parent, settings):
        customtkinter.deactivate_automatic_dpi_awareness()
        customtkinter.set_appearance_mode("dark")
        super().__init__(parent.UI)
   
        self.main_window = parent.UI
        self.Tr = parent.Tr

        self.language = parent.language
        self.from_to = f"en-{self.language}"

        self.title(self.Tr.translate("Settings", self.from_to))
        
        self.settings = settings
        self.settings_copy = settings
        self.entry_widgets = {}
   
        width = self.main_window.winfo_reqwidth() / 1.25
        height = int(self.main_window.winfo_reqheight() / 1.5) 

        self.minsize(width, height)

        
        self.grab_set()
        self.resizable(False, False)
        
        self.configure(fg_color='#2C2C2C')

        self.CANVAS_COLOR = "#2C2C2C"
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height

        self.FONT = ('Helvetica', 14)
        self.FONT_BOLD = ('Helvetica', 14, 'bold')
        
        self.current_row = 0
        
        self.Help = Helpers(self)

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
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.pack(fill='both', padx=20, pady=20, expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.bind("<MouseWheel>", self.onMouseWheel)
        self.bind("<Configure>", self.onFrameConfigure)
    
    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
    
    
    def onFrameConfigure(self, event):
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
    def set_selected_value(
            self, widget=None, selection=None, module=None, config_name=None, options=None, function=None):
    
        value = None
        
        if function == 'filedialog':
            initial_dir = self.Help.get_selected_value(config_name, self.settings[module])[1]
            value = filedialog.askdirectory(initialdir=initial_dir)
   
        elif function == 'set_default':
            value = self.settings[module][config_name]['default_value']

        elif function == 'change_checkbox_state':
            cfg_name = widget.cget('text')
            state = widget.get()
            self.settings_copy[module][config_name]['options'][cfg_name] = state
        
        if widget and value:
            widget = widget[0]

            if isinstance(widget, Textbox) or isinstance(widget, Entry):
                widget.delete(0, 'end')
                widget.insert(0, value)
            else:
                try:
                    widget.configure(text=value)
                except ValueError:
                    print(f"Text change not supported (module: {module}, config: {config_name})")
        
        
        if options:
            try:
                value = self.settings[module][config_name]['options'][selection]
            except KeyError:
                value = self.settings_copy[module][config_name]['options'][selection]
        
        if value:
            self.settings_copy[module][config_name]['selected_value'] = value


    def add_entry_widget(self, kwargs) -> Entry:
        
        category = kwargs.get('category')
        cfg = kwargs.get('all_cfg') 
        module = kwargs.get('module')
        
        entry = Entry(
                self.frame,
            )
        
        option, value = self.Help.get_selected_value(category, cfg)
        
        if value:
            entry.insert(0, value)

        if cfg.get("interact_widget_disabled"):
            entry.configure(state='disabled')

        data = {
            entry: {
                'category': category,
                'module': module
            }
        }
        
        self.entry_widgets.update(data)

        return entry
    
    
    def add_checkbox(self, name, state, kwargs) -> Checkbox:
        
        category = kwargs.get('category')
        module = kwargs.get('module')
        function = 'change_checkbox_state'

        box = Checkbox(
            self.frame,
            text = name,
            )
        if state:
            box.select()
        
        cmd = (
            f"box.configure( \
                command=lambda: self.set_selected_value( \
                    box, None, '{module}', '{category}', None, function \
                ) \
            )" 
        )
        
        exec(cmd, locals())

        return box
    

    def add_button(self, kwargs) -> Button:
        cfg = kwargs.get('cfg')
        module = kwargs.get('module')
        
        previous_widget_obj = kwargs.get('widget_obj')

        if category := cfg.get('modify_value_of'):
            pass
        else:
            category = cfg.get('category')

        text = cfg.get('text')
        font = Font(family=self.FONT[0], size=self.FONT[1])
        function = cfg.get('function')

        string_width = font.measure(text)

        button = Button(
            self.frame,
            text=text,
            width=string_width+2
        )

        cmd = (
            f"button.configure( \
                command=lambda: self.set_selected_value( \
                    previous_widget_obj, None, '{module}', '{category}', None, function \
                ) \
            )" 
        )

        exec(cmd, locals())

        return button

    
    def add_option_widget(self, kwargs) -> object:
        
        
        widget = kwargs.get('widget')
        module = kwargs.get('module')
        cfg_to_use = kwargs.get('cfg_to_use')
        category = kwargs.get('category')
        cfg = kwargs.get('cfg')
        from_to = kwargs.get('from_to')
       
        
        list_of_values = []
        options = {}
        options_copy = {}
        selected_value = ""

        if cfg.get('options'):
            if type(cfg['options']) == list:
                # Options container is list, convert to dict
                for item in cfg['options']:
                    options_copy[item] = item
            elif type(cfg['options']) == dict:
                options_copy = cfg['options']
            else: 
                print(f"Options: {type(cfg['options']).__name__} type is not supported.")
                return None
            
        
        
        for key, value in options_copy.items():
            
            trans = self.Tr.translate(key, from_to, cfg_to_use)
            options[trans] = value

            try:
                self.settings_copy[module][category]['options'] = {}
            except KeyError:
                pass 

            if selected := cfg['selected_value']:
                pass
            elif selected := cfg['default_value']:
                pass
            if selected == value:
                selected_value = trans
 
        if options:
            self.settings_copy[module][category]['options'].update(options)

        for value_name in options.keys():
            list_of_values.append(value_name)
    
        if widget == 'OptionMenu':
            menu = OptionMenu(
                self.frame,
                values=list_of_values
            )
        if widget == 'Combobox':
            menu = Combobox(
                self.frame,
                values=list_of_values
            )
        
        if selected_value:
            menu.set(selected_value)

        cmd = (
            f"menu.configure( \
                command=lambda selection: self.set_selected_value( \
                    None, selection, '{module}', '{category}', {options} \
                ) \
            )" 
        )

        exec(cmd, locals())

        if cfg.get("interact_widget_disabled"):
            menu.configure(state='disabled')

        return menu
    
    def add_widget(self, kwargs) -> object:
        widget = kwargs.get('widget')
        cfg = kwargs.get('cfg')
        column = kwargs.get('column')
        add_row = kwargs.get('add_row')
        sticky = kwargs.get('sticky')
        widget_obj = None
        

        if widget == 'OptionMenu' or widget == 'Combobox': 
            widget_obj = self.add_option_widget(kwargs)
                
        elif widget == "Entry":
            widget_obj = self.add_entry_widget(kwargs)

        elif widget == "Button":
            widget_obj = self.add_button(kwargs)

        elif widget == "Checkbox":
            
            for name, state in cfg['options'].items():
                self.add_checkbox(name, state, kwargs).grid(row=self.current_row, column=column, sticky=sticky)
                if add_row:
                    self.current_row += 1 
                

        if widget_obj and widget != "Checkbox":
            widget_obj.grid(row=self.current_row, column=column, sticky='ew')
            if add_row:
                self.current_row += 1
            return widget_obj
        else:
            return None
  
    def add_config_widgets(self):

        for module, configurations in self.settings.items():
            
            self.settings_copy[module] = configurations
            
            if module == 'MAIN':
                label_text = f"{self.Tr.translate('Main Settings', self.from_to)}"
            else:
                label_text = f"{self.Tr.translate('Module', self.from_to)}: {module}"

            # Create category label
            module_label = Label(
                self.frame, 
                text=label_text,
                text_color='white',
                font=self.FONT_BOLD,
            )
            
            module_label.grid(row=self.current_row, column=0, sticky='w')
            separator = ttk.Separator(self.frame, orient='horizontal')
            separator.grid(row=self.current_row+1, column=0, columnspan=2, sticky='ew', pady=(2,10))
            self.current_row += 2
            
            for cfg_name, cfg in configurations.items():
                
                if widget := cfg.get('interact_widget'):
                    pass
                else:
                    # Interactable widget not defined, jump to next configuration 
                    continue

                if cfg_name == 'language':
                    cfg_to_use = 'MAIN'
                else:
                    cfg_to_use = module

                # Set dictionary to be used according to default and selected language 
                if l := self.settings[cfg_to_use].get('language'):
                    from_to = f"{l['default_value']}-{self.language}"
                else:
                    from_to = self.from_to

                # Create label widget for the configuration
                cfg_label = Label(
                    self.frame, 
                    text=self.Tr.translate(cfg['label'], from_to, cfg_to_use),
                    font=self.FONT,
                    )
                
                cfg_label.grid(row=self.current_row, column=0, sticky='e', padx=(0,10))
             
                kwargs = {
                    'widget': widget,
                    'module': module, 
                    'cfg_to_use': cfg_to_use, 
                    'category': cfg_name, 
                    'all_cfg': configurations,
                    'cfg': cfg,
                    'from_to': from_to,
                    'column': 1,
                    'sticky': 'ew',
                    'add_row': cfg.get('extra_widget') == None,
                }
                widget_obj = self.add_widget(kwargs)
                                              
                if extra := cfg.get('extra_widget'):
                    if widget := extra.get('interact_widget'):
                        kwargs['cfg'] = extra
                        kwargs['widget'] = widget
                        kwargs['column'] = 2
                        kwargs['add_row'] = True
                        kwargs['sticky'] = 'w'
                        kwargs['widget_obj'] = widget_obj,
                        self.add_widget(kwargs)
                     

                self.current_row += 1
            
            Label(self.frame, text="").grid(row=self.current_row, column=0)
            self.current_row += 1

        self.canvas.columnconfigure(0, weight=0)
        self.canvas.columnconfigure(1, weight=1)
        
        self.center_window()   