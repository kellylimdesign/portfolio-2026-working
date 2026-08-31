import os, re, sys

# Rebuilds presentation/index.html from the two standalone case-study decks.
# Run this again after editing agent-identity/index.html or
# stytch-sdk-integration-builder/index.html if you want those changes
# reflected in the merged one-deck presentation:
#   python3 presentation/build.py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from scope_css import scope_css

ROOT = os.path.dirname(HERE)

def read(path):
    with open(path) as f:
        return f.read()

def extract(text, tag):
    m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', text, re.S)
    return m.group(1)

def strip_scripts(text):
    """Remove <script>...</script> blocks (inline and src=) from extracted
    body content — they're pulled out and re-embedded separately/once."""
    return re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.S)

def rewrite_paths(text, prefix):
    """Prefix bare relative asset paths with `prefix` (e.g. '../agent-identity/').
    Leaves absolute/protocol/hash/already-relative(../) refs untouched."""
    def is_bare_relative(p):
        return not re.match(r'^(https?:|mailto:|data:|#|\.\./|/)', p)

    def repl_attr(m):
        attr, quote, val = m.group(1), m.group(2), m.group(3)
        if is_bare_relative(val):
            val = prefix + val
        return f'{attr}={quote}{val}{quote}'

    text = re.sub(r'(src|href|data-src)=("|\')([^"\']*)\2', repl_attr, text)

    def repl_url(m):
        quote = m.group(1) or ''
        val = m.group(2)
        if is_bare_relative(val):
            val = prefix + val
        return f'url({quote}{val}{quote})'

    text = re.sub(r"url\((['\"]?)([^'\")]*)\1\)", repl_url, text)
    return text

# ---------- Agent Identity ----------
ai_html = read(f"{ROOT}/agent-identity/index.html")
ai_style = extract(ai_html, 'style')
ai_body = strip_scripts(extract(ai_html, 'body'))
ai_scripts = re.findall(r'<script>(.*?)</script>', ai_html, re.S)
assert len(ai_scripts) == 1, f"expected 1 inline script in agent-identity, found {len(ai_scripts)}"
ai_script = ai_scripts[0]
# scope this deck's own top-level .slide query to its own phase container --
# both decks' scripts otherwise run `document.querySelectorAll('.slide')`
# completely unscoped, which is correct standalone (only one deck's slides
# exist in that document) but would see BOTH decks' slides once merged here
AI_SLIDES_QUERY = "const slides = document.querySelectorAll('.slide');"
assert ai_script.count(AI_SLIDES_QUERY) == 1
ai_script = ai_script.replace(AI_SLIDES_QUERY, "const slides = document.querySelectorAll('#phaseAgentIdentity .slide');")

ai_scoped_css, ai_globals = scope_css(ai_style, "#phaseAgentIdentity")
print("agent-identity globals:", [g[0] for g in ai_globals])

ai_body = rewrite_paths(ai_body, "../agent-identity/")
ai_scoped_css = rewrite_paths(ai_scoped_css, "../agent-identity/")

# ---------- Stytch ----------
st_html = read(f"{ROOT}/stytch-sdk-integration-builder/index.html")
st_style = extract(st_html, 'style')
st_body = strip_scripts(extract(st_html, 'body'))
st_scripts = re.findall(r'<script>(.*?)</script>', st_html, re.S)
assert len(st_scripts) == 1, f"expected 1 inline script in stytch, found {len(st_scripts)}"
st_script = st_scripts[0]
ST_SLIDES_QUERY = "const slides = Array.from(document.querySelectorAll('.slide')).filter(s => {"
assert st_script.count(ST_SLIDES_QUERY) == 1
st_script = st_script.replace(ST_SLIDES_QUERY, "const slides = Array.from(document.querySelectorAll('#phaseStytch .slide')).filter(s => {")

st_scoped_css, st_globals = scope_css(st_style, "#phaseStytch")
print("stytch globals:", [g[0] for g in st_globals])

st_body = rewrite_paths(st_body, "../stytch-sdk-integration-builder/")
st_scoped_css = rewrite_paths(st_scoped_css, "../stytch-sdk-integration-builder/")
# the external tool.js script tag lives in stytch's <head>, not <body> -- grab separately
assert '<script src="tool.js"></script>' in st_html
tool_js_tag = '<script src="../stytch-sdk-integration-builder/tool.js"></script>'

