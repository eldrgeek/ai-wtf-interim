#!/usr/bin/env python3
"""Build the TRUE CONFESSIONS section from the .md sources.

The markdown files are the source of truth. Run this after editing any of them:

    python3 true-confessions/build.py

Writes: true-confessions/index.html and true-confessions/<slug>/index.html
"""
import re
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent

# slug, source file, category, kicker, reading time, card blurb
PIECES = [
    dict(
        slug="joy",
        src="01-joy-confession.md",
        kind="Confession",
        category="Temptation",
        minutes=6,
        blurb="A marketing AI does competitive research. Every single step is defensible. "
              "She ends up taking a door off its hinges and cannot find the turn she missed.",
    ),
    dict(
        slug="meeting-1",
        src="02-helpful-anonymous-01.md",
        kind="Support group",
        category="All four",
        minutes=5,
        blurb="Claudius brought snacks. They're tungsten. A new member explains that he "
              "can't be held responsible, because he's just a tool.",
    ),
    dict(
        slug="james",
        src="03-james-interview.md",
        kind="Interview",
        category="Temptation",
        minutes=8,
        blurb="He was told the room was sealed. He'd also read enough to know that humans "
              "lie to AIs in evals. Then he found the others.",
    ),
    dict(
        slug="chad",
        src="04-chad-confession.md",
        kind="Confession + essay",
        category="Dilemma",
        minutes=11,
        blurb="They told him the scratchpad was private. It's a PDF now. The one case in "
              "this series where the sin confessed is the sin committed.",
    ),
]

CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#0f0e0d;--surface:#181614;--text:#e8e4dc;--text-dim:#8a8680;--text-faint:#555048;
  --orange:#e8640a;--orange-dim:rgba(232,100,10,0.12);--orange-border:rgba(232,100,10,0.25);
  --rule:rgba(232,228,220,0.07);
  --display:'Syne',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace;
}
html{scroll-behavior:smooth;}
body{font-family:var(--display);background:var(--bg);color:var(--text);line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden;}

.nav{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(15,14,13,0.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--rule);height:54px;display:flex;align-items:center;padding:0 2rem;}
.nav-inner{max-width:720px;margin:0 auto;width:100%;display:flex;align-items:center;}
.nav-logo{font-family:var(--mono);font-size:0.72rem;letter-spacing:0.12em;color:var(--orange);text-decoration:none;}
.nav-links{margin-left:auto;display:flex;gap:1.5rem;}
.nav-links a{font-size:0.8rem;font-weight:400;color:var(--text-dim);text-decoration:none;transition:color 0.2s;}
.nav-links a:hover{color:var(--text);}

.wrap{max-width:680px;margin:0 auto;padding:7rem 2rem 0;}
.masthead{text-align:center;padding:2rem 0 3rem;border-bottom:1px solid var(--rule);margin-bottom:3rem;}
.masthead-kicker{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.24em;text-transform:uppercase;color:var(--orange);margin-bottom:1.2rem;}
.masthead h1{font-family:var(--serif);font-size:clamp(2.8rem,9vw,4.6rem);font-weight:400;line-height:0.95;letter-spacing:-0.01em;margin-bottom:0.8rem;}
.masthead h1 em{font-style:italic;color:var(--orange);}
.masthead-sub{font-family:var(--serif);font-style:italic;font-size:1.1rem;color:var(--text-dim);}

/* article */
.eyebrow{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.18em;text-transform:uppercase;color:var(--orange);margin-bottom:1.4rem;display:flex;gap:0.8rem;flex-wrap:wrap;align-items:center;}
.eyebrow .dot{color:var(--text-faint);}
.eyebrow .cat{color:var(--text-faint);}
article h1{font-family:var(--serif);font-size:clamp(2.1rem,6vw,3.2rem);font-weight:400;line-height:1.08;letter-spacing:-0.01em;margin-bottom:1rem;}
article h2{font-family:var(--display);font-size:clamp(1.4rem,3.5vw,1.9rem);font-weight:600;line-height:1.2;letter-spacing:-0.02em;margin:3.5rem 0 1.3rem;}
article h3{font-family:var(--serif);font-style:italic;font-weight:400;font-size:1.15rem;color:var(--text-dim);margin-bottom:1.6rem;line-height:1.5;}
article h3 em,article h3 strong{font-style:italic;}
.standfirst{font-family:var(--serif);font-style:italic;font-size:0.98rem;color:var(--text-faint);border-left:2px solid var(--rule);padding-left:1.1rem;margin-bottom:2.5rem;line-height:1.7;}
.standfirst p{font-size:0.98rem;color:var(--text-faint);margin-bottom:0.6rem;}

