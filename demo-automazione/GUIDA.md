# Demo dal vivo: «Il briefing del mattino»

È l'automazione delle slide 16 e 17, costruita davvero. **Costa zero**.

- **L'automazione** (slide 16): ogni mattina un piccolo script legge la vostra agenda e le email della notte, l'AI gratuita di Google (Gemini) le mette in ordine, e vi arriva **una pagina** con le priorità, le riunioni e a chi rispondere.
- **La parte MCP** (slide 17): le stesse cose, ma chieste **a parole a Claude**, con i connettori di Gmail, Calendario e Drive inclusi in Claude Pro.

```
⏰ 7:30 → 📅 agenda + ✉️ email → 📏 via newsletter e notifiche → 🧠 Gemini mette in ordine → 📨 il briefing nella vostra posta
```

Tempo per prepararla la prima volta: circa 15 minuti.

---

## 1. La chiave dell'AI (gratis)

1. Andate su **aistudio.google.com** con l'account Google della demo.
2. Cliccate **Get API key** → **Create API key** e copiatela.

> ⚠️ La chiave non va mai nella presentazione o su GitHub: solo nelle impostazioni dello script (passo 2).

## 2. Lo script

1. Andate su **script.google.com** → **Nuovo progetto**. Chiamatelo «Briefing del mattino».
2. Cancellate quello che c'è e incollate tutto il file `briefing-mattino.gs`. Salvate (💾).
3. A sinistra: **⚙️ Impostazioni progetto → Proprietà script → Aggiungi proprietà**:
   - Proprietà: `GEMINI_API_KEY`
   - Valore: la chiave del passo 1
4. In alto scegliete la funzione **briefing** e premete **▶ Esegui**.
5. Google chiede le autorizzazioni (Gmail e Calendario): **Consenti**.
   - Se compare «Google non ha verificato questa app»: **Avanzate → Vai a … (non sicuro)**. È normale: lo script è vostro.
6. Dopo qualche secondo vi arriva l'email **«☀️ Il tuo briefing di oggi»**.

Per riceverlo ogni mattina: scegliete la funzione **accendi** e premete **▶ Esegui**. Arriverà tra le 7 e le 8 (è Google a decidere il minuto esatto). Per spegnerlo: funzione **spegni**.

## 3. Prepariamo una mattina realistica

L'account della demo deve sembrare quello di una persona occupata.

**Nel Calendario**, per il giorno della lezione, create 3–4 eventi con degli invitati (va bene anche un vostro secondo indirizzo):

- 9:00 «Riunione vendite»
- 11:30 «Call fornitore Alfa»
- 14:00 «Colloquio candidato marketing»
- 17:00 «Consiglio di amministrazione»

**Da un altro indirizzo**, il giorno prima, mandate 5–6 email all'account della demo, per esempio:

> **Budget Q4**: «Ciao, mi serve il tuo ok sul budget Q4 entro stasera, lo presento al CdA. Elena»
> **Ritardo consegna**: «Buongiorno, purtroppo la consegna dei componenti slitterà di 5 giorni. Possiamo parlarne alla call? Fornitore Alfa»
> **CV candidato**: «Ti allego il CV del candidato di domani alle 14. HR»
> **Numeri settembre**: «Domani porto i numeri di settembre: siamo a −4%, soprattutto al Nord. Marco»
> più un paio di email poco importanti (un invito a un webinar, una conferma d'ordine).

Poi lanciate **briefing** e guardate il risultato. Se volete cambiare il tono o il contenuto, modificate il `PROMPT` in cima allo script: è la ricetta della slide 14.

## 4. In aula

1. **Slide 16:** fate vedere la simulazione, poi aprite la posta della demo e mostrate il briefing vero. Ancora meglio: aprite lo script e premete **▶ Esegui** davanti a tutti. In 10 secondi arriva l'email.
2. **Slide 17 (MCP):** in **Claude → Impostazioni → Connettori** attivate **Gmail**, **Google Calendar** e **Google Drive** con lo stesso account. Poi, in una chat nuova:
   - «Preparami il briefing di oggi: cosa conta, chi incontro, a chi devo rispondere.»
   - «Tra 10 minuti vedo Marco: cosa ci siamo detti l'ultima volta e cosa devo sapere?»
   - «Chi aspetta una mia risposta da più di 2 giorni? Prepara le bozze.»

   Claude chiede il permesso prima di creare bozze o inviare: fatelo notare al pubblico.

> **La differenza da spiegare:** lo script lavora **da solo, ogni mattina, sempre uguale** (automazione). Claude con MCP lavora **quando glielo chiedete, su quello che chiedete** (agente). Servono tutti e due.
> Per collegare Claude a migliaia di altre app (Slack, Trello, HubSpot…) c'è **Zapier MCP**: il piano gratuito ha 100 attività al mese.

## ⚠️ Privacy: da dire sempre

- Con il **piano gratuito** di Gemini, Google può usare i dati inviati per migliorare i suoi servizi. Per la demo usate un **account di prova con dati finti**.
- Per le email vere di un'azienda servono strumenti approvati dall'azienda (per esempio il piano a pagamento di Gemini o di Claude, o Copilot / Gemini già inclusi in Microsoft 365 / Google Workspace aziendale).

## Se qualcosa non va

| Problema | Cosa fare |
|---|---|
| «Manca GEMINI_API_KEY» | Passo 2.3: il nome della proprietà deve essere esattamente `GEMINI_API_KEY`. |
| Il briefing è vuoto o dice «nessuna email» | Le email devono essere in **Posta in arrivo** (non Promozioni) e arrivate nelle ultime 24 ore. Quelle mandate da voi stessi vengono saltate. |
| Errore 429 | Troppe richieste all'AI gratuita: lo script aspetta e riprova. Riprovate tra un minuto. |
| Il modello non esiste più | In cima allo script cambiate `MODELLO` con un modello Flash elencato in AI Studio. |

---

## Il briefing con Claude

La versione «a parole», con i connettori MCP di Claude (inclusi in Claude Pro).

### 1. Collegate i connettori

**Claude → Impostazioni → Connettori**: premete **Collega** su **Gmail**, **Google Calendar** e **Google Drive** ed entrate con l'account Google.

### 2. Create un Progetto con queste istruzioni

**Progetti → Nuovo progetto** → chiamatelo «Il mio briefing» → incollate nelle **istruzioni del progetto**:

```
Sei il mio assistente personale per organizzare il lavoro. Sono [il vostro ruolo, es. CEO di un'azienda di 40 persone]. Quando ti chiedo il briefing, usa il mio calendario di oggi e le email arrivate da ieri sera. Dimmi cosa conta: le 3 priorità, cosa preparare per ogni riunione, a chi rispondere e perché, cosa può aspettare. Massimo 150 parole, elenchi puntati, prima le cose urgenti. Ignora newsletter e notifiche. Non inventare: se un'informazione manca, dimmelo. Prima di creare bozze, inviare email o creare eventi, chiedimi sempre il permesso.
```

### 3. I prompt pronti (da scrivere dentro il progetto)

- ☀️ `Preparami il briefing di oggi.`
- 🤝 `Tra 10 minuti vedo [nome]: cosa ci siamo detti nelle ultime email e cosa devo sapere?`
- ✉️ `Chi aspetta una mia risposta da più di 2 giorni? Prepara le bozze, ma non inviarle.`
- 📊 `Fammi il riepilogo della settimana: riunioni fatte, decisioni prese, cose rimaste aperte.`
- 📅 `Trova 30 minuti liberi giovedì per me e [nome] e proponimi due orari.`

### 4. I permessi

Claude chiede il permesso ogni volta che usa uno strumento.
- **Leggere** (calendario, email, file): «Consenti sempre» va bene.
- **Scrivere, inviare, creare**: «Consenti una volta», e leggete prima.

### 5. Facoltativo: altre app con Zapier MCP

Su **mcp.zapier.com** scegliete le azioni che Claude può usare (es. Slack, Trello, HubSpot), copiate l'indirizzo del server e incollatelo in **Claude → Connettori → Aggiungi connettore personalizzato**. Piano gratuito: 100 attività al mese.
