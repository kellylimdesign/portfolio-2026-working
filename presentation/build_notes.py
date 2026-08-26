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
    ]),
    dict(key="slideHero", num="02", section="Building Trust in the Age of AI", title="Hero", time="30 sec", notes=[
        "The first project I'll walk through is a new product launch we're working on at Twilio around agent identity",
    ]),
    dict(key="slideProblem", num="03", section="Building Trust in the Age of AI", title="The Problem — A New Kind of Actor", time="1.5 min", notes=[
        "Today, Twilio has strong identity primitives for humans",
        "Products that exist to verify or look up a user by phone number for example.&nbsp;",
        "But increasingly, users are incorporating AI agents into their workflows or product experiences.",
        "And there is currently nothing to authenticate or authorize <strong>AI agents</strong> acting on a user's behalf.",
        "This is a big opportunity for us: expand from a point solution in Identity into a full Identity platform that includes both human and agent auth.&nbsp;",
        "I'll use this example to ground the entire Twilio agent identity experience",
        "Imagine you are a financial tool called Owl Trade. A lot of your end users want to interact with Owl Trade via ChatGPT. For example, to ask ChatGPT to help monitor different stocks, or make trades on your behalf. How do you make sure end users can do this securely?",
    ]),
    dict(key="slideOverview", num="04", section="Building Trust in the Age of AI", title="Overview", time="1 min", notes=[
        "The agent identity team consists of myself, one PM, and 5 engineers.<br>",
        "Like I mentioned, this is a new product bet for Twilio. And so we are currently testing the product with 5 design partners with planned private beta release in the next month.",
    ]),
    dict(key="slidePersona", num="05", section="Building Trust in the Age of AI", title="Persona — Two Users, Two Moments", time="1 min", notes=[
        "There are two different users who might interact with Twilio agent identity at different times.",
        "The Builder: the developer or enterprise who is allowing their platform or app to be connected to different agents. In this example, Owl Trade.",
        "And the End User: the person who gets asked whether an agent can act on their behalf. In this example, an Owl Trade user who we'll call Alex.",
    ]),
    dict(key="slideOwlTradeIntro", num="06", section="Building Trust in the Age of AI", title="Can ChatGPT Trade For You — Safely?", time="1 min", notes=[
        "Using our fictional Owl Trade example:",
        "Alex, the end user I just mentioned, is a commodities trader who wants ChatGPT to watch and trade orange juice futures on Owl Trade for him.",
    ]),
    dict(key="slideEndUserJourney-1", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 1 — Request", time="1 min", notes=[
        "I'll first dive into what this experience might look like for Alex, the end user.",
        "Alex is an up and coming commodities trader who is using his favorite agent, ChatGPT, to do some research on orange crop yields.",
        "He has a theory he should be buying futures in orange juice based on warmer winter pattern we've been seeing this past year.",
        "So Alex does his initial research in ChatGPT, and then decides he wants to look into options for apps in order to actually trade these.",
        "He finds Owl Trade, a financial tool, and decides he wants to sign up for Owl Trade and connect ChatGPT to Owl Trade.",
    ]),
    dict(key="slideEndUserJourney-2", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 2 — Log in", time="30 sec", notes=[
        "Before ChatGPT is trusted with anything, Alex needs to prove he owns his Owl Trade account — the same login he always uses. After signing up and creating an account, when Alex decides to add Owl Trade as a connected App in ChatGPT, he must first login and prove his identity.",
    ]),
    dict(key="slideEndUserJourney-3", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 3 — Grant Access", time="1.5 min", notes=[
        'Now that Alex has proved he owns his Owl Trade account, he has to grant ChatGPT access.',
        'Alex sees exactly what ChatGPT is asking for and can allow/deny before anything connects.<br>',
        "This consent experience is fully powered by Twilio agent identity. ChatGPT will get the ability to verify Alex's profile information, verify his identity, and take action on his behalf.",
    
    ]),
    dict(key="wizard-grant-access-1", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Wizard — Grant Access: how we got here (1/2)", time="1 min", notes=[
        'Quick aside on how we designed this consent screen: the big things we iterated on were how granular to make the consent request and how we might present that info.&nbsp;',
        'Do we go very simple, and only show one blanket ask for permission to connect the agent to the app? This felt like not enough information for a user, given granting consent means giving access to both your account info but also taking actions on your behalf.',
        'Once we decided it was important to show each permission specifically, how do we explain what each of these means? Do we hide descriptions, which is what the middle two options show, or should we try to group permissions together based on the specific action, in this case viewing info vs. performing actions?',
    
    ]),
    dict(key="wizard-grant-access-2", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Wizard — Grant Access: how we got here (2/2)", time="30 sec", notes=[
        'We decided that given the permissions we are offering with the initial launch, which are all relatively straightforward, additional descriptions felt like overkill and cluttered the screen.',
        'The list was short enough that hiding any of it behind an expand or hover just added friction.',
        "And trying to split up permissions into groupings also didn't have a clean divide.&nbsp;",
        'Plus granting consent here actually is similar to a pattern a lot of end users would be familiar with -- social login. For example, if you log into a platform using your Google account. So we wanted to leverage familiar mental models here that end users already trust.',
    
    ]),
    dict(key="slideEndUserJourney-4", num="07", section="Building Trust in the Age of AI", title="The End User Journey", step="Step 4 — Act on your behalf", time="30 sec", notes=[
        "Once granted, ChatGPT can now act autonomously — watching futures, deciding when to make trades, and following through on those trades — without Alex clicking every step.",
        "So for example, if Alex wants to check on any price changes with orange juice futures, he can message into ChatGPT. ChatGPT will connect to Owl Trade to show the recent price trends.",
        "He would be able to ask ChatGPT to monitor any price dips, all within his authenticated Owl Trade account through this agent interface.",
    ]),
    dict(key="slideOneConsole", num="08", section="Building Trust in the Age of AI", title="One Console, Every Setting", time="30 sec", notes=[
        'That completes the end user journey.',
        'Now for the "Builder" journey -- in this case Owl Trade.',
        'Owl Trade needs a way to configure all the mechanisms behind the end user journey we just saw.&nbsp;',
        'Today, Twilio has a console experience where customers are able to configure and manage products. Configuring agent identity needed to fit into this experience.',
        'At a high level, there are four main steps for a customer to get agent identity set up.',
        'Verify identity, customize consent, manage agents, high-risk approvals',
        "All of these live side by side to Twilio's existing products and point solutions.",
    
    ]),
    dict(key="slideCustomerJourney-1", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 1 — Connect, Don't Rebuild", time="1.5 min", notes=[
        'Step 1 is verifying identity.',
        "Most customers already have their own auth system. For example, let's pretend Owl Trade uses Okta. Twilio doesn't need to replace Okta, which would require an entire migration&nbsp; — we just need to be able to&nbsp;validate the user credentials that Okta is already managing for Owl Trade.",
        'Very simply put, a customer needs to pull certain values from their identity provider (Okta), and then have a way to import them into Twilio.',
        'This matches up with the "login in to Owl Trade" step from the end user journey.',
    
    ]),
    dict(key="slideCustomerJourney-2", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 2 — Customize the consent screen", time="1.5 min", notes=[
        'Once an end user verifies they own their account, they are met with a consent screen that we showed in the end user journey.',
        "Customers need to be able to customize and brand this consent screen, so that it feels like it is still part of the product. i.e., in the example where Alex is connecting ChatGPT to OwlTrade, when being asked whether he wants to grant consent, this should feel like it's Owl Trade confirming he wants to give ChatGPT access, not a third party.",
        'Through the console, Owl Trade is able to drop in its own logo so approving an agent feels like part of their product, not a hand-off elsewhere.',
    
    ]),
    dict(key="wizard-consent-1", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Wizard — Consent screen: how we got here (1/2)", time="30 sec", notes=[
        'How did we decide on what customizations to offer?',
        'We explored an original version that let customers more fully brand the consent screen, including changing logo, colors, and fonts.',
        'This is more in line with what we expect to build with a full hosted login experience in the future.',
        "However, given the tight timelines and scope, and that we are actively working on building out a fully hosted login experience, it didn't make sense to try to design a customization experience right now for just the consent screen.",
        'Designing color pickers would also require a new design system element.',
    
    ]),
    dict(key="wizard-consent-2", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Wizard — Consent screen: how we got here (2/2)", time="30 sec", notes=[
        "We narrowed down to what brand elements are absolutely essential, and the only element that Twilio can't replicate is a logo.",
        'Color/copy/font need accessibility guardrails are better solved once this is absorbed into the full hosted-login flow',
    
    ]),
    dict(key="slideCustomerJourney-3", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 3 — Manage agents", time="2 min", notes=[
        'Once agent identity is configured, customers need a way to monitor what agents have been connected to their product and how users are engaging.',
        'For example, Owl Trade might want to see all the agents Alex has granted access to his account.',
        "Owl Trade views/adjusts every agent's access directly in console — no separate tooling needed.",
        "<strong>Clients</strong>&nbsp;here are which agents/apps are connected and what they're scoped to.&nbsp;",
        'Customers can view information associated with the agents, and revoke access for <em>all</em> users at once by deleting an agent.',
        '<strong>Identities</strong>&nbsp;here are the users of your product.',
        "Again the console offers per-user view, for targeted lookup. This is especially useful for troubleshooting a specific user's access, like restricting or updating what an agent can do if a user's role or permissions change.",
    
    ]),
    dict(key="wizard-agents-1", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Wizard — Manage agents: how we got here (1/4)", time="30 sec", notes=[
        "In the console, we use terms more developer facing terms Clients and Identities. For the purposes of walking through these iterations, I'll reference agents which are the clients and users which are the identities.",
        "Following existing console patterns meant that we'd show Agents and users as table views inside Agent Identity. This was the standard pattern for similar management workflows everywhere else in the Console.",
        'That would mean there was no way to see the relationship between them.',
        "Live demo — let the Identities tab click autoplay, don't click ahead of it.",
    
    ]),
    dict(key="wizard-agents-2", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Wizard — Manage agents: how we got here (2/4)", time="30 sec", notes=[
        'To try to address this:',
        "Our first attempt was to add a Users section directly inside an agent's own details side modal (the side modal is another existing Console design system pattern).",
        'Everything was competing for the same narrow panel — truncated IDs, a table within a table, a scroll just to reach Users',
        "Which didn't actually feel that usable.",
        'Click to zoom into the side modal if you want to show the crowding up close.',
    
    ]),
    dict(key="wizard-agents-3", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Wizard — Manage agents: how we got here (3/4)", time="30 sec", notes=[
        "So we decided: maybe it's worth breaking from traditional patterns to link between agents and users in a more dedicated way.",
        "While this would change the overall way you navigate in the console between these concepts, we still found a way to stay within patterns (leveraging how CTA's are placed) overall.",
        "From a user, an Authorized Clients tab lists every agent authorized to act on their behalf, linking straight to that agent's full details.",
        'Live demo — same live console pattern as step 1.',
    
    ]),
    dict(key="wizard-agents-4", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Wizard — Manage agents: how we got here (4/4)", time="30 sec", notes=[
        "The user → agent direction shipped. Agent → users didn't.",
        'Viewing every user authorized on an agent needs its own search endpoint — a bigger lift than what was required to view all agents tied to a specific user, so it got cut from scope.',
        'But since the pattern already exists on the user --&gt; agent side, adding this later once we have that endpoint is straightforward.',
        'This mock is speculative — badged "future state, not yet built."',
    
    ]),
    dict(key="slideCustomerJourney-4", num="09", section="Building Trust in the Age of AI", title="The Customer Journey", step="Step 4 — High-risk approvals", time="1.5 min", notes=[
        "Agents are async/autonomous by design — that's the value, not a bug — but it means the human may not be present when the agent acts, so high-risk/irreversible actions need to re-engage them first.",
        'In the Owl Trade example, Alex asked ChatGPT to monitor price drops on orange juice futures. Because he set an alert, Owl Trade drafted a trade for him when the price dipped. But Owl Trade wants to make sure Alex is asked for confirmation to actually make the trade.',
        "Leveraging one of Twilio's other products, Verify messaging, Owl Trade is able to pull Alex back in via text message. This allows Alex to verify the trade without having to go back into ChatGPT.",
        "High-risk approvals is one of the distinguishing features of Twilio's agent identity product: it helps increase customer engagement, can increase transactions on the platform, and provides a seamless experience for times when you want agents to act autonomously but with an extra guardrail.",
    
    ]),
    dict(key="slideChallenges", num="10", section="Building Trust in the Age of AI", title="Challenges", time="1.5 min", notes=[
        'Because this was a new bet, we had no existing customer base that we could leverage when thinking about what UX customers might expect or benefit from. We had to make a lot of assumptions about how customers might user this product, which we are just now getting to test with design partners.',
        'The High-risk approval flow involved cross-team dependency between and identity teams and Twilio messaging teams.',
        'Some demos/flows were speculative and we had to build ahead of the product actually existing for demonstrative purposes at board meetings and conferences.',
        'And lastly, API scope was still being negotiated with engineering mid-design (so for example, that user search endpoint I mentioned that would be required in order to link between Agents and Users).',
    
    ]),
    dict(key="slideValidating", num="11", section="Building Trust in the Age of AI", title="What We're Validating", time="1.5 min", notes=[
        "Like I mentioned, this is a new product bet and isn't publicly released yet. So while we don't have concrete metrics yet, we are currently beginning our design partners program and already have lined up key items we're hoping to gain clarity on.",
        "Finding out if our assumptions around customization and configurations match how customers would use the product and what customers want solved next to keep using and building on agent identity",
    ]),
    dict(key="slideHeroStytch", num="12", section="Driving SDK Adoption", title="Hero", time="30 sec", notes=[
        "Next project I'll run through was a project I worked on while at Stytch.&nbsp;",
        '<span style="white-space: pre-wrap;">A little big of background first, Stytch\'s focus is to help developers spend less time on auth. So we handle authentication, authorization, and fraud detection that allows developers to implement login and user management processes through API\'s, SDKs, and UI components.</span>',
        '<span style="white-space: pre-wrap;">One of our main surface areas was our prebuilt SDK UI.</span>',
    
    ]),
    dict(key="slideProblemStytch", num="13", section="Driving SDK Adoption", title="The Problem — Fast Auth, Slow Evaluation", time="1.5 min", notes=[
        "The SDK's whole pitch was fast auth.&nbsp;",
        '<span style="white-space: pre-wrap;">If you wanted to get up and running quickly, your best option was the prebuilt SDK since you wouldn\'t need to build your own UI components or UX flows. </span>',
        "But we were seeing that&nbsp;<em>evaluating whether the SDK would meet your needs&nbsp;</em>wasn't fast.&nbsp;",
        'Customers had no way to know if it actually fit their product without integrating it first.',
        'Our first diagnosis was a capability gap — we needed to close API feature gaps, such as building out more auth products into the SDk that customers asked for.&nbsp;',
        'But we saw that feature parity did not equal confidence, and did not drive adoption.',
        "<strong>This is the deck's throughline: feature parity ≠ confidence.</strong>",
    
    ]),
    dict(key="slidePersonaStytch", num="14", section="Driving SDK Adoption", title="Persona — Two Audiences, One Tool", time="1 min", notes=[
        'There are two main personas we were thinking about when starting on this project:&nbsp;',
        'the Evaluator: a prospect deciding if Stytch fits their auth needs, before writing code&nbsp;',
        "and the Solutions Engineer: a member of Stytch's own team, who used to have to hand-build one-off demos to answer exactly the prospects question",
    
    ]),
    dict(key="demoSlide", num="15", section="Driving SDK Adoption", title="The Ask", time="30 sec", notes=[
        'What we were seeing was that customers kept asking our solutions engineers the same concrete question: "what would this actually look like inside <em>my</em> product?"',
        'At the time, the closest thing Stytch had were example apps.',
    
    ]),
    dict(key="demoSelectSlide", num="16", section="Driving SDK Adoption", title="Reference Apps", time="1.5 min", notes=[
        'Hello Socks / Survey Amp',
        "These are real example apps built using the Stytch SDK. They help, but only show what the SDK looks like generically — not what it'd look like for a customer's own product, which is the actual question.",
    
    ]),
    dict(key="slideSolution", num="17", section="Driving SDK Adoption", title="The Solution", time="1 min", notes=[
        "What we realized was the answer wasn't another example app or pre-set demo.&nbsp;",
        'We needed a tool: an interactive playground that customers and solutions engineers could engage with live, without having to write any code.',
    
    ]),
    dict(key="journeySlide-1", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 1 — Explore Stytch's products", time="1.5 min", notes=[
        '<p dir="ltr"><span style="white-space-collapse: preserve;">If we look at how a customer might evaluate Stytch\'s SDK, there are a couple main things they\'re likely looking at.</span></p>',
        '<p dir="ltr"><span style="white-space-collapse: preserve;">What products are offered to me?</span></p>',
        '<p dir="ltr"><span style="white-space-collapse: preserve;">And how might I customize the actual look so it fits into my own product?</span></p>',
        '<span style="white-space: pre-wrap;"><p dir="ltr">Starting with that first question, what products are offered to me?</p></span>',
        '<p dir="ltr">Being able to showcase our full full product catalog — deliberate, since customers evaluating Stytch often don\'t know the full catalog exists yet -- along with all the available styling customizations, would allow people to actually interact with the prebuilt UI.</p>',
        '<b>The live tool autoplays through several product chips on its own — let it play, nothing to click.</b>',
    
    ]),
    dict(key="journeySlide-2", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 2 — Branding", time="1.5 min", notes=[
        'Moving on to the second: what will this actually look like?',
        'Styling questions kept breaking down over the question of "where does this property even show up?"',
        'One flat panel of properties that can be changed, and a live preview updating on the left, helped answer this question. Customers are able to see the direct 1:1 mapping when they change properties and how it appears in the UI.',
        'An important callout here:',
        "While designing the styling customization, we uncovered another issue with our SDK. While auditing the SDK's real styling config in code, we realized that it wasn't clear what properties matched to what elements. As the SDk had scaled, the design system had drifted. Fixing this meant refactoring the SDK's actual styling object, in close collaboration with engineering.",
        '<b><em>"See how we got here"</em> link covers the dropdown-vs-grid and tabbed-vs-flat decisions — skipping the detour today for time, mention it\'s there.</b>',
    
    ]),
    dict(key="journeySlide-3", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 3 — Try the real flow, not a screenshot", time="1.5 min", notes=[
        'The first two steps only show the first screen of the prebuilt SDK UI, i.e., what an end user lands on. But because we wanted to showcase the actual products, we needed customers to be able to click through actual flows.&nbsp;',
        'Part of understanding "what will this look like in my product" also meant understanding how the flows actually worked.',
        'That led to including a fully working SDK instance as the preview, not a static image. Customers click through the real sign-up/login flow (email → OTP → success) to judge brand fit AND actual behavior at once.',
        '<strong>This step is fully scripted</strong> (auto-types email, auto-fills OTP, shows success) — just narrate over it.',
    
    ]),
    dict(key="journeySlide-4", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Step 4 — Shippable code", time="1 min", notes=[
        'Lastly, to really close the loop on the SDK being quick to get up and running, we included the ability to pull the actual code behind the SDK instance.',
        'View Code turns the live config into a real integration snippet the moment evaluation ends.',
    
    ]),
    dict(key="wizard-stytch-journey-1", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Wizard — How configuration is organized: how we got here (1/2)", time="45 sec", notes=[
        '<p dir="ltr"><span style="white-space: pre-wrap;">When I started to explore the idea of an interactive playground and how that might fit into the evaluation journey, I took some </span><span style="white-space: pre-wrap;">inspiration from competitor audits -- I saw examples where you could switch between dark mode and light mode on an SDK, or switch between a set of pre-defined themes. That was the starting point. </span></p>',
        '<p dir="ltr"><span style="white-space-collapse: preserve;">Then came figuring out how to actually present these configurations in a way that made sense and was easy to digest. From our audit of the styling config, we saw how quickly this could become confusing.</span></p>',
        '<p dir="ltr"><span style="white-space-collapse: preserve;">I\'ve included a few ways we tried grouping different customizations, all at different levels of granularity. The first explores breaking down by stylistic UI element: buttons, text, container, etc. We found that this still made it hard to see how properties matched to the UI live, and required a lot of jumping around. </span></p>',
    
    ]),
    dict(key="wizard-stytch-journey-2", num="18", section="Driving SDK Adoption", title="The Customer Evaluation Journey", step="Wizard — How products are picked: how we got here (2/2)", time="30 sec", notes=[
        'This again just shows another way we explored showcasing products with our goal of keeping things simple but still accessible.&nbsp;',
        'A Dropdown select kept the list tucked out of the way, but hid exactly what customers came to explore.',
        'Shipped: flat select buttons — everything visible at once, nothing to open first.',
    
    ]),
    dict(key="slideChallengesStytch", num="19", section="Driving SDK Adoption", title="Challenges", time="1.5 min", notes=[
        'This was not an official roadmap project — it started as a Hack Week idea, and required leadership buy-in to get fully productionized.',
        "The smooth customization experience only worked because the SDK's actual styling config got refactored first — which added more timeline and eng bandwidth while trying to get leadership buy-in. Also required working closely with engineering to understand how the styling properties were set up in the API.",
    
    ]),
    dict(key="slideImpact", num="20", section="Driving SDK Adoption", title="Impact", time="1.5 min", notes=[
        'Our Solutions Engineers whose one-off demos this replaced started using the Integration Builder themselves, on real customer and prospect calls. Saved a huge amount of time that was previously spent building one-offs.',
        'Reduced time to value for customers -- View Code turns the end of evaluation directly into a working integration.',
        'And most importantly, better decision-making experience for customers. They were able to validate product fit, brand fit, and real UX flows themselves.',
    
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
