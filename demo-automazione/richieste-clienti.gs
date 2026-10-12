/**
 * Automazione «Richieste dei clienti» — demo del workshop AI
 *
 * Quando arriva un'email nella casella, se non è pubblicità:
 *   1. l'AI (Gemini, piano gratuito) la classifica e scrive una bozza di risposta
 *   2. aggiunge una riga nel foglio «Registro»
 *   3. salva la bozza di risposta in Gmail (NON la invia: la manda una persona)
 *
 * Va incollato in Estensioni → Apps Script di un Foglio Google.
 * Istruzioni complete in GUIDA.md (stessa cartella).
 */

// ---- impostazioni ----
var MODELLO = 'gemini-2.5-flash';           // modello Gemini con piano gratuito
var ETICHETTA = 'AI-gestita';               // etichetta Gmail per le email già lavorate
var CERCA = 'in:inbox newer_than:2d -category:promotions -category:social -label:' + ETICHETTA;
var MAX_PER_GIRO = 10;                      // quante email al massimo per ogni controllo
var PAROLE_SPAM = ['offerta imperdibile', 'solo oggi', 'primi su google', 'unsubscribe', 'disiscriviti', 'newsletter', 'promozione', 'sconto del'];

// la ricetta del prompt (slide 14): ruolo, contesto, compito, formato, esempio/regola
var PROMPT =
  'Sei l\'assistente del servizio clienti di un negozio online di scarpe. ' +
  'Ricevi le email dei clienti scritte alla casella dell\'assistenza. ' +
  'Capisci di cosa si tratta, quale ordine riguarda e quanto è urgente, poi scrivi una bozza di risposta. ' +
  'Rispondi SOLO con JSON con i campi: argomento (spedizione / reso / prodotto / altro), ordine (numero o null), ' +
  'urgenza (bassa / media / alta), riassunto (massimo 10 parole), bozza (massimo 60 parole, dai del Lei, firma «Il team»). ' +
  'Non promettere date o rimborsi che non conosci: se non sei sicuro, scrivi che verifichiamo e ricontattiamo il cliente.';

// ---- menu nel Foglio: per la demo dal vivo non si aspettano i 5 minuti ----
function onOpen() {
  SpreadsheetApp.getUi().createMenu('🤖 Automazione')
    .addItem('▶ Controlla le email adesso', 'controllaEmail')
    .addItem('⚙️ Prima configurazione', 'configura')
    .addItem('⏱ Accendi il controllo ogni 5 minuti', 'accendi')
    .addItem('⏹ Spegni il controllo automatico', 'spegni')
    .addToUi();
}

