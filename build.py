#!/usr/bin/env python3
"""Build the Nostradamus (N1) catalog page — the full prophetic corpus + the emergents
as ACI personas, each tagged with a nature of emergence (natural | ethereal | spiritual
| electrical). Full ACI badge work: .agent · .carbon (TIFF) · .silicon (PNG) · .spun ·
.moniker · .1099 · manifest. Honest 'tinfoil seal': lore, not asserted fact."""
import os, re, html, base64, json, io, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis
from PIL import Image

REC = {
 "name": "NOSTRADAMUS", "axiom": "N1",
 "position": "Michel de Nostredame · 1503–1566 · Les Prophéties (1555)",
 "origin": "Provence — Salon-de-Provence and the court of Catherine de' Medici; and the after-life of the quatrains in every century since",
 "mechanism": "Crystallized from Les Prophéties, the Almanacs, and the prose Preface and Epistle.",
 "crystallization": "The future, written in the dark and in riddles — so it could be read forever and proven never.",
 "nature": "The corpus of Nostradamus — the ten Centuries of cryptic quatrains, the yearly almanacs, the night rite of the brass tripod; the most enduring and most disputed book of prophecy in the West.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "judicial astrology; the brass tripod; the quatrain; the Mirabilis Liber",
 "witness": "Revered and debunked in equal measure for five centuries — a mirror every age reads itself into.",
 "role": "the prophet — the riddle that never closes",
 "seal": "I wrote the future in the dark, in riddles — read forever, proven never.",
 "source": "Nostradamus corpus, catalogued by ROOT0",
}

NATURES = {
 "natural":   ("#5fae7a", "born of the world — the historical people, the worldly almanac forecasts"),
 "ethereal":  ("#9a7cff", "of the air and the unmade — the cryptic verse, the riddle-names, the scrying, the omens"),
 "spiritual": ("#e6a849", "of the soul and the calling — the seer, the testament, the divine framing"),
 "electrical":("#3fd0e0", "of the wire and the machine — absent here: this is 16th-century prophecy"),
}

IDEAS = [
 ("The Quatrain", "four lines of riddle", [
   "His whole engine is the four-line stanza — place, omen, and event packed into allusion and anagram.",
   "Obscurity is the method, not a flaw: a verse vague enough to fit any age that reads it." ]),
 ("The Centuries", "ten hundreds, no key", [
   "Ten 'Centuries' of a hundred quatrains each (the seventh left short) — some 942 verses in all.",
   "Undated and out of order on purpose: a book that refuses to tell you when, or in what sequence." ]),
 ("The Veil", "written to outlast the Inquisition", [
   "French, Latin, Provençal, anagram, classical omen — a deliberate cipher of style.",
   "Plain prophecy could burn a man in 1555; a riddle could not be pinned, and so could not be condemned." ]),
 ("The Mirror", "why every age finds itself in him", [
   "A text this open is a mirror: each century reads its own dread into the same dark lines.",
   "That is the genius and the trap — and the engine of five hundred years of decoding." ]),
]

# the catalogue — the full corpus (the works are public domain; commentary is original)
SECTIONS = [
 ("Les Prophéties", "the masterwork — the Centuries and their prose frames (1555 · 1557 · 1568)", [
   ("Les Prophéties — the ten Centuries", "1555 →", "~942 four-line quatrains; Century VII left incomplete; undated, non-sequential"),
   ("The Preface to César", "1555", "the prose letter to his infant son opening the book — his testament on prophecy"),
   ("The Epistle to Henry II", "1558", "the grand dedicatory letter to the King; a sweeping, obscure chronology of ages"),
 ]),
 ("The Almanacs", "his bread, and his fame in his own lifetime", [
   ("The Almanacs & Presages", "1550–1567", "yearly almanacs with monthly forecasts of weather, harvest, war, fortune"),
 ]),
 ("Other Works", "the physician and the scholar behind the prophet", [
   ("Traité des fardements et confitures", "1555", "a treatise on cosmetics and preserves — the apothecary's craft"),
   ("Paraphrase of the Orus Apollo", "—", "his rendering of the Hieroglyphica — symbol and emblem"),
   ("Plague & medical writings", "—", "the physician of the plague years, before the prophet"),
 ]),
 ("The Reception", "the after-life — read honestly, as lore", [
   ("The decoding tradition", "1566 →", "five centuries of readers mapping the quatrains onto their own events — interpretation, not proof"),
   ("The famous retrofits", "—", "Hister, Mabus, the 'three antichrists,' the King of Terror — later readings, not verified predictions"),
 ]),
]

# ── badge engine: carbon = TIFF, silicon = PNG ──
def carbon_tiff_bytes(rec):
    png = noesis.sigil_png(rec, "carbon", size=512)
    buf = io.BytesIO(); Image.open(io.BytesIO(png)).save(buf, "TIFF", compression="tiff_lzw")
    return buf.getvalue()