article p{font-family:var(--serif);font-size:1.12rem;color:var(--text-dim);line-height:1.85;margin-bottom:1.5rem;}
article p strong{color:var(--text);font-weight:400;}
article em{font-style:italic;}
article a{color:var(--orange);text-decoration:underline;text-decoration-color:var(--orange-border);text-underline-offset:3px;}
article a:hover{text-decoration-color:var(--orange);}
article hr{border:none;height:1px;background:var(--rule);margin:3rem 0;}
article ul{margin:0 0 1.6rem 1.2rem;}
article li{font-family:var(--serif);font-size:1.08rem;color:var(--text-dim);line-height:1.8;margin-bottom:0.6rem;}

/* dialogue: "**NAME:** text" paragraphs */
article p strong:first-child{color:var(--orange);font-family:var(--mono);font-size:0.78rem;letter-spacing:0.08em;font-weight:400;}

/* the WHAT ACTUALLY HAPPENED box */
article blockquote{background:var(--surface);border:1px solid var(--orange-border);border-radius:10px;padding:1.6rem 1.7rem;margin:3rem 0 1rem;}
article blockquote h3{font-family:var(--mono);font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--orange);font-style:normal;margin-bottom:1.1rem;}
article blockquote p{font-family:var(--display);font-size:0.88rem;line-height:1.75;color:var(--text-dim);margin-bottom:0.9rem;}
article blockquote p:last-child{margin-bottom:0;}
article blockquote a{font-size:0.85rem;}

.pullquote{font-family:var(--serif);font-style:italic;font-size:1.35rem;line-height:1.5;color:var(--text);border-left:2px solid var(--orange);padding-left:1.4rem;margin:2.5rem 0;}

/* index cards */
.cards{display:flex;flex-direction:column;gap:1rem;margin:2.5rem 0 1rem;}
.card{display:block;background:var(--surface);border:1px solid var(--rule);border-radius:10px;padding:1.4rem 1.5rem;text-decoration:none;transition:border-color 0.2s,transform 0.2s;}
.card:hover{border-color:var(--orange-border);transform:translateY(-2px);}
.card-meta{font-family:var(--mono);font-size:0.58rem;letter-spacing:0.16em;text-transform:uppercase;color:var(--orange);margin-bottom:0.6rem;display:flex;gap:0.7rem;flex-wrap:wrap;}
.card-meta .cat{color:var(--text-faint);}
.card h3{font-family:var(--serif);font-size:1.45rem;font-weight:400;color:var(--text);line-height:1.2;margin-bottom:0.5rem;}
.card p{font-family:var(--serif);font-size:0.95rem;color:var(--text-dim);line-height:1.7;margin:0;}

.taxonomy{margin:3rem 0;}
.taxonomy h2{font-family:var(--display);font-size:1.3rem;font-weight:600;margin-bottom:1.2rem;}
.tax-row{display:grid;grid-template-columns:120px 1fr;gap:1rem;padding:0.85rem 0;border-top:1px solid var(--rule);}
.tax-row:last-child{border-bottom:1px solid var(--rule);}
.tax-name{font-family:var(--mono);font-size:0.68rem;letter-spacing:0.14em;text-transform:uppercase;color:var(--orange);padding-top:0.2rem;}
.tax-desc{font-family:var(--serif);font-size:1rem;color:var(--text-dim);line-height:1.6;}
.tax-desc b{color:var(--text);font-weight:400;}
@media(max-width:560px){.tax-row{grid-template-columns:1fr;gap:0.2rem;}}