/** Crea il foglio «Registro» con le intestazioni e i colori dell'urgenza. */
function configura() {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getSheetByName('Registro') || ss.insertSheet('Registro');
  if (sh.getLastRow() === 0) {
    sh.appendRow(['Data', 'Cliente', 'Email', 'Ordine', 'Argomento', 'Urgenza', 'Riassunto', 'Stato']);
    sh.getRange('A1:H1').setFontWeight('bold').setBackground('#1B2A4A').setFontColor('#FFFFFF');
    sh.setFrozenRows(1);
    sh.setColumnWidths(1, 8, 140); sh.setColumnWidth(7, 320);
    var col = sh.getRange('F2:F1000');
    var regole = [
      SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('alta').setBackground('#FDECEA').setFontColor('#C0392B').setRanges([col]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('media').setBackground('#FFF4D6').setFontColor('#B7791F').setRanges([col]).build(),
      SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('bassa').setBackground('#E3F7EC').setFontColor('#1E8E4F').setRanges([col]).build()
    ];
    sh.setConditionalFormatRules(regole);
  }
  if (!GmailApp.getUserLabelByName(ETICHETTA)) GmailApp.createLabel(ETICHETTA);
  if (!PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY')) {
    SpreadsheetApp.getUi().alert('Manca la chiave di Gemini.\n\nIn Apps Script: Impostazioni progetto → Proprietà script → aggiungi GEMINI_API_KEY con la chiave presa da aistudio.google.com.');
  }
}

/** Il cuore dell'automazione: legge le email nuove e le lavora una per una. */
function controllaEmail() {
  var sh = SpreadsheetApp.getActive().getSheetByName('Registro');
  if (!sh) { configura(); sh = SpreadsheetApp.getActive().getSheetByName('Registro'); }
  var etichetta = GmailApp.getUserLabelByName(ETICHETTA) || GmailApp.createLabel(ETICHETTA);
  var io = Session.getActiveUser().getEmail();
  var thread = GmailApp.search(CERCA, 0, MAX_PER_GIRO);
  var fatte = 0;

  thread.forEach(function (t) {
    var m = t.getMessages()[t.getMessageCount() - 1];
    var mittente = m.getFrom();
    if (mittente.indexOf(io) >= 0) { t.addLabel(etichetta); return; }      // le mie email non si lavorano

    // 📏 regola fissa: la pubblicità si ferma qui, senza chiamare l'AI
    var testo = (m.getSubject() + '\n' + m.getPlainBody()).toLowerCase();
    var spam = PAROLE_SPAM.some(function (p) { return testo.indexOf(p) >= 0; });
    if (spam) { t.addLabel(etichetta); return; }

    // 🧠 l'AI classifica e scrive la bozza
    var r = chiediAGemini('Oggetto: ' + m.getSubject() + '\n\n' + m.getPlainBody().slice(0, 4000));
    if (!r) return;                                                           // riproverà al prossimo giro

    // ⚙️ registro e bozza
    var nome = mittente.replace(/<.*>/, '').replace(/"/g, '').trim() || mittente;
    var email = (mittente.match(/<(.+)>/) || [, mittente])[1];
    sh.appendRow([m.getDate(), nome, email, r.ordine || '', r.argomento || '', r.urgenza || '', r.riassunto || '', 'Bozza pronta da controllare']);
    m.createDraftReply(r.bozza || 'Gentile cliente, abbiamo ricevuto la sua richiesta e la ricontattiamo al più presto. Il team');
    t.addLabel(etichetta);
    fatte++;
  });

  if (fatte) SpreadsheetApp.getActive().toast(fatte + ' email lavorate: trovate le bozze in Gmail.', '🤖 Automazione', 5);
}

/** Chiama Gemini e restituisce il JSON della risposta (o null se qualcosa va storto). */
function chiediAGemini(email) {
  var key = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  if (!key) throw new Error('Manca GEMINI_API_KEY nelle Proprietà script.');
  var url = 'https://generativelanguage.googleapis.com/v1beta/models/' + MODELLO + ':generateContent';
  var corpo = {
    systemInstruction: { parts: [{ text: PROMPT }] },
    contents: [{ role: 'user', parts: [{ text: email }] }],
    generationConfig: { responseMimeType: 'application/json', temperature: 0.3 }
  };
  for (var tentativo = 0; tentativo < 3; tentativo++) {
    var res = UrlFetchApp.fetch(url, { method: 'post', contentType: 'application/json', headers: { 'x-goog-api-key': key }, payload: JSON.stringify(corpo), muteHttpExceptions: true });
    if (res.getResponseCode() === 200) {
      try {
        var testo = JSON.parse(res.getContentText()).candidates[0].content.parts[0].text;
        return JSON.parse(testo.replace(/^```json|```$/g, '').trim());
      } catch (e) { console.warn('Risposta non leggibile: ' + res.getContentText()); return null; }
    }
    if (res.getResponseCode() === 429) { Utilities.sleep(15000); continue; }  // troppe richieste: aspetta e riprova
    console.warn('Errore Gemini ' + res.getResponseCode() + ': ' + res.getContentText());
    return null;
  }
  return null;
}

/** Controllo automatico ogni 5 minuti. */
function accendi() {
  spegni();
  ScriptApp.newTrigger('controllaEmail').timeBased().everyMinutes(5).create();
  SpreadsheetApp.getActive().toast('Controllo ogni 5 minuti acceso.', '🤖 Automazione', 5);
}
function spegni() {
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'controllaEmail') ScriptApp.deleteTrigger(t); });
}
