# from tkinter import Menu

from customtkinter import (CTk as Tk, CTkTextbox as Textbox, CTkEntry as Entry, CTkButton as Button, 
                           CTkScrollbar as Scrollbar, CTkCanvas as Canvas, CTkImage as ImageTk,
                           CTkLabel as Label)

import customtkinter

from PIL import Image, ImageDraw, ImageFont


class UI(Tk):
    def __init__(self, master=None):
        customtkinter.deactivate_automatic_dpi_awareness()
        self.master = Tk.__init__(self, master)
        
        self.title(f"SeduGPT")

        width = self.winfo_screenwidth() / 2
        height = self.winfo_screenheight() / 2
        
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

        self.LABEL_FONT = ('Helvetica', 20)

        self.SEPARATOR = "\n"

        

        self.create_widgets()

    
    def text_insert(self, msg, tag=None):
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

        # Label(self.master, text="SeduGPT", font=self.LABEL_FONT).grid(row=0, column=0, padx=20, sticky='w')
        self.canvas = Canvas(
            self.master,
            bg=self.CANVAS_COLOR,
            height=int(self.CANVAS_HEIGHT),
            width=int(self.CANVAS_WIDTH),
            bd=0,
            highlightthickness=0,
        )
       
        self.canvas.grid(row=1, column=0, padx=20, pady=(0,10))

        self.txt = Textbox(
            self.canvas, 
            wrap='word', 
            fg_color=self.TEXTBOX_FG, 
            text_color=self.TEXTBOX_TEXT_COLOR,
            font=self.FONT,
            width=self.canvas.winfo_reqwidth(),
            height=self.canvas.winfo_reqheight(),
            state='disabled',
            border_width=0
        )

        self.txt.pack(fill='both', expand=False)

       
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
            self.master, 
            placeholder_text="Kirjoita viesti...", 
            fg_color=self.ENTRY_FG, 
            text_color=self.ENTRY_TEXT_COLOR, 
            font=self.FONT,
            width=self.canvas.winfo_reqwidth(),
        )

        
        
        self.entry.grid(row=2, column=0, pady=(10,20))

        emoji = self.emoji_img(50, "⚙️")
        self.settings_button = Button(
            self,
            text="", 
            image=emoji, 
            font=self.FONT_BOLD,
            width=20,
        )
        self.settings_button.grid(row=0, column=1, sticky='e', pady=(20,0), padx=(0,20))
        
        self.send_button = Button(self.master, text="➤", font=self.FONT_BOLD, width=20)
        self.send_button.grid(row=2, column=1, sticky='w', pady=(10,20))

        