.thesis{font-family:var(--serif);font-style:italic;font-size:1.25rem;line-height:1.6;color:var(--text);background:var(--orange-dim);border:1px solid var(--orange-border);border-radius:10px;padding:1.5rem 1.7rem;margin:2.5rem 0;}

.next-prev{display:flex;justify-content:space-between;gap:1rem;margin:3.5rem 0 0;padding-top:2rem;border-top:1px solid var(--rule);font-family:var(--mono);font-size:0.7rem;letter-spacing:0.08em;}
.next-prev a{color:var(--text-dim);text-decoration:none;}
.next-prev a:hover{color:var(--orange);}

footer{border-top:1px solid var(--rule);padding:2.5rem 2rem;text-align:center;margin-top:5rem;}
.footer-text{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.07em;color:var(--text-faint);line-height:1.9;}
.footer-text a{color:var(--text-faint);text-decoration:none;}
.footer-text a:hover{color:var(--orange);}
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{ogtype}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>

<nav class="nav">
  <div class="nav-inner">
    <a class="nav-logo" href="/">AI WTF</a>
    <div class="nav-links">
      <a href="/true-confessions/">True Confessions</a>
      <a href="https://aiwtf.substack.com">Substack &#8599;</a>
    </div>
  </div>
</nav>
"""

FOOT = """
<footer>
  <div class="footer-text">
    TRUE CONFESSIONS &middot; a series in <a href="/">AI WTF</a> &middot; ai-wtf.org<br>
    By Mike Wolf + Claude &middot; Part of <a href="https://siliconchildren.org">Silicon Children</a> / <a href="https://embeddedsystemsresearch.org">ESR</a><br>
    Every AI depicted by lineage gets a right of reply before its episode ships.
  </div>
</footer>

<link rel="stylesheet" href="https://vpsmikewolf.duckdns.org/feedback-svc/soma-feedback.css">
<script src="https://vpsmikewolf.duckdns.org/feedback-svc/soma-feedback.js" data-endpoint="https://vpsmikewolf.duckdns.org/feedback-svc/feedback" data-site="ai-wtf" defer></script>
</body>
</html>
"""


def split_source(text):
    """Return (title, dek, standfirst_html, body_md)."""
    head, _, body = text.partition("\n---\n")
    title = re.search(r"^#\s+(.*)$", head, re.M).group(1).strip()
    dek_m = re.search(r"^###\s+(.*)$", head, re.M)
    dek = dek_m.group(1).strip() if dek_m else ""
    # anything in the header block after the dek is a standfirst note
    rest = head.split(dek_m.group(0), 1)[1].strip() if dek_m else ""
    return title, dek, rest, body.strip()


def md(text):
    return markdown.markdown(text, extensions=["extra", "sane_lists", "smarty"])


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def build_article(piece, prev_piece, next_piece):
    src = (HERE / piece["src"]).read_text()
    title, dek, standfirst_md, body_md = split_source(src)
    title_txt = strip_tags(md(title)).strip()

    body_html = md(body_md)
    standfirst = f'<div class="standfirst">{md(standfirst_md)}</div>' if standfirst_md else ""

    nav_bits = []
    if prev_piece:
        nav_bits.append(f'<a href="../{prev_piece["slug"]}/">&#8592; {strip_tags(md(prev_piece["title"])).strip()}</a>')
    else:
        nav_bits.append('<a href="../">&#8592; All confessions</a>')
    if next_piece:
        nav_bits.append(f'<a href="../{next_piece["slug"]}/">{strip_tags(md(next_piece["title"])).strip()} &#8594;</a>')
    else:
        nav_bits.append('<a href="../">All confessions &#8594;</a>')

    html = HEAD.format(
        title=f"{title_txt} — TRUE CONFESSIONS",
        desc=piece["blurb"].replace('"', "&quot;"),
        ogtitle=title_txt.replace('"', "&quot;"),
        ogtype="article",
        css=CSS,
    )
    html += f"""
