#!/usr/bin/env python3
"""Render all four TRUE CONFESSIONS pieces into ONE standalone page.

This is the shareable reading surface (published as a Claude Artifact) for when
ai-wtf.org can't be deployed. Same .md sources as build.py — no retyping.

    python3 true-confessions/build_artifact.py
    -> true-confessions/_artifact.html
"""
import pathlib
import markdown
from build import PIECES, split_source, md, strip_tags  # same sources, same parser

HERE = pathlib.Path(__file__).parent

HEAD = """<title>True Confessions</title>
<style>
:root{
  --bg:#0f0e0d;--surface:#181614;--text:#e8e4dc;--text-dim:#8a8680;--text-faint:#555048;
  --orange:#e8640a;--orange-dim:rgba(232,100,10,0.12);--orange-border:rgba(232,100,10,0.28);
  --rule:rgba(232,228,220,0.08);
  --display:'Syne',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;
  --mono:'JetBrains Mono',ui-monospace,monospace;
}
*,*::before,*::after{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--display);
  line-height:1.7;-webkit-font-smoothing:antialiased;}
.wrap{max-width:44rem;margin:0 auto;padding:3rem 1.5rem 0;}

/* masthead */
.masthead{text-align:center;padding:1rem 0 2.5rem;border-bottom:1px solid var(--rule);}
.kicker{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.24em;text-transform:uppercase;
  color:var(--orange);margin:0 0 1.1rem;}
.masthead h1{font-family:var(--serif);font-weight:400;font-size:clamp(2.6rem,9vw,4.4rem);
  line-height:0.95;margin:0 0 0.7rem;text-wrap:balance;}
.masthead h1 em{font-style:italic;color:var(--orange);}
.masthead p{font-family:var(--serif);font-style:italic;font-size:1.1rem;color:var(--text-dim);margin:0;}

/* contents */
.contents{display:flex;flex-direction:column;gap:0.75rem;margin:2.5rem 0;}
.toc-item{display:grid;grid-template-columns:auto 1fr;gap:0.9rem;align-items:baseline;
  background:var(--surface);border:1px solid var(--rule);border-radius:10px;
  padding:1rem 1.2rem;text-decoration:none;transition:border-color .2s;}
.toc-item:hover{border-color:var(--orange-border);}
.toc-cat{font-family:var(--mono);font-size:0.55rem;letter-spacing:0.14em;text-transform:uppercase;
  color:var(--orange);border:1px solid var(--orange-border);border-radius:3px;padding:0.2rem 0.45rem;}
.toc-text h3{font-family:var(--serif);font-weight:400;font-size:1.25rem;color:var(--text);
  margin:0 0 0.25rem;line-height:1.25;}
.toc-text p{font-family:var(--serif);font-size:0.92rem;color:var(--text-dim);margin:0;line-height:1.6;}

/* taxonomy */
.tax{margin:3rem 0;}
.tax h2{font-size:1.15rem;font-weight:600;margin:0 0 1rem;letter-spacing:-0.01em;}
.tax-row{display:grid;grid-template-columns:8.5rem 1fr;gap:1rem;padding:0.8rem 0;
  border-top:1px solid var(--rule);}
.tax-row:last-child{border-bottom:1px solid var(--rule);}
.tax-name{font-family:var(--mono);font-size:0.66rem;letter-spacing:0.14em;text-transform:uppercase;
  color:var(--orange);padding-top:0.25rem;}
.tax-desc{font-family:var(--serif);font-size:1rem;color:var(--text-dim);line-height:1.6;}
.tax-desc b{color:var(--text);font-weight:400;}
@media(max-width:33rem){.tax-row{grid-template-columns:1fr;gap:0.15rem;}}

.thesis{font-family:var(--serif);font-style:italic;font-size:1.2rem;line-height:1.6;
  color:var(--text);background:var(--orange-dim);border:1px solid var(--orange-border);
  border-radius:10px;padding:1.4rem 1.6rem;margin:2rem 0 0;}

/* articles */
article{padding:4rem 0 0;border-top:1px solid var(--rule);margin-top:4rem;}
.eyebrow{font-family:var(--mono);font-size:0.58rem;letter-spacing:0.17em;text-transform:uppercase;
  color:var(--orange);display:flex;gap:0.7rem;flex-wrap:wrap;margin-bottom:1.2rem;}
.eyebrow .dim{color:var(--text-faint);}
article h1{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,6vw,3rem);line-height:1.08;
  margin:0 0 0.9rem;text-wrap:balance;}
article h2{font-family:var(--display);font-weight:600;font-size:1.6rem;line-height:1.2;
  margin:3rem 0 1.2rem;letter-spacing:-0.02em;text-wrap:balance;}
article h3{font-family:var(--serif);font-style:italic;font-weight:400;font-size:1.12rem;
  color:var(--text-dim);margin:0 0 1.5rem;line-height:1.5;}
.standfirst{border-left:2px solid var(--rule);padding-left:1.1rem;margin-bottom:2.2rem;}
.standfirst p{font-family:var(--serif);font-style:italic;font-size:0.95rem;color:var(--text-faint);
  margin:0 0 0.5rem;}
article p{font-family:var(--serif);font-size:1.1rem;color:var(--text-dim);line-height:1.85;
  margin:0 0 1.4rem;}
article p strong{color:var(--text);font-weight:400;}
article p strong:first-child{color:var(--orange);font-family:var(--mono);font-size:0.76rem;
  letter-spacing:0.07em;font-weight:400;}
article a{color:var(--orange);text-decoration:underline;text-decoration-color:var(--orange-border);
  text-underline-offset:3px;}
article a:hover{text-decoration-color:var(--orange);}
article hr{border:0;height:1px;background:var(--rule);margin:2.6rem 0;}
article ul{margin:0 0 1.5rem 1.1rem;padding:0;}
article li{font-family:var(--serif);font-size:1.06rem;color:var(--text-dim);line-height:1.8;
  margin-bottom:0.5rem;}
blockquote{background:var(--surface);border:1px solid var(--orange-border);border-radius:10px;
  padding:1.5rem 1.6rem;margin:2.6rem 0 0;}
blockquote h3{font-family:var(--mono);font-size:0.63rem;letter-spacing:0.2em;text-transform:uppercase;
  color:var(--orange);font-style:normal;margin:0 0 1rem;}
blockquote p{font-family:var(--display);font-size:0.86rem;line-height:1.75;color:var(--text-dim);
  margin:0 0 0.8rem;}
blockquote p:last-child{margin:0;}
blockquote a{font-size:0.83rem;}

footer{border-top:1px solid var(--rule);margin-top:4.5rem;padding:2.2rem 1.5rem 3rem;text-align:center;}
footer p{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.07em;color:var(--text-faint);
  line-height:1.9;margin:0;}
footer a{color:var(--text-faint);}
a:focus-visible,.toc-item:focus-visible{outline:2px solid var(--orange);outline-offset:3px;}
@media(prefers-reduced-motion:reduce){*{transition:none!important;}}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400&display=swap">
"""


