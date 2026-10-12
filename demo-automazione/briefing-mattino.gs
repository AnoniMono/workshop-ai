/**
 * Automazione «Il briefing del mattino» — demo del workshop AI
 *
 * Ogni mattina:
 *   1. legge l'agenda di oggi (Google Calendar) e le email arrivate da ieri sera (Gmail)
 *   2. scarta newsletter, promozioni e notifiche (regola fissa, senza AI)
 *   3. l'AI (Gemini, piano gratuito) mette in ordine: priorità, riunioni, a chi rispondere
 *   4. vi manda il briefing via email: una pagina sola
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
  'Massimo 150 parole in tutto, frasi brevi. Ignora newsletter e notifiche. Non inventare: se un\'informazione manca, dillo.';

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

  // 4. ⚙️ vi manda il briefing
  GmailApp.sendEmail(io, '☀️ Il tuo briefing di oggi', testoSemplice(b), { htmlBody: html(b, eventi.length, email.length), name: 'Il tuo briefing' });
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

function lista(arr, fn) { return (arr || []).map(fn).join(''); }
function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

function html(b, nEventi, nEmail) {
  var t = function (x) { return '<p style="margin:16px 0 4px;font-weight:bold;color:#4A5568">' + x + '</p>'; };
  return '<div style="font-family:Arial,sans-serif;max-width:560px;color:#1B2A4A;line-height:1.5">' +
    '<h2 style="margin:0 0 4px">☀️ ' + esc(b.saluto || 'Buongiorno!') + '</h2>' +
    '<p style="margin:0;color:#718096;font-size:13px">' + nEventi + ' riunioni · ' + nEmail + ' email lette per te</p>' +
    t('🔴 Le priorità') + '<ul>' + lista(b.priorita, function (p) { return '<li>' + esc(p) + '</li>'; }) + '</ul>' +
    t('📅 Le riunioni') + '<ul>' + lista(b.riunioni, function (r) { return '<li><b>' + esc(r.ora) + ' ' + esc(r.titolo) + '</b>: ' + esc(r.preparare) + '</li>'; }) + '</ul>' +
    t('✉️ A chi rispondere') + '<ul>' + lista(b.rispondere, function (r) { return '<li><b>' + esc(r.chi) + '</b> · ' + esc(r.oggetto) + ': ' + esc(r.perche) + '</li>'; }) + '</ul>' +
    t('🟢 Può aspettare') + '<p style="margin:0">' + esc(b.aspettare) + '</p>' +
    '<p style="margin-top:20px;color:#A0AEC0;font-size:12px">Scritto da un\'AI: può sbagliare. Le decisioni restano tue.</p></div>';
}

function testoSemplice(b) {
  return (b.saluto || 'Buongiorno!') + '\n\nPRIORITÀ\n- ' + (b.priorita || []).join('\n- ') +
    '\n\nRIUNIONI\n' + lista(b.riunioni, function (r) { return '- ' + r.ora + ' ' + r.titolo + ': ' + r.preparare + '\n'; }) +
    '\nA CHI RISPONDERE\n' + lista(b.rispondere, function (r) { return '- ' + r.chi + ' (' + r.oggetto + '): ' + r.perche + '\n'; }) +
    '\nPUÒ ASPETTARE\n' + (b.aspettare || '');
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
