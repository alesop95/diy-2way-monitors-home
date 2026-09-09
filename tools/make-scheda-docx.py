#!/usr/bin/env python3
"""Genera la scheda operativa di reinstallazione in formato .docx, pronta da stampare.

Perche' serve. La scheda che si porta accanto alla macchina durante la reinstallazione
non puo' essere il file Markdown: chi azzera il disco non ha davanti la postazione di
sviluppo, quindi il documento va stampato su carta. Il .docx e' il formato di stampa, e
la sua sorgente tracciata e' docs/10-ambiente/scheda-reinstallazione.md.

Perche' e' uno strumento e non un documento scritto a mano. Un .docx compilato a mano
non e' riproducibile: se la procedura cambia, la carta e il repository divergono senza
che nessuno se ne accorga. Il 2026-09-08 e' successo davvero, e in forma istruttiva. La
scheda .docx era stata costruita alle 15:10 con codice che viveva soltanto nella
sessione, e due minuti dopo la fase 4.2 della procedura ha guadagnato l'avvertenza sulla
casella di formattazione che si attiva da se'. Il crash della sessione ha portato via il
codice, quindi la carta era indietro rispetto alla documentazione e non c'era modo di
riallinearla se non riscrivendo tutto. Il racconto e' in MS-070 di docs/OPERATIONS-LOG.md.

Cosa NON fa. Non legge il Markdown per convertirlo: il contenuto della scheda vive qui
sotto come dati, perche' la carta ha vincoli che il Markdown non ha, cioe' due pagine di
spazio, caselle da spuntare a penna e riquadri colorati sul passo irreversibile. La
sorgente Markdown e questo strumento vanno quindi tenuti allineati a mano, ed e' il
prezzo dichiarato di avere un documento di stampa curato. Se le due divergono ha ragione
la procedura completa, come la scheda stessa dichiara in apertura.

Sui dati di licenza. Il Machine Identifier e il Release Code di Akabak non compaiono nel
documento generato, se non lo si chiede: stamparli mette un codice di attivazione
permanente su un foglio di carta, e per la reinstallazione non servono, perche' il codice
resta valido e viene reinserito dal file riservato quando serve. Con --con-licenza il
generatore li legge da _notes/licenze-akabak-riservato.md, che il .gitignore esclude, e
aggiunge una sezione finale. In quel caso il foglio va trattato come materiale riservato.

Non usa librerie di terze parti. Un .docx e' un archivio zip di documenti XML, e le
quattro parti che servono si scrivono direttamente: cosi' lo strumento gira su qualunque
Python 3 senza installare niente, come gli altri strumenti di questo progetto.

Uso:
    python tools/make-scheda-docx.py
    python tools/make-scheda-docx.py --out "C:/Users/Utente/Downloads/scheda.docx"
    python tools/make-scheda-docx.py --con-licenza

Esce con codice 1 se la destinazione non e' scrivibile o se --con-licenza non trova i
valori nel file riservato, 0 altrimenti.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Dati della scheda
# ---------------------------------------------------------------------------
# I valori di macchina provengono da docs/10-ambiente/fotografia-macchina-2026-09-07.md,
# che e' l'unica fonte osservata sulla macchina, non dal documento sorgente originale.

TITOLO = "REINSTALLAZIONE UBUNTU STUDIO · SCHEDA OPERATIVA"
SOTTOTITOLO = (
    "ASUS H170-PRO · BIOS 3805 · utente alesop95 · NVMe 500 GB nvme0n1 · "
    "chiavetta Kingston GPT/UEFI · Ubuntu Studio 26.04.1 LTS"
)

# I due riquadri in testa. Il primo nomina il rischio, il secondo nomina il modo
# concreto in cui l'errore si commette, che e' la parte che l'operatore non indovina.
RIQUADRI = [
    (
        "PASSO IRREVERSIBILE",
        "nvme0n1p4 (/home, 402,98 GB) va MONTATA, NON formattata. Se si sbaglia qui, la sola "
        "copia che resta è il backup da 4,4 GB.",
    ),
    (
        "COME SI SBAGLIA, IN CONCRETO",
        "La casella di formattazione si attiva da sé quando si seleziona un filesystem nel "
        "menu della riga. Su nvme0n1p4 il menu del filesystem non si tocca affatto: si "
        "imposta soltanto il punto di montaggio. Il controllo che conta è la schermata di "
        "riepilogo prima di scrivere, dove una formattazione deve comparire soltanto per "
        "nvme0n1p2. Fino a quel pulsante nulla è stato scritto sul disco.",
    ),
]

PARTIZIONI_INTESTAZIONE = ["Partizione", "FS", "Dimensione", "Mount point", "Azione"]
PARTIZIONI_LARGHEZZE = [1500, 800, 1300, 1700, 4806]
PARTIZIONI = [
    ("nvme0n1p1", "vfat", "1,13 GB", "/boot/efi", "riusare, NON formattare", False),
    ("nvme0n1p2", "ext4", "80,00 GB", "/", "FORMATTARE, è il sistema vecchio", False),
    ("nvme0n1p3", "swap", "16,00 GB", "swap", "riusare", False),
    (
        "nvme0n1p4",
        "ext4",
        "402,98 GB",
        "/home",
        "MONTARE, NON FORMATTARE - non toccare il menu del filesystem",
        True,
    ),
]

BIOS_INTESTAZIONE = ["Percorso BIOS", "Valore", "Motivo"]
BIOS_LARGHEZZE = [3400, 1200, 5506]
BIOS = [
    (
        "Advanced → APM Configuration → Power On By PCI-E/PCI",
        "Enabled",
        "È il Wake-on-LAN: su ASUS si chiama così.",
    ),
    (
        "Advanced → APM Configuration → ErP Ready",
        "Disabled",
        "Se ErP è attivo il BIOS taglia l'alimentazione alla scheda di rete a macchina "
        "spenta e il Wake-on-LAN non funziona, qualunque cosa dica l'altra voce. È il "
        "motivo per cui il WoL abilitato spesso non va.",
    ),
    (
        "Boot → CSM → Launch CSM",
        "Disabled",
        "La chiavetta è GPT/UEFI senza CSM: il CSM va spento o si rischia un avvio in "
        "modalità legacy.",
    ),
    (
        "Secure Boot",
        "invariato",
        "Lasciare come è. Ubuntu Studio si installa comunque.",
    ),
]

BIOS_CHIUSURA = (
    "Le prime due voci sono entrambe necessarie per il Wake-on-LAN: la seconda annulla la "
    "prima se resta come è. Le quattro modifiche si fanno in un'unica sessione, poi F10 per "
    "salvare e uscire."
)

# La sequenza operativa. L'ultimo campo e' l'evidenziazione: "rosso" per il passo
# irreversibile, "giallo" per i passi in cui un errore costa tempo ma non dati.
SEQUENZA = [
    ("Spegnimento pulito", "Spegni la macchina in modo pulito dal sistema, non con il pulsante. Ci sono già 24 spegnimenti non protetti in archivio.", None),
    ("Chiavetta + BIOS", "Infila la chiavetta e accendi premendo Del per entrare nel BIOS.", None),
    ("Quattro modifiche", "Fai le quattro modifiche della tabella BIOS, poi F10 per salvare e uscire.", None),
    ("Boot menu", "Riaccendi premendo F8 (su ASUS apre il menu di avvio temporaneo) e scegli la voce UEFI della Kingston.", None),
    ("Avvio live", "Scegli Try or Install Ubuntu Studio. NON cercare la voce Check disc for defects: su questa immagine non esiste più, il controllo del supporto è automatico e il suo esito si legge dopo in /var/log/installer/casper-md5check.json.", None),
    ("Partizionamento manuale", "PRIMO DEI TRE MOMENTI. Nell'installatore scegli il partizionamento manuale, cioè Something else o Partizionamento manuale. Non scegliere in nessun caso la cancellazione del disco né l'installazione guidata.", "giallo"),
    ("nvme0n1p2 → /", "Punto di montaggio /  ·  formattazione SPUNTATA  ·  ext4. È la sola partizione da azzerare.", None),
    ("nvme0n1p4 → /home", "SECONDO DEI TRE MOMENTI, ed è quello irreversibile. Imposta SOLTANTO il punto di montaggio /home. NON toccare il menu del filesystem: selezionare un filesystem spunta la formattazione da sé. La casella di formattazione deve restare vuota. Se sbagli qui perdi 402,98 GB, e la sola copia che resta è il backup da 4,4 GB.", "rosso"),
    ("nvme0n1p1 → /boot/efi", "Punto di montaggio /boot/efi  ·  formattazione NON SPUNTATA. Si riusa quella esistente.", "giallo"),
    ("nvme0n1p3 → swap", "Assegna come swap.", None),
    ("Schermata di riepilogo", "TERZO DEI TRE MOMENTI, ed è l'unico controllo che conta davvero. Leggi l'elenco delle operazioni previste: una formattazione deve comparire SOLTANTO per nvme0n1p2. Se la parola compare accanto a nvme0n1p4 o a nvme0n1p1, torna indietro. Fino a questo pulsante nulla è stato scritto sul disco.", "rosso"),
    ("Utente", "Usa lo stesso nome alesop95, altrimenti il /home esistente risulta di proprietà di un altro identificativo numerico e i permessi vanno corretti a mano.", "giallo"),
]

VERIFICHE_TITOLO = "4 · PRIMO AVVIO, TRE VERIFICHE"
VERIFICHE_COMANDI = [
    "ls -la /home/alesop95/ && df -h /home",
    "ls ~/electroacoustics && ls -la ~/Desktop",
    "lsb_release -a && uname -r",
]
VERIFICHE_CHIUSURA = (
    "Il /home deve contenere i materiali e i prefix Wine, e ~/electroacoustics deve esserci "
    "con i suoi 281 file. Se /home risulta vuoto la formattazione è avvenuta: a quel punto si "
    "ripristina l'archivio di backup, che sta su questa postazione Windows."
)

DIFETTI_TITOLO = "5 · DUE COSE CHE L'INSTALLATORE SBAGLIA"
DIFETTI = [
    "Swap: la partizione nvme0n1p3 viene ignorata e marcata Unchanged nel riepilogo, e al suo "
    "posto nasce un file /swap.img da 4 GB sulla radice. Restano 15 GB inutilizzati e "
    "l'ibernazione non è più possibile. Si corregge dopo, in /etc/fstab, mettendo la "
    "partizione per UUID al posto del file.",
    "Limiti realtime: i file in /etc/security/limits.d/ concedono rtprio 95 e memlock unlimited "
    "ai gruppi audio e pipewire, ma l'utente creato dall'installatore non appartiene a nessuno "
    "dei due. Leggere quei file non rivela niente perché il loro contenuto è giusto: il "
    "difetto si vede solo con ulimit -r -l, che risponde 0 e 8192. Si corregge aggiungendo "
    "l'utente ai due gruppi e riaccedendo.",
]

CHIUSURA_TITOLO = "DOPO L'INSTALLAZIONE"
CHIUSURA = [
    "Si riprende da qui: servono le fasi 6, 7 e 8 della procedura completa. Prima cosa, e in "
    "quest'ordine perché l'ordine conta: dichiarare l'architettura i386 con dpkg "
    "--add-architecture, poi installare Wine, poi creare il prefix di Akabak a 32 bit. "
    "Dichiarare i386 dopo aver installato Wine non tira dentro i pacchetti a 32 bit, e Akabak "
    "non parte.",
    "Fotografia del sistema vecchio già salvata, 23 file: elenco pacchetti, fstab, prefix "
    "Wine, catena audio, limiti realtime, cronologia apt. Sulla macchina non serve più niente "
    "via SSH.",
]

# ---------------------------------------------------------------------------
# Composizione del documento OOXML
# ---------------------------------------------------------------------------

ROSSO = "C00000"
ROSSO_TENUE = "FDE7E7"
GIALLO_TENUE = "FFF6DA"
GRIGIO_INTESTAZIONE = "DDDDDD"
GRIGIO_TESTO = "444444"
MONO = "Consolas"


def esc(testo: str) -> str:
    """Testo pronto per un nodo XML."""
    return html.escape(testo, quote=False)


def run(
    testo: str,
    *,
    grassetto: bool = False,
    colore: str | None = None,
    dimensione: int = 19,
    mono: bool = False,
) -> str:
    """Un tratto di testo. La dimensione e' in mezzi punti, come vuole OOXML."""
    prop = []
    if mono:
        prop.append(f'<w:rFonts w:ascii="{MONO}" w:hAnsi="{MONO}" w:cs="{MONO}"/>')
    if grassetto:
        prop.append("<w:b/><w:bCs/>")
    if colore:
        prop.append(f'<w:color w:val="{colore}"/>')
    prop.append(f'<w:sz w:val="{dimensione}"/><w:szCs w:val="{dimensione}"/>')
    return (
        f"<w:r><w:rPr>{''.join(prop)}</w:rPr>"
        f'<w:t xml:space="preserve">{esc(testo)}</w:t></w:r>'
    )


