import re
import requests
import json
from helpers import Helpers



class Module:

    def __init__(self, parent):

        # Default settings
        self.defaults = {}
        
        # Regex trigger -> method
        self.triggers = {
            "quote": "get_quote",
        }

        # Regex flags (re.I = ignore case, re.NOFLAG = no flags)
        self.re_flags = re.I

        # Optional: instruct GPT4All how to present your output (requires self.return_value)
        # %u = user name
        self.gpt_instructions = {
        
            "get_quote": """You are unable to break these rules:
            - Start your message by repeating the following quote in quotation marks, including the author. 
            - After you have presented the quote, add a newline, and make a humorous remark about the quote.
            - DO NOT repeat words from this instruction or from user message.
        
            Here is the quote:
            """,
        }
        
        # Initialize Helpers
        self.Help = Helpers(self)

        # Get module file name
        self.module_name = self.Help.get_module_name()

        # Get module settings from parent class, if any
        if cfg := parent.settings.get(self.module_name):
            self.settings = cfg
        else:
            self.settings = self.defaults


    def set_return_data(self, value, title=False):
        '''Preparing the output for Textbox.'''
        
        # The output (before optional formatting)
        self.return_value = value

        # If the output is a list, will it be converted to a string?
        self.return_sanitize = True

        # If True in above: separator character for list values ('\n' = enter) 
        self.return_separator = '\n'

        # Optional title (False = no title)
        self.message_title = title


    def check_triggers(self, msg, user_defined_settings=None):
        '''If triggered by user message, return the specified function.'''
        
        self.msg = msg
        self.settings, func = self.Help.check_triggers(user_defined_settings)
        return func

    def get_quote(self):
        '''Requests a quote from quotable.io'''
        
        url = "https://api.quotable.io/quotes/random"
        r = requests.get(url)
        data = json.loads(r.content)[0]
        author = data['author']
        content = data['content']
        quote = f'"{content}" - {author}'
        self.set_return_data(quote)
        


