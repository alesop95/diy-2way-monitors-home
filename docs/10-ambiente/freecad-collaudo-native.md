# FreeCAD: preparazione utente e collaudo dei formati

Stato del giro 2026-11-18/19: FreeCAD 1.1.4 presente come AppImage ufficiale verificata, avvio console e grafico collaudati, comando utente e voce menu creati da modelli versionati. La prova riguarda un pannello campione parametrico, non il cabinet finale. Il [successivo riavvio](collaudo-dopo-riavvio-2026-11.md) è stato verificato riaprendo i tre modelli del kit e con una nuova apertura grafica; restano i collaudi della catena audio con l'hardware scelto.

I sorgenti dei collaudi e i modelli restano nel repository canonico dei monitor; il gemello home recording riceve questa procedura attraverso il blocco ambiente condiviso.

## Perché questo canale

Il canale scelto è il rilascio stabile [FreeCAD 1.1.4](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.4), AppImage Linux x86_64 da 820812280 byte. La versione è isolata nella cartella utente, con impronta controllata e senza modificare pacchetti Wine o dipendenze di sistema. L'impronta del rilascio è `f6dc6ba676e5ac96a565ebc8d657232f94c6158e85b4352141bd1a46f6b43434`; è stata confrontata sia con il descrittore scaricato sia con il valore conservato dalla ricognizione precedente.

Il programma è in `~/.local/opt/freecad-1.1.4/`. Il comando `~/.local/bin/freecad-1.1.4` e la voce `~/.local/share/applications/freecad-1.1.4.desktop` sono stati creati solo se i rispettivi percorsi non esistevano. I modelli sono in `config/freecad/`; la voce menu non cambia le associazioni predefinite dei documenti. `desktop-file-validate` termina senza errori e segnala soltanto che le categorie principali multiple possono mostrare la voce in più sezioni del menu.

## Sequenza eseguita

I comandi di preparazione seguenti sono stati eseguiti nella shell Ubuntu attraverso SSH; una cartella di versione già presente deve essere ispezionata prima di ripetere il download. Il file è nuovo e diventa eseguibile dopo la verifica.

```bash
mkdir -p "$HOME/.local/opt/freecad-1.1.4"
cd "$HOME/.local/opt/freecad-1.1.4"
curl --fail --location --retry 2 --output FreeCAD_1.1.4-Linux-x86_64-py311.AppImage https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage
curl --fail --location --retry 2 --output FreeCAD_1.1.4-Linux-x86_64-py311.AppImage-SHA256.txt https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage-SHA256.txt
sha256sum --check FreeCAD_1.1.4-Linux-x86_64-py311.AppImage-SHA256.txt
chmod u+x FreeCAD_1.1.4-Linux-x86_64-py311.AppImage
./FreeCAD_1.1.4-Linux-x86_64-py311.AppImage freecadcmd --help
```

Per i collaudi si è creata una cartella nuova con `mktemp -d /tmp/diy-freecad-20261118-XXXXXXXX`, poi trasferiti `tools/collauda-freecad.py` e `tools/collauda-freecad-gui.FCMacro` da questa postazione con scp. Nei comandi parametrizzati sotto, `<CARTELLA_PROVA>` è il percorso restituito; i file di configurazione sono separati da quelli d'uso ordinario.

```bash
DIY_CAD_TEST_DIR=<CARTELLA_PROVA>/normal ~/.local/opt/freecad-1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage freecadcmd -u <CARTELLA_PROVA>/user-normal.cfg -s <CARTELLA_PROVA>/system-normal.cfg <CARTELLA_PROVA>/collauda-freecad.py
DIY_CAD_TEST_DIR=<CARTELLA_PROVA>/negative DIY_CAD_TEST_SCALE_STEP=2 ~/.local/opt/freecad-1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage freecadcmd -u <CARTELLA_PROVA>/user-negative.cfg -s <CARTELLA_PROVA>/system-negative.cfg <CARTELLA_PROVA>/collauda-freecad.py
```