# ---------- Hand-reconciled global rules (body/html/:root) ----------
GLOBAL_CSS = """
  :root{
    --cream:#FFFFFF;
    --ink:#17161B;
    --ink-70:rgba(23,22,27,.7);
    --ink-45:rgba(23,22,27,.45);
    --line:rgba(23,22,27,.14);
    --bezel:#0E0E10;
    --white:#fff;
    --mono:'Space Mono', ui-monospace, monospace;
    --sans:'Inter', -apple-system, sans-serif;
    --sf-system:-apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
  }
  html, body { height:100%; margin:0; }
  body {
    background:var(--cream); color:var(--ink); font-family:var(--sans);
    overflow:hidden; -webkit-font-smoothing:antialiased;
  }
"""

# .speaker-notes-* rules come back from scope_css() as "global" (see the
# comment in scope_css.py) since each deck's JS appends its notes panel
# straight to <body>, outside either phase container -- both decks define
# the identical rule, so keep just one copy per selector
seen_selectors = set()
notes_css_parts = []
for sel, body in ai_globals + st_globals:
    if sel in ('body', 'html') or sel.startswith('body') or sel.startswith('html'):
        continue  # already hand-reconciled above
    if sel in seen_selectors:
        continue
    seen_selectors.add(sel)
    notes_css_parts.append(f"{sel}{{{body}}}")
GLOBAL_CSS += "\n" + "\n".join(notes_css_parts) + "\n"

