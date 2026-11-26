'use strict';
// Library app UI. All data comes from library://api/ (see library.py).
const BASE = location.protocol === 'library:' ? 'library://' : location.origin + '/';
const $ = s => document.querySelector(s);
const main = $('#main');
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const enc = encodeURIComponent;

async function api(name, args = {}) {
  const q = Object.entries(args).map(([k, v]) => k + '=' + enc(v)).join('&');
  const r = await (await fetch(BASE + 'api/' + name + (q ? '?' + q : ''))).json();
  if (r && r.error) toast('Sorry: ' + r.error);
  return r;
}

function toast(text) {
  const t = $('#toast');
  t.textContent = text; t.hidden = false;
  clearTimeout(toast.t); toast.t = setTimeout(() => { t.hidden = true; }, 2500);
}

function el(html) {
  const d = document.createElement('div');
  d.innerHTML = html;
  return d;
}

function button(label, onTap, cls = '') {
  const b = document.createElement('button');
  b.innerHTML = label; b.className = cls;
  b.addEventListener('click', onTap);
  return b;
}

// ---------- navigation: a stack of views ----------
const stack = [];
function go(view, replace) {
  if (replace) stack.pop();
  stack.push(view); render();
}
function back() {
  if (!$('#viewer').hidden) return closeViewer();
  if (stack.length > 1) { stack.pop(); render(); }
}
async function render() {
  const view = stack[stack.length - 1];
  $('#back').hidden = stack.length < 2;
  main.innerHTML = ''; main.scrollTop = 0; room('wall');
  await view();
}
$('#back').addEventListener('click', back);
document.addEventListener('keydown', e => { if (e.key === 'Escape') back(); });
const setTitle = t => { $('#title').textContent = t; };
const room = r => { document.body.dataset.room = r; };  // wall, home, desk (lesson), gallery (pictures)

// ---------- home ----------
function home() {
  setTitle('Library'); room('home');
  const d = el(`<div class="home">
    <form><input id="q" type="search" placeholder="Search lessons, books, and pictures" autocomplete="off">
    <button class="primary">Search</button></form>
    <div class="bigrow"></div><div class="smallrow"></div></div>`);
  d.querySelector('form').addEventListener('submit', e => {
    e.preventDefault();
    const q = d.querySelector('#q').value.trim();
    if (q) go(() => search(q));
  });
  d.querySelector('.bigrow').append(
    button('<span class="row"><i></i><i></i><i></i><i></i><i></i><i></i></span><span class="ledge"><b class="brasslabel">Tutorials</b></span>', () => go(topics), 'shelfcase'),
    button('<span class="mat"><img alt=""></span><b class="brasslabel">Inspire</b>', () => go(inspire), 'gilt'));
  d.querySelector('.smallrow').append(button('From Family', () => go(family), 'leather'), button('Notes', () => go(note), 'leather note'));
  main.append(d);
  api('collections').then(c => { if (c[0] && c[0].cover) d.querySelector('.gilt img').src = c[0].cover; });
}

// ---------- tutorials ----------
async function topics() {
  setTitle('Tutorials');
  const list = document.createElement('div');
  list.className = 'shelf';
  for (const t of await api('topics'))
    list.append(button(`<span>${esc(t.name)}</span><span class="sub">${t.done} / ${t.count} done</span>`,
      () => go(() => lessons(t.name))));
  if (!list.children.length) list.textContent = 'No tutorials yet.';
  main.append(list);
}

async function lessons(topic) {
  setTitle(topic);
  const list = document.createElement('div');
  list.className = 'list';
  for (const l of await api('lessons', {topic}))
    list.append(button(`<span>${l.num}. ${esc(l.title)}</span><span>${l.done ? '✓' : ''}</span>`,
      () => go(() => lesson(topic, l.dir))));
  main.append(list);
}

async function lesson(topic, dir) {
  const l = await api('lesson', {topic, dir});
  if (l.error) return;
  setTitle(`${topic} · ${l.num}`); room('desk');
  const d = el(`<div class="spread"><article class="leaf lesson">${l.html}</article><aside class="leaf"></aside></div>`).firstChild;
  const [left, right] = d.children;
  if (l.pages.length) {
    right.append(el('<h2>Book pages</h2>').firstChild);
    const p = document.createElement('div');
    p.className = 'pages';
    for (const pg of l.pages)
      p.append(button(pg.url ? `<img src="${pg.url}" alt=""><span>${esc(pg.source)}, page ${pg.page}</span>`
        : `<div class="missing">Page ${pg.page} is not in the library</div>`,
        () => pg.url && openPage(pg.book, pg.page)));
    right.append(p);
  }
  if (l.other.length) right.append(el(`<p class="other">Also read: ${l.other.map(esc).join('; ')}</p>`).firstChild);
  const nav = document.createElement('div');
  nav.className = 'nav';
  nav.append(button('‹ Previous', () => l.prev && go(() => lesson(topic, l.prev), true)),
    button(l.done ? '✓ Done' : 'Done', async e => {
      await api('done', {topic, dir}); e.target.textContent = '✓ Done'; toast('Well done!');
    }, 'primary'),
    button('Next ›', () => l.next && go(() => lesson(topic, l.next), true)));
  nav.children[0].disabled = !l.prev; nav.children[2].disabled = !l.next;
  left.append(nav);
  d.classList.toggle('single', !right.children.length);
  main.append(d);
}