def para(
    contenuto: str,
    *,
    stile: str | None = None,
    centrato: bool = False,
    sfondo: str | None = None,
    bordo: str | None = None,
    dopo: int | None = None,
) -> str:
    """Un paragrafo, eventualmente in un riquadro colorato."""
    prop = []
    if stile:
        prop.append(f'<w:pStyle w:val="{stile}"/>')
    if bordo:
        prop.append(
            "<w:pBdr>"
            f'<w:top w:val="single" w:color="{bordo}" w:sz="6" w:space="4"/>'
            f'<w:bottom w:val="single" w:color="{bordo}" w:sz="6" w:space="4"/>'
            f'<w:left w:val="single" w:color="{bordo}" w:sz="18" w:space="6"/>'
            f'<w:right w:val="single" w:color="{bordo}" w:sz="6" w:space="4"/>'
            "</w:pBdr>"
        )
    if sfondo:
        prop.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{sfondo}"/>')
    if centrato:
        prop.append('<w:jc w:val="center"/>')
    if dopo is not None:
        prop.append(f'<w:spacing w:after="{dopo}"/>')
    apertura = f"<w:pPr>{''.join(prop)}</w:pPr>" if prop else ""
    return f"<w:p>{apertura}{contenuto}</w:p>"


def cella(contenuto: str, larghezza: int, sfondo: str | None = None) -> str:
    prop = [f'<w:tcW w:w="{larghezza}" w:type="dxa"/>']
    if sfondo:
        prop.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{sfondo}"/>')
    prop.append(
        '<w:tcMar><w:top w:w="40" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
        '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>'
    )
    return f"<w:tc><w:tcPr>{''.join(prop)}</w:tcPr>{contenuto}</w:tc>"