SHARED_TOPBAR_CSS = """
  /* ---- shared topbar — drives BOTH case studies as one continuous deck.
     Each deck's own topbar (scoped under #phaseAgentIdentity/#phaseStytch)
     is hidden below; this is the only nav chrome the presenter ever sees. */
  .topbar{
    position:fixed; top:0; left:0; right:0; height:56px;
    display:grid; grid-template-columns:1fr auto 1fr; align-items:center;
    padding:0 64px; z-index:1000; background:var(--cream);
    transition:opacity .3s ease;
  }
  /* the wizard overlay sits above this bar (z-index:1100, see below) so its
     backdrop can visually dim the topbar instead of cutting off underneath
     it — but .topbar itself needs to stay *above* the overlay too, or its
     own position:fixed+z-index stacking context traps sharedPrevBtn/
     sharedNextBtn at z-index:1000 regardless of their own z-index, making
     them unclickable through the overlay. Bumping the whole bar above the
     overlay (1200 > 1100) keeps next/prev usable while a wizard is open —
     which is the deck's own established behavior (the wizard's in-modal
     arrows and the shared next/prev already delegate to the same go()) —
     and fading its opacity down while :has() detects an active wizard
     keeps the "covered" look the overlay's backdrop is going for.
  */
  .topbar{z-index:1200;}
  body:has(#historyOverlay.active) .topbar,
  body:has(#historyOverlay.active) .exit-link,
  body:has(#stytchHistoryOverlay.active) .topbar,
  body:has(#stytchHistoryOverlay.active) .exit-link{opacity:.4;}

  /* matches the per-deck redesign (agent-identity/stytch-sdk-integration-
     builder): plain sans deck-label + centered dots/counter/arrows +
     fixed-corner "Exit", instead of the old mono brand link + circled
     arrows. sharedDeckLabel's text is kept in sync with whichever phase is
     active by showPhase() below ("Twilio" / "Stytch") since this bar spans
     both decks as one continuous presentation. .dots keeps its own
     flex-wrap/max-width (unlike the single-deck versions) since a 22-slide
     combined track needs to wrap. */
  .deck-label{font-family:var(--sans); font-size:13px; color:var(--ink-45); justify-self:start;}
  .dots{display:flex; align-items:center; gap:7px; flex-wrap:wrap; max-width:420px; justify-content:center;}
  .dot{width:6px; height:6px; border-radius:50%; background:var(--line); transition:background .2s;}
  .dot.active{background:var(--ink);}
  .counter-nav{justify-self:center; display:flex; align-items:center; gap:10px;}
  .counter{font-family:var(--sans); font-size:12px; color:var(--ink-45);}
  .navbtn{
    width:26px; height:26px; border:none; background:transparent;
    display:flex; align-items:center; justify-content:center; cursor:pointer;
    color:var(--ink-45); flex-shrink:0; transition:color .15s ease;
  }
  .navbtn:hover{color:var(--ink);}
  .navbtn svg{width:14px; height:14px;}
  /* fixed top-right "Exit" control, same behavior as the standalone decks'
     (just "Exit" at rest, grows to "Exit to landing page" on hover) — sits
     outside .topbar so it isn't a grid item, but still needs the same
     z-index:1200 treatment (and the opacity dim above) to stay usable/
     consistent while the wizard overlay is open. */
  .exit-link{
    position:fixed; top:20px; right:36px; z-index:1200;
    display:inline-block; overflow:hidden; white-space:nowrap; max-width:23px;
    font-family:var(--sans); font-size:13px; font-weight:400; color:var(--ink-45);
    text-decoration:none; transition:color .2s ease, max-width .6s ease;
    background:var(--cream);
  }
  .exit-link:hover{color:var(--ink); max-width:125px;}
  /* Speaker View is presenter-only (opened with the "S" key regardless, see
     COORDINATOR_JS) and doesn't need to be a visible on-screen control —
     kept in the DOM (not removed) so the existing getElementById().onclick
     wiring below still has an element to attach to. */
  .speaker-view-btn{
    display:none;
    appearance:none; cursor:pointer; align-items:center; gap:6px;
    font-family:var(--mono); font-size:11px; letter-spacing:.04em; color:var(--ink-45);
    background:transparent; border:1px solid var(--line); border-radius:20px; padding:5px 12px;
  }
  .speaker-view-btn:hover{color:var(--ink); border-color:var(--ink-45);}
  .speaker-view-btn svg{width:13px; height:13px;}
  /* hide each deck's OWN topbar entirely — the shared one above replaces both */
  #phaseAgentIdentity > .topbar, #phaseStytch > .topbar{display:none !important;}
  /* both phase wrappers hold a child .deck{height:100vh}, and neither wrapper
     itself is taken out of normal flow -- so before showPhase() sets one to
     display:none on the very first render, the page is briefly ~200vh tall
     (both decks' full height stacked) and genuinely scrollable. If anything
     in either deck's own setup code focuses an off-screen element during
     that window, the browser scrolls to reveal it, and because
     history.scrollRestoration defaults to "auto", that stray scroll gets
     re-applied (and can compound further) on every subsequent reload --
     confirmed live: scrollY grew by exactly one slide's 14px fade-in
     transform on each hard refresh. Taking both wrappers out of flow
     entirely removes the scrollable page height in the first place, so
     there's never anywhere for a stray scroll to land. */
  #phaseAgentIdentity, #phaseStytch{position:absolute; inset:0;}
  /* the shared topbar sits at z-index:1000 so it stays above ordinary deck
     content -- but the "how we got here" wizard overlay is only z-index:100
     in the standalone deck (correctly above *its own* topbar, which is a
     much lower z-index:50 there), so once merged it was rendering *behind*
     this shared one instead of covering it. Bump it above the shared topbar
     specifically for the merged build, without touching the standalone
     deck's own (already-correct) stacking. */
  /* !important: this block is concatenated *before* the deck's own scoped
     CSS (same reason the topbar-hiding rule above needs it too) — same
     selector specificity, so without it the later rule would win instead */
  #phaseAgentIdentity .history-overlay{z-index:1100 !important;}
  /* same fix, same reason, for the SDK deck's own single-wizard overlay */
  #phaseStytch .history-overlay{z-index:1100 !important;}
"""

full_css = GLOBAL_CSS + "\n" + SHARED_TOPBAR_CSS + "\n" + ai_scoped_css + "\n" + st_scoped_css

SHARED_TOPBAR_HTML = """
  <div class="topbar">
    <div class="deck-label" id="sharedDeckLabel">Twilio</div>
    <div class="counter-nav">
      <button class="speaker-view-btn" id="speakerViewBtn" title="Open speaker notes in a separate window (S)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 9h18"/></svg>
        Speaker View
      </button>
      <button class="navbtn" id="sharedPrevBtn" aria-label="Previous">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <span class="counter" id="sharedCounterNow">01</span>
      <div class="dots" id="sharedDots"></div>
      <span class="counter" id="sharedCounterTotal">00</span>
      <button class="navbtn" id="sharedNextBtn" aria-label="Next">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
      </button>
    </div>
  </div>

  <a class="exit-link" href="../" aria-label="Exit to landing page">Exit&nbsp;to landing page</a>
"""