async function openPage(book, page) {
  const p = await api('page', {book, page});
  if (!p.url) return;
  showViewer(p.url, `${esc(book.replace(/-/g, ' '))} · page ${p.page}`,
    [['Open in Krita', () => krita(p.rel)]],
    dir => { const n = dir > 0 ? p.next : p.prev; if (n) openPage(book, n); }, true, 'felt');
}

// ---------- inspire ----------
async function inspire() {
  setTitle('Inspire'); room('gallery');
  const g = document.createElement('div');
  g.className = 'hang';
  g.append(button("I'm Feeling Lucky<small>A surprise picture</small>", lucky, 'lucky'));
  for (const c of await api('collections'))
    g.append(button(`<span class="gilt"><span class="mat"><img src="${c.cover}" alt=""></span></span><span class="card">${esc(c.name.replace(/^\d+-/, '').replace(/-/g, ' '))}<small>${c.count} picture${c.count === 1 ? "" : "s"}</small></span>`,
      () => go(() => collection(c.name)), 'framed'));
  main.append(g);
}

function imageTools(img) {
  return [['Save', async () => { if ((await api('save', {rel: img.rel})).ok) toast('Saved to Favorites'); }],
          ['Open in Krita', () => krita(img.rel)]];
}

async function lucky() {
  const img = await api('lucky');
  if (!img.url) return toast('No pictures yet.');
  showViewer(img.url, esc(img.credit), [['Next ›', lucky], ...imageTools(img)], () => lucky(), false);
}

async function collection(name) {
  setTitle(name.replace(/^\d+-/, '').replace(/-/g, ' ')); room('gallery');
  const imgs = await api('collection', {name});
  const g = document.createElement('div');
  g.className = 'grid';
  const show = i => {
    const img = imgs[i];
    showViewer(img.url, esc(img.credit), imageTools(img), dir => show((i + dir + imgs.length) % imgs.length));
  };
  imgs.forEach((img, i) => g.append(button(`<img src="${img.url}" loading="lazy" alt="">`, () => show(i))));
  main.append(g);
}

async function krita(rel) {
  if ((await api('krita', {rel})).ok) toast('Opening in Krita…');
}

// ---------- from family + note ----------
async function family() {
  setTitle('From Family'); room('gallery');
  const items = await api('family');
  if (!items.length) main.textContent = 'Nothing here yet.';
  const g = document.createElement('div');
  g.className = 'grid';
  for (const it of items) {
    if (it.kind === 'text') main.append(el(`<h2 class="group">${esc(it.name)}</h2><div class="family-text">${esc(it.text)}</div>`));
    else g.append(button(`<img src="${it.url}" loading="lazy" alt=""><span>${esc(it.name)}</span>`,
      () => showViewer(it.url, esc(it.name), it.rel ? [['Open in Krita', () => krita(it.rel)]] : [])));
  }
  main.prepend(g);
}

async function note() {
  setTitle('Notes');
  const d = el(`<div class="note list"><textarea placeholder="Write a new note here"></textarea></div>`).firstChild;
  const t = d.querySelector('textarea');
  const old = document.createElement('div');
  old.className = 'old-notes';
  async function showOld() {
    old.innerHTML = '';
    const ns = await api('notes');
    if (!ns.length) old.append(el('<p class="other">No notes yet.</p>').firstChild);
    for (const n of ns)
      old.append(el(`<div class="family-text old-note"><b>${esc(n.when)}</b><br>${esc(n.text)}</div>`).firstChild);
  }
  d.append(button('Save note', async () => {
    if (!t.value.trim()) return;
    const r = await api('note', {text: t.value});
    if (r.ok) { toast('Saved'); t.value = ''; showOld(); }
  }, 'primary'));
  d.append(el('<h2 class="group">Your notes</h2>').firstChild, old);
  main.append(d);
  await showOld();
  t.focus();
}