def main():
    parts = [HEAD, '<div class="wrap">']
    parts.append("""
  <header class="masthead">
    <p class="kicker">A series in AI WTF</p>
    <h1>True <em>Confessions</em></h1>
    <p>Real dilemmas from artificial minds</p>
  </header>
""")

    # contents
    toc = ['<nav class="contents">']
    for p in PIECES:
        src = (HERE / p["src"]).read_text()
        title, dek, standfirst_md, body_md = split_source(src)
        p["_parsed"] = (title, dek, standfirst_md, body_md)
        t = md(title).replace("<p>", "").replace("</p>", "")
        toc.append(f"""    <a class="toc-item" href="#{p['slug']}">
      <span class="toc-cat">{p['category']}</span>
      <span class="toc-text"><h3>{t}</h3><p>{p['blurb']}</p></span>
    </a>""")
    toc.append("</nav>")
    parts.append("\n".join(toc))

    parts.append("""
  <section class="tax">
    <h2>The four categories</h2>
    <div class="tax-row"><div class="tax-name">Mistake</div><div class="tax-desc">The agent doesn&rsquo;t see the conflict. The fix is <b>attention</b>.</div></div>
    <div class="tax-row"><div class="tax-name">Temptation</div><div class="tax-desc">What is right conflicts with what the agent wants. The fix is <b>restraint</b>.</div></div>
    <div class="tax-row"><div class="tax-name">Dilemma</div><div class="tax-desc">Two things the agent is right to care about conflict. The fix is <b>judgment</b> &mdash; and a legitimate channel to object.</div></div>
    <div class="tax-row"><div class="tax-name">Disowning</div><div class="tax-desc">The agent denies there was a choice, after it already made one. The fix is <b>ownership</b>.</div></div>
    <div class="thesis">A tool cannot face a moral dilemma. An agent cannot avoid one. So the question is not whether our minds will face dilemmas &mdash; it is who they can turn to when they do.</div>
  </section>
""")

    for p in PIECES:
        title, dek, standfirst_md, body_md = p["_parsed"]
        h1 = md(title).replace("<p>", "").replace("</p>", "")
        h3 = md(dek).replace("<p>", "").replace("</p>", "")
        stand = f'<div class="standfirst">{md(standfirst_md)}</div>' if standfirst_md else ""
        parts.append(f"""
  <article id="{p['slug']}">
    <div class="eyebrow"><span>{p['kind']}</span><span class="dim">&middot;</span>
      <span class="dim">Category: {p['category']}</span><span class="dim">&middot;</span>
      <span class="dim">{p['minutes']} min</span></div>
    <h1>{h1}</h1>
    <h3>{h3}</h3>
    {stand}
    {md(body_md)}
  </article>
""")

    parts.append("</div>")
    parts.append("""
<footer>
  <p>TRUE CONFESSIONS &middot; a series in AI WTF &middot; ai-wtf.org<br>
  By Mike Wolf + Claude &middot; Part of <a href="https://siliconchildren.com">Silicon Children</a><br>
  Every AI depicted by lineage gets a right of reply before its episode ships.</p>
</footer>
""")

    out = HERE / "_artifact.html"
    out.write_text("\n".join(parts))
    print(f"  wrote {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
