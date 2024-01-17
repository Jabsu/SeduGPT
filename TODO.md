### Esivalmistelu
- [x] Struktuuri, testikoodinpätkät
- [x] GitHub
    - [x] README.md
    - [x] TODO.md
    - [x] Muut olennaiset

### v0.1 — Proof of Concept
- [x] GUI-raakaversio 🤢
- [x] Ensimmäinen moduuli: Ruokalistat
- [x] Modulaarisuusvalmistelua
    - [x] Moduulien vakiofunktiot
    - [x] main.py: Moduulien importtaus & initialisaatio (< config.py)
    - [x] main.py: check_triggers-iterointi moduuli kerrallaan
        - [x] Botti ulostaa tekstin moduulin määrittämällä tavalla
        - [x] Komentorivi- ja GUI-ulostus
- [x] Komentorivitoiminnallisuusvalmistelua

### v0.3 — Pronssi
- [x] UI:n kaunistelua
    - [x] Lopullista versiota kutakuinkin vastaava layout
    - [x] Viesteihin irssi-tyyliset prefixit ja tageja hyödyntävä väritys
    - [x] Tkinter -> customtkinter
- [ ] Textbox-tagien hyödyntäminen moduulimäärityksin
- [ ] Textbox-emojeihin värit!
- [ ] Moduulikohtainen konfigurointi (frontend & backend)
    - [ ] config.py -> settings.json
    - [ ] import, export, defaults, exceptions
    - [ ] Asetusikkuna (modulaarisuus huomioiden)  
        📝 Määritellään moduulissa: Label, variablen nimi, oletusarvo, widget-tyyppi  
        📝 Tuki useille asetuksille
- [ ] Debug-moodi (logging, output oksennetaan chattiin)
- [ ] Toinen moduuli: Sää
- [ ] Mahdollisesti: Tkinter -> PySide

### v0.6 — Hopea
- [ ] EHKÄ: GPT-integraatio
- [ ] Wiki
    - [ ] Moduulikohtainen info
    - [ ] Opas moduulien tekijöille
- [ ] Lisää moduuleja!

### v1.0 — Kulta
- [ ] py2exe

### Perfektionismi, Bertie Bottin joka maun rakeet
- [ ] Ennakoiva tekstinsyöttö (Nokian T9?)