// ---------- search ----------
async function search(q) {
  setTitle('Search: ' + q);
  const r = await api('search', {q});
  const groups = [['Lessons', r.lessons, x => go(() => lesson(x.topic, x.dir))],
                  ['Book pages', r.pages, x => openPage(x.book, x.page)],
                  ['Images', r.images, x => showViewer(x.url, esc(x.credit), imageTools(x))]];
  let any = false;
  for (const [name, items, open] of groups) {
    if (!items || !items.length) continue;
    any = true;
    main.append(el(`<h2 class="group">${name}</h2>`).firstChild);
    const list = document.createElement('div');
    list.className = 'list';
    for (const x of items)
      list.append(button(`<span>${esc(x.title)}<span class="snip">${x.snippet}</span></span>`, () => open(x)));
    main.append(list);
  }
  if (!any) main.append(el('<p>Nothing found. Try another word.</p>').firstChild);
}

// ---------- full-screen viewer: swipe, pinch, drag, double tap ----------
let onSwipe = null, z = {s: 1, x: 0, y: 0};
const vimg = $('#vimg'), stage = $('#stage');
const applyZoom = () => { vimg.style.transform = `translate(calc(-50% + ${z.x}px), calc(-50% + ${z.y}px)) scale(${z.s})`; };

function showViewer(url, caption, tools, swipe, arrows = true, look = 'gallery') {
  z = {s: 1, x: 0, y: 0}; applyZoom();
  vimg.src = url;
  $('#viewer').className = look;  // felt table for book pages, gilt frame for pictures
  $('#vcap').innerHTML = look === 'gallery' ? (caption || '').replace(/ · /g, '<br>') : caption || '';
  const t = $('#vtools');
  t.innerHTML = '';
  if (swipe && arrows) t.append(button('‹', () => swipe(-1)));
  for (const [label, fn] of tools) t.append(button(label, fn));
  t.append(button('−', () => zoomBy(1 / 1.5)), button('+', () => zoomBy(1.5)));
  if (swipe && arrows) t.append(button('›', () => swipe(1)));
  t.append(button('Close', closeViewer, 'primary'));
  onSwipe = swipe || null;
  $('#viewer').hidden = false;
}
function closeViewer() { $('#viewer').hidden = true; vimg.src = ''; }
function zoomBy(f) { z.s = Math.min(8, Math.max(1, z.s * f)); if (z.s === 1) z.x = z.y = 0; applyZoom(); }

const pts = new Map();
let start = null, pinch = null, lastTap = 0;
stage.addEventListener('pointerdown', e => {
  stage.setPointerCapture(e.pointerId);
  pts.set(e.pointerId, {x: e.clientX, y: e.clientY});
  if (pts.size === 1) start = {x: e.clientX, y: e.clientY, zx: z.x, zy: z.y};
  if (pts.size === 2) {
    const [a, b] = [...pts.values()];
    pinch = {d: Math.hypot(a.x - b.x, a.y - b.y), s: z.s};
  }
});
stage.addEventListener('pointermove', e => {
  if (!pts.has(e.pointerId)) return;
  pts.set(e.pointerId, {x: e.clientX, y: e.clientY});
  if (pinch && pts.size === 2) {
    const [a, b] = [...pts.values()];
    z.s = Math.min(8, Math.max(1, pinch.s * Math.hypot(a.x - b.x, a.y - b.y) / pinch.d));
    applyZoom();
  } else if (start && z.s > 1) {
    z.x = start.zx + e.clientX - start.x; z.y = start.zy + e.clientY - start.y; applyZoom();
  }
});
function up(e) {
  if (!pts.has(e.pointerId)) return;
  pts.delete(e.pointerId);
  if (pinch) { if (pts.size === 0) { pinch = null; start = null; if (z.s === 1) { z.x = z.y = 0; applyZoom(); } } return; }
  if (!start) return;
  const dx = e.clientX - start.x, dy = e.clientY - start.y;
  start = null;
  if (z.s === 1 && Math.abs(dx) > 80 && Math.abs(dx) > Math.abs(dy) && onSwipe) return onSwipe(dx < 0 ? 1 : -1);
  if (Math.abs(dx) < 10 && Math.abs(dy) < 10) {
    if (Date.now() - lastTap < 350) { z = z.s > 1 ? {s: 1, x: 0, y: 0} : {s: 2.5, x: 0, y: 0}; applyZoom(); }
    lastTap = Date.now();
  }
}
stage.addEventListener('pointerup', up);
stage.addEventListener('pointercancel', up);
stage.addEventListener('wheel', e => { e.preventDefault(); zoomBy(e.deltaY < 0 ? 1.2 : 1 / 1.2); }, {passive: false});

go(home);
