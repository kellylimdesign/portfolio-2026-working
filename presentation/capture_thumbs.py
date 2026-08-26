from playwright.sync_api import sync_playwright
import pathlib, base64, io, os
from PIL import Image

# Re-captures the "mini deck" thumbnails in notes.html (presentation/notes-thumbs.json)
# from the actual rendered slides. Run this again if the deck's visuals change:
#   python3 presentation/capture_thumbs.py
# then rebuild notes.html: python3 presentation/build_notes.py

HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
BASE = HERE.parent
OUT_JSON = HERE / "notes-thumbs.json"

# (global slide index, key, step-number-or-None)
PLAN = [
    (0, "slideAboutMe", None),
    (1, "slideHero", None),
    (2, "slideProblem", None),
    (3, "slideOverview", None),
    (4, "slidePersona", None),
    (5, "slideOwlTradeIntro", None),
    (6, "slideEndUserJourney-1", 1),
    (6, "slideEndUserJourney-2", 2),
    (6, "slideEndUserJourney-3", 3),
    (6, "slideEndUserJourney-4", 4),
    (7, "slideOneConsole", None),
    (8, "slideCustomerJourney-1", 1),
    (8, "slideCustomerJourney-2", 2),
    (8, "slideCustomerJourney-3", 3),
    (8, "slideCustomerJourney-4", 4),
    (9, "slideChallenges", None),
    (10, "slideValidating", None),
    (11, "slideHeroStytch", None),
    (12, "slideProblemStytch", None),
    (13, "slidePersonaStytch", None),
    (14, "demoSlide", None),
    (15, "demoSelectSlide", None),
    (16, "slideSolution", None),
    (17, "journeySlide-1", 1),
    (17, "journeySlide-2", 2),
    (17, "journeySlide-3", 3),
    (17, "journeySlide-4", 4),
    (18, "slideChallengesStytch", None),
    (19, "slideImpact", None),
    (20, "slideThankYou", None),
]

def get_active_slide_handle(page):
    return page.evaluate_handle("""() => {
        const ai = document.getElementById('phaseAgentIdentity');
        const st = document.getElementById('phaseStytch');
        const root = getComputedStyle(ai).display !== 'none' ? ai : st;
        return root.querySelector('.slide.active');
    }""")

def visible_viewport_clip(page):
    # some slides render taller than the 900px viewport (they extend below
    # it, unscrolled, since .slide is absolutely positioned starting at
    # top:56px) -- an *element* screenshot auto-scrolls the oversized
    # element fully into view first, which drags the page down and leaves
    # the fixed topbar visually overlapping the now-shifted slide content.
    # Clipping to the actual on-screen viewport region instead (what a
    # human watching the presenter's shared screen would actually see)
    # avoids that scroll entirely.
    return {"x": 0, "y": 56, "width": 1440, "height": 900 - 56}

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto(f"file://{BASE}/presentation/index.html")
    page.wait_for_timeout(500)

    results = {}
    last_global_idx = None
    for global_idx, key, step in PLAN:
        if global_idx != last_global_idx:
            page.evaluate(f"document.querySelectorAll('#sharedDots .dot')[{global_idx}].click()")
            page.wait_for_timeout(650)
            last_global_idx = global_idx
        if step is not None:
            page.evaluate(f"""() => {{
                const ai = document.getElementById('phaseAgentIdentity');
                const st = document.getElementById('phaseStytch');
                const root = getComputedStyle(ai).display !== 'none' ? ai : st;
                const slide = root.querySelector('.slide.active');
                const item = slide.querySelector('.step-nav-item[data-step="{step}"] .step-nav-head');
                if (item) item.click();
            }}""")
            page.wait_for_timeout(500)
        raw = page.screenshot(clip=visible_viewport_clip(page))
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        # downscale for a fast-loading thumbnail -- these are recognition aids,
        # not full-fidelity reproductions
        img.thumbnail((640, 640))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=72)
        results[key] = base64.b64encode(buf.getvalue()).decode("ascii")
        print(f"captured {key} ({img.size[0]}x{img.size[1]}, {len(buf.getvalue())} bytes)")

    b.close()

import json
with open(OUT_JSON, "w") as f:
    json.dump(results, f)
print("wrote", OUT_JSON, "-", sum(len(v) for v in results.values()), "base64 chars total")
