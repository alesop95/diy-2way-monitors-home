"""Figure scientifiche dai modelli verificati, con il design system di account."""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path
import math
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import fontManager
import acustica_cabinet as ac
from fattibilita_basso import lr4_hp,transform,target_frequency
from studio_sistema_audio import closed_box
from studio_completamento import ROOT,build_report
from progetto_cabinet import load_project

REPORT=ROOT/'research-vault/completamento-20261125/risultati.json'
PUBLIC=ROOT/'docs/figure/completamento-20261125'
COLORS=['#4D11A7','#57CCF6','#AFD100','#0A0A0A']


def render(fontdir):
    report=json.loads(REPORT.read_text(encoding='utf-8'));report.pop('generated_at',None)
    if report!=build_report(): raise RuntimeError('Rapporto non corrente: rigenerare prima dei grafici')
    for filename in ('Altro-Grotesk-Book.ttf','Altro-Serif-Light.ttf'):
        font=fontdir/filename
        if not font.is_file(): raise FileNotFoundError('Font di account assente: '+filename)
        fontManager.addfont(str(font))
    plt.rcParams.update({'font.family':'Altro Grotesk Book','font.size':11,
        'axes.titlesize':14,'axes.titlepad':14,'axes.labelsize':11,'axes.edgecolor':'#D0D4E3',
        'text.color':'#0A0A0A','axes.labelcolor':'#0A0A0A','xtick.color':'#0A0A0A','ytick.color':'#0A0A0A',
        'grid.color':'#D0D4E3','legend.frameon':False,'svg.fonttype':'path','svg.hashsalt':'diy-completamento'})
    config,geometries=load_project()
    drivers={d['id']:d for d in json.loads((ROOT/'data/driver-candidati.json').read_text(encoding='utf-8'))['woofers']}
    f=np.geomspace(20,500,801);hp=lr4_hp(f,35)
    figures={}
    fig,axes=plt.subplots(1,3,figsize=(13,5),layout='constrained')
    for axis,row in zip(axes,report['sealed']):
        driver=drivers[row['driver']]
        raw=closed_box(f,driver['fs_hz'],driver['qts'],driver['vas_l'],row['net_assumed_l'])
        corrected=raw*hp*transform(f,row['fc_hz'],row['qtc'],target_frequency(60,-2,35),1/math.sqrt(2))
        axis.semilogx(f,20*np.log10(abs(raw)*hp),color=COLORS[0],label='Chiusa + HP35')
        axis.semilogx(f,20*np.log10(abs(corrected)),color=COLORS[0],ls='--',label='Chiusa + LT + HP35')
        for fb,color in zip((40,45,50),COLORS[1:]):
            p=next(p for p in report['reflex'] if p['id']==row['id'] and p['fb_hz']==fb and p['diameter_mm']==30 and p['port_q_hypothetical']==10)
            h=ac.vented_box(f,driver['fs_hz'],driver['qts'],driver['vas_l'],p['net_volume_l'],fb,10)['total']
            axis.semilogx(f,20*np.log10(abs(h)*hp),color=color,label=f'Reflex {fb} Hz')
        axis.set(title=row['id']+' / '+row['driver'].split('-')[0],xlabel='Frequenza [Hz]',ylabel='Livello relativo [dB]',
                 xlim=(20,500),ylim=(-35,5))
        axis.set_xticks([20,60,200,500],['20','60','200','500']);axis.minorticks_off()
        axis.axhline(-2,color='#D0D4E3',ls=':');axis.axvline(60,color='#D0D4E3',ls=':')
        axis.grid(True,which='both');axis.legend(fontsize=9,loc='lower right')
    figures['chiusa-reflex']=fig

    fig,axes=plt.subplots(1,3,figsize=(13,5),layout='constrained')
    for axis,variant in zip(axes,config['variants']):
        for fb,color in zip((35,40,45,50),COLORS):
            rows=[r for r in report['reflex'] if r['id']==variant['id'] and r['fb_hz']==fb and r['port_q_hypothetical']==10]
            for row,marker in zip(rows,('o','s','^')):
                axis.scatter(row['internal_length_mm']+row['diameter_mm'],row['port_mach_peak_max'],
                             marker=marker,color=color,s=65)
                axis.annotate(str(row['diameter_mm']),
                    (row['internal_length_mm']+row['diameter_mm'],row['port_mach_peak_max']),xytext=(4,4),textcoords='offset points',fontsize=9)
            axis.plot([],[],color=color,label=f'{fb} Hz')
        depth=variant['cabinet']['depth']-2*variant['cabinet']['thickness']
        axis.axvline(depth,color='#0A0A0A',ls='--',lw=1,label='Profondità interna')
        axis.axhline(.05,color='#D0D4E3',ls=':',label='Mach 0,05: riferimento')
        axis.set(title=variant['id'],xlabel='Tratto interno + 1 diametro libero [mm]',ylabel='Mach di picco, ipotesi 90 dB',ylim=(0,.1))
        axis.grid();axis.legend(fontsize=8)
    figures['condotto-ingombro-velocita']=fig

    fig,axes=plt.subplots(1,3,figsize=(13,5),layout='constrained')
    frequencies=np.geomspace(500,8000,161);angles=np.linspace(-60,60,121)
    cmap=LinearSegmentedColormap.from_list('Intrawelt',['#FFFFFF','#57CCF6','#4D11A7'])
    for axis,variant,geo in zip(axes,config['variants'],report['cabinet_details']):
        values=ac.two_way_response(frequencies[None,:],angles[:,None],drivers[variant['woofer']]['sd_cm2'],
            geometries[variant['tweeter']]['sd_cm2'],geo['driver_spacing_mm'],2600,0,capacitor_uf=47)
        image=axis.pcolormesh(frequencies,angles,20*np.log10(np.maximum(abs(values),1e-9)),
            cmap=cmap,vmin=-30,vmax=0,shading='auto',rasterized=True,antialiased=False,edgecolors='none')
        axis.set_xscale('log');axis.set_xticks([500,1000,2600,8000],['500','1k','2,6k','8k'])
        axis.minorticks_off()
        axis.set(title=variant['id']+f" / {geo['driver_spacing_mm']:g} mm",xlabel='Frequenza [Hz]',ylabel='Angolo verticale [gradi]')
        axis.axhline(10,color='#0A0A0A',lw=.6,ls=':');axis.axhline(-10,color='#0A0A0A',lw=.6,ls=':')
    fig.colorbar(image,ax=axes,label='Livello relativo [dB]',ticks=[-30,-20,-10,-6,-3,0],shrink=.85)
    figures['direttivita-ideale']=fig

    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    cf=np.geomspace(200,10000,301)
    rc=ac.series_capacitor_response(cf,3.2,47)
    axes[0].semilogx(cf,20*np.log10(abs(rc)),color=COLORS[0],label='Solo RC, 3,2 ohm e 47 µF')
    summed=ac.two_way_response(cf,0,124,6.2,132,2600,0,capacitor_uf=47)
    axes[0].semilogx(cf,20*np.log10(abs(summed)),color=COLORS[1],label='Somma LR4 con RC')
    axes[0].axhline(0,color='#D0D4E3',ls=':');axes[0].axvline(2600,color='#D0D4E3',ls=':')
    axes[0].set(title='La protezione entra nel crossover',xlabel='Frequenza [Hz]',ylabel='Livello relativo [dB]',ylim=(-16,1))
    axes[0].legend(fontsize=9);axes[0].grid()
    axes[0].set_xticks([200,1000,2600,10000],['200','1k','2,6k','10k']);axes[0].minorticks_off()
    for variant,color in zip(config['variants'],COLORS):
        rows=[r for r in report['electrical_hypotheses'] if r['id']==variant['id'] and r['mode']=='ascolto']
        axes[1].plot([r['amplifier_gain_hypothetical_db'] for r in rows],
            [r['woofer_voltage_demand_upper_bound_vrms'] for r in rows],color=color,marker='o',label=variant['id'])
    axes[1].axhline(32/math.sqrt(2),color='#0A0A0A',ls='--',label='Rail 32 V: tetto ideale')
    axes[1].set(title='Richiesta prima del clipping',xlabel='Guadagno del finale ipotizzato [dB]',ylabel='Tensione woofer [Vrms]')
    axes[1].legend(fontsize=9);axes[1].grid()
    axes[1].set_xticks([20,26,32])
    figures['condensatore-e-livelli']=fig
    result={}
    provenance={'report_sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),
                'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'status':'Modelli nominali, non misure'}
    for name,fig in figures.items():
        svg=io.StringIO();fig.savefig(svg,format='svg',metadata={'Date':None,'Creator':'figure_completamento.py'})
        data=svg.getvalue();pos=data.index('>',data.index('<svg'))+1
        data=data[:pos]+'\n<metadata id="provenienza-diy">'+html.escape(json.dumps(provenance))+'</metadata>'+data[pos:]
        pdf=io.BytesIO();fig.savefig(pdf,format='pdf',dpi=180,metadata={'CreationDate':None,'ModDate':None,'Creator':'figure_completamento.py'})
        result[name]={'svg':data.encode('utf-8'),'pdf':pdf.getvalue()};plt.close(fig)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'build/completamento-20261125-figure')
    parser.add_argument('--font-dir',type=Path,default=ROOT/'build/consegna-cabinet-20261119/assets')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args();figures=render(args.font_dir)
    if args.check:
        stale=[name for name,formats in figures.items() if not (PUBLIC/(name+'.svg')).is_file() or (PUBLIC/(name+'.svg')).read_bytes()!=formats['svg']]
        print(json.dumps({'figure_da_rigenerare':stale}));return int(bool(stale))
    args.out.mkdir(parents=True,exist_ok=False);PUBLIC.mkdir(parents=True,exist_ok=True)
    for name,formats in figures.items():
        for extension,data in formats.items():(args.out/(name+'.'+extension)).write_bytes(data)
        target=PUBLIC/(name+'.svg')
        sys.path.insert(0,str(ROOT/'.claude/templates/tools'))
        from rigenera_sicuro import scrivi
        if scrivi(str(target),formats['svg'].decode('utf-8'),silenzioso=True):
            raise RuntimeError('Figura con contenuto autorato: rigenerazione fermata')
    print(json.dumps({'figure':len(figures),'destinazione':str(PUBLIC.relative_to(ROOT))}))
    return 0


if __name__=='__main__':raise SystemExit(main())
