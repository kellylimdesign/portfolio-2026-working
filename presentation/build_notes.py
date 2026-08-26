import json, os, html

# Rebuilds presentation/notes.html (the synced "mini deck" speaker view) from
# the slide metadata below + presentation/notes-thumbs.json (screenshots —
# see capture_thumbs.py). Run this after editing notes content or re-running
# the thumbnail capture:
#   python3 presentation/build_notes.py

HERE = os.path.dirname(os.path.abspath(__file__))
THUMBS = json.load(open(os.path.join(HERE, "notes-thumbs.json")))

# ordered 1:1 with the deck's own 21-slide sequence; step-grouped slides
# (End User Journey, Customer Journey, Journey) contribute one entry per step,
# all sharing the same "num" badge since they're one slide in the deck
DECK = [
    dict(key="slideAboutMe", num="01", section="Intro", title="About Me", time="1–2 min", notes=[
        "Intro: Senior Product Designer @ Twilio, previously Stytch (acquired by Twilio, Nov 2025).",
        "Throughline for both case studies: identity is moving beyond static credentials — from verifying humans to also verifying and constraining AI agents acting on their behalf.",
        "Order: Agent Identity first (Twilio), then the Stytch SDK Integration Builder.",
    ]),
    dict(key="slideHero", num="02", section="Building Trust in the Age of AI", title="Hero", time="30 sec", notes=[
        "Title card — let it breathe. Land one line: identity for a brand-new kind of actor, the AI agent.",
    ]),
    dict(key="slideProblem", num="03", section="Building Trust in the Age of AI", title="The Problem — A New Kind of Actor", time="1.5 min", notes=[
        "Twilio has strong identity primitives for humans (Verify, Lookup — phone/email) but nothing to authenticate or authorize <strong>AI agents</strong> acting on a user's behalf.",
        "It's also an opportunity: expand from a point solution in Identity into a full Identity platform — an underserved but eager market. Ties to the Nov 2025 Stytch acquisition thesis: identity has to handle delegated/agent operations, and distinguish humans, trusted agents, and rogue agents.",
        "Ground it immediately with Owl Trade so it's not abstract: a fictional trading app whose users want to connect ChatGPT to trade for them — how do you do that safely?",
    ]),
    dict(key="slideOverview", num="04", section="Building Trust in the Age of AI", title="Overview", time="1 min", notes=[
        "Let the headline animation play (point solution → full identity platform) — don't talk over it.",
        "Team: 1 designer (you), 1 PM, 5 engineers.",
        "Status: 5 design partners onboarded now, private beta targeted Fall 2026 — sets up that impact will be forward-looking, not shipped-usage numbers.",
    ]),
    dict(key="slidePersona", num="05", section="Building Trust in the Age of AI", title="Persona — Two Users, Two Moments", time="1 min", notes=[
        "Two moments, two audiences: the Builder (configures identity + approvals ahead of time — Owl Trade) and the End User (asked in the moment whether an agent can act for them — Alex).",
        "Worth naming: there are two initiation patterns in the real product beyond this demo — a platform proactively opening itself to agents, vs. a user asking a third-party agent to act inside a platform they already use (this demo is the second one).",
    ]),
    dict(key="slideOwlTradeIntro", num="06", section="Building Trust in the Age of AI", title="Can ChatGPT Trade For You — Safely?", time="1 min", notes=[
        "Set the scene concretely: Alex is a commodities trader who wants ChatGPT to watch and trade OJ futures on Owl Trade for him.",
        "Flag once: Owl Trade and Alex are fictional/illustrative, not a real customer.",
    ]),
    dict(key="slideEndUserJourney-1", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 1 — Request", time="1 min", notes=[
        "Alex asks ChatGPT to do something; ChatGPT flags it needs Owl Trade access and surfaces Owl Trade's own integration right there.",
        'Live mock: click the "+" to open Explore Apps → Owl Trade. It autoplays briefly on its own — let it run.',
    ]),
    dict(key="slideEndUserJourney-2", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 2 — Log in", time="30 sec", notes=[
        "Before ChatGPT is trusted with anything, Alex proves it's really him — the same login he always uses. Deliberately no new trust mechanism invented here.",
    ]),
    dict(key="slideEndUserJourney-3", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 3 — Grant Access", time="1.5 min", notes=[
        "Alex sees exactly what ChatGPT is asking for and can allow/deny before anything connects.",
        'Real design-iteration point (V1 simple → V4 risk-tiered) lives behind "See how we got here" — skipping that detour today for time, but it\'s there if asked.',
        "Landed on a familiar OAuth-style consent screen: reusing a mental model people already trust beats inventing a new one.",
    ]),
    dict(key="slideEndUserJourney-4", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 4 — Act on your behalf", time="30 sec", notes=[
        "Once granted, ChatGPT acts autonomously — watching futures, deciding, following through — without Alex clicking every step.",
        "That autonomy is the whole point of agents, and exactly why the human-in-the-loop safety net (coming up) has to exist.",
    ]),
    dict(key="slideOneConsole", num="08", section="Building Trust in the Age of AI", title="One Console, Every Setting", time="30 sec", notes=[
        "All of this — verify identity, customize consent, manage agents, high-risk approvals — configured in one place: Twilio Console, next to a customer's other Twilio point solutions. Not a separate product to learn.",
    ]),
    dict(key="slideCustomerJourney-1", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 1 — Connect, Don't Rebuild", time="1.5 min", notes=[
        "Most customers already have their own auth system (Owl Trade uses Okta). Twilio doesn't replace it — it validates a JWT that system hands off.",
        "Mechanics if asked: customer's auth issues a JWT → Twilio tells them the expected issuer/audience/claim schema → JWT + public keys validated against a console-configured profile → after consent, Twilio issues an agent token.",
        "<strong>This console demo is scripted/autoplaying</strong> — let it run, don't click ahead of it (a stray click cancels the script mid-flight).",
    ]),
    dict(key="slideCustomerJourney-2", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 2 — Customize the consent screen", time="1.5 min", notes=[
        "Owl Trade drops in its own logo so approving an agent feels like part of their product, not a hand-off elsewhere.",
        "Why just logo for now, deliberately: it's the one brand element Twilio can't replicate; color/copy/font need accessibility guardrails better solved once this is absorbed into the future full hosted-login flow — designed for that migration from day one, not bolted on later.",
    ]),
    dict(key="slideCustomerJourney-3", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 3 — Manage agents", time="2 min", notes=[
        "Owl Trade views/adjusts every agent's access directly in console — no separate tooling.",
        '<strong>Clients</strong> = which agents/apps are connected and what they\'re scoped to. Deleting one revokes access for <em>all</em> users at once — a bigger, more deliberate action with different confirmation messaging than a per-user revoke. Answers: "which AI agents have my users authorized, and what can they do?"',
        "<strong>Identities</strong> = the per-user view, for targeted lookup/revocation. Revoking here is reversible — the user is just re-prompted for consent next time, not locked out.",
    ]),
    dict(key="slideCustomerJourney-4", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 4 — High-risk approvals", time="1.5 min", notes=[
        "Agents are async/autonomous by design — that's the value, not a bug — but it means the human may not be present when the agent acts, so high-risk/irreversible actions need to re-engage them first.",
        "Why SMS/RCS specifically: not just familiarity — it reuses Twilio's own Verify messaging infra instead of building new channel infra, RCS-first for a branded single-click approval with SMS as fallback, and email was deliberately cut for v1 to limit scope.",
    ]),
    dict(key="slideChallenges", num="10", section="Building Trust in the Age of AI", title="Challenges", time="1.5 min", notes=[
        "Cross-team dependency between the identity/RCS teams and Verify.",
        "A genuinely new bet with no internal playbook to copy.",
        "Some demos/flows were speculative — built ahead of the product actually existing.",
        "API scope was still being negotiated with engineering mid-design (one planned reverse-lookup link between Clients and Identities got cut from scope).",
    ]),
    dict(key="slideValidating", num="11", section="Building Trust in the Age of AI", title="What We're Validating", time="1.5 min", notes=[
        "No usage data yet — pre-launch, currently in a structured design-partner program ahead of Fall 2026 private beta.",
        "Five real open questions on the table: consent-screen customization beyond a logo, config clarity, which platform actions need HITL, what custom scopes partners need, what to solve next.",
        "Ties back to what these bets are in service of: usage (accounts/agent identities), brand affinity in the Identity market, ARR.",
    ]),
    dict(key="slideHeroStytch", num="12", section="Driving SDK Adoption", title="Hero", time="30 sec", notes=[
        "Title card. Prebuilt SDK auth UI was supposed to be the fast path — no components to build — but adoption didn't match that promise.",
    ]),
    dict(key="slideProblemStytch", num="13", section="Driving SDK Adoption", title="The Problem — Fast Auth, Slow Evaluation", time="1.5 min", notes=[
        "The SDK's whole pitch was fast auth. But <em>evaluating</em> it wasn't fast — customers had no way to know if it actually fit their product without integrating it first.",
        "First read was a capability gap — closed API feature-parity gaps first. Customers still weren't adopting. The real blocker was never capability, it was proof/confidence.",
        "<strong>This is the deck's throughline: feature parity ≠ confidence.</strong>",
    ]),
    dict(key="slidePersonaStytch", num="14", section="Driving SDK Adoption", title="Persona — Two Audiences, One Tool", time="1 min", notes=[
        "Two audiences: the Evaluator (a team deciding if Stytch fits, before writing code) and the Solutions Engineer (Stytch's own team, who used to hand-build one-off demos to answer exactly the Evaluator's question).",
        "Don't spoil it yet, but unlike Owl Trade's two personas, the SE side isn't hypothetical — it pays off on the Impact slide.",
    ]),
    dict(key="demoSlide", num="15", section="Driving SDK Adoption", title="The Ask", time="30 sec", notes=[
        'Customers kept asking the same concrete question: "what would this actually look like inside <em>my</em> product?" The closest thing Stytch had were example apps.',
    ]),
    dict(key="demoSelectSlide", num="16", section="Driving SDK Adoption", title="Reference Apps", time="1.5 min", notes=[
        "Hello Socks / Survey Amp: real example apps built on the SDK. They help, but only show what the SDK looks like generically — not what it'd look like for a customer's own product, which is the actual question.",
        'Click through one or both briefly — this is meant to land as "close, but not quite the answer."',
    ]),
    dict(key="slideSolution", num="17", section="Driving SDK Adoption", title="The Solution", time="1 min", notes=[
        "The answer wasn't another demo — it was a tool: an interactive playground, live, before any code is written. This is the pivot into the deck's centerpiece.",
    ]),
    dict(key="journeySlide-1", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 1 — Explore Stytch's products", time="1.5 min", notes=[
        "Full product catalog as a button grid, not hidden behind a dropdown/search — deliberate, since customers evaluating Stytch often don't know the full catalog exists yet.",
        "The live tool autoplays through several product chips on its own — let it play, nothing to click.",
    ]),
    dict(key="journeySlide-2", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 2 — Branding", time="1.5 min", notes=[
        'One flat panel of properties, not sections/tabs you already have to know to look in — styling questions kept breaking down over "where does this property even show up?"',
        "Root cause: auditing the SDK's real config showed the mapping between the design system and the SDK's settings had drifted as things scaled — even the Stytch team couldn't always say what mapped to what. Fixing this meant refactoring the SDK's actual styling object, in close collaboration with engineering.",
        '<em>"See how we got here"</em> link covers the dropdown-vs-grid and tabbed-vs-flat decisions — skipping the detour today for time, mention it\'s there.',
    ]),
    dict(key="journeySlide-3", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 3 — Try the real flow, not a screenshot", time="1.5 min", notes=[
        "Not a static preview — a fully working SDK instance. Customers click through the real sign-up/login flow (email → OTP → success) to judge brand fit AND actual behavior at once.",
        "<strong>This step is fully scripted</strong> (auto-types email, auto-fills OTP, shows success) — just narrate over it.",
    ]),
    dict(key="journeySlide-4", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 4 — Shippable code", time="1 min", notes=[
        'View Code turns the live config into a real integration snippet the moment evaluation ends — "how do I get this into my product, quickly" is already answered, not a separate build step.',
    ]),
    dict(key="slideChallengesStytch", num="19", section="Driving SDK Adoption", title="Challenges", time="1.5 min", notes=[
        "Not a roadmap project — started as a Hack Week idea, needed leadership buy-in to get fully productionized.",
        "The smooth customization experience only worked because the SDK's actual styling config got refactored first — working closely with engineering, not just a UI layer on top of what existed.",
    ]),
    dict(key="slideImpact", num="20", section="Driving SDK Adoption", title="Impact", time="1.5 min", notes=[
        "No adoption/conversion numbers yet, but real validation: the Solutions Engineers whose one-off demos this replaced started using the Integration Builder themselves, on real customer and prospect calls.",
        "Recap: fast/easy preview replacing the SE-demo workaround, View Code cutting time-to-value, customers now validating product fit/brand fit/real UX flows themselves instead of taking it on faith.",
    ]),
    dict(key="slideThankYou", num="21", section="Driving SDK Adoption", title="Thank You / Questions?", time="1 min", notes=[
        "Thank you — open it up to questions.",
    ]),
]

