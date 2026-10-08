# Voto dal telefono

Nella sala di Turing (slide 3, anno 1950) gli studenti possono votare dal telefono nel "gioco dell'imitazione". Il proiettore mostra un QR code. I ragazzi lo inquadrano, scelgono la risposta e i voti compaiono in diretta sullo schermo.

È tutto **gratis** e non serve nessuna carta di credito. Una volta online, **qualunque insegnante** apre il link della presentazione e il voto funziona e basta.

## Cosa è già pronto

- **Database Supabase** (piano Free), progetto `workshop-ai`. Contiene due tabelle, `vote_rooms` e `votes`, e una pulizia automatica notturna che cancella i voti più vecchi di 2 giorni.
- **La presentazione è già collegata al database.** In `ai-workshop.html` sono già inseriti `SUPA_URL` e `SUPA_KEY`. La chiave è quella *anon*, pubblica per design: le regole del database permettono solo di leggere e votare.
- **Il "keep-alive"** (`.github/workflows/keepalive.yml`). Supabase mette in pausa i progetti gratuiti dopo circa 7 giorni di inattività. Questo piccolo compito automatico di GitHub "sveglia" il database ogni 3 giorni, così il voto funziona sempre, anche tra un workshop e l'altro.

## Cosa manca: mettere la presentazione online (GitHub Pages)

I telefoni devono poter aprire la presentazione, quindi deve stare su internet.

1. Crea su GitHub un repository **pubblico**, ad esempio `workshop-ai`.
2. Carica `ai-workshop.html`, `VOTO-DA-TELEFONO.md` e la cartella `.github`. Il keep-alive funziona solo se è dentro il repository.
3. Vai su **Settings → Pages**. Alla voce **Branch** scegli `main` e la cartella `/ (root)`, poi premi **Save**.
4. Dopo uno o due minuti la presentazione è online a un indirizzo come questo:
   `https://TUO-UTENTE.github.io/workshop-ai/ai-workshop.html`

Se la presentazione viene aperta **da quell'indirizzo**, il QR code punta automaticamente lì e non serve altro.

Se invece qualcuno la apre **dal file sul proprio computer**, il QR code deve sapere l'indirizzo online. In `ai-workshop.html` cerca `var VOTE_PAGE=''` e incolla l'indirizzo tra gli apici.

## Prova prima del workshop

1. Apri l'indirizzo online e vai alla slide 3, anno 1950, scheda **2 · Il gioco dell'imitazione**.
2. Inquadra il QR con due telefoni e vota: le barre sul proiettore si muovono in diretta.
3. Clicca **A** o **B** sul proiettore: sui telefoni compare la risposta giusta.

## Da sapere

- **Classi separate:** ogni volta che la presentazione viene aperta crea un **codice stanza** nuovo (ad esempio `K7QF`), quindi le classi non si mescolano mai.
- **Limiti del piano Free** di Supabase: 200 connessioni in tempo reale insieme e 500 MB di database. Per un workshop scolastico è molto più del necessario.
- **Privacy:** non si raccolgono nomi né dati personali. Ogni telefono riceve solo un codice casuale, che serve a evitare voti doppi.
- **Serve internet** sia sul computer del proiettore sia sui telefoni (va bene anche il Wi-Fi della scuola).
- **Senza internet** la slide funziona lo stesso: la classe vota per alzata di mano e l'insegnante clicca A o B.
- **Mai condividere la chiave `service_role`** di Supabase. Nella presentazione c'è solo quella *anon*, ed è giusto così.
