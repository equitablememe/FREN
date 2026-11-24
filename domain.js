// Browser-independent notebook contract. No model, transport, or adjudication.
export const VERSION = 1;
export const KINDS = ['observation', 'evidence', 'inference', 'hypothesis', 'contradiction', 'unknown', 'lead', 'next_action'];
export function uid(random = globalThis.crypto) {
  if (typeof random?.randomUUID === 'function') return random.randomUUID();
  // randomUUID is secure-context-only; getRandomValues also supports local HTTP previews.
  const bytes = random.getRandomValues(new Uint8Array(16));
  bytes[6] = (bytes[6] & 15) | 64; bytes[8] = (bytes[8] & 63) | 128;
  const hex = [...bytes].map(b => b.toString(16).padStart(2,'0')).join('');
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
}
const nonempty = (value, label, max = 12000) => {
  if (typeof value !== 'string' || !value.trim() || value.length > max) throw new Error(`${label} must contain 1–${max} characters.`);
  return value.trim();
};
const optional = (value = '', label = 'Field') => {
  if (typeof value !== 'string' || value.length > 4000) throw new Error(`${label} is too long or invalid.`);
  return value.trim();
};
function timestamp(value) {
  if (typeof value !== 'string' || !Number.isFinite(Date.parse(value))) throw new Error('Invalid timestamp.');
  return value;
}
export function emptyState() { return {schema_version: VERSION, revision: 0, notebooks: []}; }
export function newNotebook(question, sample = false) {
  return {id: uid(), question: nonempty(question, 'Question', 300), created_at: new Date().toISOString(), sample, entries: []};
}
export function newEntry({kind, text, source = '', test = ''}) {
  if (!KINDS.includes(kind)) throw new Error('Choose a supported record type.');
  const entry = {id: uid(), kind, text: nonempty(text, 'Note'), source: optional(source, 'Source'), test: optional(test, 'Test'), created_at: new Date().toISOString(), done: false};
  if (kind === 'evidence' && !entry.source) throw new Error('Evidence needs a source. Use “Lead” for an untraced tip.');
  if (kind === 'hypothesis' && !entry.test) throw new Error('Add a test that could disprove this explanation.');
  return entry;
}
export function validateState(raw) {
  if (!raw || raw.schema_version !== VERSION || !Number.isSafeInteger(raw.revision) || raw.revision < 0 || !Array.isArray(raw.notebooks) || raw.notebooks.length > 200) throw new Error('Unsupported or damaged FREN mobile notebook file.');
  if (new TextEncoder().encode(JSON.stringify(raw)).byteLength > 900000) throw new Error('Notebook storage is full (900 KB). Export a backup before continuing in a new browser profile.');
  const ids = new Set();
  let entryCount = 0;
  const checkId = value => {
    const id = nonempty(value, 'Record ID', 100);
    if (ids.has(id)) throw new Error('Duplicate record ID.');
    ids.add(id); return id;
  };
  return {schema_version: VERSION, revision: raw.revision, notebooks: raw.notebooks.map(n => {
    if (!n || !Array.isArray(n.entries) || typeof n.sample !== 'boolean' || (entryCount += n.entries.length) > 5000) throw new Error('Invalid notebook or too many entries.');
    return {id: checkId(n.id), question: nonempty(n.question, 'Question', 300), created_at: timestamp(n.created_at), sample: n.sample, entries: n.entries.map(e => {
      if (!e || !KINDS.includes(e.kind) || typeof e.done !== 'boolean' || (e.done && e.kind !== 'next_action')) throw new Error('Invalid notebook entry.');
      const item = {id: checkId(e.id), kind: e.kind, text: nonempty(e.text, 'Note'), source: optional(e.source), test: optional(e.test), created_at: timestamp(e.created_at), done: e.done};
      if (item.kind === 'evidence' && !item.source) throw new Error('Evidence source is missing.');
      if (item.kind === 'hypothesis' && !item.test) throw new Error('Hypothesis test is missing.');
      return item;
    })};
  })};
}
export function discipline(notebook) {
  const findings = [];
  if (notebook.entries.filter(e => e.kind === 'hypothesis').length === 1 && notebook.entries.some(e => e.kind === 'unknown')) findings.push('Consider another explanation while unknowns remain.');
  return findings;
}
export function toBrief(notebook) {
  const ofKind = kind => notebook.entries.filter(e => e.kind === kind);
  return {
    question: notebook.question,
    evidence: ofKind('evidence').map(e => ({evidence_id: e.id, description: e.text, source_id: e.source, status: 'reported'})),
    hypotheses: ofKind('hypothesis').map(e => ({hypothesis_id: e.id, statement: e.text, status: 'open', supporting_evidence: [], contradicting_evidence: [], falsification_test: e.test})),
    contradictions: ofKind('contradiction').map(e => e.text), unknowns: ofKind('unknown').map(e => e.text),
    leads: ofKind('lead').map(e => e.text), next_actions: ofKind('next_action').filter(e => !e.done).map(e => e.text),
    authority_claim: 'none', discipline_findings: discipline(notebook),
    mobile: {schema_version: VERSION, notebook_id: notebook.id, sample: notebook.sample, created_at: notebook.created_at, entries: structuredClone(notebook.entries), generated_by: 'fren-mobile-0.1.0', model_connected: false, verification_status: 'not_evaluated'}
  };
}
export function backup(state) { return {format: 'FREN-mobile-backup', exported_at: new Date().toISOString(), state: validateState(state)}; }
export function mergeBackup(current, value) {
  if (value?.format !== 'FREN-mobile-backup') throw new Error('Choose a FREN mobile backup, not a single notebook brief.');
  const incoming = validateState(value.state);
  const existing = new Map(current.notebooks.map(n => [n.id, n]));
  const notebooks = [...current.notebooks];
  let added = 0;
  for (const n of incoming.notebooks) {
    const previous = existing.get(n.id);
    if (previous && JSON.stringify(previous) !== JSON.stringify(n)) throw new Error('This backup contains a different version of an existing notebook. Nothing was imported.');
    if (!previous) { notebooks.push(n); added++; }
  }
  return {state: validateState({...current, notebooks}), added};
}
export class NotebookStore {
  constructor(storage, key = 'fren.mobile.v1') { this.storage = storage; this.key = key; }
  load() {
    const raw = this.storage.getItem(this.key);
    return raw === null ? emptyState() : validateState(JSON.parse(raw));
  }
  save(next, expectedRevision) {
    const existing = this.load();
    if (existing.revision !== expectedRevision) throw new Error('Another tab changed your notebooks. Reload before saving; your draft is still here.');
    const checked = validateState({...next, revision: expectedRevision + 1});
    this.storage.setItem(this.key, JSON.stringify(checked));
    return checked;
  }
}