def tabella(righe: list[str], larghezze: list[int]) -> str:
    griglia = "".join(f'<w:gridCol w:w="{l}"/>' for l in larghezze)
    return (
        "<w:tbl><w:tblPr>"
        f'<w:tblW w:w="{sum(larghezze)}" w:type="dxa"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:color="BBBBBB"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="BBBBBB"/>'
        '<w:left w:val="single" w:sz="4" w:color="BBBBBB"/>'
        '<w:right w:val="single" w:sz="4" w:color="BBBBBB"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="BBBBBB"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="BBBBBB"/>'
        "</w:tblBorders>"
        f"</w:tblPr><w:tblGrid>{griglia}</w:tblGrid>{''.join(righe)}</w:tbl>"
    )


def riga_intestazione(voci: list[str], larghezze: list[int]) -> str:
    celle = "".join(
        cella(para(run(v, grassetto=True, colore="222222", dimensione=17)), l, GRIGIO_INTESTAZIONE)
        for v, l in zip(voci, larghezze)
    )
    return f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{celle}</w:tr>'


def corpo_partizioni() -> str:
    righe = [riga_intestazione(PARTIZIONI_INTESTAZIONE, PARTIZIONI_LARGHEZZE)]
    for nome, fs, dim, mount, azione, critica in PARTIZIONI:
        sfondo = ROSSO_TENUE if critica else None
        celle = [
            cella(para(run(nome, grassetto=True, mono=True)), PARTIZIONI_LARGHEZZE[0], sfondo),
            cella(para(run(fs, mono=True)), PARTIZIONI_LARGHEZZE[1], sfondo),
            cella(para(run(dim)), PARTIZIONI_LARGHEZZE[2], sfondo),
            cella(para(run(mount, grassetto=True, mono=True)), PARTIZIONI_LARGHEZZE[3], sfondo),
            cella(
                para(run(azione, grassetto=critica, colore=ROSSO if critica else None)),
                PARTIZIONI_LARGHEZZE[4],
                sfondo,
            ),
        ]
        righe.append(f"<w:tr>{''.join(celle)}</w:tr>")
    return tabella(righe, PARTIZIONI_LARGHEZZE)


