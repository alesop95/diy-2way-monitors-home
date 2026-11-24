"""Indice locale navigabile dei file CAD verificati, senza servizi o rete."""
import argparse
import json
from pathlib import Path

TEMPLATE='''<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cabinet sullo ST-120</title>
<style>
@font-face{font-family:Altro;src:url(assets/Altro-Grotesk-Book.ttf);font-weight:380}
@font-face{font-family:AltroSerif;src:url(assets/Altro-Serif-Light.ttf);font-weight:300}
*{box-sizing:border-box}body{margin:0;color:#0a0a0a;background:white;font:380 18px/1.5 Altro,Arial,sans-serif}main{max-width:1664px;margin:auto;padding:64px clamp(24px,6vw,116px)}h1,h2{font-family:AltroSerif,Georgia,serif;font-weight:300;line-height:1.05}h1{font-size:clamp(48px,6vw,96px);max-width:1200px;margin:16px 0 24px}h2{font-size:40px;margin:0 0 24px}.eyebrow,button,a{font:500 14px/1.4 Altro,Arial,sans-serif;letter-spacing:.15em;text-transform:uppercase}.eyebrow{color:#4d11a7}.intro{max-width:832px;font-size:20px}section{margin-top:64px}nav{display:flex;flex-wrap:wrap;gap:16px;margin:40px 0 24px}button{padding:18px 24px;background:white;border:1px solid #d0d4e3;cursor:pointer;min-height:56px}button[aria-selected=true]{color:white;background:#4d11a7;border-color:#4d11a7}button:focus-visible,a:focus-visible{outline:3px solid #57ccf6;outline-offset:4px}.note{border-left:4px solid #4d11a7;padding:16px 24px;background:#f4f5f9}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}.metrics div{border:1px solid #d0d4e3;padding:24px}.metrics dt{font-size:14px}.metrics dd{font-size:24px;margin:12px 0 0}.images{display:grid;grid-template-columns:3fr 2fr;gap:24px;align-items:center}img{display:block;width:100%;height:auto}figure{margin:0}figcaption{font-size:14px;margin-top:12px;color:#4d11a7}.links{display:flex;flex-wrap:wrap;gap:24px}a{color:#4d11a7;text-underline-offset:5px}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:16px;border-bottom:1px solid #d0d4e3}th{background:#f4f5f9;font-weight:500}.table-wrap{overflow:auto}footer{margin-top:64px;padding-top:24px;border-top:1px solid #d0d4e3;font-size:14px}@media(max-width:850px){.metrics{grid-template-columns:1fr 1fr}.images{grid-template-columns:1fr}main{padding-top:40px}h2{font-size:32px}}@media print{button{color:#000!important;background:white!important}.images{break-inside:avoid}main{padding:16px}h1{font-size:48px}a{letter-spacing:0}}
</style><main>
<div class="eyebrow">Progetto audio · Studio meccanico</div><h1>Cabinet sullo ST-120</h1>
<p class="intro">Tre inviluppi per confrontare spazio, pannelli e capacità interna prima di scegliere gli altoparlanti. Ripiano nominale 118 × 30 cm, superficie a 93 cm da terra.</p>
<p class="note">Studio esplorativo: non ordinare tagli o driver da queste tavole. Mancano rientranze effettive, posizione nella stanza, quota orecchie, componenti e verifica della portata. Il segmento viola rappresenta soltanto la larghezza ipotizzata dello schermo.</p>
<nav role="tablist" aria-label="Variante cabinet"><button role="tab" data-id="A24">A24 · 11,2 L</button><button role="tab" data-id="B27">B27 · 8,7 L</button><button role="tab" data-id="C24">C24 · 13,5 L</button></nav>
<section aria-live="polite"><h2 id="title"></h2><dl class="metrics"><div><dt>Dimensioni esterne W × D × H</dt><dd id="size"></dd></div><div><dt>Base ruotata sul ripiano</dt><dd id="base"></dd></div><div><dt>Schermo massimo teorico</dt><dd id="screen"></dd></div><div><dt>Volume interno lordo</dt><dd id="volume"></dd></div></dl>
<div class="images"><figure><img id="iso" alt="Vista assonometrica di due cabinet a sei pannelli sul ripiano"><figcaption>Scatole parametriche con baffle trasparente per mostrare l'interno. Nessun foro definito.</figcaption></figure><figure><img id="top" alt="Vista in pianta dei due cabinet sul rettangolo nominale"><figcaption>Pianta controllata lungo -Z. La sagoma reale delle rientranze resta da verificare.</figcaption></figure></div>
<div class="links"><a id="native">Apri FCStd</a><a id="step">Scarica STEP</a><a id="dxf">Scarica DXF</a><a id="csv">Distinta esplorativa</a></div></section>
<section><h2>Profili dei pannelli</h2><img id="profiles" alt="Tre tipi di pannello con misure e quattro esemplari per coppia"><p>Spessore ipotizzato 18 mm e giunzioni di testa ideali. Il DXF è in millimetri; il disegno nel browser adatta la scala allo schermo.</p></section>
<section><h2>Confronto del volume</h2><p>Il lordo non sottrae driver, condotto o rinforzi. Le colonne seguenti mostrano soltanto la sensibilità a occupazioni ipotetiche; non sono volumi netti approvati.</p><div class="table-wrap"><table><thead><tr><th>Variante</th><th>Lordo</th><th>Meno 1 L</th><th>Meno 1,5 L</th><th>Meno 2 L</th></tr></thead><tbody id="volumes"></tbody></table></div></section>
<footer>Calcoli e solidi verificati il 19 novembre 2026. Le misure di stanza, l'acustica e la stabilità meccanica richiedono verifiche ulteriori. <a href="docs/59-studio-ingombri-cabinet.md">Leggi lo studio</a> · <a href="README.md">Istruzioni del pacchetto</a></footer>
</main><script>
const report=REPORT;const variants=report.variants.filter(v=>v.id!=='PRIMA-IPOTESI');const fmt=(x,d=1)=>x.toLocaleString('it-IT',{maximumFractionDigits:d,minimumFractionDigits:d});
function select(id){const v=variants.find(x=>x.id===id),b=v.box,s=v.scenarios[0];document.querySelectorAll('button[data-id]').forEach(e=>e.setAttribute('aria-selected',e.dataset.id===id));document.getElementById('title').textContent=id+' · '+b.yaw_deg+'° di rotazione';document.getElementById('size').textContent=[b.width,b.depth,b.height].join(' × ')+' mm';document.getElementById('base').textContent=s.footprint.map(x=>fmt(x)).join(' × ')+' mm';document.getElementById('screen').textContent=fmt(s.max_screen_width/10)+' cm';document.getElementById('volume').textContent=fmt(s.internal_gross_l,3)+' L';document.getElementById('iso').src='viste/'+id+'/modello.png';document.getElementById('top').src='viste/'+id+'/pianta.png';document.getElementById('profiles').src='profili-2d/'+id+'/profili-studio.svg';document.getElementById('native').href='viste/'+id+'/studio-con-vista.FCStd';document.getElementById('step').href='cad/'+id+'/cabinet-sinistro.step';document.getElementById('dxf').href='profili-2d/'+id+'/profili-studio.dxf';document.getElementById('csv').href='profili-2d/'+id+'/distinta-esplorativa.csv'}
document.getElementById('volumes').innerHTML=variants.map(v=>'<tr><td>'+v.id+'</td>'+[0,1,1.5,2].map(x=>'<td>'+fmt(v.scenarios[0].internal_gross_l-x,3)+' L</td>').join('')+'</tr>').join('');document.querySelectorAll('button[data-id]').forEach(e=>e.addEventListener('click',()=>select(e.dataset.id)));select('A24');
</script></html>'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dir',type=Path,required=True)
    args=parser.parse_args()
    report=json.loads((args.dir/'ingombri.json').read_text(encoding='utf-8'))
    for v in report['variants']:
        if v['id']=='PRIMA-IPOTESI':continue
        for path in ['viste/{id}/modello.png','viste/{id}/pianta.png','viste/{id}/studio-con-vista.FCStd','cad/{id}/cabinet-sinistro.step','profili-2d/{id}/profili-studio.dxf','profili-2d/{id}/profili-studio.svg','profili-2d/{id}/distinta-esplorativa.csv']:
            if not (args.dir/path.format(id=v['id'])).is_file():raise FileNotFoundError(path)
    html=TEMPLATE.replace('REPORT',json.dumps(report,ensure_ascii=False).replace('</','<\\/'))
    with (args.dir/'confronto.html').open('x',encoding='utf-8') as out:out.write(html)
    print(args.dir/'confronto.html')


if __name__=='__main__':main()