for d in DECK:
    d.setdefault("step", None)
    if d["key"] not in THUMBS:
        raise SystemExit(f"missing thumbnail for {d['key']!r} — run capture_thumbs.py")
    d["thumb"] = THUMBS[d["key"]]


def esc(s):
    return html.escape(s, quote=True)


def render_notes_li(items):
    return "".join(f"<li>{it}</li>" for it in items)


def deck_json_entry(d):
    return {
        "key": d["key"],
        "num": d["num"],
        "section": d["section"],
        "title": d["title"],
        "step": d["step"],
        "time": d["time"],
        "notesHtml": render_notes_li(d["notes"]),
        "thumb": "data:image/jpeg;base64," + d["thumb"],
    }


# escape a literal "</script" so it can't prematurely close the <script
# type="application/json"> tag it's embedded in -- defensive; none of the
# authored notes/images contain this today, but edits saved later will
# round-trip through this same file format so it's worth guarding for good
DECK_JSON = json.dumps([deck_json_entry(d) for d in DECK]).replace("</script", "<\\/script")

OUTLINE_ROWS = []
for d in DECK:
    title = d["title"] if not d["step"] else f'{d["title"]} — {d["step"]}'
    OUTLINE_ROWS.append(
        f'<button class="outline-row" data-key="{esc(d["key"])}">'
        f'<span class="outline-num">{d["num"]}</span>'
        f'<span class="outline-title">{esc(title)}</span>'
        f'<span class="outline-time">{esc(d["time"])}</span>'
        f'</button>'
    )