def corpo_bios() -> str:
    righe = [riga_intestazione(BIOS_INTESTAZIONE, BIOS_LARGHEZZE)]
    for indice, (percorso, valore, motivo) in enumerate(BIOS):
        sfondo = "F2F2F2" if indice % 2 else None
        celle = [
            cella(para(run(percorso, grassetto=True, dimensione=18)), BIOS_LARGHEZZE[0], sfondo),
            cella(para(run(valore, grassetto=True, colore=ROSSO)), BIOS_LARGHEZZE[1], sfondo),
            cella(para(run(motivo, dimensione=16)), BIOS_LARGHEZZE[2], sfondo),
        ]
        righe.append(f"<w:tr>{''.join(celle)}</w:tr>")
    return tabella(righe, BIOS_LARGHEZZE)


def corpo_sequenza() -> str:
    larghezze = [520, 560, 9026]
    righe = []
    for numero, (titolo, testo, evidenza) in enumerate(SEQUENZA, start=1):
        sfondo = {"rosso": ROSSO_TENUE, "giallo": GIALLO_TENUE}.get(evidenza)
        contenuto = (
            run(f"{titolo} - ", grassetto=True, colore=ROSSO if evidenza == "rosso" else None, dimensione=18)
            + run(testo, dimensione=18)
        )
        celle = [
            cella(para(run("\u2610", dimensione=26), centrato=True), larghezze[0], sfondo),
            cella(para(run(str(numero), grassetto=True, dimensione=20), centrato=True), larghezze[1], sfondo),
            cella(para(contenuto), larghezze[2], sfondo),
        ]
        righe.append(f"<w:tr>{''.join(celle)}</w:tr>")
    return tabella(righe, larghezze)


