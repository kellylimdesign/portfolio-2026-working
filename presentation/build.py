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
# same cross-contamination risk in the speaker-notes code: it independently
# reads "whichever .slide is active" to key its notes lookup, unscoped
AI_NOTES_QUERY = "const s = document.querySelector('.slide.active');"
assert ai_script.count(AI_NOTES_QUERY) == 1
ai_script = ai_script.replace(AI_NOTES_QUERY, "const s = document.querySelector('#phaseAgentIdentity .slide.active');")

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
ST_NOTES_QUERY = "const s = document.querySelector('.slide.active');"
assert st_script.count(ST_NOTES_QUERY) == 1
st_script = st_script.replace(ST_NOTES_QUERY, "const s = document.querySelector('#phaseStytch .slide.active');")

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
  }
  .brand{font-family:var(--mono); font-size:12px; letter-spacing:.06em; color:var(--ink-45); justify-self:start;}
  .brand-home{display:inline-flex; align-items:center; gap:6px; color:inherit; text-decoration:none;}
  .brand-home svg{width:14px; height:14px;}
  .brand-home:hover{color:var(--ink);}
  .dots{justify-self:center; display:flex; gap:6px; flex-wrap:wrap; max-width:420px; justify-content:center;}
  .dot{width:6px; height:6px; border-radius:50%; background:var(--line); transition:background .2s;}
  .dot.active{background:var(--ink);}
  .counter-nav{justify-self:end; display:flex; align-items:center; gap:10px;}
  .counter{font-family:var(--mono); font-size:12px; letter-spacing:.06em; color:var(--ink-45);}
  .navbtn{
    width:26px; height:26px; border-radius:50%;
    border:1px solid var(--line); background:transparent;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; color:var(--ink); flex-shrink:0;
  }
  .navbtn:hover{background:var(--ink); color:var(--cream); border-color:var(--ink);}
  .navbtn svg{width:14px; height:14px;}
  /* hide each deck's OWN topbar entirely — the shared one above replaces both */
  #phaseAgentIdentity > .topbar, #phaseStytch > .topbar{display:none !important;}
"""

full_css = GLOBAL_CSS + "\n" + SHARED_TOPBAR_CSS + "\n" + ai_scoped_css + "\n" + st_scoped_css

SHARED_TOPBAR_HTML = """
  <div class="topbar">
    <div class="brand"><a class="brand-home" href="../"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>Back to landing page</a></div>
    <div class="dots" id="sharedDots"></div>
    <div class="counter-nav">
      <button class="navbtn" id="sharedPrevBtn" aria-label="Previous">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
      </button>
      <div class="counter"><span id="sharedCounterNow">01</span> / <span id="sharedCounterTotal">00</span></div>
      <button class="navbtn" id="sharedNextBtn" aria-label="Next">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
      </button>
    </div>
  </div>
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

  function syncTopbar(){
    const gi = currentGlobalIndex();
    counterNowEl.textContent = String(gi + 1).padStart(2, '0');
    dotEls.forEach((d, i) => d.classList.toggle('active', i === gi));
  }

  // each deck's speaker-notes panel/hint is appended straight to <body> by
  // its own script (not inside either phase container), so they don't get
  // hidden by toggling elAI/elST above -- both would otherwise stay visible
  // and stack on top of each other regardless of which phase is showing
  const aiNotesPanel = document.getElementById('agentIdentityNotesPanel');
  const stNotesPanel = document.getElementById('stytchNotesPanel');
  const aiNotesHint = document.getElementById('agentIdentityNotesHint');
  const stNotesHint = document.getElementById('stytchNotesHint');

  function showPhase(phase){
    activePhase = phase;
    elAI.style.display = phase === 'agentIdentity' ? '' : 'none';
    elST.style.display = phase === 'stytch' ? '' : 'none';
    if (aiNotesPanel) aiNotesPanel.style.display = phase === 'agentIdentity' ? '' : 'none';
    if (stNotesPanel) stNotesPanel.style.display = phase === 'stytch' ? '' : 'none';
    if (aiNotesHint) aiNotesHint.style.display = phase === 'agentIdentity' ? '' : 'none';
    if (stNotesHint) stNotesHint.style.display = phase === 'stytch' ? '' : 'none';
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
    if (e.key === 'r' || e.key === 'R') syncTopbar();
  });

  showPhase('agentIdentity');
})();
"""

BOOTSTRAP_JS = """
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
