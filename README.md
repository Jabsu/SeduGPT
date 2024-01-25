# SeduGPT
A modular chat companion, particularly for programmer students in Sedu.

Purposes: 
- To _theoritecally_ encourage programming students to practice with Python by making modules
- For me to have fun
<br/>
<br/>
```
-===[ 𝐏𝐫𝐨𝐣𝐞𝐜𝐭 𝐒𝐭𝐚𝐭𝐮𝐬 ]===-

   📝 Initial preparation
-> ⚙️ Proof of Concept  
   🥉 Bronze  
   🥈 Silver  
   🥇 Gold  
```

See [TODO.md](https://github.com/Jabsu/SeduGPT/blob/main/TODO.md) for plans and progress.
<br/>
<br/>
## Features
- Modular
    - Make multiple regular expression triggers to call a specific function
        - Data returned to chat (Tk.Textbox) can be 
            - Currently supported formats:
    - Easily add user interface configurations (which will be shown on settings GUI) by using a dict
        - Currently supported interactive widgets: OptionMenu 
    - Instructions for detailed module development coming soon
    - Fun and useful modules might be integrated to the project
- Included modules
    - [quite_edible.py](): Gets the lunch menu from a selected campus
        - **Finnish only**
        - Triggers: food related verbs/nouns
        - Parameters: the day of week
        - Example sentences:
            - "Mitäs tiistaina syötiin?"
            - "Mahtaako tänään olla sapuskana jotain erityisen innostavaa vai olisiko mielekkäämpää lähteä syömään esimerkiksi McDonald'siin mahdollisista terveyshaitoista piittaamatta?"
    - [foreca.py](): Obligatory weather inquiries
        - **Work in progress**
- In consideration: GPT integration (GPT4All)



### Installation  
1. Install Python 3.8+ (recommended: 3.12+)
2. Install the required libraries: `pip install -U -r requirements.txt`
3. Activate/deactivate modules in config.py