def blocco_comandi(comandi: list[str]) -> str:
    return "".join(
        para(run(c, mono=True, dimensione=18), sfondo="F2F2F2", dopo=0) for c in comandi
    )


def sezione_licenza(riservato: Path) -> str:
    """Legge i due valori dal file riservato non versionato."""
    testo = riservato.read_text(encoding="utf-8")
    identificatore = re.search(r"Machine Identifier\s+(\S+)", testo)
    codice = re.search(r"Release Code\s+(\S+)", testo)
    if not identificatore or not codice:
        raise ValueError(
            f"in {riservato} non trovo Machine Identifier e Release Code: "
            "il file esiste ma non ha il formato atteso"
        )
    return (
        para(run("5 · LICENZA AKABAK E VACS", grassetto=True), stile="Heading1")
        + para(
            run(
                "Foglio riservato: porta un codice di attivazione permanente. Si inserisce una "
                "volta sola, da AKABAK, nel prefix a 32 bit; VACS non ne chiede un secondo.",
                dimensione=17,
                colore=GRIGIO_TESTO,
            )
        )
        + blocco_comandi(
            [
                f"Machine Identifier   {identificatore.group(1)}",
                f"Release Code         {codice.group(1)}",
            ]
        )
    )


def documento(con_licenza: Path | None) -> str:
    corpo = [
        para(run(TITOLO, grassetto=True, colore=ROSSO, dimensione=28), dopo=40),
        para(run(SOTTOTITOLO, colore=GRIGIO_TESTO, dimensione=16), dopo=160),
    ]
    for etichetta, testo in RIQUADRI:
        corpo.append(
            para(
                run(f"{etichetta}: ", grassetto=True, colore=ROSSO, dimensione=20)
                + run(testo, grassetto=True, colore=ROSSO, dimensione=20),
                sfondo=ROSSO_TENUE,
                bordo=ROSSO,
                dopo=170,
            )
        )
    corpo += [
        para(run("1 · MAPPA DELLE PARTIZIONI", grassetto=True), stile="Heading1"),
        corpo_partizioni(),
        para(run("2 · BIOS ASUS H170-PRO (BIOS 3805)", grassetto=True), stile="Heading1"),
        corpo_bios(),
        para(run(BIOS_CHIUSURA, dimensione=17)),
        para(run("3 · SEQUENZA OPERATIVA", grassetto=True), stile="Heading1"),
        corpo_sequenza(),
        para(run(VERIFICHE_TITOLO, grassetto=True), stile="Heading1"),
        blocco_comandi(VERIFICHE_COMANDI),
        para(run(VERIFICHE_CHIUSURA, dimensione=17)),
        para(run(DIFETTI_TITOLO, grassetto=True), stile="Heading1"),
    ]
    corpo += [para(run(d, dimensione=17)) for d in DIFETTI]
    corpo += [
        para(run(CHIUSURA_TITOLO, grassetto=True), stile="Heading1"),
    ]
    corpo += [para(run(t, dimensione=17)) for t in CHIUSURA]
    if con_licenza is not None:
        corpo.append(sezione_licenza(con_licenza))

    sezione = (
        "<w:sectPr>"
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="850" w:right="850" w:bottom="850" w:left="850" '
        'w:header="0" w:footer="0" w:gutter="0"/>'
        "</w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(corpo)}{sezione}</w:body></w:document>"
    )


