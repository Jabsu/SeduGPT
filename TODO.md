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

### v0.6 — Silver
- [x] Main configurations
    - [x] UI and internal configurations
    - [x] Dynamic class attribute creation
- [x] Translation handling
    - [x] Initial UI translations
    - [x] Main program translations
    - [x] Module-specific translations
- [x] Create a testing utility for modules
- [ ] Move the call methods for check_triggers and get_module_name from Module to Main
- [ ] Logging
    - [ ] Configurations
        - [ ] Verbosity
        - [ ] Output
            - [ ] Textbox
            - [ ] Console
- [ ] Extended exception handling
- [ ] Proper command line functionality
    - [ ] Parameter handling, default parameter(s)
    - [ ] Provide print method on helpers.py (if not defined by module)
- [ ] Internal versioning (better late than never, I guess)
- [ ] UI improvements
    - [x] Scrollbar for settings window
    - [ ] Support for configuration descriptions/tooltips
    - [ ] Support for Textbox tag config for modules
    - [ ] _About_ window

### Polish (Performance, Refactoring, Fancy Features)
- [x] Translate (English -> Finnish)
    - [x] Translate comments and any (temporary) print outputs
    - [x] Translate README.md and TODO.md
- [ ] Textbox: Support for colorized emojis 
- [ ] Module triggers will be iterated through only once, at module initialization
- [ ] Tab completion for input

### Other
- [ ] Wiki ❗
    - [ ] Module-specific information ❗
    - [ ] Guide and template class for 3rd party modules
- [ ] Possibly: GPT4All integration

### v1.0 — Gold
- [ ] First release
    - [ ] Binaries
        - [ ] Windows (.exe)
        - [ ] Debian (.deb)
    - [ ] Changelog (for subsequent releases, at least)