#!/usr/bin/env python3
"""Applica a index.html (CV Studio):
 1. più spazio nella barra di export
 2. modulo della lettera di motivazione più elegante
Uso:  python applica_modifiche.py index.html   ->  scrive index.html (backup in index.html.bak)
"""
import re, sys, shutil

path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
src = open(path, encoding="utf-8").read().replace("\r\n", "\n")
shutil.copyfile(path, path + ".bak")

CSS = r"""
/* ---------- Barra export: più respiro ---------- */
.head-inner{gap:18px}
#docSw{gap:24px}
.export-card{gap:14px;padding:16px 14px 14px;border:1px solid #2f3a41;border-radius:12px;background:rgba(18,24,28,.55)}
.export-card #scopeSw{padding:3px}
.export-row{gap:8px}
@media (min-width:961px){
  .editor-header{padding:24px 18px 22px}
  #docSw{padding-top:6px}
  #docSw .lang-btn{padding:6px 0 12px}
  .export-card #scopeSw .lang-btn{padding:8px 6px}
  .export-main{height:42px}
  .export-alt button{width:42px;height:42px}
  .doc-title-row{height:42px}
}

/* ---------- Modulo lettera ---------- */
.fe-sec[data-g="letter"] .fe-body{gap:16px}
.fe-grp{display:flex;flex-direction:column;gap:14px;padding:16px 14px 14px;border:1px solid #3d4a52;border-radius:12px;background:#1c2328}
.fe-grp-t{display:flex;align-items:center;gap:12px;font-family:'Playfair Display',serif;font-style:italic;font-size:16px;color:#ffd9a0}
.fe-grp-t:after{content:'';flex:1;height:1px;background:linear-gradient(90deg,#e8b370,transparent)}
.fe-sec[data-g="letter"] .fe-f>span{font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#e9eef0}
.fe-sec[data-g="letter"] .fe-f>span small{display:block;margin-top:2px;font-size:11.5px;font-weight:400;letter-spacing:0;text-transform:none;font-style:italic;color:#9fb0b8}
.fe-sec[data-g="letter"] .fe-f input,
.fe-sec[data-g="letter"] .fe-f textarea{padding:10px 12px;border-radius:9px}
.fe-sec[data-g="letter"] .fe-f textarea[data-p="letter.body"]{min-height:300px;font-family:'Merriweather',Georgia,serif;font-size:14px;line-height:1.75}
"""

DICT_ADD = r"""
  "fg.recipient":["Destinataire","Recipient","Destinatario"],
  "fg.content":["Contenu","Content","Contenuto"],
  "fg.closing":["Conclusion","Closing","Conclusione"],"""

NEW_FUNC = r"""const labHtml=l=>{const m=String(l).match(/^(.*?)\s*\((.+)\)\s*$/);return m?`${esc(m[1])} <small>${esc(m[2])}</small>`:esc(l)};
const fGrp=(label,body)=>`<div class="fe-grp"><div class="fe-grp-t">${esc(label)}</div>${body}</div>`;
function buildLetterForm(){
  const F=(k,kind,r)=>fIn(t("f.l."+k),"letter."+k,kind,r);
  return fSec("letter",
    fGrp(t("fg.recipient"),F("recipient")+F("company")+F("address"))
   +fGrp(t("fg.content"),fTwo(F("city"),F("date"))+F("subject")+F("greeting")+F("body","area",14))
   +fGrp(t("fg.closing"),F("closing")+F("signature")));
}
"""

def must(cond, msg):
    if not cond:
        sys.exit("ERRORE: " + msg + " (file non modificato, backup in " + path + ".bak)")

# 1) CSS: in fondo al secondo <style>
must(src.count("</style>\n</head>") == 1, "fine dello <style> non trovata")
src = src.replace("</style>\n</head>", CSS + "</style>\n</head>")

# 2) DICT
anchor = '"f.l.signature":["Signature (vide = ton nom)","Signature (empty = your name)","Firma (vuota = il tuo nome)"],'
must(src.count(anchor) == 1, "riga f.l.signature non trovata")
src = src.replace(anchor, anchor + DICT_ADD)

# 3) buildLetterForm
pat = re.compile(r"function buildLetterForm\(\)\{.*?\n\}\n(?=function buildForm\(\))", re.S)
must(len(pat.findall(src)) == 1, "funzione buildLetterForm non trovata")
src = pat.sub(lambda m: NEW_FUNC, src)

# 4) fIn: etichette con nota piccola
old = '<label class="fe-f"><span>${esc(label)}</span>'
must(src.count(old) == 1, "etichetta in fIn non trovata")
src = src.replace(old, '<label class="fe-f"><span>${labHtml(label)}</span>')

open(path, "w", encoding="utf-8").write(src)
print("Fatto: modifiche applicate a", path)