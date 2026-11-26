"""Confronto riproducibile di risposte su file: nessuna acquisizione o qualifica hardware."""
import argparse
import csv
from dataclasses import dataclass
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys

import numpy as np


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')


@dataclass
class Curve:
    frequency_hz: object
    magnitude_db: object
    phase_deg: object=None
    coherence: object=None

    def __post_init__(self):
        for name in ('frequency_hz','magnitude_db','phase_deg','coherence'):
            value=getattr(self,name)
            if value is None:continue
            value=np.array(value,dtype=float,copy=True)
            if value.ndim!=1 or not np.all(np.isfinite(value)):
                raise ValueError('Vettori numerici finiti richiesti: '+name)
            setattr(self,name,value)
        n=len(self.frequency_hz)
        if n<2 or np.any(self.frequency_hz<=0) or np.any(np.diff(self.frequency_hz)<=0):
            raise ValueError('Servono almeno due frequenze positive e strettamente crescenti')
        for value in (self.magnitude_db,self.phase_deg,self.coherence):
            if value is not None and len(value)!=n:raise ValueError('Colonne di lunghezza diversa')
        if self.coherence is not None and np.any((self.coherence<0)|(self.coherence>1)):
            raise ValueError('Coerenza fuori intervallo [0,1]')

    def complex_response(self):
        if self.phase_deg is None:raise ValueError('La fase non è disponibile')
        with np.errstate(over='raise',invalid='raise'):
            return 10**(self.magnitude_db/20)*np.exp(1j*np.deg2rad(self.phase_deg))


def read_curve(path,format='frd'):
    return _parse_curve(Path(path).read_bytes(),format)


def _parse_curve(raw,format):
    if format not in ('frd','osm_frd','osm_csv'):raise ValueError('Formato non supportato')
    rows=[];columns=None
    for number,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        line=line.strip()
        if not line or line.startswith(('#','*',';')):continue
        fields=next(csv.reader([line])) if format=='osm_csv' else re.split(r'[\s;]+',line)
        expected=(2,3) if format=='frd' else (4,)
        if len(fields) not in expected or (columns is not None and columns!=len(fields)):
            raise ValueError(f'Colonne incoerenti o non previste dal formato, riga {number}')
        columns=len(fields)
        try:rows.append([float(field) for field in fields])
        except ValueError as exc:raise ValueError(f'Dato non numerico, riga {number}') from exc
    if not rows:raise ValueError('File privo di dati numerici')
    values=np.asarray(rows,dtype=float)
    return Curve(values[:,0],values[:,1],values[:,2] if columns>=3 else None,
                 values[:,3] if columns==4 else None)


def _target(target):
    keys=('minimum_hz','maximum_hz','reference_db','tolerance_db','max_gap_octaves','minimum_coherence')
    try:result={name:float(target[name]) for name in keys}
    except (KeyError,TypeError,ValueError) as exc:raise ValueError('Bersaglio incompleto o non numerico') from exc
    if not all(np.isfinite(v) for v in result.values()):raise ValueError('Bersaglio non finito')
    if not 0<result['minimum_hz']<result['maximum_hz'] or result['tolerance_db']<0 or result['max_gap_octaves']<=0:
        raise ValueError('Banda, tolleranza o risoluzione del bersaglio non valide')
    if not 0<=result['minimum_coherence']<=1:raise ValueError('Soglia di coerenza non valida')
    return result


