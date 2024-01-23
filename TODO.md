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
- [ ] Moduulien triggerit käydään läpi vain kerran (initialisoinnin yhteydessä)
- [x] helpers.py moduuleissa toistuvia funktioita varten
- [ ] Textbox-tagien hyödyntäminen moduulimäärityksin
- [ ] Textbox-emojeihin värit!
- [x] Moduulikohtainen konfigurointi (frontend & backend)
    - [x] config.py -> settings.json
    - [x] Asetusten tallentaminen ja lataaminen
    - [x] Asetusikkuna (modulaarisuus huomioiden)  
- [ ] Debug-moodi (logging, output oksennetaan chattiin)
- [ ] Toinen moduuli: Sää

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
