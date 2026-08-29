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
