# SeduGPT
Modulaarinen keskustelukumppani Sedun opiskelijoille.
<br/>
<br/>
```
-===[ 𝗣𝗿𝗼𝗷𝗲𝗸𝘁𝗶𝗻 𝘀𝘁𝗮𝘁𝘂𝘀 ]===-

-> 📝 Esivalmistelu
   ⚙️ Proof of Concept  
   🥉 Pronssi  
   🥈 Hopea  
   🥇 Kulta  
```

Lisätietoja projektin edistymisestä: [TODO.md](https://github.com/Jabsu/SeduGPT/blob/main/TODO.md)
<br/>
<br/>
## Toiminnot (kehitteillä)
- Modulaarinen
    - Opiskelijat voivat ohjelmointia harjoitellakseen kehitellä SeduGPT:lle *vallattomia* lisäosia!
        - Ohjeet moduulien kehittämiseen tulossa myöhemmin
        - Hauskat ja hyödylliset moduulit integroidaan projektiin
- Ensisijaiset moduulit:
    - ruokalista.py: Kertoo valitsemasi kampuksen ruokalistan
    - sää.py: Kertoo paikkakuntasi sään (ei bottia ilman säätä)
    - tivi-antti.py: Antti-open rajapinnan kanssa keskusteleva kontrolleri
- Iso ehkä: GPT-integraatio
    - The dream: Keywordien sijaan botti ymmärtää kokonaisia lauseita ja pystyy ilmaisemaan moduulien generoimat tiedot kirjavin sanavalinnoin 
        - Vaihtoehdot:
            - OpenAI:n rajapinta 
                - Maksullinen ☹️
            - ChatGPT- tai Copilot-integraatio selaindataa hyödyntäen
                - TOS-rikkomus ☹️
            - GPT4All + valmennukset esim. Sedun sivustodatalla


### Käyttöönotto  
1. Asenna Python 3.8+ (suositeltavaa: 3.12+)
2. Asenna vaaditut kirjastot: `pip install -U -r requirements.txt`
3. Sorki config.py-tiedostoa (placeholder)