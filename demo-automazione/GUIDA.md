# Demo dal vivo: l'automazione «Richieste dei clienti»

È l'automazione delle slide 16 e 17, costruita davvero. **Costa zero**.

- **L'automazione** (slide 16) gira sul vostro account Google: Gmail + Fogli Google + uno script (Apps Script) + l'AI gratuita di Google (Gemini).
- **La parte MCP** (slide 17) usa Claude con i connettori di Gmail, Google Drive e Calendario, inclusi in Claude Pro.

```
Email ad assistenza  →  è pubblicità?  →  Gemini classifica e scrive la bozza
                     →  riga nel foglio «Registro»  →  bozza in Gmail  →  la mandate voi
```

Tempo per prepararla la prima volta: circa 20 minuti.

---

## 1. La chiave dell'AI (gratis)

1. Andate su **aistudio.google.com** con l'account Google della demo.
2. Cliccate **Get API key** → **Create API key** e copiatela.

Il piano gratuito basta per la demo. I limiti precisi li vedete in AI Studio.

> ⚠️ Non mettete la chiave nella presentazione o su GitHub: va solo nello script (passo 2).

## 2. Il foglio e lo script

1. Create un nuovo **Foglio Google** e chiamatelo «Richieste clienti».
2. Menu **Estensioni → Apps Script**.
3. Cancellate quello che c'è e incollate tutto il file `richieste-clienti.gs`. Salvate (💾).
4. A sinistra: **⚙️ Impostazioni progetto → Proprietà script → Aggiungi proprietà**:
   - Proprietà: `GEMINI_API_KEY`
   - Valore: la chiave del passo 1
5. Tornate al Foglio e ricaricate la pagina. Compare il menu **🤖 Automazione**.
6. **🤖 Automazione → ⚙️ Prima configurazione**. Google chiede le autorizzazioni (Gmail e Fogli): **Consenti**.
   - Se compare «Google non ha verificato questa app», cliccate **Avanzate → Vai a … (non sicuro)**. È normale: lo script è vostro.
   - Si crea il foglio **Registro** e l'etichetta Gmail **AI-gestita**.

## 3. Proviamola

Da un **altro** indirizzo email (il vostro personale va benissimo) mandate all'account della demo le email qui sotto, poi **🤖 Automazione → ▶ Controlla le email adesso**.

**Pacco in ritardo** (urgenza alta)
> Oggetto: ordine 48213
> Buongiorno, ho ordinato le scarpe il 2 ottobre ma non sono ancora arrivate. Mi servono per sabato. Potete aiutarmi? Giulia

**Cambio taglia** (urgenza media)
> Oggetto: cambio scarpe
> Salve, le scarpe dell'ordine 47950 sono un po' piccole. Posso cambiarle con il numero 42? Marco

**Pubblicità** (si ferma alla regola, senza AI)
> Oggetto: Primi su Google in 7 giorni!!!
> Offerta imperdibile: porta il tuo sito primo su Google. Solo oggi 99 €!

Cosa deve succedere:

- nel **Registro** compaiono 2 righe, con l'urgenza colorata;
- in **Gmail → Bozze** ci sono 2 risposte pronte;
- la pubblicità ha l'etichetta *AI-gestita* ma nessuna riga e nessuna bozza.

Se volete che giri da sola: **🤖 Automazione → ⏱ Accendi il controllo ogni 5 minuti**. Per la demo in aula è meglio il pulsante «Controlla adesso», così non si aspetta.

## 4. La parte MCP: Claude lavora sul registro

In **Claude** (Pro): **Impostazioni → Connettori**, attivate **Gmail**, **Google Drive** e **Google Calendar** con lo stesso account Google della demo.

Poi, in una chat nuova, provate le tre richieste della slide 17:

1. «Leggi il foglio *Richieste clienti* su Drive: quali richieste urgenti sono arrivate oggi? Prepara le risposte come bozze in Gmail.»
2. «Fammi il riepilogo delle richieste di questa settimana e preparalo come email per il responsabile.»
3. «Giulia Verdi ha scritto di nuovo: fissa una chiamata con lei domani mattina nel mio calendario.»

Claude chiede il permesso prima di creare bozze, inviare email o creare eventi. Mostratelo al pubblico: è il punto della slide.

> Il connettore di Google Drive **legge** i fogli ma non li modifica: per scrivere nel registro c'è l'automazione.
> Per collegare Claude a migliaia di altre app (Slack, Trello, HubSpot…) c'è **Zapier MCP**: il piano gratuito ha 100 attività al mese condivise con gli altri Zap.

## 5. Prima della lezione

- Mandate le email di prova **qualche minuto prima** e lasciatele *non lavorate*, così in aula premete «Controlla adesso» e il pubblico vede comparire righe e bozze.
- Per ricominciare da zero: cancellate le righe del Registro (non l'intestazione), le bozze e l'etichetta *AI-gestita* dalle email.
- **Privacy:** è un account di prova con dati finti. Con email vere di clienti servono strumenti approvati dall'azienda.

## Se qualcosa non va

| Problema | Cosa fare |
|---|---|
| «Manca GEMINI_API_KEY» | Passo 2.4: il nome della proprietà deve essere esattamente `GEMINI_API_KEY`. |
| Nessuna riga nuova | L'email deve essere nella **Posta in arrivo**, non in Promozioni o Social, e arrivata negli ultimi 2 giorni. Le email mandate da voi stessi vengono saltate. |
| Errore 429 | Troppe richieste all'AI gratuita: lo script aspetta e riprova. Se succede spesso, mandate meno email insieme. |
| Il modello non esiste più | In cima allo script cambiate `MODELLO` con un modello Flash elencato in AI Studio. |