def analyse_curve(curve,target,valid_range_hz=None):
    target=_target(target);lo=target['minimum_hz'];hi=target['maximum_hz']
    issues=[]
    if curve.frequency_hz[0]>lo or curve.frequency_hz[-1]<hi:issues.append('frequency_coverage')
    if valid_range_hz is not None:
        valid=np.asarray(valid_range_hz,dtype=float)
        if valid.shape!=(2,) or not np.all(np.isfinite(valid)) or not 0<valid[0]<valid[1]:
            raise ValueError('Banda valida dichiarata non corretta')
        if valid[0]>lo or valid[1]<hi:issues.append('declared_valid_band')
    selected=(curve.frequency_hz>=lo)&(curve.frequency_hz<=hi)
    frequency=curve.frequency_hz[selected]
    if 'frequency_coverage' not in issues:
        frequency=np.unique(np.r_[lo,frequency,hi])
        magnitude=np.interp(np.log(frequency),np.log(curve.frequency_hz),curve.magnitude_db)
    else:magnitude=curve.magnitude_db[selected]
    relevant_intervals=(curve.frequency_hz[:-1]<hi)&(curve.frequency_hz[1:]>lo)
    original_gaps=np.diff(np.log2(curve.frequency_hz))[relevant_intervals]
    gap=float(np.max(original_gaps)) if len(original_gaps) else None
    if gap is None or gap>target['max_gap_octaves']+1e-12:issues.append('frequency_grid')
    with np.errstate(over='raise',invalid='raise'):
        deviation=np.abs(magnitude-target['reference_db'])
    maximum=float(np.max(deviation)) if len(deviation) else None
    worst=float(frequency[np.argmax(deviation)]) if len(deviation) else None
    coherence=None
    if curve.coherence is not None and len(frequency):
        coherence=float(np.min(np.interp(np.log(frequency),np.log(curve.frequency_hz),curve.coherence)))
    status=('insufficient_coverage' if issues else 'low_coherence' if coherence is not None and coherence<target['minimum_coherence']
            else 'within_bounds' if maximum is not None and maximum<=target['tolerance_db']+1e-12 else 'outside_bounds')
    return {'status':status,'coverage_issues':issues,'maximum_deviation_db':maximum,'worst_frequency_hz':worst,
            'maximum_gap_octaves':gap,'minimum_coherence':coherence,'phase_available':curve.phase_deg is not None,
            'declared_valid_band_hz':None if valid_range_hz is None else list(map(float,valid_range_hz)),
            'physical_validity_verified':False,'comparison_scope':'samples_and_interpolated_band_endpoints'}


def _direction(row):
    try:plane=row['plane'];angle=float(row['angle_deg'])
    except (KeyError,TypeError,ValueError) as exc:raise ValueError('Direzione non valida') from exc
    if plane not in ('axial','horizontal','vertical') or not np.isfinite(angle) or abs(angle)>180 or (plane=='axial' and angle!=0):
        raise ValueError('Direzione non valida')
    return plane,angle


def _inside(root,name):
    if not isinstance(name,str):raise ValueError('percorso non testuale')
    relative=PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or ':' in name or '\\' in name:
        raise ValueError('percorso non relativo al dataset')
    result=(root/name).resolve(strict=True)
    if not result.is_relative_to(root) or not result.is_file():raise ValueError('percorso fuori dal dataset')
    return result


def _exports(id,curve):
    stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n')
    writer.writerow(['frequency_hz','magnitude_db','phase_deg','coherence'])
    fmt=lambda value:format(float(value),'.12g')
    for n,f in enumerate(curve.frequency_hz):
        writer.writerow([fmt(f),fmt(curve.magnitude_db[n]),'' if curve.phase_deg is None else fmt(curve.phase_deg[n]),
                         '' if curve.coherence is None else fmt(curve.coherence[n])])
    result={'curves/'+id+'.csv':stream.getvalue().encode('utf-8')}
    if curve.phase_deg is not None:
        result['curves/'+id+'.frd']=(''.join('\t'.join(fmt(v) for v in row)+'\n'
            for row in zip(curve.frequency_hz,curve.magnitude_db,curve.phase_deg))).encode('utf-8')
    return result