COORDINATOR_JS = """
(function(){
  const AI = window.__agentIdentityDeck;
  const ST = window.__stytchDeck;
  const elAI = document.getElementById('phaseAgentIdentity');
  const elST = document.getElementById('phaseStytch');
  const dotsEl = document.getElementById('sharedDots');
  const counterTotalEl = document.getElementById('sharedCounterTotal');
  const counterNowEl = document.getElementById('sharedCounterNow');
  const deckLabelEl = document.getElementById('sharedDeckLabel');

  let activePhase = 'agentIdentity';
  const totalAI = AI.visibleCount;
  const totalST = ST.visibleCount;
  const grandTotal = totalAI + totalST;
  counterTotalEl.textContent = String(grandTotal).padStart(2, '0');

  for (let i = 0; i < grandTotal; i++) {
    const d = document.createElement('div');
    d.className = 'dot';
    d.onclick = () => jumpTo(i);
    dotsEl.appendChild(d);
  }
  const dotEls = dotsEl.querySelectorAll('.dot');

  function currentGlobalIndex(){
    if (activePhase === 'agentIdentity') return AI.currentVisibleNumber() - 1;
    return totalAI + (ST.currentVisibleNumber() - 1);
  }

  // ---- speaker view: a separate window (notes.html) kept in sync with
  // whichever slide/step is on screen here, the same way Keynote/PowerPoint
  // presenter view works -- open once, share only this window/tab, and the
  // notes window (on your other monitor, or your phone) advances itself.
  let speakerWin = null;
  function currentNoteKey(){
    // the "how we got here" wizard is an overlay on top of a slide, not a
    // slide change, so the plain .slide.active lookup below never moves
    // while it's open -- check it first and key off its own step (Trust's
    // wizard has multiple named groups sharing one overlay shell; the SDK
    // deck's is a single, group-less wizard reusing the same overlay/step
    // markup -- #historyOverlay is Trust's original, unrenamed id, and
    // #stytchHistoryOverlay is the SDK deck's own, renamed during the merge
    // specifically to avoid colliding with Trust's, so checking both is
    // unambiguous regardless of which phase is active)
    const aiOverlay = document.getElementById('historyOverlay');
    if (aiOverlay && aiOverlay.classList.contains('active')) {
      const stage = aiOverlay.querySelector('.history-stage.active-group[data-history-group]');
      const stepEl = stage ? stage.querySelector('.history-step.active[data-step]') : null;
      if (stage && stepEl) return 'wizard-' + stage.dataset.historyGroup + '-' + stepEl.dataset.step;
    }
    const stOverlay = document.getElementById('stytchHistoryOverlay');
    if (stOverlay && stOverlay.classList.contains('active')) {
      const stepEl = stOverlay.querySelector('.history-step.active[data-step]');
      if (stepEl) return 'wizard-stytch-journey-' + stepEl.dataset.step;
    }
    const root = activePhase === 'agentIdentity' ? elAI : elST;
    const activeSlide = root.querySelector('.slide.active');
    if (!activeSlide || !activeSlide.id) return null;
    const step = activeSlide.querySelector('.step-nav-item.active');
    // not every step-nav is the shared data-step convention -- the SDK
    // deck's Reference Apps slide uses its own __stepNav (data-src/data-url,
    // no data-step), so `.active` matches but dataset.step is undefined.
    // Falling back to the plain slide id there is correct anyway: notes
    // don't distinguish which reference app is showing, just the one slide.
    return (step && step.dataset.step) ? (activeSlide.id + ':' + step.dataset.step) : activeSlide.id;
  }
  function pushNotesState(){
    if (!speakerWin || speakerWin.closed) return;
    speakerWin.postMessage({ type: 'ai-present-notes', key: currentNoteKey() }, '*');
  }
  function openSpeakerView(){
    if (speakerWin && !speakerWin.closed) { speakerWin.focus(); return; }
    speakerWin = window.open('notes.html', 'aiPresentSpeakerNotes', 'width=520,height=880');
    // a message sent the instant a popup opens can get dropped before the
    // browser finishes wiring up the cross-window channel (confirmed with
    // this exact popup: notes.html's own on-load "ready" ping to us was
    // silently lost every time, while the same postMessage call fired a
    // second later worked fine) -- retrying a few times over ~2s is a cheap,
    // robust fix that doesn't depend on catching that ping at all
    [0, 150, 400, 800, 1500].forEach((delay) => setTimeout(pushNotesState, delay));
  }
  window.addEventListener('message', (e) => {
    if (!e.data || e.source !== speakerWin) return;
    // the speaker view is a full remote control, not just a display: arrow
    // keys pressed there (it has its own focus, separate from this window)
    // and outline-row clicks both drive this deck, which then reports its
    // new state back through the normal syncTopbar() -> pushNotesState()
    // path below -- single source of truth stays here, the notes window
    // never predicts what the deck will do
    if (e.data.type === 'ai-present-notes-ready') pushNotesState();
    if (e.data.type === 'ai-present-nav') go(e.data.dir);
    if (e.data.type === 'ai-present-jump') jumpTo(e.data.globalIdx);
  });
  document.getElementById('speakerViewBtn').onclick = openSpeakerView;

  function syncTopbar(){
    const gi = currentGlobalIndex();
    counterNowEl.textContent = String(gi + 1).padStart(2, '0');
    dotEls.forEach((d, i) => d.classList.toggle('active', i === gi));
    pushNotesState();
  }

  function showPhase(phase){
    activePhase = phase;
    elAI.style.display = phase === 'agentIdentity' ? '' : 'none';
    elST.style.display = phase === 'stytch' ? '' : 'none';
    deckLabelEl.textContent = phase === 'agentIdentity' ? 'Twilio' : 'Stytch';
    syncTopbar();
  }

  function jumpTo(globalIdx){
    if (globalIdx < totalAI) {
      AI.jumpToVisibleNumber(globalIdx + 1);
      showPhase('agentIdentity');
    } else {
      ST.jumpToVisibleNumber(globalIdx - totalAI + 1);
      showPhase('stytch');
    }
  }

  // called from inside each deck's own go() the instant it hits its own
  // edge with nowhere further to go in that direction (see the PRESENT &&
  // ... window.__aiPresentBoundary check in each deck's go()) -- this is
  // the ONLY place phase-switching happens, so it's automatically immune to
  // false positives from step-nav/overlay navigation, which return out of
  // go() before ever reaching that check
  window.__aiPresentBoundary = function(fromPhase, dir){
    if (fromPhase === 'agentIdentity' && dir === 1) {
      showPhase('stytch');
      ST.jumpToFirst();
    } else if (fromPhase === 'stytch' && dir === -1) {
      showPhase('agentIdentity');
      AI.jumpToLast();
    }
    syncTopbar();
  };

  function go(dir){
    if (activePhase === 'agentIdentity') AI.go(dir);
    else ST.go(dir);
    syncTopbar();
  }

  document.getElementById('sharedPrevBtn').onclick = () => go(-1);
  document.getElementById('sharedNextBtn').onclick = () => go(1);
  window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') go(1);
    if (e.key === 'ArrowLeft') go(-1);
    if (e.key === 'r' || e.key === 'R') jumpTo(0);
    if (e.key === 's' || e.key === 'S') openSpeakerView();
  });

  showPhase('agentIdentity');
  window.scrollTo(0, 0);
})();
"""