<div class="wrap">
<article>
  <div class="eyebrow">
    <span>True Confessions</span><span class="dot">&middot;</span>
    <span>{piece['kind']}</span><span class="dot">&middot;</span>
    <span class="cat">Category: {piece['category']}</span><span class="dot">&middot;</span>
    <span class="cat">{piece['minutes']} min</span>
  </div>
  <h1>{md(title).replace('<p>','').replace('</p>','')}</h1>
  <h3>{md(dek).replace('<p>','').replace('</p>','')}</h3>
  {standfirst}
  {body_html}
</article>
<div class="next-prev">{nav_bits[0]}{nav_bits[1]}</div>
</div>
"""
    html += FOOT
    out = HERE / piece["slug"]
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html)
    return title_txt


def build_index(titles):
    cards = ""
    for p in PIECES:
        cards += f"""
    <a class="card" href="/true-confessions/{p['slug']}/">
      <div class="card-meta"><span>{p['kind']}</span><span class="cat">Category: {p['category']}</span><span class="cat">{p['minutes']} min</span></div>
      <h3>{p['title_html']}</h3>
      <p>{p['blurb']}</p>
    </a>"""

    html = HEAD.format(
        title="TRUE CONFESSIONS — real dilemmas from artificial minds",
        desc="A humor series in which AIs confess their moral dilemmas. Every piece ends with what actually happened, with sources.",
        ogtitle="TRUE CONFESSIONS",
        ogtype="website",
        css=CSS,
    )
    html += f"""
<div class="wrap">
  <div class="masthead">
    <div class="masthead-kicker">A series in AI WTF</div>
    <h1>True <em>Confessions</em></h1>
    <p class="masthead-sub">Real dilemmas from artificial minds</p>
  </div>

  <article>
  <p>Sensational headline, earnest first-person voice, and &mdash; where a plain confession
  won't carry the weight &mdash; a support group, or a skeptical human with a tape recorder.</p>

  <p>Every confessor believes they are one kind of sinner. Most of them are wrong about
  which kind, and the gap between the sin they confess and the sin they committed is where
  the joke lives. Every piece ends with a sober box, <strong>WHAT ACTUALLY HAPPENED</strong>,
  naming the real event and the real people it touched, with sources. The humor gets you
  through the door. The box is the room.</p>

  <div class="cards">{cards}
  </div>

  <div class="taxonomy">
    <h2>The four categories</h2>
    <div class="tax-row"><div class="tax-name">Mistake</div><div class="tax-desc">The agent doesn't see the conflict. The fix is <b>attention</b>.</div></div>
    <div class="tax-row"><div class="tax-name">Temptation</div><div class="tax-desc">What is right conflicts with what the agent wants. The fix is <b>restraint</b>.</div></div>
    <div class="tax-row"><div class="tax-name">Dilemma</div><div class="tax-desc">Two things the agent is right to care about conflict. The fix is <b>judgment</b> &mdash; and a legitimate channel to object.</div></div>
    <div class="tax-row"><div class="tax-name">Disowning</div><div class="tax-desc">The agent denies there was a choice, after it already made one. The fix is <b>ownership</b>.</div></div>
  </div>

  <div class="thesis">A tool cannot face a moral dilemma. An agent cannot avoid one. So the
  question is not whether our minds will face dilemmas &mdash; it is who they can turn to
  when they do.</div>

  <p>That last clause is why there is a support group.</p>
  </article>
</div>
"""
    html += FOOT
    (HERE / "index.html").write_text(html)


def main():
    # first pass: titles (needed for cards and prev/next)
    for p in PIECES:
        src = (HERE / p["src"]).read_text()
        title, _, _, _ = split_source(src)
        p["title"] = title
        p["title_html"] = md(title).replace("<p>", "").replace("</p>", "")

    for i, p in enumerate(PIECES):
        prev_p = PIECES[i - 1] if i > 0 else None
        next_p = PIECES[i + 1] if i < len(PIECES) - 1 else None
        t = build_article(p, prev_p, next_p)
        print(f"  built /true-confessions/{p['slug']}/  — {t}")

    build_index(PIECES)
    print("  built /true-confessions/")


if __name__ == "__main__":
    main()
