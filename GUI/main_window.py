from tkinter import *

class UI(Tk):
    def __init__(self, master=None):
        self.master = Tk.__init__(self, master)
        self.title(f"SeduGPT")
        self.config()
        self.create_widgets()

        
    def config(self):
        '''Konstantinopolis!'''

        self.BG_GRAY = "#ABB2B9"
        self.BG_COLOR = "#17202A"
        self.TEXT_COLOR = "#EAECEE"

        self.FONT = "Consolas 14"
        self.FONT_BOLD = "Consolas 13 bold"

        self.USERNAME = "TÖRTTÖ"
        self.BOT_NAME = "𝐒𝐞𝐝𝐮𝐆𝐏𝐓" 

        self.USER_PREFIX = '-====[ '
        self.USER_SUFFIX = ' ]====-'
        
        self.SEPARATOR = "\n"

    def create_widgets(self):
        
        self.txt = Text(self, wrap=WORD, bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)
        
        # self.scrollbar = Scrollbar(self.master)
        # self.scrollbar.place(relheight=1, relx=0.974)
        
        self.entry = Entry(self, bg="#2C3E50", fg=self.TEXT_COLOR, font=self.FONT, width=55)
        self.entry.grid(row=2, column=0)
        
        self.send_button = Button(self, text="Lähetä", font=self.FONT_BOLD, bg=self.BG_GRAY)
        self.send_button.grid(row=2, column=1)

        self.settings_button = Button(self, text="Asetukset", font=self.FONT_BOLD, bg=self.BG_GRAY)
        self.settings_button.grid(row=0)
        

        
   