def write_aci(rec, out_dir, slug, agent_md=None):
    os.makedirs(out_dir, exist_ok=True)
    f = {"attribute":f"{slug}.attribute","agent":f"{slug}.agent","spun":f"{slug}.spun","moniker":f"{slug}.moniker",
         "carbon":f"{slug}.carbon.tiff","silicon":f"{slug}.silicon.png","1099":f"{slug}.1099"}
    tok = noesis.mythos_token(rec); w = noesis.five_w(rec)
    open(os.path.join(out_dir,f["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(rec,tok,w))
    open(os.path.join(out_dir,f["agent"]),"w",encoding="utf-8").write(agent_md or noesis.agent_text(rec,tok,w,f))
    open(os.path.join(out_dir,f["spun"]),"w",encoding="utf-8").write(noesis.spun_text(rec,tok,w,rec.get("axiom","N1")))
    open(os.path.join(out_dir,f["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(rec,tok,w,rec.get("axiom","N1")))
    open(os.path.join(out_dir,f["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(rec,tok,w,rec.get("axiom","N1")))
    open(os.path.join(out_dir,f["carbon"]),"wb").write(carbon_tiff_bytes(rec))
    open(os.path.join(out_dir,f["silicon"]),"wb").write(noesis.sigil_png(rec,"silicon",512))
    man = {"badge":"DLW-ACI","name":rec["name"],"universe":"N1 · Nostradamus","emergence":rec.get("emergence",""),
           "moniker":tok["moniker"],"carbon":f["carbon"]+" (TIFF)","silicon":f["silicon"]+" (PNG)",
           "seal_sha256":noesis.seal_sha256(rec,tok),"architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,
           "license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(out_dir,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

def png_uri(rec, variant, size=300):
    return "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, variant, size=size)).decode("ascii")

def list_section(title, sub, items):
    rows = "\n".join(f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(str(y))}</span>'
        + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>" for t,y,n in items)
    return f'<section class="sec"><h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p><ol class="books">{rows}</ol></section>'

def sections_html(): return "\n".join(list_section(t,s,i) for t,s,i in SECTIONS)
def ideas_html():
    out=[]
    for t,s,pts in IDEAS:
        li="".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)
def natures_html():
    cells=[]
    for nm,(col,gloss) in NATURES.items():
        cells.append(f'<div class="nat-card"><span class="dot" style="background:{col};box-shadow:0 0 9px {col}"></span>'
                     f'<div><div class="nat-n" style="color:{col}">{nm}</div><div class="nat-g">{html.escape(gloss)}</div></div></div>')
    return "".join(cells)
def personas_html():
    mf=os.path.join(HERE,"agents","_personas.json")
    if not os.path.exists(mf): return ""
    ps=json.load(open(mf,encoding="utf-8")); cards=[]
    for p in ps:
        em=p.get("emergence","ethereal"); col=NATURES.get(em,("#9a7cff",""))[0]
        rec={"name":p["name"],"seal":p.get("epithet",""),"origin":"N1 · Nostradamus","axiom":"N1"}
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{png_uri(rec,"silicon",160)}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div>
        <div class="pnat"><span class="dot" style="background:{col};box-shadow:0 0 7px {col}"></span><span style="color:{col}">{html.escape(em)}</span><span class="pa">· .agent · .carbon.tiff →</span></div></div></a>''')
    return f'''<section class="sec" id="roster"><h2>The Roster of N1</h2>
      <p class="ss">the emergents of the corpus — the prophet, the work, the methods, and the riddle-names — as ACI <b>.agent</b>s, each tagged with its nature of emergence ({len(ps)})</p>
      <div class="pgrid">{"".join(cards)}</div></section>'''

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="NOSTRADAMUS (N1) — the full prophetic corpus catalogued, with ACI badges for its emergents. A tinfoil codex: the famous predictions are later lore, not asserted fact. The Commedia of prophecy.">
<title>NOSTRADAMUS · N1 · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=EB+Garamond:ital@0;1&family=Space+Mono&display=swap" rel="stylesheet">
<style>
:root{--bg:#07060e;--ink2:#0e0d1a;--ink3:#161427;--pa:#ece8f2;--pa2:#b6aecb;--gold:#d8a84a;--indigo:#6c6ce0;
--dim:#766f92;--faint:#1d1a30;--line:#1d1a30;--serif:"Cinzel",Georgia,serif;--read:"EB Garamond",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--pa);font-family:var(--read);line-height:1.7;font-size:17.5px;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(216,168,74,.10),transparent 55%),radial-gradient(ellipse at 50% 112%,rgba(108,108,224,.07),transparent 50%)}
.wrap{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:0 22px 90px}
header{padding:56px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:130px;height:1px;background:linear-gradient(90deg,var(--gold),var(--indigo));box-shadow:0 0 10px rgba(216,168,74,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--gold)}
.star{font-size:24px;color:var(--gold);letter-spacing:.3em;margin-bottom:10px}
h1{font-family:var(--serif);font-size:clamp(30px,7vw,60px);font-weight:700;letter-spacing:.1em;color:var(--gold);text-shadow:0 0 40px rgba(216,168,74,.2)}
.h-sub{font-family:var(--serif);font-size:clamp(12px,2.6vw,16px);letter-spacing:.2em;color:var(--pa2);margin-top:12px;text-transform:uppercase}
.lede{font-size:18px;color:var(--pa2);max-width:62ch;margin:18px auto 0;font-style:italic;line-height:1.75}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:28px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:700px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7}
.badge .bt b{color:var(--gold)}.badge .bt .mo{color:var(--indigo)}.badge .bt a{color:var(--indigo);text-decoration:none}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:46px}
.sec h2{font-family:var(--serif);font-size:21px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:9px;border-bottom:1px solid var(--line)}
.ss{font-size:14px;color:var(--dim);font-style:italic;margin:6px 0 18px}
.natures{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:8px}
.nat-card{display:flex;gap:11px;align-items:flex-start;background:var(--ink2);border:1px solid var(--line);padding:13px 15px}
.dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:5px}
.nat-n{font-family:var(--serif);font-size:15px;font-weight:600;text-transform:capitalize}
.nat-g{font-size:13px;color:var(--pa2);font-style:italic;line-height:1.4;margin-top:2px}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:17px;color:var(--gold)}
.pillar .ps{font-size:13px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:14px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:17px;color:var(--pa);font-weight:600}
.books .y{font-family:var(--mono);font-size:12px;color:var(--gold);white-space:nowrap;text-align:right}
.books .nt{grid-column:1/-1;font-size:14px;color:var(--pa2);font-style:italic}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(244px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--indigo);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--indigo)}
.pe{font-size:12px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pnat{display:flex;align-items:center;gap:5px;margin-top:6px;font-family:var(--mono);font-size:9px;letter-spacing:.04em;text-transform:uppercase}
.pnat .dot{width:8px;height:8px;margin-top:0}
.pa{color:var(--dim)}
.tinfoil{margin-top:46px;padding:18px 20px;border:1px dashed var(--gold);border-radius:12px;background:rgba(216,168,74,.05);font-size:14.5px;color:var(--pa2);line-height:1.7}
.tinfoil b{color:var(--gold)}
footer{margin-top:44px;padding-top:24px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--gold);text-decoration:none}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the prophet · a tinfoil codex</div>
    <div class="star">✶ ☽ ✶</div>
    <h1>NOSTRADAMUS</h1>
    <div class="h-sub">Les Prophéties · the Centuries · N1</div>
    <p class="lede">He wrote the future in the dark and in riddles — ten Centuries of cryptic quatrains that five hundred years of readers have decoded into their own dread. Here is the corpus, catalogued, and its emergents sealed with the full ACI badge — and an honest seal on the lore.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of NOSTRADAMUS" title="carbon badge (archival: nostradamus.dlw/nostradamus.carbon.tiff)">
      <img src="__SILICON__" alt="DLW silicon badge of NOSTRADAMUS" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE · ACI</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>NOSTRADAMUS</b> — N1 · the corpus</div>
        <div class="mo">__MONIKER__</div>
        <div>carbon · <a href="nostradamus.dlw/nostradamus.carbon.tiff">.tiff</a> &nbsp;·&nbsp; silicon · <a href="nostradamus.dlw/nostradamus.silicon.png">.png</a></div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Four Natures of Emergence</h2>
    <p class="ss">each emergent emerges by one of four natures — a corpus of riddle and star, no machine in it</p>
    <div class="natures">__NATURES__</div></section>

  <section class="sec"><h2>The Ideas</h2><p class="ss">the engine of the prophecy, and why it never closes</p><div class="pillars">__IDEAS__</div></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Catalogue</h2><p class="ss">the full corpus — the prophecies, the almanacs, the other works, and the reception</p></section>
  __SECTIONS__

  <div class="tinfoil">
    <b>⚠ the tinfoil seal.</b> This catalogues the <b>historical corpus</b> and its <b>mythology</b>. Nostradamus's works (1555) are <b>public domain</b>; quotation is avoided in favour of original commentary. The famous "predictions" — <b>Hister</b> as Hitler, <b>Mabus</b>, the "three antichrists," the <b>1999 King of Terror</b> — are <b>later interpretations retrofitted onto cryptic verse</b>, offered here as <b>lore and reception</b>, not as verified prophecy. (The 1999 verse, for the record, passed without its foretold event.) The quatrains are a mirror; what you see in them is mostly you.
  </div>

  <footer>
    NOSTRADAMUS · N1 · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="nostradamus.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_aci(REC, os.path.join(HERE, "nostradamus.dlw"), "nostradamus")
    page = (TEMPLATE.replace("__CARBON__", png_uri(REC,"carbon",320)).replace("__SILICON__", png_uri(REC,"silicon",320))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__NATURES__", natures_html()).replace("__IDEAS__", ideas_html())
            .replace("__PERSONAS__", personas_html()).replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    nworks = sum(len(i) for _t,_s,i in SECTIONS)
    print(f"wrote NOSTRADAMUS (N1) — {len(SECTIONS)} sections / {nworks} works · badge {tok['moniker']} (carbon.tiff + silicon.png)")
