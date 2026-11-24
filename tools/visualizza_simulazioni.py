"""Figura scientifica corrente: dati canonici del basso, nessuna nuova taratura."""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from fattibilita_basso import highpass,lr4_hp,transform

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research-vault/sistema-autonomo-20261120/fattibilita-basso.json'
TARGET=ROOT/'docs/figure/sistema-autonomo/fattibilita-basso.svg'


def render():
    report=json.loads(REPORT.read_text(encoding='utf-8'))
    font=ROOT/'build/consegna-cabinet-20261119/assets/Altro-Grotesk-Book.ttf'
    body=FontProperties(fname=str(font),size=10)
    heading=FontProperties(fname=str(font),size=13)
    matplotlib.rcParams.update({'svg.fonttype':'path','svg.hashsalt':'diy-2way-basso',
                                 'axes.edgecolor':'#D0D4E3','axes.labelcolor':'#0A0A0A',
                                 'text.color':'#0A0A0A','xtick.color':'#0A0A0A','ytick.color':'#0A0A0A'})
    frequencies=np.geomspace(20,500,800)
    fig,axes=plt.subplots(2,3,figsize=(16,9),sharex=True,sharey=True)
    legend=None
    for axis,row in zip(axes.flat,report['rows']):
        raw=highpass(frequencies,row['fc_hz'],row['qtc'])
        protected=raw*lr4_hp(frequencies,report['protection_hz'])
        corrected=protected*transform(frequencies,row['fc_hz'],row['qtc'],report['target_fc_hz'],report['target_q'])
        db=lambda x:20*np.log10(abs(x))
        at60=highpass(60,row['fc_hz'],row['qtc'])*lr4_hp(60,report['protection_hz'])
        assert abs(float(db(at60))-row['protected_60_db'])<1e-9
        corrected60=at60*transform(60,row['fc_hz'],row['qtc'],report['target_fc_hz'],report['target_q'])
        assert abs(float(db(corrected60))-report['target_edge_db'])<1e-9
        lines=[]
        for values,color,label,style in ((raw,'#4D11A7','Cassa chiusa senza EQ','-'),
                                          (protected,'#57CCF6','Cassa + HP35','--'),
                                          (corrected,'#AFD100','Cassa + LT nominale + HP35','-')):
            line,=axis.semilogx(frequencies,db(values),color=color,lw=2.2,label=label,ls=style)
            lines.append(line)
        low,high=row['fixed_eq_scenario_60_db_range']
        uncertainty=axis.errorbar([60],[-2],yerr=[[(-2)-low],[high-(-2)]],color='#000000',
                                 marker='o',markersize=4,capsize=5,lw=1.4,label='81 scenari a 60 Hz')
        legend=(*lines,uncertainty)
        axis.axhline(-2,color='#000000',ls=':',lw=.8)
        axis.axvline(60,color='#D0D4E3',ls=':',lw=.8)
        driver='SB16' if row['driver'].startswith('SB16') else 'SB15'
        note=' (base)' if driver=='SB16' and row['box']=='A24' else ''
        axis.set_title(f"{driver} / {row['box']}{note} · {row['net_l']:.2f} L",fontproperties=heading,pad=10)
        axis.set_ylim(-55,6); axis.set_xlim(20,500)
        axis.set_xticks([20,35,60,100,200,500],['20','35','60','100','200','500'])
        axis.minorticks_off(); axis.grid(color='#D0D4E3',lw=.6,alpha=.8)
        for tick in (*axis.get_xticklabels(),*axis.get_yticklabels()): tick.set_fontproperties(body)
        axis.set_xlabel('Frequenza [Hz]',fontproperties=body)
        axis.set_ylabel('Livello relativo [dB]',fontproperties=body)
    fig.suptitle('Estensione in basso: cassa chiusa, protezione e correzione nominale',fontproperties=FontProperties(fname=str(font),size=21),y=.97)
    fig.legend(legend,[p.get_label() for p in legend],loc='upper center',bbox_to_anchor=(.5,.91),
               ncol=4,frameon=False,prop=body)
    fig.text(.07,.035,'Sei abbinamenti matematici, non scelte esecutive. Intervalli: scenari ipotetici a EQ fissa, non tolleranze di fabbrica.\nModello a piccoli segnali; stanza, direttività e prestazioni reali non misurate.',fontproperties=body)
    fig.subplots_adjust(left=.07,right=.98,top=.83,bottom=.15,hspace=.4,wspace=.17)
    output=io.StringIO(); fig.savefig(output,format='svg',metadata={'Date':None,'Creator':'visualizza_simulazioni.py'}); plt.close(fig)
    svg=output.getvalue()
    provenance={'report':str(REPORT.relative_to(ROOT)).replace('\\','/'),
                'report_sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),
                'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'matplotlib':matplotlib.__version__,'curves':18,'panels':6,
                'status':'Modello nominale, non misura dei diffusori'}
    position=svg.index('>',svg.index('<svg'))+1
    return (svg[:position]+'\n<metadata id="provenienza-diy">'+html.escape(json.dumps(provenance,ensure_ascii=False))+'</metadata>'+svg[position:]).encode('utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    result=render()
    if args.check:
        ok=TARGET.exists() and TARGET.read_bytes()==result
        print('Figura basso: '+('coerente con dati e generatore' if ok else 'da rigenerare'))
        raise SystemExit(0 if ok else 1)
    TARGET.parent.mkdir(parents=True,exist_ok=True); TARGET.write_bytes(result)
    print(str(TARGET.relative_to(ROOT)))


if __name__=='__main__': main()
