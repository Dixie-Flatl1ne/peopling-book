(function () {
  var bar = document.getElementById('bar');
  var pct = document.getElementById('pct');
  var rail = document.getElementById('rail');
  var btn = document.getElementById('tocBtn');
  var scrim = document.getElementById('scrim');
  var chapters = [].slice.call(document.querySelectorAll('.chapter, #overview'));
  var navItems = {};
  [].forEach.call(document.querySelectorAll('.nav-ch'), function (li) {
    navItems[li.getAttribute('data-ch')] = li;
  });

  /* ---- mobile contents drawer ---- */
  function setDrawer(open) {
    rail.classList.toggle('open', open);
    scrim.hidden = !open;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  btn.addEventListener('click', function () {
    setDrawer(!rail.classList.contains('open'));
  });
  scrim.addEventListener('click', function () { setDrawer(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setDrawer(false);
  });
  rail.addEventListener('click', function (e) {
    if (e.target.closest('a') && window.matchMedia('(max-width:1120px)').matches) setDrawer(false);
  });

  /* ---- progress + active chapter ---- */
  var active = null;
  function update() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    bar.style.width = (p * 100).toFixed(2) + '%';
    pct.textContent = Math.round(p * 100) + '%';

    var mark = window.scrollY + 140;
    var cur = null;
    for (var i = 0; i < chapters.length; i++) {
      if (chapters[i].offsetTop <= mark) cur = chapters[i];
    }
    if (cur && cur.id !== active) {
      active = cur.id;
      for (var k in navItems) navItems[k].classList.toggle('active', k === active);
      var li = navItems[active];
      if (li && rail.scrollHeight > rail.clientHeight) {
        var top = li.offsetTop, h = li.offsetHeight;
        if (top < rail.scrollTop || top + h > rail.scrollTop + rail.clientHeight) {
          rail.scrollTo({ top: Math.max(0, top - rail.clientHeight / 3), behavior: 'smooth' });
        }
      }
    }
    /* highlight the section inside the active chapter */
    if (active && navItems[active]) {
      var secs = navItems[active].querySelectorAll('.nav-secs li');
      var host = document.getElementById(active);
      var heads = host ? host.querySelectorAll('.sec[id]') : [];
      var idx = -1;
      for (var j = 0; j < heads.length; j++) {
        if (heads[j].offsetTop <= mark) idx = j;
      }
      for (var s = 0; s < secs.length; s++) secs[s].classList.toggle('active', s === idx);
    }
  }

  var ticking = false;
  function onScroll() {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(function () { update(); ticking = false; });
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  document.fonts && document.fonts.ready.then(update);
  update();
})();

/* A single recording keeps chapters continuous during background playback. */
(function () {
  var audio = document.getElementById('book-audio');
  if (!audio) return;
  var data = JSON.parse(document.getElementById('audio-data').textContent);
  var chapters = data.chapters;
  var select = document.getElementById('audio-chapter');
  var speed = document.getElementById('audio-speed');
  var back = document.getElementById('audio-back');
  var forward = document.getElementById('audio-forward');
  var status = document.getElementById('audio-status');
  var key = 'peopling-audio:' + data.version;
  var saved = null, ready = false, currentChapter = -1, lastSave = 0;
  var storageOK = true;
  var media = 'mediaSession' in navigator ? navigator.mediaSession : null;
  try {
    saved = JSON.parse(localStorage.getItem(key));
    localStorage.setItem(key + ':check', '1');
    localStorage.removeItem(key + ':check');
  } catch (e) { storageOK = false; }

  function message() {
    status.textContent = storageOK ? 'Your place is saved on this device.' : 'Playback works, but this browser cannot save your place. Download the MP3 to keep it offline.';
  }
  function stamp(seconds) {
    var n = Math.floor(seconds);
    return (n >= 3600 ? Math.floor(n / 3600) + ':' : '') + String(Math.floor(n / 60) % 60).padStart(2, '0') + ':' + String(n % 60).padStart(2, '0');
  }
  function save() {
    if (!ready || !storageOK) return;
    try {
      localStorage.setItem(key, JSON.stringify({ time: audio.ended ? 0 : audio.currentTime, rate: audio.playbackRate }));
    } catch (e) { storageOK = false; message(); }
    lastSave = Date.now();
  }
  function position() {
    if (media && media.setPositionState && isFinite(audio.duration) && audio.duration > 0) {
      try { media.setPositionState({ duration: audio.duration, playbackRate: audio.playbackRate, position: Math.min(audio.currentTime, audio.duration) }); } catch (e) { /* Optional on older browsers. */ }
    }
  }
  function update() {
    var index = 0;
    for (var i = 1; i < chapters.length; i++) {
      if (chapters[i].start <= audio.currentTime) index = i;
    }
    select.value = String(index);
    if (index !== currentChapter) {
      currentChapter = index;
      if (media && 'MediaMetadata' in window) {
        media.metadata = new MediaMetadata({ title: chapters[index].title, artist: 'Stefan van der Wel', album: 'Peopling · AI narration' });
      }
    }
    position();
  }
  function seek(time) {
    if (!ready || !isFinite(time)) return;
    audio.currentTime = Math.max(0, Math.min(time, audio.duration));
    update();
    save();
  }
  function play() {
    var pending = audio.play();
    if (pending && pending.catch) pending.catch(function () { status.textContent = 'Press play on the audio controls to start listening.'; });
  }
  function metadata() {
    if (ready || !isFinite(audio.duration) || audio.duration <= 0) return;
    ready = true;
    back.disabled = forward.disabled = select.disabled = false;
    message();
    if (saved && typeof saved.rate === 'number' && [].some.call(speed.options, function (option) { return Number(option.value) === saved.rate; })) {
      audio.playbackRate = saved.rate;
      speed.value = String(saved.rate);
    }
    if (saved && typeof saved.time === 'number' && isFinite(saved.time) && saved.time > 0 && saved.time < audio.duration - 2) {
      audio.currentTime = saved.time;
      if (storageOK) status.textContent = 'Ready to resume at ' + stamp(saved.time) + '. Press play.';
    }
    update();
  }
  back.addEventListener('click', function () { seek(audio.currentTime - 15); });
  forward.addEventListener('click', function () { seek(audio.currentTime + 15); });
  select.addEventListener('change', function () { seek(chapters[Number(select.value)].start); });
  speed.addEventListener('change', function () { audio.playbackRate = Number(speed.value); });
  audio.addEventListener('loadedmetadata', metadata);
  audio.addEventListener('timeupdate', function () { update(); if (Date.now() - lastSave > 5000) save(); });
  audio.addEventListener('seeked', function () {
    save();
    message();
    if (storageOK && audio.paused && audio.currentTime > 0) status.textContent = 'Ready to resume at ' + stamp(audio.currentTime) + '. Press play.';
  });
  audio.addEventListener('ratechange', function () { speed.value = String(audio.playbackRate); save(); position(); });
  audio.addEventListener('pause', function () { save(); if (media) media.playbackState = 'paused'; });
  audio.addEventListener('play', function () { message(); if (media) media.playbackState = 'playing'; });
  audio.addEventListener('ended', function () { save(); status.textContent = 'You have reached the end of the book.'; if (media) media.playbackState = 'none'; });
  audio.addEventListener('error', function () { status.textContent = 'The recording could not load. Check your connection and reload, or use the MP3 download link.'; });
  window.addEventListener('pagehide', save);
  document.addEventListener('visibilitychange', function () { if (document.hidden) save(); });
  if (media && media.setActionHandler) {
    var actions = {
      play: play,
      pause: function () { audio.pause(); },
      seekbackward: function (details) { seek(audio.currentTime - (details.seekOffset || 15)); },
      seekforward: function (details) { seek(audio.currentTime + (details.seekOffset || 15)); },
      seekto: function (details) { seek(details.seekTime); },
      previoustrack: function () { seek(chapters[Math.max(0, currentChapter - 1)].start); },
      nexttrack: function () { seek(chapters[Math.min(chapters.length - 1, currentChapter + 1)].start); }
    };
    Object.keys(actions).forEach(function (action) {
      try { media.setActionHandler(action, actions[action]); } catch (e) { /* Not all actions are supported. */ }
    });
  }
  document.getElementById('audio-extras').hidden = false;
  message();
  if (audio.readyState >= 1) metadata();
})();
