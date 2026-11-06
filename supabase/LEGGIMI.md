# Claude per la sfida del Modulo 3

Senza questa funzione il modulo usa solo il modello aperto gratuito di Pollinations. Con questa funzione, nella sfida compare anche Claude. La chiave API resta su Supabase e non arriva mai ai PC.

## Prima di attivarla

Gli studenti hanno 16-18 anni. Le regole di Anthropic chiedono garanzie aggiuntive a chi rende Claude disponibile a minorenni tramite API. Leggi le regole attuali di Anthropic e decidi con la scuola e la Fondazione se attivarla. Questa funzione limita gli argomenti e la lunghezza dei testi, ma non basta da sola a dimostrare che le regole sono rispettate.

## Come attivarla

1. Crea una chiave su console.anthropic.com e imposta un limite di spesa sull'account.
2. Installa la Supabase CLI ed esegui:

   ```
   supabase link --project-ref ylkwwzvhqfwirxqlufai
   supabase secrets set ANTHROPIC_API_KEY=la-tua-chiave
   supabase functions deploy ai --no-verify-jwt
   ```

3. In `stampa-3d-robotica.html` imposta:

   ```
   var M3_AI_URL='https://ylkwwzvhqfwirxqlufai.supabase.co/functions/v1/ai';
   ```

## Costo

Il modello è `claude-opus-5-5` ($4 per milione di token in ingresso, $20 in uscita). La pagina limita ogni studente a 15 richieste per ciascuna delle tre attività con l'AI (gara, banco, braccio): al massimo 1350 per 30 studenti. Ogni risposta è limitata a 4000 token: il caso peggiore, solo in uscita, è circa $108. Di solito si spende molto meno, ma va misurato in una prova. Per spendere meno si può cambiare il modello nella funzione.

Il limite per studente è nella pagina e il limite per classe vale per singola istanza della funzione: il vero tetto di spesa è quello impostato sull'account.
