/**
 * Automazione «Il briefing del mattino» — demo del workshop AI
 *
 * Ogni mattina:
 *   1. legge l'agenda di oggi (Google Calendar) e le email arrivate da ieri sera (Gmail)
 *   2. scarta newsletter, promozioni e notifiche (regola fissa, senza AI)
 *   3. l'AI (Gemini, piano gratuito) mette in ordine: priorità, riunioni, a chi rispondere
 *   4. vi manda il briefing su Telegram: un messaggio solo, sul telefono
 *
 * Non manda niente a nessun altro e non risponde a nessuno: le decisioni restano vostre.
 * Istruzioni complete in GUIDA.md (stessa cartella).
 */

// ---- impostazioni ----
var MODELLO = 'gemini-2.5-flash';           // modello Gemini con piano gratuito (vedi aistudio.google.com)
var ORA = 7;                                 // il briefing arriva tra le 7 e le 8
var CERCA = 'in:inbox newer_than:1d -category:promotions -category:social -category:updates -category:forums';
var MAX_EMAIL = 25;
var NON_IMPORTANTI = ['noreply', 'no-reply', 'newsletter', 'notifiche', 'notification', 'unsubscribe', 'disiscriviti'];

// la ricetta del prompt (slide 14): ruolo, contesto, compito, formato, regole
var PROMPT =
  'Sei l\'assistente personale di una persona molto impegnata. ' +
  'Ogni mattina ricevi la sua agenda di oggi e le email arrivate dalla sera prima. ' +
  'Dimmi cosa conta oggi: le 3 priorità, cosa preparare per ogni riunione (usando le email con le persone che incontra), ' +
  'a chi rispondere e perché, e cosa può aspettare. ' +
  'Rispondi SOLO con JSON con i campi: saluto (una frase), priorita (massimo 3 frasi), ' +
  'riunioni (lista di {ora, titolo, preparare}), rispondere (lista di {chi, oggetto, perche}), aspettare (una frase). ' +
  'Massimo 150 parole in tutto, frasi brevi: si legge sul telefono. Ignora newsletter e notifiche. Non inventare: se un\'informazione manca, dillo.';

/** ▶ Il cuore dell'automazione. Si può lanciare a mano per la demo (Esegui) o dal timer. */
function briefing() {
  var io = Session.getActiveUser().getEmail();
  var oggi = new Date();

  // 1. agenda di oggi
  var eventi = CalendarApp.getDefaultCalendar().getEventsForDay(oggi).filter(function (e) { return !e.isAllDayEvent(); });
  var agenda = eventi.map(function (e) {
    var ospiti = e.getGuestList().map(function (g) { return g.getEmail(); }).filter(function (m) { return m !== io; });
    var precedente = '';
    if (ospiti.length) {                                   // l'ultima email scambiata con chi incontro
      var t = GmailApp.search('(from:' + ospiti[0] + ' OR to:' + ospiti[0] + ')', 0, 1)[0];
      if (t) precedente = ' | ultima email con ' + ospiti[0] + ': «' + t.getFirstMessageSubject() + '» ' + t.getMessages().pop().getPlainBody().slice(0, 300);
    }
    return Utilities.formatDate(e.getStartTime(), Session.getScriptTimeZone(), 'HH:mm') + ' ' + e.getTitle() +
      (ospiti.length ? ' (con ' + ospiti.join(', ') + ')' : '') + precedente;
  });

  // 2. email da ieri sera, senza il rumore (📏 regola fissa)
  var email = [];
  GmailApp.search(CERCA, 0, MAX_EMAIL).forEach(function (t) {
    var m = t.getMessages().pop(), da = m.getFrom().toLowerCase();
    if (da.indexOf(io.toLowerCase()) >= 0) return;
    if (NON_IMPORTANTI.some(function (p) { return da.indexOf(p) >= 0; })) return;
    email.push('Da: ' + m.getFrom() + ' | Oggetto: ' + m.getSubject() + ' | ' + m.getPlainBody().replace(/\s+/g, ' ').slice(0, 400));
  });

  // 3. 🧠 l'AI mette in ordine
  var dati = 'AGENDA DI OGGI:\n' + (agenda.join('\n') || 'nessuna riunione') + '\n\nEMAIL ARRIVATE:\n' + (email.join('\n') || 'nessuna email importante');
  var b = chiediAGemini(dati);
  if (!b) { console.warn('L\'AI non ha risposto: riprova tra qualche minuto.'); return; }

  // 4. ⚙️ vi manda il briefing su Telegram
  inviaTelegram(messaggio(b, eventi.length, email.length));
}

