# SeduGPT
A modular chat companion designed particularly for programming students at Sedu.

SeduGPT aims to: 
- _Theoretically_ encourage programming students to practice with Python by making modules  
- Engage students – or at least myself – in the fine art of tomfoolery

###### Human-made™ — Original, not artificial
</br>

```  
-===[ 𝐏𝐫𝐨𝐣𝐞𝐜𝐭 𝐒𝐭𝐚𝐭𝐮𝐬 ]===-

📝 Initial Preparations ✔️
⚙️ Proof of Concept ✔️
🥉 Bronze ✔️
🥈 Silver  
🏅 Electrum  
🥇 Gold  
```  

See [TODO.md](https://github.com/Jabsu/SeduGPT/blob/main/TODO.md) for my plans and progress.
<br/>
<br/>
## Features
- Modular
    - Make any number of regular expression triggers (reactions to user input) to call a specific function
        - Although this is a chatbot first and foremost, modules don't have to return anything (i.e. they can be self-contained programs)
    - Make some quick adjustments to the (optional) chat output by choosing a type, adding a title, formatting the text (such as colors, font style), etc. 
        - Work in progress
    - Easily add user interface configurations (with labels and interactive widgets) by using a dict
        - All modules have a common settings window on which the widgets will show up
    - Detailed instructions for module development coming soon
    - Fun and useful modules might be integrated into the repository
    - See [wiki](https://github.com/Jabsu/SeduGPT/wiki) for module creation instructions
- Included modules
    - [quite_edible.py](): Gets the lunch menu from a selected campus
        - **FINNISH ONLY**
        - Triggers: Food related verbs/nouns (e.g. ruokana, syömme, syötiin, safka)
        - Parameters: The day of the week, conjugated or not
        - Example sentences:
            - "Mitäs tiistaina syötiin?"
            - "Mahtaako tänään olla sapuskana jotain erityisen innostavaa vai olisiko mielekkäämpää lähteä syömään esimerkiksi McDonald'siin mahdollisista terveyshaitoista piittaamatta?"
    - [foreca.py](): Obligatory weather inquiries – a chatbot is severely incomplete without such an important feature
        - **Work in progress**, no functionality as of yet
- GPT integration (GPT4All)
    - Supported languages: English
    - Session based context memory coming soon!
    


### Installation  
1. Install Python 3.8+ (recommended: 3.12+)
2. Install the required libraries: `pip install -U -r requirements.txt`
3. Launch main.py and have some semblance of fun!
