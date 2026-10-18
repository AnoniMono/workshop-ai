# Voto dal telefono

In molte slide gli studenti partecipano dal telefono: il gioco dell'imitazione e la sfida ad AlphaGo nel museo, i disegni, il gatto vero, l'immagine da creare, lo studio con l'AI e tutto il blocco di etica. Il proiettore mostra un QR code, i ragazzi lo inquadrano e le risposte compaiono in diretta sullo schermo.

È tutto **gratis** e non serve nessuna carta di credito. Una volta online, **qualunque insegnante** apre il link della presentazione e il voto funziona e basta.

## Un solo link per tutto il workshop

Tutti i QR code portano allo **stesso link** (`…/ai-workshop.html?stanza=CODICE`). Basta inquadrarlo una volta e tenere la pagina aperta:

- quando sul proiettore c'è un'attività, il telefono la apre **da solo** (entro pochi secondi);
- quando sul proiettore c'è una slide normale, il telefono mostra **«Guardate la presentazione»**.

## Nomi e parolacce

- **Prima di tutto il telefono chiede il nome** (nome e iniziale del cognome, ad esempio «Giulia R.»). Lo studente sa che comparirà sullo schermo accanto a quello che scrive. Il nome resta salvato sul telefono; in basso c'è il tasto «Cambia nome».
- **Sul proiettore** ogni argomento del dibattito mostra chi l'ha scritto; nella nuvola di parole il nome compare passando sopra la parola. Cliccando su «N telefoni» (nel riquadro del QR delle slide di etica) si apre **«Chi c'è»**, l'elenco dei nomi collegati.
- **Parolacce e bestemmie vengono bloccate** sul telefono (nomi, argomenti del dibattito, parole della nuvola), anche se scritte con lettere ripetute, spazi, accenti o numeri al posto delle lettere. Se qualcuno riesce comunque a farle arrivare, **il proiettore le nasconde** e scrive all'insegnante chi le ha mandate.
- Il filtro non è perfetto: per un testo che passa lo stesso, sul proiettore c'è sempre la ✕ per nasconderlo.

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

1. Apri l'indirizzo online e inquadra un QR qualsiasi con due telefoni. Scrivi un nome su ciascuno: compare «Guardate la presentazione».
2. Vai alla slide del dibattito (etica): i telefoni passano da soli al dibattito. Scrivi un argomento: compare sul proiettore con il nome.
3. Prova a scrivere una parolaccia: il telefono la rifiuta.
4. Torna a una slide normale: i telefoni tornano a «Guardate la presentazione».

## Da sapere

- **Classi separate:** ogni volta che la presentazione viene aperta crea un **codice stanza** nuovo (ad esempio `K7QF`), quindi le classi non si mescolano mai.
- **Limiti del piano Free** di Supabase: 200 connessioni in tempo reale insieme e 500 MB di database. Per un workshop scolastico è molto più del necessario.
- **Privacy:** si raccoglie solo il nome scritto dallo studente (nome e iniziale del cognome, nient'altro), legato al codice stanza e a un codice casuale del telefono. La pulizia automatica notturna cancella nomi e risposte dopo 2 giorni.
- **Serve internet** sia sul computer del proiettore sia sui telefoni (va bene anche il Wi-Fi della scuola).
- **Senza internet** la slide funziona lo stesso: la classe vota per alzata di mano e l'insegnante clicca A o B.
- **Mai condividere la chiave `service_role`** di Supabase. Nella presentazione c'è solo quella *anon*, ed è giusto così.
