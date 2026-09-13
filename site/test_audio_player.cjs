// Run with: node --test site/test_audio_player.cjs
const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, 'app.js'), 'utf8');
const playerSource = source.slice(source.indexOf('/* A single recording'));

function player({ saved = null, blocked = false, media = false } = {}) {
  function element(properties = {}) {
    const listeners = {};
    return Object.assign({
      value: '', disabled: true, hidden: true, textContent: '',
      addEventListener(type, fn) { (listeners[type] ||= []).push(fn); },
      emit(type) { (listeners[type] || []).forEach(fn => fn()); }
    }, properties);
  }
  const chapters = [{ title: 'Overview', start: 0 }, { title: 'Chapter 1', start: 60 }, { title: 'Epilogue', start: 120 }];
  const audio = element({ currentTime: 0, duration: NaN, playbackRate: 1, readyState: 0, ended: false, paused: true,
    play() { this.paused = false; this.emit('play'); return Promise.resolve(); },
    pause() { this.paused = true; this.emit('pause'); }
  });
  const ids = { 'book-audio': audio, 'audio-data': { textContent: JSON.stringify({ version: 'edition.mp3', chapters }) } };
  ['audio-chapter', 'audio-speed', 'audio-back', 'audio-forward', 'audio-status', 'audio-extras'].forEach(id => { ids[id] = element(); });
  ids['audio-speed'].options = [0.75, 1, 1.25, 1.5, 1.75, 2].map(value => ({ value: String(value) }));
  const storage = new Map(saved ? [['peopling-audio:edition.mp3', JSON.stringify(saved)]] : []);
  const window = element();
  const document = element({ hidden: false, getElementById: id => ids[id] });
  const localStorage = {
    getItem(key) { if (blocked) throw Error('Storage denied'); return storage.get(key) || null; },
    setItem(key, value) { if (blocked) throw Error('Storage denied'); storage.set(key, value); },
    removeItem(key) { storage.delete(key); }
  };
  const actions = {};
  const navigator = media ? { mediaSession: { setPositionState() {}, setActionHandler(name, fn) {
    if (name === 'seekto') throw Error('Unsupported action');
    actions[name] = fn;
  } } } : {};
  vm.runInNewContext(playerSource, { document, window, navigator, localStorage, Date, isFinite });
  return { audio, ids, actions, window, document,
    metadata() { audio.duration = 180; audio.readyState = 1; audio.emit('loadedmetadata'); },
    saved() { return JSON.parse(storage.get('peopling-audio:edition.mp3') || 'null'); }
  };
}

test('resume waits for metadata and never autoplays or overwrites the saved point early', () => {
  const p = player({ saved: { time: 75, rate: 1.5 } });
  p.audio.emit('timeupdate');
  assert.equal(p.saved().time, 75);
  assert.equal(p.audio.currentTime, 0);
  p.metadata();
  assert.equal(p.audio.currentTime, 75);
  assert.equal(p.audio.playbackRate, 1.5);
  assert.equal(p.audio.paused, true);
  assert.match(p.ids['audio-status'].textContent, /resume at 01:15/);
  assert.equal(p.ids['audio-chapter'].value, '1');
  p.ids['audio-forward'].emit('click'); p.audio.emit('seeked');
  assert.match(p.ids['audio-status'].textContent, /resume at 01:30/);
});

test('chapter and skip controls preserve pause state, clamp time and persist on page exit', () => {
  const p = player(); p.metadata();
  p.ids['audio-back'].emit('click'); assert.equal(p.audio.currentTime, 0);
  p.ids['audio-chapter'].value = '2'; p.ids['audio-chapter'].emit('change');
  assert.equal(p.audio.currentTime, 120); assert.equal(p.audio.paused, true);
  p.audio.currentTime = 175; p.ids['audio-forward'].emit('click');
  assert.equal(p.audio.currentTime, 180);
  p.audio.currentTime = 99; p.window.emit('pagehide'); assert.equal(p.saved().time, 99);
  p.audio.ended = true; p.audio.emit('ended'); assert.equal(p.saved().time, 0);
});

test('blocked storage and unsupported media actions do not break playback controls', () => {
  const p = player({ blocked: true, media: true }); p.metadata();
  assert.equal(p.ids['audio-extras'].hidden, false);
  assert.match(p.ids['audio-status'].textContent, /cannot save/);
  p.actions.play(); assert.equal(p.audio.paused, false);
  p.actions.seekforward({ seekOffset: 30 }); assert.equal(p.audio.currentTime, 30);
  p.actions.nexttrack(); assert.equal(p.audio.currentTime, 60);
  p.ids['audio-speed'].value = '2'; p.ids['audio-speed'].emit('change'); assert.equal(p.audio.playbackRate, 2);
});

test('invalid saved times and rates are ignored', () => {
  const p = player({ saved: { time: 1000000, rate: -5 } }); p.metadata();
  assert.equal(p.audio.currentTime, 0); assert.equal(p.audio.playbackRate, 1);
});