OUTLINE_HTML = "\n".join(OUTLINE_ROWS)

TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Speaker Notes — Building Trust / Driving SDK Adoption</title>
<style>
  :root{
    --ink:#17161B;
    --ink-70:rgba(23,22,27,.72);
    --ink-45:rgba(23,22,27,.48);
    --line:rgba(23,22,27,.13);
    --paper:#FBFAF8;
    --card:#F3F1EC;
    --sans:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --mono:ui-monospace, "SF Mono", "Space Mono", Menlo, Consolas, monospace;
  }
  *{box-sizing:border-box;}
  html,body{margin:0; padding:0; height:100%;}
  body{
    background:var(--paper); color:var(--ink); font-family:var(--sans);
    -webkit-font-smoothing:antialiased; line-height:1.5;
    display:flex; flex-direction:column; min-height:100%;
  }
  .page{max-width:640px; margin:0 auto; padding:20px 20px 40px; width:100%;}

  header{margin-bottom:16px;}
  .eyebrow-row{display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:10px;}
  .eyebrow{
    font-family:var(--mono); font-size:11px; letter-spacing:.09em; text-transform:uppercase;
    color:var(--ink-45); margin:0; display:flex; align-items:center; gap:8px;
  }
  .live-dot{width:7px; height:7px; border-radius:50%; background:var(--line); flex-shrink:0;}
  .live-dot.on{background:#2E7D46;}
  .save-file-btn{
    appearance:none; cursor:pointer; flex-shrink:0;
    font-family:var(--mono); font-size:10.5px; letter-spacing:.03em; color:var(--ink-70);
    background:var(--card); border:1px solid var(--line); border-radius:20px; padding:5px 12px;
  }
  .save-file-btn:hover{background:var(--ink); color:#fff; border-color:var(--ink);}
  .budget{
    display:flex; align-items:stretch; gap:0; border:1px solid var(--line); border-radius:10px;
    overflow:hidden;
  }
  .budget-cell{flex:1; padding:8px 12px; border-right:1px solid var(--line);}
  .budget-cell:last-child{border-right:none;}
  .budget-label{font-family:var(--mono); font-size:9.5px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-45); margin:0 0 2px;}
  .budget-value{font-family:var(--mono); font-size:14px; font-weight:600; font-variant-numeric:tabular-nums;}

  /* ---- NOW card — the mini deck's current slide ---- */
  .now-card{
    border:1px solid var(--line); border-radius:14px; overflow:hidden; background:#fff;
    margin-top:18px; box-shadow:0 6px 20px rgba(23,22,27,.06);
  }
  .now-thumb-wrap{position:relative; background:var(--ink); aspect-ratio:16/10;}
  .now-thumb{width:100%; height:100%; object-fit:cover; display:block;}
  .now-badge{
    position:absolute; top:10px; left:10px; font-family:var(--mono); font-size:11px;
    background:rgba(23,22,27,.72); color:#fff; padding:3px 9px; border-radius:20px;
    letter-spacing:.04em;
  }
  .now-body{padding:16px 18px 18px;}
  .now-section{font-family:var(--mono); font-size:10px; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-45); margin:0 0 4px;}
  .now-title-row{display:flex; align-items:baseline; justify-content:space-between; gap:10px;}
  .now-title{font-size:18px; font-weight:700; margin:0; letter-spacing:-.005em; text-wrap:balance;}
  .now-time{
    font-family:var(--mono); font-size:11px; color:var(--ink-45); white-space:nowrap;
    background:var(--card); border-radius:9px; padding:2px 8px; flex-shrink:0;
  }
  .now-step{font-family:var(--mono); font-size:11px; letter-spacing:.03em; color:var(--ink-70); margin:6px 0 0;}
  .now-notes-row{display:flex; align-items:flex-start; gap:8px; margin-top:12px;}
  /* contenteditable goes on this wrapping div, not the <ul> it contains --
     making a <ul> itself contenteditable is a known cross-browser minefield
     (typing can blur the element entirely, mid-edit) */
  .now-notes{margin:0; font-size:14.5px; color:var(--ink-70); flex:1; min-width:0; border-radius:8px;}
  .now-notes ul{margin:0; padding-left:19px;}
  .now-notes li{margin-bottom:6px;}
  .now-notes li:last-child{margin-bottom:0;}
  .now-notes strong{color:var(--ink); font-weight:700;}
  .now-notes em{font-style:normal; text-decoration:underline; text-decoration-color:var(--line); text-underline-offset:2px;}
  .now-notes[contenteditable="true"]{
    outline:2px dashed var(--ink-45); outline-offset:6px;
    background:var(--card); padding:8px 8px 8px 19px; margin-left:-8px;
  }
  .edit-toggle-btn{
    appearance:none; cursor:pointer; flex-shrink:0; width:26px; height:26px; border-radius:50%;
    border:1px solid var(--line); background:#fff; color:var(--ink-45); font-size:12px;
    display:flex; align-items:center; justify-content:center;
  }
  .edit-toggle-btn:hover{border-color:var(--ink-45); color:var(--ink);}
  .edit-toggle-btn.active{background:var(--ink); color:#fff; border-color:var(--ink);}
  .edit-hint{
    font-size:11.5px; color:var(--ink-45); margin:8px 0 0; font-style:italic;
  }

  /* ---- NEXT card — small, quiet preview of what's coming ---- */
  .next-wrap{margin-top:12px;}
  .next-label{font-family:var(--mono); font-size:10px; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-45); margin:0 0 6px;}
  .next-card{
    display:flex; gap:12px; align-items:center; border:1px solid var(--line); border-radius:12px;
    padding:8px; background:var(--card);
  }
  .next-thumb{width:96px; aspect-ratio:16/10; object-fit:cover; border-radius:7px; flex-shrink:0; background:var(--ink);}
  .next-title{font-size:13px; font-weight:700; margin:0 0 2px;}
  .next-step{font-family:var(--mono); font-size:10.5px; color:var(--ink-45); margin:0;}
  .next-empty{font-size:13px; color:var(--ink-45); padding:14px; text-align:center;}

  /* ---- collapsible full outline (pre-flight browsing, not needed live) ---- */
  details.outline{margin-top:22px; border-top:1px solid var(--line); padding-top:14px;}
  summary.outline-summary{
    font-family:var(--mono); font-size:11px; letter-spacing:.06em; text-transform:uppercase;
    color:var(--ink-45); cursor:pointer; list-style:none;
  }
  summary.outline-summary::-webkit-details-marker{display:none;}
  summary.outline-summary::before{content:"▸ "; }
  details[open] summary.outline-summary::before{content:"▾ "; }
  .outline-list{display:flex; flex-direction:column; margin-top:10px;}
  .outline-row{
    appearance:none; text-align:left; background:none; border:none; border-bottom:1px solid var(--line);
    display:flex; align-items:center; gap:12px; padding:8px 4px; cursor:pointer; font-family:var(--sans); color:var(--ink);
  }
  .outline-row:hover{background:var(--card);}
  .outline-row.current-outline{background:var(--card); font-weight:600;}
  .outline-num{font-family:var(--mono); font-size:11px; color:var(--ink-45); width:22px; flex-shrink:0;}
  .outline-title{flex:1; font-size:12.5px;}
  .outline-time{font-family:var(--mono); font-size:10px; color:var(--ink-45); flex-shrink:0;}

  footer{margin-top:auto; padding:16px 20px; border-top:1px solid var(--line); font-size:11px; color:var(--ink-45); text-align:center;}
