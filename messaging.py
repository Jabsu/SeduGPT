import time
import threading


class Messaging(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent


    def run(self):
        self.parent.msg = self.parent.UI.entry.get()
        
        if not self.parent.msg:
            return
        
        self.parent.UI.entry.delete(0, 'end')
        
        self.send_prefix('user') 
        self.parent.UI.text_insert(self.parent.msg+'\n', tag='msg')
        
        self.iterate_module_triggers()

    def iterate_module_triggers(self):
        '''Iterates through module triggers. 
        
        TO-DO: 
        Load the triggers into memory instead of iterating through them repeatedly, so that 
        a quarter of a millisecond would be saved on a 386 SX (@ 12 MHz, 4 MB RAM, less than 640 kB 
        of conventional memory).'''
        
        triggered = False

        for module in self.parent.modules:
            
            
            self.current_mod = module.Module(self.parent)
            # mod_name = self.current_mod.get_module_name()
            
            # If triggered by user message, module returns a specific method, which is then called
            if module_func := self.current_mod.check_triggers(self.parent.msg):
                
                triggered = True
                
                func = getattr(self.current_mod, module_func)
                func()
                
                self.bot_output(True)

        if not triggered:
            # Not triggered by any module; bot outputs the default text
            self.bot_output(False)


    def sanitize(self, content):
        '''Convert List to String. 
        
        TO-DO: Other conversions.'''

        ret = content

        if type(content) == list:
            # Use the separator defined in the module for joining the values
            ret = self.current_mod.return_separator.join(content)

        if type(content) == dict:
            pass

        return ret
    

    def send_prefix(self, user):
        '''Format and send a prefix to chat (HH:MM <user>); tags (prefix, prefix2) point to colors
        configured in main_window.py. 
        
        TO-DO: More dynamic/modular tag support.'''
        
        clock = time.strftime("%H:%M ")
        self.parent.UI.text_insert(clock, 'prefix')      
        self.parent.UI.text_insert('<', 'prefix2')
     
        if user == 'bot':
            user_name = self.parent.bot_name
            self.parent.UI.text_insert('@', 'prefix2')
        else:
            user_name = self.parent.user_name
            self.parent.UI.text_insert('+', 'prefix2')

        self.parent.UI.text_insert(user_name, user)      
        self.parent.UI.text_insert('> ' , 'prefix2')

    
    def bot_output(self, triggered_by_module=False):
        '''Bot's output to chat.'''
        
        if not triggered_by_module:
            bot_msg = self.parent.GPT.generate(self.parent.msg)
        else:
            bot_msg = self.current_mod.return_value
            
            # If the return value set in a module is not String and 'sanitize' is set to True, 
            # the value will be converted to String
            if type(bot_msg) != 'str' and self.current_mod.return_sanitize:
                bot_msg = self.sanitize(bot_msg)

     
        self.send_prefix('bot') 

        if self.parent.args != "--gui":
            # Use the module's print method (if implemented) when not using the GUI
            # TO-DO: Finalize the command line functionalities
            try:
                self.current_mod.print()
            except:
                print(f'{self.current_mod.get_module_name()} does not have a print method.')
        else:
            if triggered_by_module:
                
                # If set by module, add a title to the output
                if title := self.current_mod.message_title:
                    self.parent.UI.text_insert(title, tag='title')
                   
            
            self.parent.UI.text_insert(bot_msg+'\n', tag='msg')