STILI = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    "<w:docDefaults><w:rPrDefault><w:rPr>"
    '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
    '<w:sz w:val="19"/><w:szCs w:val="19"/><w:lang w:val="it-IT"/>'
    "</w:rPr></w:rPrDefault>"
    '<w:pPrDefault><w:pPr><w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr>'
    "</w:pPrDefault></w:docDefaults>"
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    "<w:name w:val=\"Normal\"/></w:style>"
    '<w:style w:type="paragraph" w:styleId="Heading1">'
    '<w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:spacing w:before="220" w:after="90"/>'
    '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="C00000"/></w:pBdr></w:pPr>'
    f'<w:rPr><w:b/><w:bCs/><w:color w:val="{ROSSO}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
    "</w:style></w:styles>"
)

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    "</Types>"
)

RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    "</Relationships>"
)

RELS_DOCUMENTO = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    "</Relationships>"
)


def scrivi(destinazione: Path, con_licenza: Path | None) -> None:
    parti = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": RELS,
        "word/_rels/document.xml.rels": RELS_DOCUMENTO,
        "word/document.xml": documento(con_licenza),
        "word/styles.xml": STILI,
    }
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destinazione, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, contenuto in parti.items():
            z.writestr(nome, contenuto.encode("utf-8"))


def main() -> int:
    radice = Path(__file__).resolve().parent.parent
    predefinita = radice / "_notes" / "scheda-reinstallazione-ubuntu-studio.docx"

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--out",
        type=Path,
        default=predefinita,
        help="percorso del .docx da scrivere; il valore predefinito sta sotto _notes/, "
        "che il .gitignore esclude, perche' e' materiale di stampa e non documentazione",
    )
    ap.add_argument(
        "--con-licenza",
        action="store_true",
        help="aggiunge la sezione con Machine Identifier e Release Code, letti da "
        "_notes/licenze-akabak-riservato.md. Il foglio stampato diventa riservato",
    )
    args = ap.parse_args()

    riservato = radice / "_notes" / "licenze-akabak-riservato.md"
    if args.con_licenza and not riservato.is_file():
        print(f"errore: --con-licenza richiede {riservato}, che non esiste", file=sys.stderr)
        return 1

    try:
        scrivi(args.out, riservato if args.con_licenza else None)
    except (OSError, ValueError) as errore:
        print(f"errore: {errore}", file=sys.stderr)
        return 1

    passi = len(SEQUENZA)
    print(f"scritto {args.out}")
    print(f"{passi} passi in sequenza, {len(PARTIZIONI)} partizioni, {len(BIOS)} voci di BIOS")
    if args.con_licenza:
        print("ATTENZIONE: il documento contiene il Release Code. Foglio riservato.")
    else:
        print("senza dati di licenza; con --con-licenza li aggiunge da _notes/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