</style>
</head>
<body>
<div class="page">
  <header>
    <div class="eyebrow-row">
      <p class="eyebrow"><span class="live-dot" id="liveDot"></span><span id="liveLabel">Waiting for the deck window…</span></p>
      <button class="save-file-btn" id="saveFileBtn" title="Download this window's notes.html with your edits baked in">Save notes.html</button>
    </div>
    <div class="budget">
      <div class="budget-cell">
        <p class="budget-label">Agent Identity</p>
        <p class="budget-value">~20.5 min</p>
      </div>
      <div class="budget-cell">
        <p class="budget-label">SDK Adoption</p>
        <p class="budget-value">~16 min</p>
      </div>
      <div class="budget-cell">
        <p class="budget-label">Total / target</p>
        <p class="budget-value">~36.5 / 40 min</p>
      </div>
    </div>
  </header>

  <div class="now-card" id="nowCard">
    <div class="now-thumb-wrap">
      <img class="now-thumb" id="nowThumb" src="" alt="">
      <span class="now-badge" id="nowBadge">01 / 21</span>
    </div>
    <div class="now-body">
      <p class="now-section" id="nowSection"></p>
      <div class="now-title-row">
        <h1 class="now-title" id="nowTitle"></h1>
        <span class="now-time" id="nowTime"></span>
      </div>
      <p class="now-step" id="nowStep" hidden></p>
      <div class="now-notes-row">
        <div class="now-notes" id="nowNotes"></div>
        <button class="edit-toggle-btn" id="editToggleBtn" title="Edit these notes">✎</button>
      </div>
      <p class="edit-hint" id="editHint" hidden>Editing — click away or press ✓ when done. Don't forget "Save notes.html" to keep it.</p>
    </div>
  </div>

  <div class="next-wrap">
    <p class="next-label">Up Next</p>
    <div class="next-card" id="nextCard"></div>
  </div>

  <details class="outline">
    <summary class="outline-summary">Full outline (21 slides)</summary>
    <div class="outline-list" id="outlineList">