BOOTSTRAP_JS = """
  // belt-and-suspenders alongside the position:absolute fix on the phase
  // wrappers above: don't let the browser restore/compound a scroll
  // position across reloads at all, in case anything anywhere ever nudges
  // scroll again in the future
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  if (!location.search.includes('present')) {
    location.replace(location.pathname + '?present=1' + location.hash);
  }
"""

out = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Presentation — Building Trust in the Age of AI / Driving SDK Adoption</title>
<script>{BOOTSTRAP_JS}</script>
<style>
{full_css}
</style>
</head>
<body>
{SHARED_TOPBAR_HTML}
<div id="phaseAgentIdentity">
{ai_body}
</div>
<div id="phaseStytch" style="display:none;">
{st_body}
</div>

<script>
  // set before either deck's own script runs, so their keydown listeners
  // gate off their own (now hidden) arrow-key handling in favor of the
  // shared coordinator below
  window.__aiPresentMerged = true;
</script>

{tool_js_tag}

<script>
{ai_script}
</script>

<script>
{st_script}
</script>

<script>
{COORDINATOR_JS}
</script>
</body>
</html>
"""

out_path = f"{ROOT}/presentation/index.html"
with open(out_path, "w") as f:
    f.write(out)
print(f"wrote {out_path}, {len(out)} bytes")
