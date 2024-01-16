# from tkinter import Menu

from customtkinter import (CTk as Tk, CTkTextbox as Textbox, CTkEntry as Entry, CTkButton as Button, 
                           CTkScrollbar as Scrollbar, CTkCanvas as Canvas, CTkImage as ImageTk)

from PIL import Image, ImageDraw, ImageFont


class UI(Tk):
    def __init__(self, master=None):
        self.master = Tk.__init__(self, master)
        
        self.title(f"SeduGPT")

        # customtkinter.set_widget_scaling(1.0)
        
        width = self.winfo_screenwidth() / 2
        height = self.winfo_screenheight() / 2
        
        # self.geometry(f"{width/2}x{height/2}")
        self.resizable(False, False)

        self.CANVAS_COLOR = "#2C2C2C"
        self.CANVAS_WIDTH = width
        self.CANVAS_HEIGHT = height
        
        self.BG_GRAY = "#ABB2B9"
        self.BG_COLOR = "#17202A"
        self.TEXT_COLOR = "#EAECEE"
        
        self.TEXTBOX_FG = "#2C2C2C"
        self.TEXTBOX_TEXT_COLOR = "#FFFFFF"
        
        self.ENTRY_FG = "#FFFFFF"
        self.ENTRY_TEXT_COLOR = "#000000"

        self.FONT = ('Consolas', 14)
        self.FONT_BOLD = ('Consolas', 14, 'bold')

        self.SEPARATOR = "\n"
        
        self.create_widgets()

    
    def text_insert(self, msg, tag=None):
        # self.decorate_text(msg)
        self.txt.configure(state='normal')
        

        self.txt.insert('end', f'{msg}', tags=tag)
        if tag == 'msg':
            self.txt.see('end')
        
        self.txt.configure(state='disabled')
    


    def emoji_img(self, size, text):
        font = ImageFont.truetype("seguiemj.ttf", size=int(round(size*72/96, 0))) 
        im = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(im)
        draw.text((size, size/2), text, embedded_color=True, font=font, anchor="mm")
        return ImageTk(im)

    def open_settings_window(self):
        pass

    def create_rectangle(self):
        pass

    def create_widgets(self):

        
        '''
        # Tehdään old school -menu
        menubar = Menu(self, tearoff=0)
        menu = Menu(menubar, tearoff=0)

        menu.add_command(label='Asetukset', command=lambda: self.open_settings_window(),
                         font=self.FONT)
        menu.add_separator()
        menu.add_command(label="Poistu", command=self.destroy, font=self.FONT)
        menubar.add_cascade(label="Menu", menu=menu)
        
        self.config(menu=menubar)
        '''
     


        self.canvas = Canvas(
            self,
            bg=self.CANVAS_COLOR,
            height=self.CANVAS_HEIGHT,
            width=self.CANVAS_WIDTH,
            bd=0,
            highlightthickness=0,
        )

        self.canvas.grid(row=1, padx=20, pady=20)

        
        self.txt = Textbox(
            self.canvas, 
            wrap='word', 
            fg_color=self.TEXTBOX_FG, 
            text_color=self.TEXTBOX_TEXT_COLOR,
            font=self.FONT,
            width=self.CANVAS_WIDTH/2,
            height=self.CANVAS_HEIGHT/2,
            state='disabled',
            border_width=0
        )

        self.txt.pack(fill='both', expand=True)

        self.txt.tag_config("prefix", foreground="#6f6f6f")
        self.txt.tag_config("prefix2", foreground="#909090")
        self.txt.tag_config("title", foreground="#ffffff")
        self.txt.tag_config("msg", foreground="#cccccc")
        self.txt.tag_config("user", foreground="#a1a1a1")
        self.txt.tag_config("bot", foreground="#fe65cb")
        
        self.canvas.create_window(0,0, window=self.txt, anchor='nw')

        self.scrollbar = Scrollbar(self.txt)
        # self.scrollbar.place(relheight=1, relx=0.974)
        
        self.entry = Entry(
            self, 
            placeholder_text="Kirjoita viesti...", 
            fg_color=self.ENTRY_FG, 
            text_color=self.ENTRY_TEXT_COLOR, 
            font=self.FONT,
            width=self.CANVAS_WIDTH/2,
        )

        
        
        self.entry.grid(row=2, column=0)

        text = "⚙️"
        emoji = self.emoji_img(50, "⚙️")
        self.settings_button = Button(
            self,
            text="", 
            image=emoji, 
            font=self.FONT_BOLD,
            width=20,
        )
        self.settings_button.grid(row=0, column=1, sticky='e')
        
        self.send_button = Button(self, text="➤", font=self.FONT_BOLD, width=20)
        self.send_button.grid(row=2, column=1, sticky='w')
     

    
        

        
   