def analyse_dataset(manifest_path):
    path=Path(manifest_path).resolve(strict=True);root=path.parent;raw=path.read_bytes()
    data=json.loads(raw.decode('utf-8-sig'))
    if not isinstance(data,dict):raise ValueError('Il manifesto deve essere un oggetto')
    if data.get('schema')!='speaker-response-dataset-1':raise ValueError('Schema dataset non supportato')
    if data.get('data_kind') not in ('synthetic','simulated','measured'):raise ValueError('Provenienza obbligatoria')
    if data.get('level_unit') not in ('dB_relative','dB_SPL'):raise ValueError('Unità di livello obbligatoria')
    target=_target(data.get('target'))
    rows=data.get('curves',[]);requested=data.get('required_directions',[])
    if not isinstance(rows,list) or not isinstance(requested,list):raise ValueError('Curve e direzioni devono essere liste')
    required=[_direction(row) for row in requested]
    if not required or len(set(required))!=len(required):raise ValueError('Direzioni richieste mancanti o duplicate')
    ids=set();directions=set();results=[];exports={'inputs/'+path.name:raw};inputs={path.name:sha(raw)}
    for row in rows:
        if not isinstance(row,dict):raise ValueError('Ogni curva deve essere un oggetto')
        id=row.get('id','')
        if not isinstance(id,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,48}',id) or id in ids:
            raise ValueError('ID curva non valido o duplicato')
        ids.add(id);direction=_direction(row)
        if direction in directions:raise ValueError('direzione duplicata')
        directions.add(direction)
        source=_inside(root,row['path']);name=PurePosixPath(row['path']).as_posix()
        before=source.read_bytes();curve=_parse_curve(before,row.get('format','frd'))
        inputs[name]=sha(before)
        exports['inputs/'+name]=before
        result=analyse_curve(curve,target,row.get('valid_range_hz'))
        results.append({'id':id,'plane':direction[0],'angle_deg':direction[1],'input':name,
                        'input_format':row.get('format','frd'),'required_direction':direction in required,**result})
        exports.update(_exports(id,curve))
    missing=[{'plane':p,'angle_deg':a} for p,a in required if (p,a) not in directions]
    statuses=[r['status'] for r in results if r['required_direction']]
    status=('incomplete' if missing or 'insufficient_coverage' in statuses else
            'within_bounds' if all(s=='within_bounds' for s in statuses) else 'outside_bounds')
    report={'schema':'speaker-characterization-report-1','data_kind':data['data_kind'],'level_unit':data['level_unit'],
            'provenance_status':'declared_not_independently_verified','target':target,
            'required_directions':[{'plane':p,'angle_deg':a} for p,a in required],
            'missing_directions':missing,'status':status,'curves':results,'input_sha256':inputs,
            'generator_sha256':sha(Path(__file__).read_bytes()),'numpy_version':np.__version__,
            'hardware_qualified':False,'gll_generated':False}
    return report,exports


def build_bundle(manifest_path):
    report,files=analyse_dataset(manifest_path);files['report.json']=json_bytes(report)
    files['manifest.json']=json_bytes({'schema':'response-file-bundle-1',
                                      'files':{name:sha(raw) for name,raw in sorted(files.items())}})
    return files


def write_bundle(manifest_path,output):
    files=build_bundle(manifest_path);output=Path(output);output.mkdir(parents=True,exist_ok=False)
    for name,raw in files.items():
        path=output/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    return json.loads(files['report.json'])


def check_bundle(manifest_path,output):
    files=build_bundle(manifest_path);output=Path(output)
    actual={p.relative_to(output).as_posix():p for p in output.rglob('*') if p.is_file()}
    errors=['file inatteso: '+name for name in actual.keys()-files.keys()]
    errors+=['file assente o diverso: '+name for name,raw in files.items()
             if name not in actual or actual[name].read_bytes()!=raw]
    return sorted(errors)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:
        if args.check:
            errors=check_bundle(args.manifest,args.out)
            status=None if errors else json.loads((args.out/'report.json').read_text(encoding='utf-8'))['status']
            print(json.dumps({'errors':errors,'data_status':status,'hardware_qualified':False},ensure_ascii=False))
            return int(bool(errors))
        report=write_bundle(args.manifest,args.out)
        print(json.dumps({'data_kind':report['data_kind'],'status':report['status'],
                          'curves':len(report['curves']),'hardware_qualified':False},ensure_ascii=False));return 0
    except (OSError,ValueError,KeyError,TypeError,FloatingPointError) as exc:
        print('Errore: '+str(exc),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