__OUTLINE_ROWS__
    </div>
  </details>

  <footer>Opened from the deck's own "Speaker View" button — advances automatically as you click through.</footer>
</div>

<script type="application/json" id="deckData">__DECK_JSON__</script>
<script>
  // DECK lives in a non-executing JSON <script> tag, not a plain JS const,
  // specifically so edits can be written back into deckData.textContent and
  // then "Save notes.html" can serialize a real, reloadable copy of this
  // page with those edits baked in (see buildSavedHtml() below) -- a plain
  // `const DECK = [...]` literal has no DOM node to update, so edits would
  // only ever live in memory for this one session
  const DECK = JSON.parse(document.getElementById('deckData').textContent);
  const byKey = {};
  DECK.forEach((d, i) => { byKey[d.key] = i; });

  // one-time snapshot of the page exactly as it shipped, before any edits or
  // navigation touch the DOM -- "Save notes.html" edits this pristine copy's
  // deckData text rather than serializing the live, currently-mid-edit page,
  // so the saved file reopens cleanly on slide 1, not wherever you left off
  const PRISTINE_HTML = document.documentElement.outerHTML;
  const PRISTINE_DECK_JSON = document.getElementById('deckData').textContent;

  // restore any edits saved locally (autosaved on every keystroke, see
  // scheduleCommit below) so a plain reload doesn't lose unsaved-to-file work
  try {
    const saved = JSON.parse(localStorage.getItem('aiPresentNotesEdits') || '{}');
    DECK.forEach((d) => { if (typeof saved[d.key] === 'string') d.notesHtml = saved[d.key]; });
  } catch (err) { /* corrupt/missing localStorage entry -- just skip restoring */ }

  const liveDot = document.getElementById('liveDot');
  const liveLabel = document.getElementById('liveLabel');
  const nowThumb = document.getElementById('nowThumb');
  const nowBadge = document.getElementById('nowBadge');
  const nowSection = document.getElementById('nowSection');
  const nowTitle = document.getElementById('nowTitle');
  const nowTime = document.getElementById('nowTime');
  const nowStep = document.getElementById('nowStep');
  const nowNotes = document.getElementById('nowNotes');
  const nextCard = document.getElementById('nextCard');
  const outlineRows = Array.from(document.querySelectorAll('.outline-row'));
  const editToggleBtn = document.getElementById('editToggleBtn');
  const editHint = document.getElementById('editHint');
  const saveFileBtn = document.getElementById('saveFileBtn');

  let currentIdx = 0;
  let editing = false;
  let commitTimer = null;

  function persistEdits(){
    const map = {};
    DECK.forEach((d) => { map[d.key] = d.notesHtml; });
    localStorage.setItem('aiPresentNotesEdits', JSON.stringify(map));
    // escape a literal "</script" the same way the original build did --
    // .textContent itself doesn't care, but this string gets spliced back
    // into raw HTML later if you click "Save notes.html"
    document.getElementById('deckData').textContent = JSON.stringify(DECK).replace(/<\/script/g, '<\\/script');
  }

  // called before this window shows a different slide, and before saving --
  // without it, an edit you were mid-typing gets silently discarded the
  // instant the deck advances (renderIndex overwrites nowNotes.innerHTML)
  function commitEdit(){
    if (!editing) return;
    const d = DECK[currentIdx];
    // notesHtml is stored as bare <li> fragments (no wrapping <ul>) -- pull
    // just the <ul>'s contents back out, matching what renderIndex wraps it
    // in below, so re-rendering doesn't nest a fresh <ul> around this one
    // on every edit
    const ul = nowNotes.querySelector('ul');
    const newHtml = ul ? ul.innerHTML : nowNotes.innerHTML;
    if (d.notesHtml === newHtml) return;
    d.notesHtml = newHtml;
    persistEdits();
  }

  function setEditing(on){
    commitEdit();
    editing = on;
    nowNotes.contentEditable = on ? 'true' : 'false';
    editToggleBtn.classList.toggle('active', on);
    editToggleBtn.textContent = on ? '✓' : '✎';
    editToggleBtn.title = on ? 'Done editing' : 'Edit these notes';
    editHint.hidden = !on;
    if (on) nowNotes.focus();
  }

  function renderIndex(idx){
    commitEdit();
    if (editing) setEditing(false);
    currentIdx = idx;
    const d = DECK[idx];
    nowThumb.src = d.thumb;
    nowThumb.alt = d.title;
    nowBadge.textContent = d.num + ' / 21';
    nowSection.textContent = d.section;
    nowTitle.textContent = d.title;
    nowTime.textContent = d.time;
    if (d.step) { nowStep.textContent = d.step; nowStep.hidden = false; }
    else { nowStep.hidden = true; }
    nowNotes.innerHTML = '<ul>' + d.notesHtml + '</ul>';

    const next = DECK[idx + 1];
    if (next) {
      nextCard.innerHTML =
        '<img class="next-thumb" src="' + next.thumb + '" alt="">' +
        '<div><p class="next-title">' + next.title + '</p>' +
        '<p class="next-step">' + (next.step || (next.num + ' / 21')) + '</p></div>';
    } else {
      nextCard.innerHTML = '<p class="next-empty">That\\u2019s the end of the deck.</p>';
    }

    outlineRows.forEach((row) => row.classList.toggle('current-outline', row.dataset.key === d.key));
  }

  function highlight(key){
    if (!key) return;
    // the deck's coordinator sends step-based keys as "slideId:N" (colon);
    // this window's own DECK entries key step slides as "slideId-N" (hyphen,
    // valid as an HTML id) -- convert before lookup or every step-slide
    // message here silently misses and the display goes stale
    const idx = byKey[key.replace(':', '-')];
    if (idx === undefined) return;
    // a no-op push for the slide already showing (the deck re-sends state a
    // few times right after "Speaker View" opens, to work around a message
    // that can silently drop on the very first send) would otherwise still
    // run renderIndex() and kick you out of edit mode mid-keystroke for no
    // actual reason -- skip entirely when nothing has changed
    if (idx === currentIdx) return;
    renderIndex(idx);
  }

  // this window is a full remote control when opened from the deck, not
  // just a display: arrow keys and outline-row clicks here drive the deck
  // window, which reports its new state back through the normal
  // 'ai-present-notes' message below -- this window never guesses ahead of
  // what the deck actually does, it just asks and waits to hear back
  function requestNav(dir){
    if (window.opener) window.opener.postMessage({ type: 'ai-present-nav', dir }, '*');
  }
  function requestJump(key){
    const idx = byKey[key];
    if (idx === undefined) return;
    if (window.opener) {
      window.opener.postMessage({ type: 'ai-present-jump', globalIdx: Number(DECK[idx].num) - 1 }, '*');
    } else {
      // no deck window to answer to (opened standalone) -- just browse locally
      renderIndex(idx);
    }
  }

  outlineRows.forEach((row) => {
    row.addEventListener('click', () => requestJump(row.dataset.key));
  });

  editToggleBtn.addEventListener('click', () => setEditing(!editing));

  // autosave to localStorage as you type, well before you'd think to click
  // "Save notes.html" -- a crash or accidental close mid-edit shouldn't cost
  // you the notes you just wrote
  nowNotes.addEventListener('input', () => {
    // some browsers can drop DOM focus off a contenteditable element after
    // the very first keystroke that follows a mouse click into it (seen
    // reliably in testing here) -- the edit still applies either way, but
    // losing focus would make the cursor visibly vanish mid-type, so put it
    // back at the end rather than leave that stuck
    if (document.activeElement !== nowNotes) {
      const range = document.createRange();
      range.selectNodeContents(nowNotes);
      range.collapse(false);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      nowNotes.focus();
    }
    clearTimeout(commitTimer);
    commitTimer = setTimeout(commitEdit, 400);
  });

  window.addEventListener('keydown', (e) => {
    // gate on the explicit "editing" flag, not document.activeElement --
    // the flag reflects intent (you toggled edit mode on) and can't drift,
    // where focus is a transient browser-tracked state that (see above)
    // isn't reliable enough to hang slide-navigation-vs-typing on
    if (editing) return;
    if (e.key === 'ArrowRight') requestNav(1);
    if (e.key === 'ArrowLeft') requestNav(-1);
  });

  window.addEventListener('message', (e) => {
    if (!e.data || e.data.type !== 'ai-present-notes') return;
    liveDot.classList.add('on');
    liveLabel.textContent = 'Synced to the deck window';
    highlight(e.data.key);
  });

  // builds a real, standalone copy of this page with your current edits
  // baked into its deckData -- starting from the PRISTINE page as loaded
  // (not the live, possibly mid-navigation DOM) so the saved file reopens
  // the same way this one originally did, just with updated notes
  function buildSavedHtml(){
    commitEdit();
    const currentJson = document.getElementById('deckData').textContent;
    return PRISTINE_HTML.replace(PRISTINE_DECK_JSON, currentJson);
  }

  saveFileBtn.addEventListener('click', () => {
    const html = '<!doctype html>\\n' + buildSavedHtml();
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'notes.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    saveFileBtn.textContent = 'Saved ✓ — move it into presentation/';
    setTimeout(() => { saveFileBtn.textContent = 'Save notes.html'; }, 2600);
  });

  renderIndex(0);

  if (window.opener) {
    window.opener.postMessage({ type: 'ai-present-notes-ready' }, '*');
  } else {
    liveLabel.textContent = "Opened standalone — not synced (open via the deck's Speaker View button instead)";
  }
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__DECK_JSON__", DECK_JSON).replace("__OUTLINE_ROWS__", OUTLINE_HTML)
out_path = os.path.join(HERE, "notes.html")
with open(out_path, "w") as f:
    f.write(out)
print(f"wrote {out_path}, {len(out)} bytes, {len(DECK)} deck entries")
