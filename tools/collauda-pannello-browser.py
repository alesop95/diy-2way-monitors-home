"""Browser reale con peer controllato per la sola interfaccia; nessun DSP hardware."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading
import time
from test_monitor_dsp import FakePeer
from pannello_ascolto import Session,make_server

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'build/controllo-ascolto'

JAVASCRIPT=r'''
const fs=require('node:fs');
const [port,url,out]=process.argv.slice(1);
(async()=>{
 const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
 const page=targets.find(p=>p.type==='page');
 const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise((ok,no)=>{ws.onopen=ok;ws.onerror=no});
 let id=0;const pending=new Map();
 ws.onmessage=e=>{const r=JSON.parse(e.data);if(pending.has(r.id)){let p=pending.get(r.id);pending.delete(r.id);clearTimeout(p.timer);r.error?p.no(Error(r.error.message)):p.ok(r.result)}};
 function send(method,params={}){return new Promise((ok,no)=>{const key=++id;const timer=setTimeout(()=>{pending.delete(key);no(Error('Timeout CDP '+method))},10000);pending.set(key,{ok,no,timer});ws.send(JSON.stringify({id:key,method,params}))})}
 async function evaluate(expression){const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value}
 await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1280,height:1200,deviceScaleFactor:1,mobile:false});await send('Page.navigate',{url});
 const result=await evaluate(`(async()=>{
  const wait=async f=>{let end=Date.now()+8000;while(!f()){if(Date.now()>end)throw Error('Stato UI non raggiunto');await new Promise(r=>setTimeout(r,40))}};
  const $=id=>document.getElementById(id);
  await wait(()=>$('profile')&&$('profile').options.length===2);await document.fonts.ready;
  $('prepare').click();await wait(()=>!$('enable').disabled);
  $('volume').value='-24';$('volume').dispatchEvent(new Event('input'));$('enable').click();await wait(()=>$('state').textContent==='Ascolto in corso');
  $('volume').value='-18';$('volume').dispatchEvent(new Event('input'));$('volume').dispatchEvent(new Event('change'));await wait(()=>$('actual').textContent.includes('-18 dB'));
  return {profiles:2,playing:true,volume_ui:-18,desktop_overflow:document.body.scrollWidth>innerWidth,
          fonts:[document.fonts.check('20px "Altro Grotesk"'),document.fonts.check('300 48px "Altro Serif"')]};
 })()`);
 let shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});fs.writeFileSync(out+'/desktop-qa.png',Buffer.from(shot.data,'base64'));
 await evaluate(`(async()=>{document.getElementById('mute').click();let end=Date.now()+5000;while(!document.getElementById('actual').textContent.includes('silenziato')){if(Date.now()>end)throw Error('Mute UI non raggiunto');await new Promise(r=>setTimeout(r,40))}document.getElementById('profile').value='ascolto';document.getElementById('prepare').click();})()`);
 await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
 await new Promise(r=>setTimeout(r,1200));
 result.mobile=await evaluate(`({width:innerWidth,overflow:document.body.scrollWidth>innerWidth,profile:document.getElementById('profile').value,
  mute:document.getElementById('actual').textContent.includes('silenziato'),buttons:[...document.querySelectorAll('button')].every(b=>{let r=b.getBoundingClientRect();return r.x>=0&&r.right<=innerWidth})})`);
 shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true});fs.writeFileSync(out+'/mobile-qa.png',Buffer.from(shot.data,'base64'));
 console.log(JSON.stringify(result));
 try{await send('Browser.close')}catch(e){};ws.close();
})().catch(e=>{console.error(e.stack);process.exitCode=1});
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    report=OUT/'browser-qa.json'
    sources=['tools/pannello_ascolto.py','config/controllo-ascolto/index.html',str(Path(__file__).relative_to(ROOT)).replace('\\','/')]
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}
    if args.check:
        saved=json.loads(report.read_text(encoding='utf-8')); valid=saved['passed'] is True and saved['source_sha256']==hashes
        print('Browser pannello: '+('rapporto coerente' if valid else 'da ripetere')); raise SystemExit(0 if valid else 1)
    peer=FakePeer(loaded_state='Running'); peer.muted=True; peer.volume=-60
    profiles={name:json.loads((ROOT/f'config/controllo-ascolto/{name}-file.json').read_text(encoding='utf-8')) for name in ('mix','ascolto')}
    session=Session(peer,profiles); server=make_server(session,port=0)
    stop=threading.Event(); watcher=threading.Thread(target=session.supervise,args=(stop,),daemon=True)
    http=threading.Thread(target=server.serve_forever,daemon=True); watcher.start(); http.start()
    OUT.mkdir(parents=True,exist_ok=True)
    edge=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe')
    with tempfile.TemporaryDirectory(prefix='pannello-qa-',dir=ROOT/'build') as tmp:
        proc=subprocess.Popen([str(edge),'--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking',
            '--disable-extensions','--disable-component-update','--remote-debugging-port=0',f'--user-data-dir={tmp}','about:blank'],
            stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            active=Path(tmp)/'DevToolsActivePort'; deadline=time.monotonic()+10
            while not active.exists():
                if time.monotonic()>deadline: raise TimeoutError('Browser non pronto')
                time.sleep(.05)
            port=active.read_text().splitlines()[0]
            result=subprocess.run([shutil.which('node'),'-e',JAVASCRIPT,port,
                f'http://127.0.0.1:{server.server_address[1]}',str(OUT)],capture_output=True,text=True,timeout=40)
            if result.returncode: raise RuntimeError(result.stderr)
            data=json.loads(result.stdout)
            assert data['fonts']==[True,True] and not data['desktop_overflow'] and not data['mobile']['overflow']
            assert data['mobile']['buttons'] and data['mobile']['mute'] and data['mobile']['profile']=='ascolto'
            data.update(passed=True,backend='Peer controllato: prova UI, non audio o hardware',source_sha256=hashes)
            report.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(data,ensure_ascii=False))
            proc.wait(timeout=5)
        finally:
            if proc.poll() is None: proc.terminate(); proc.wait(timeout=5)
            stop.set(); watcher.join(timeout=3); server.shutdown(); server.server_close(); http.join(timeout=2); session.close()


if __name__=='__main__': main()
