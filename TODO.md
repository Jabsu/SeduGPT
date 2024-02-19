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
    - [x] Initial constant (common) methods for modules
    - [x] main.py: Importing and initializing modules (config.py)
    - [x] main.py: Iterating through check_triggers methods in modules
    - [x] Semi-configurable type and formatting for output   
    - [x] Output to Textbox and command prompt
- [x] Crude command prompt functionality

### v0.3 — Bronze
- [x] Improving UI/UX
    - [x] Better layout, more close representation of the final look  
    - [x] IRC-style (specifically irssi-style) formatting for messages + coloring with tags
    - [x] Tkinter -> customtkinter
- [x] Move common functions into a Helpers class
- [x] Module configuration (frontend & backend)
    - [x] config.py -> settings.json
    - [x] Importing/exporting settings
    - [x] Settings window with module specific widgets
    - [x] Handling changes (such as new/renamed keys) on default settings
- [x] Translate everything from Finnish to English
    - [x] Translate comments and any (temporary) print outputs
    - [x] Translate README.md and TODO.md

### v0.6 — Silver
- [x] Main configurations
    - [x] UI and internal configurations
    - [x] Dynamic class attribute creation
- [x] Translation handling
    - [x] Initial UI translations
    - [x] Main program translations
    - [x] Module-specific translations
- [x] Create a testing utility for modules
- [x] Threading: Keep UI responsive during long processes
- [x] Scrollbar for settings window
- [x] GPT4All integration
    - [ ] Per session context memory ❗
    - [ ] Module support ❗
- [ ] Make config.py redundant ❗
    - [ ] Make module importing configurable on the UI
    - [ ] Make settings.json location configurable on the UI
    - [ ] Make GPT4All settings configurable on the UI
        - [ ] Add progress bar for model download

### v0.9 — Electrum
- [ ] Proper command line functionality ❗
    - [ ] Parameter handling, default parameter(s)
    - [ ] Provide print method on helpers.py (if not defined by module)
- [ ] Logging (configurable verbosity, print to chat/console) ❗
- [ ] UI improvements
    - [ ] Possibly: customtkinter -> PySide
    - [ ] Support for colorized emojis
    - [ ] Support for module-specific configuration descriptions/tooltips
    - [ ] Support for module-specific text formatting (font, emphasis, colors)
    - [ ] "About" window
- [ ] Tab completion
- [ ] Module triggers should be iterated through only once, at module initialization
- [ ] Move the call methods for check_triggers and get_module_name from Module to Main
- [ ] Extended exception handling
- [ ] Extended test_modules functionality
- [ ] More precise internal versioning (better late than never, I guess)

### Other
- [ ] Wiki ❗
    - [ ] Module-specific information ❗
    - [ ] Guide and template class for 3rd party modules ❗

### v1.0 — Gold
- [ ] First release
    - [ ] Binaries
        - [ ] Windows (.exe)
        - [ ] Debian (.deb)
    - [ ] Changelog (for subsequent releases, at least)