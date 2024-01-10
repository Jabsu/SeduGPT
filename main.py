from tkinter import *
from modules.ruokalista import Food
from ui import UI

class Main:
    def __init__(self):
        self.UI = UI()
        self.UI.send_button.config(command=lambda: self.send())
        self.UI.bind('<Return>', lambda event=None: self.send())
        self.UI.mainloop()

    def send(self, event=None):
        '''Lähetetään SMS.'''

        user_msg = self.UI.entry.get().lower()
        
        if not user_msg:
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
    Main()