L'esecuzione normale ha scritto `status=success`. Il controllo negativo è fallito sul volume STEP, otto volte quello atteso: il controllo osserva il solido reimportato, non la sola esistenza del file. FreeCAD può intercettare un'eccezione Python e terminare comunque la console: per questo è obbligatorio leggere il rapporto, senza dedurre l'esito dal solo codice del processo.

Per la prova grafica è stato usato Xvfb già installato. La macro finale attiva la sottofinestra del modello, acquisisce l'immagine e chiude prima il documento e poi la finestra principale. L'esecuzione osservata ha un rapporto `window_captured` e codice del processo 0, entrambi necessari. Il rapporto non dichiara da solo una chiusura riuscita.

```bash
DIY_CAD_TEST_NATIVE=<CARTELLA_PROVA>/normal/pannello-prova.FCStd DIY_CAD_TEST_GUI_DIR=<CARTELLA_PROVA>/gui-view LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a ~/.local/opt/freecad-1.1.4/FreeCAD_1.1.4-Linux-x86_64-py311.AppImage -u <CARTELLA_PROVA>/user-gui-view.cfg -s <CARTELLA_PROVA>/system-gui-view.cfg <CARTELLA_PROVA>/collauda-freecad-gui-view.FCMacro
~/.local/bin/freecad-1.1.4 freecadcmd --version
desktop-file-validate ~/.local/share/applications/freecad-1.1.4.desktop
```

Il nome `collauda-freecad-gui-view.FCMacro` è la copia trasferita della macro finale versionata. Rapporti, log, screenshot e artefatti sono stati riportati nel livello privato del repository. Una copia del campione è in `~/electroacoustics/collaudi/freecad-20261118`, in una cartella nuova: resta disponibile dopo la pulizia automatica di `/tmp`.

## Risultati che copre la prova

| Prova | Criterio osservato |
|---|---|
| Solido | Un solido valido, pannello 240 × 300 × 18 mm con foro di raggio 40 mm |
| Parametri | Variando la larghezza di 10 mm il volume cambia di 54000 mm³; ripristinato il valore iniziale |
| FCStd | Salvataggio e riapertura mantengono parametri, validità e volume |
| STEP | Reimportazione con un solido e dimensioni e volume attesi |
| DXF | Reimportazione con quattro segmenti e un cerchio, piano Z=0, dimensioni e centro del foro attesi |
| Unità DXF | Campo INSUNITS letto nel file con valore 4, millimetri |
| Controllo negativo | STEP a scala doppia rilevato come errato dal confronto del volume |
| GUI | Documento aperto sotto Xvfb, vista del modello attiva e chiusura del processo con codice 0 |

Il volume analitico di confronto è `(240 × 300 - pi × 40²) × 18 = 1205522,131576614 mm³`. La prova non definisce misure del cabinet, posizione dei driver, costo, tolleranze di lavorazione o risposta acustica. I DXF costruttivi finali dovranno essere verificati sul progetto approvato e sul processo del falegname.

## Troubleshooting osservato

### L'AppImage cerca un display anche nella ricognizione

Osservato su Ubuntu nel giro del 18/19 novembre: il primo avvio senza display fallisce con il backend Qt xcb, anche impostando offscreen. La lettura del launcher mostra che AppRun forza xcb. La stessa AppImage permette di selezionare `freecadcmd` come primo argomento: questo percorso ha esposto l'aiuto ed eseguito il collaudo console. Per la GUI si usa Xvfb. Non sono state installate librerie sulla base del solo messaggio generico del plugin Qt.

### Un rapporto grafico positivo precede un errore in chiusura

La prima macro acquisiva la finestra e poi usciva direttamente dall'applicazione Qt; il log mostrava un errore durante la chiusura. Il rapporto scritto prima dell'uscita non provava la terminazione del processo. La macro finale chiude documento e finestra principale e il comando di prova conserva separatamente il codice del processo. La nuova esecuzione ha terminato con codice 0.

### La schermata mostra la pagina iniziale anziché il modello

L'ispezione della prima schermata ha mostrato la pagina Start pur con il modello aperto. Il controllo finale seleziona la sottofinestra corrispondente al documento e verifica il titolo attivo prima della cattura. Apertura del documento, visualizzazione e chiusura sono quindi controlli distinti, non un unico messaggio di successo.