function chiediAGemini(dati) {
  var key = PropertiesService.getScriptProperties().getProperty('GEMINI_API_KEY');
  if (!key) throw new Error('Manca GEMINI_API_KEY: Impostazioni progetto → Proprietà script.');
  var corpo = {
    systemInstruction: { parts: [{ text: PROMPT }] },
    contents: [{ role: 'user', parts: [{ text: dati }] }],
    generationConfig: { responseMimeType: 'application/json', temperature: 0.3 }
  };
  for (var i = 0; i < 3; i++) {
    var res = UrlFetchApp.fetch('https://generativelanguage.googleapis.com/v1beta/models/' + MODELLO + ':generateContent', {
      method: 'post', contentType: 'application/json', headers: { 'x-goog-api-key': key }, payload: JSON.stringify(corpo), muteHttpExceptions: true });
    if (res.getResponseCode() === 200) {
      try { return JSON.parse(JSON.parse(res.getContentText()).candidates[0].content.parts[0].text.replace(/^```json|```$/g, '').trim()); }
      catch (e) { console.warn('Risposta non leggibile: ' + res.getContentText()); return null; }
    }
    if (res.getResponseCode() === 429) { Utilities.sleep(15000); continue; }   // troppe richieste: aspetta e riprova
    console.warn('Errore Gemini ' + res.getResponseCode() + ': ' + res.getContentText()); return null;
  }
  return null;
}

/* ---- Telegram ---- */
function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

/** Il messaggio, in HTML semplice (Telegram accetta solo <b>, <i> e pochi altri). */
function messaggio(b, nEventi, nEmail) {
  var righe = function (arr, fn) { return (arr || []).map(fn).join('\n'); };
  return '☀️ <b>' + esc(b.saluto || 'Buongiorno!') + '</b>\n<i>' + nEventi + ' riunioni · ' + nEmail + ' email lette per te</i>\n\n' +
    '🔴 <b>Le priorità</b>\n' + righe(b.priorita, function (p) { return '• ' + esc(p); }) + '\n\n' +
    '📅 <b>Le riunioni</b>\n' + righe(b.riunioni, function (r) { return '• <b>' + esc(r.ora) + ' ' + esc(r.titolo) + '</b>: ' + esc(r.preparare); }) + '\n\n' +
    '✉️ <b>A chi rispondere</b>\n' + righe(b.rispondere, function (r) { return '• <b>' + esc(r.chi) + '</b> · ' + esc(r.oggetto) + ': ' + esc(r.perche); }) + '\n\n' +
    '🟢 <b>Può aspettare</b>\n' + esc(b.aspettare) + '\n\n<i>Scritto da un\'AI: può sbagliare. Le decisioni restano tue.</i>';
}

function inviaTelegram(testo) {
  var p = PropertiesService.getScriptProperties(), token = p.getProperty('TELEGRAM_TOKEN'), chat = p.getProperty('TELEGRAM_CHAT_ID');
  if (!token) throw new Error('Manca TELEGRAM_TOKEN: Impostazioni progetto → Proprietà script.');
  if (!chat) throw new Error('Manca TELEGRAM_CHAT_ID: scrivete /start al vostro bot e lanciate collegaTelegram.');
  var res = UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    payload: JSON.stringify({ chat_id: chat, text: testo, parse_mode: 'HTML', disable_web_page_preview: true }) });
  if (res.getResponseCode() !== 200) console.warn('Errore Telegram ' + res.getResponseCode() + ': ' + res.getContentText());
}

/** 🔗 Da lanciare una volta sola, DOPO aver scritto /start al vostro bot su Telegram: trova la vostra chat e la salva. */
function collegaTelegram() {
  var p = PropertiesService.getScriptProperties(), token = p.getProperty('TELEGRAM_TOKEN');
  if (!token) throw new Error('Prima mettete TELEGRAM_TOKEN nelle Proprietà script.');
  var r = JSON.parse(UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/getUpdates', { muteHttpExceptions: true }).getContentText());
  var msg = (r.result || []).map(function (u) { return u.message; }).filter(Boolean).pop();
  if (!msg) throw new Error('Nessun messaggio trovato: aprite il bot su Telegram, scrivete /start e rilanciate.');
  p.setProperty('TELEGRAM_CHAT_ID', String(msg.chat.id));
  inviaTelegram('✅ Collegato! Da domani il briefing arriva qui.');
  console.log('Fatto: chat ' + msg.chat.id + ' collegata.');
}

/** ⏱ Accende il briefing automatico ogni mattina (tra le ORA e le ORA+1). */
function accendi() {
  spegni();
  ScriptApp.newTrigger('briefing').timeBased().everyDays(1).atHour(ORA).create();
  console.log('Fatto: il briefing arriverà ogni mattina tra le ' + ORA + ' e le ' + (ORA + 1) + '.');
}
function spegni() {
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'briefing') ScriptApp.deleteTrigger(t); });
}
