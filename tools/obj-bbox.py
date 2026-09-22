#!/usr/bin/env python3
"""Misura il parallelepipedo che contiene una mesh OBJ, per verificarne la scala.

Perche' serve. La via decisa in PA-020 usa una scansione da telefono come sagoma su cui
ricalcare il modello della stanza, e poggia su una premessa che va verificata prima di
fidarsene: che la scala esca metrica. ARCore la ricava combinando le immagini con i
sensori inerziali, quindi in teoria esce giusta, ma l'errore da cui difendersi non e'
quello casuale su una quota, e' la deriva di scala, che sposta tutte le frequenze modali
nella stessa direzione e si presenta tre fasi piu' avanti come un disaccordo fra Octave e
REW. Il ragionamento e' in docs/30-modellazione-e-simulazione.md.

La verifica non richiede alcuno strumento di misura, e questo e' il punto. Si scansiona un
oggetto le cui dimensioni siano note per norma e non per misura, tipicamente una risma di
carta A4 chiusa, che e' una scatola con spigoli netti le cui due facce maggiori misurano
297 per 210 millimetri per la norma ISO 216. Si esporta in OBJ e si confronta il
parallelepipedo contenente con quei due numeri. Un metro a nastro non serve, e nemmeno lo
strumento di misura dell'applicazione, che potrebbe non esserci e la cui precisione non e'
dichiarata.

Come si legge l'esito. Lo strumento stampa le tre dimensioni del parallelepipedo
contenente, ordinate dalla maggiore alla minore, sia nell'unita' del file sia nell'ipotesi
che quella unita' sia il metro. Con --riferimento si dichiara la dimensione nota in
millimetri e lo strumento calcola lo scarto percentuale sulla dimensione piu' vicina,
dicendo se stia sotto la soglia. La soglia predefinita e' l'uno per cento, che e' quella
che le quattro diagonali di controllo della tabella F di docs/35-rilievo-geometrico.md
richiedono al modello finito.

Il limite che decide come si imposta la prova, e va conosciuto prima di fidarsi dei numeri.
Il parallelepipedo e' allineato agli assi del file, non all'oggetto: se l'oggetto e' ruotato
rispetto a quegli assi, i lati risultano piu' lunghi del vero, e di quanto dipende dalla
rotazione. La rotazione attorno alla verticale di una scansione e' arbitraria, perche'
dipende da dove si trovava chi scansionava, quindi i due lati orizzontali sovrastimano e non
sono un riferimento affidabile. Il lato verticale invece lo e', perche' ARCore conosce la
direzione della gravita' e la mesh ne esce allineata.

Ne segue la forma corretta della prova, che costa meno di una sofisticazione dello
strumento: la dimensione nota va messa in verticale. Un foglio A4 appoggiato in piedi contro
un oggetto, con il lato lungo verticale, offre 297 millimetri lungo l'asse che si puo'
credere, e se e' la cosa piu' alta nell'inquadratura l'estensione verticale della mesh e'
quella del foglio. Su un oggetto appoggiato piatto, la sola dimensione confrontabile e' la
sua altezza.

Cosa NON fa. Non apre Blender, non triangola, non ripara la mesh e non tocca il file: legge
le sole righe dei vertici e ne ricava gli estremi, che e' tutto cio' che serve a una
verifica di scala e costa un passaggio sequenziale invece di una importazione. Non decide
se la scansione sia buona: una mesh bucata o rumorosa puo' avere un parallelepipedo
contenente corretto, quindi un esito verde qui dice che la scala e' giusta e non che il
rilievo sia utilizzabile. E non riconosce l'oggetto: se nell'inquadratura e' entrata anche
la scrivania, il parallelepipedo contiene la scrivania, ed e' la prima cosa da sospettare
davanti a un numero fuori scala di molto.

Uso:
    python tools/obj-bbox.py <file.obj>
    python tools/obj-bbox.py <file.obj> --riferimento 297
    python tools/obj-bbox.py <file.obj> --riferimento 297 --soglia 2

Esce con codice 1 se lo scarto supera la soglia, oppure se il file non contiene vertici,
0 altrimenti. Senza --riferimento esce sempre 0, perche' non c'e' nulla da giudicare.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def leggi_estremi(percorso: Path) -> tuple[list[float], list[float], int]:
    """Ritorna minimi, massimi e numero di vertici letti dalle righe `v` di un OBJ."""
    minimi = [float("inf")] * 3
    massimi = [float("-inf")] * 3
    letti = 0
    with percorso.open("r", encoding="utf-8", errors="replace") as f:
        for riga in f:
            if not riga.startswith("v "):
                continue
            pezzi = riga.split()
            if len(pezzi) < 4:
                continue
            try:
                coord = [float(pezzi[1]), float(pezzi[2]), float(pezzi[3])]
            except ValueError:
                continue
            for i in range(3):
                if coord[i] < minimi[i]:
                    minimi[i] = coord[i]
                if coord[i] > massimi[i]:
                    massimi[i] = coord[i]
            letti += 1
    return minimi, massimi, letti


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("file", help="la mesh OBJ da misurare")
    ap.add_argument(
        "--riferimento",
        type=float,
        default=None,
        metavar="MM",
        help="dimensione nota dell'oggetto in millimetri, per esempio 297 per il lato lungo di un A4",
    )
    ap.add_argument(
        "--soglia",
        type=float,
        default=1.0,
        metavar="PCT",
        help="scarto percentuale massimo accettato, predefinito 1.0",
    )
    args = ap.parse_args()

    percorso = Path(args.file)
    if not percorso.is_file():
        print(f"file non trovato: {percorso}")
        return 1

    minimi, massimi, letti = leggi_estremi(percorso)
    if letti == 0:
        print(f"nessun vertice letto in {percorso.name}: non e' un OBJ con geometria")
        return 1

    lati = sorted((massimi[i] - minimi[i] for i in range(3)), reverse=True)
    print(f"{percorso.name}: {letti} vertici")
    print("parallelepipedo contenente, allineato agli assi del file,")
    print("dal lato maggiore al minore:")
    for etichetta, lato in zip(("maggiore", "intermedio", "minore"), lati):
        print(f"  {etichetta:<11} {lato:.6f} unita'   = {lato * 1000:.1f} mm se l'unita' e' il metro")
    print("i due lati orizzontali sovrastimano se l'oggetto e' ruotato rispetto agli assi;")
    print("il verticale e' affidabile, perche' la mesh esce allineata alla gravita'.")

    if args.riferimento is None:
        print("\nsenza --riferimento non c'e' nulla da giudicare: la scala si verifica")
        print("contro una dimensione nota per norma, non contro un'attesa.")
        return 0

    atteso_m = args.riferimento / 1000.0
    vicino = min(lati, key=lambda lato: abs(lato - atteso_m))
    scarto = (vicino - atteso_m) / atteso_m * 100.0
    print(f"\nriferimento dichiarato: {args.riferimento:.1f} mm")
    print(f"lato piu' vicino:       {vicino * 1000:.1f} mm")
    print(f"scarto:                 {scarto:+.2f} per cento, soglia {args.soglia:.2f}")

    if abs(scarto) <= args.soglia:
        print("la scala e' metrica entro la soglia: la scansione si puo' usare come sagoma.")
        return 0

    print("lo scarto supera la soglia. Prima di concludere che la scala sia sbagliata,")
    print("va escluso che il parallelepipedo contenga altro oltre all'oggetto, perche'")
    print("in quel caso il numero descrive l'inquadratura e non la scala.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
