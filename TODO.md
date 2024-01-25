### Initial Preparations
- [x] Structure, test code
- [x] GitHub
    - [x] README.md
    - [x] TODO.md
    - [x] Other relevant stuff

### v0.1 — Proof of Concept
- [x] Initial (crude) GUI 🤢
- [x] First module: quite_edible.py
- [x] Modularity preparations
    - [x] Initial constant (common) functions for modules
    - [x] main.py: Importing and initializing modules (config.py)
    - [x] main.py: Iterating through check_triggers functions in modules
    - [x] Semi-configurable type and formatting for output   
    - [x] Output to Textbox and command prompt
- [x] Crude command prompt functionality

### v0.3 — Bronze
- [x] Improving UI/UX
    - [x] Better layout, more close representation of the final look  
    - [x] IRC-style (specifically irssi-style) formatting for messages + coloring with tags
    - [x] Tkinter -> customtkinter
- [ ] Module triggers will be iterated through only once, at module initialization
- [ ] Move the call functions for check_triggers and get_module_name from modules to main
- [x] Add helpers.py for common/convenient module functions 
- [ ] Textbox: Support for colorized emojis 
- [ ] Module configuration (frontend & backend)
    - [x] config.py -> settings.json
    - [x] Importing/exporting settings
    - [x] Settings window with module specific widgets
    - [x] Handling changes in module default settings (such as new config widgets) when settings.json has been already created
    - [ ] Scrollbar for settings window
    - [ ] Textbox: Configurable tags (formatting) for output
- [ ] Debug mode (with an option to output to Textbox)
- [ ] Global language setting
- [ ] Tab completion for input

### v0.6 — Silver
- [ ] Possibly: GPT4All integration
- [ ] Wiki
    - [ ] Module-specific information
    - [ ] Guide for creating modules (required functions, default settings, etc.)

### v1.0 — Gold
- [ ] py2exe

### Included Modules
- [x] quite_edible.py 
- [ ] foreca.py
