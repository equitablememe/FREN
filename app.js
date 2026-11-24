import {emptyState, newNotebook, newEntry, validateState, toBrief, backup, mergeBackup, NotebookStore, discipline} from './domain.js';
const $ = id => document.getElementById(id);
const esc = text => String(text).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels = {observation:'Observation', evidence:'Evidence · reported', inference:'Inference', hypothesis:'Hypothesis · open', contradiction:'Contradiction', unknown:'Unknown', lead:'Lead', next_action:'Next step'};
const date = value => new Date(value).toLocaleDateString(undefined, {month:'short', day:'numeric'});
let state = emptyState(), store, selected = null, filter = 'all', timer;
try { store = new NotebookStore(window.localStorage); state = store.load(); }
catch { $('save-status').textContent = 'Storage unavailable · no changes saved'; document.body.classList.add('storage-failed'); }
const storageOkay = !document.body.classList.contains('storage-failed');
if (!storageOkay) $('backup').disabled = true;
function toast(message) { $('toast').textContent = message; $('toast').hidden = false; clearTimeout(timer); timer = setTimeout(() => $('toast').hidden = true, 5500); }
function commit(next) {
  if (!storageOkay) throw new Error('Storage could not be read. Existing data was left untouched. Use another browser or restore a backup there.');
  // Validate and persist before updating the rendered state; failed writes keep form drafts.
  state = store.save(validateState(next), state.revision);
  renderLists();
}
function show(view) {
  document.querySelectorAll('.view').forEach(el => el.hidden = el.id !== `view-${view}`);
  document.querySelectorAll('[data-view]').forEach(el => { const active = el.dataset.view === (view === 'detail' ? 'notebooks' : view); el.classList.toggle('active', active); if (el.closest('nav')) el.setAttribute('aria-current', active ? 'page' : 'false'); });
  if (view === 'steps') renderSteps();
  window.scrollTo({top:0, behavior:'instant'});
}
function empty(title, text) { return `<div class="empty"><span class="empty-mark" aria-hidden="true">✧</span><div><h3>${esc(title)}</h3><p>${esc(text)}</p></div></div>`; }
function notebookCard(n) {
  return `<button class="notebook-card" data-notebook="${esc(n.id)}"><div class="card-top"><span>${n.sample ? 'SAMPLE NOTEBOOK' : 'OPEN NOTEBOOK'}</span><span>${esc(date(n.created_at))}</span></div><h3>${esc(n.question)}</h3><div class="card-bottom"><span>${n.entries.length} ${n.entries.length === 1 ? 'note' : 'notes'} · ${n.entries.filter(e => e.kind === 'unknown').length} open ${n.entries.filter(e => e.kind === 'unknown').length === 1 ? 'question' : 'questions'}</span><span class="arrow" aria-hidden="true">↗</span></div></button>`;
}
function renderLists() {
  const sorted = [...state.notebooks].reverse();
  $('recent-notebooks').innerHTML = sorted.slice(0, 2).map(notebookCard).join('') || empty('Something on your mind?', 'Start with a question. The rest can unfold from there.');
  $('notebook-list').innerHTML = sorted.map(notebookCard).join('') || empty('Your first thread starts here.', 'Create a notebook for an idea, a project, or a question.');
}
function current() { return state.notebooks.find(n => n.id === selected); }
function renderDetail() {
  const n = current(); if (!n) return;
  $('notebook-title').textContent = n.question;
  $('notebook-label').textContent = n.sample ? 'SAMPLE · FICTIONAL PRACTICE NOTES' : `YOUR NOTEBOOK · ${date(n.created_at)}`;
  const findings = discipline(n);
  $('discipline').textContent = findings.join(' '); $('discipline').hidden = !findings.length;
  document.querySelectorAll('[data-filter]').forEach(el => el.classList.toggle('selected', el.dataset.filter === filter));
  const entries = n.entries.filter(e => filter === 'all' || (filter === 'sources' ? ['observation','evidence'].includes(e.kind) : filter === 'questions' ? ['unknown','contradiction'].includes(e.kind) : e.kind === filter));
  $('entry-list').innerHTML = [...entries].reverse().map(e => `<article class="entry" data-kind="${e.kind}"><div class="card-top"><span class="tag">${esc(labels[e.kind])}</span><time datetime="${esc(e.created_at)}">${esc(date(e.created_at))}</time></div><p>${esc(e.text)}</p>${e.source ? `<p class="source">SOURCE · ${esc(e.source)}</p>` : ''}${e.test ? `<p class="test">TEST · ${esc(e.test)}</p>` : ''}</article>`).join('') || empty(filter === 'all' ? 'A fresh page.' : 'Nothing in this view yet.', 'Add a note below to keep the thread going.');
}
function openNotebook(id) {
  if (selected !== id && $('entry-text').value.trim() && !window.confirm('Leave this unsaved note? Copy it first if you want to keep it.')) return;
  if (selected !== id) { $('capture-form').reset(); updateKind(); }
  selected = id; filter = 'all'; renderDetail(); show('detail');
}
function updateKind() {
  const kind = $('entry-kind').value;
  $('test-field').hidden = kind !== 'hypothesis'; $('entry-test').required = kind === 'hypothesis';
  $('entry-source').required = kind === 'evidence'; $('source-hint').textContent = kind === 'evidence' ? '(required)' : '(optional)';
}
function renderSteps() {
  const steps = state.notebooks.flatMap(n => n.entries.filter(e => e.kind === 'next_action').map(e => ({n,e})));
  steps.sort((a,b) => Number(a.e.done) - Number(b.e.done));
  $('step-list').innerHTML = steps.map(({n,e}) => `<article class="step ${e.done ? 'done' : ''}"><input type="checkbox" id="step-${esc(e.id)}" data-step="${esc(e.id)}" ${e.done ? 'checked' : ''}><div><label for="step-${esc(e.id)}">${esc(e.text)}</label><button class="text-button" data-notebook="${esc(n.id)}">${esc(n.sample ? 'Sample · ' : '')}${esc(n.question)} ↗</button></div></article>`).join('') || empty('A little forward motion.', 'Add a “Next step” in a notebook. It will show up here.');
}
function download(value, name) {
  const url = URL.createObjectURL(new Blob([JSON.stringify(value,null,2)], {type:'application/json'}));
  const a = document.createElement('a'); a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
}
document.addEventListener('click', event => {
  const target = event.target.closest('button, a'); if (!target) return;
  if (target.dataset.view) show(target.dataset.view);
  if (target.classList.contains('brand')) { event.preventDefault(); show('home'); }
  if (target.dataset.notebook) openNotebook(target.dataset.notebook);
  if (target.dataset.filter) { filter = target.dataset.filter; renderDetail(); }
  if (target.dataset.action === 'new') { $('new-error').textContent = ''; $('new-dialog').showModal(); $('question').focus(); }
  if (target.dataset.action === 'sample') {
    try {
      const existing = state.notebooks.find(n => n.sample); if (existing) { openNotebook(existing.id); return; }
      const n = newNotebook('Could a repair café work in our town?', true);
      n.entries = [
        newEntry({kind:'observation',text:'Practice example: the community room appears to be unused on Saturday mornings.',source:'Fictional walkthrough note'}),
        newEntry({kind:'hypothesis',text:'Practice example: a monthly repair café could help neighbors keep useful things out of the trash.',test:'Ask ten neighbors to name one item they would bring; revise the idea if there is little interest.'}),
        newEntry({kind:'unknown',text:'Practice example: are volunteers and a suitable room actually available?'}),
        newEntry({kind:'next_action',text:'Practice example: ask the community center about room availability.'})
      ];
      commit({...state, notebooks:[...state.notebooks,n]}); openNotebook(n.id);
    } catch(error) { toast(error.message); }
  }
});
$('cancel-new').addEventListener('click', () => $('new-dialog').close());
$('new-form').addEventListener('submit', event => {
  event.preventDefault();
  try { const n = newNotebook($('question').value); commit({...state,notebooks:[...state.notebooks,n]}); $('new-dialog').close(); $('new-form').reset(); openNotebook(n.id); }
  catch(error) { $('new-error').textContent = error.message; }
});
$('capture-form').addEventListener('submit', event => {
  event.preventDefault(); $('capture-error').textContent = '';
  try {
    const n = current(); if (!n) throw new Error('Open a notebook first.');
    const entry = newEntry(Object.fromEntries(new FormData(event.target)));
    commit({...state,notebooks:state.notebooks.map(item => item.id === n.id ? {...item,entries:[...item.entries,entry]} : item)});
    event.target.reset(); updateKind(); filter = 'all'; renderDetail(); toast('Note saved in this browser.');
  } catch(error) { $('capture-error').textContent = error.message; }
});
$('entry-kind').addEventListener('change', updateKind);
$('jump-capture').addEventListener('click', () => { $('capture-form').scrollIntoView({block:'start',behavior:'instant'}); $('entry-text').focus({preventScroll:true}); });
$('step-list').addEventListener('change', event => {
  const id = event.target.dataset.step; if (!id) return;
  try { commit({...state, notebooks:state.notebooks.map(n => ({...n,entries:n.entries.map(e => e.id === id ? {...e,done:event.target.checked} : e)}))}); renderSteps(); }
  catch(error) { event.target.checked = !event.target.checked; toast(error.message); }
});
$('backup').addEventListener('click', () => { download(backup(state), 'FREN-mobile-backup.json'); toast('Backup download requested.'); });
$('export-brief').addEventListener('click', () => { const n = current(); if(n) { download(toBrief(n), `FREN-brief-${n.id.slice(0,8)}.json`); toast('Notebook brief download requested.'); } });
$('import-file').addEventListener('change', async event => {
  try {
    const file = event.target.files[0]; if (!file) return;
    if (file.size > 1024*1024) throw new Error('Choose a backup smaller than 1 MB.');
    const result = mergeBackup(state, JSON.parse(await file.text()));
    if (result.added) commit(result.state);
    toast(result.added ? `Added ${result.added} notebook(s).` : 'These notebooks are already here.');
  } catch(error) { toast(`Nothing imported. ${error.message}`); }
  finally { event.target.value = ''; }
});
window.addEventListener('beforeunload', event => {
  if ($('entry-text').value.trim() || ($('new-dialog').open && $('question').value.trim())) { event.preventDefault(); event.returnValue = ''; }
});
window.addEventListener('storage', event => { if(event.key === store?.key) toast('Another tab changed your notebooks. Reload after saving a copy of any draft.'); });
let installPrompt;
window.addEventListener('beforeinstallprompt', event => { event.preventDefault(); installPrompt = event; $('install').hidden = false; });
$('install').addEventListener('click', async () => { if(installPrompt) { await installPrompt.prompt(); installPrompt = null; $('install').hidden = true; } });
if ('serviceWorker' in navigator && window.isSecureContext) {
  navigator.serviceWorker.register('./sw.js').then(() => navigator.serviceWorker.ready).then(() => $('offline-status').textContent = 'App shell saved for offline use. Your browser controls storage retention.').catch(() => $('offline-status').textContent = 'Offline shell unavailable. Your notes still use browser storage.');
} else $('offline-status').textContent = 'Offline installation needs HTTPS or localhost.';
renderLists(); updateKind();
