class Translations:
    '''WIP'''
    
    def __init__(self, translations=None):
        
        dictionary = {
            'MAIN': {
                'en-fi': {
                    'Main Settings': 'Pääasetukset',
                    'Settings File': 'Asetustiedosto',
                    'Settings': 'Asetukset',
                    'Language': 'Kieli',
                    'English': 'Englanti',
                    'Finnish': 'Suomi',
                    'Module': 'Moduuli',
                }
            }
        }

        self.dictionary = dictionary
        
        if translations:
            # Additional translations have been provided; update the dictionary
            self.dictionary.update(translations)

    
    def update_dictionary(self, module, translations):
        '''Update translations dictionary with the provided dictionary.'''


        dict = {module: translations}
        self.dictionary.update(dict)

        

    def translate(self, word=None, dict="en-fi", module="MAIN") -> str:
        '''Translate a word or a phrase.

        Example: Translate("lentokonesuihkuturbiinimoottoriapumekaanikkoaliupseerioppilas", 
        dict="en-fi")
        '''
        
        
        origin, target = dict.split('-')

        if word == None or origin == target:
            return word
        
        if not self.dictionary.get(module):
            # No dictionary found for provided module
            return word
   
        pairs = self.dictionary[module].get(f"{origin}-{target}")
        reversed = self.dictionary[module].get(f"{target}-{origin}")

        if pairs:
            try:
                word = pairs[word]
            except KeyError:
                pass
        elif reversed and pairs:
            try:
                # Reverse lookup
                word = list(pairs.keys())[list(pairs.values()).index(word)]
            except KeyError:
                pass

        return word

