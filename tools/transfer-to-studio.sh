#!/usr/bin/env bash
# Trasferisce i materiali pesanti del progetto sulla macchina Ubuntu Studio.
# Non cancella nulla sull'origine: la rimozione resta una decisione manuale,
# da prendere dopo che il confronto delle impronte SHA-256 e' andato a buon fine.
#
# Uso:
#   bash tools/transfer-to-studio.sh --verifica    solo controlli preliminari
#   bash tools/transfer-to-studio.sh               trasferimento completo
#
# L'host e la destinazione si possono sovrascrivere da ambiente:
#   STUDIO_HOST=alesop95@192.168.10.204 STUDIO_BASE=~/electroacoustics bash tools/transfer-to-studio.sh

set -euo pipefail

STUDIO_HOST="${STUDIO_HOST:-alesop95@192.168.10.204}"
STUDIO_BASE="${STUDIO_BASE:-electroacoustics}"
SOLO_VERIFICA=0
[ "${1:-}" = "--verifica" ] && SOLO_VERIFICA=1

RADICE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MATERIALI="$RADICE/Akabak + VACS"

# Mappa origine -> sottocartella di destinazione. Una riga per file.
MAPPA=(
  "AKABAK_Pro_v324b126.exe|installers"
  "VACS_64_v213b33.exe|installers"
  "VACS_32_v213b33.exe|installers"
  "AKABAK-Examples.zip|examples"
  "Gmail - Akabak 3 license.pdf|licenze"
  "update AKABAK (Joerg Panzer)_2026-03-19_10-18-32.jpg|licenze"
  "randteam.url|licenze"
)
DOCX="_notes/full_electroacoustics.docx"

nota()  { printf '  %s\n' "$*"; }
titolo(){ printf '\n== %s ==\n' "$*"; }
errore(){ printf 'ERRORE: %s\n' "$*" >&2; }

titolo "Controlli preliminari"

mancanti=0
for strumento in ssh sha256sum; do
  if command -v "$strumento" >/dev/null 2>&1; then
    nota "$strumento presente"
  else
    errore "$strumento non trovato sul PATH"
    mancanti=1
  fi
done
[ "$mancanti" -eq 0 ] || { errore "installare gli strumenti mancanti e rilanciare"; exit 1; }

# rsync e' preferibile perche' riprende un trasferimento interrotto, ma su Git Bash
# per Windows non c'e'. In sua assenza si usa scp, che copia sempre da capo.
if command -v rsync >/dev/null 2>&1; then
  COPIA=rsync
  nota "rsync presente: trasferimento riprendibile"
else
  COPIA=scp
  if command -v scp >/dev/null 2>&1; then
    nota "rsync assente, si usa scp: un'interruzione richiede di ricopiare il file da capo"
  else
    errore "ne' rsync ne' scp trovati sul PATH"
    exit 1
  fi
fi

if [ ! -d "$MATERIALI" ]; then
  errore "cartella dei materiali non trovata: $MATERIALI"
  exit 1
fi
nota "cartella dei materiali trovata"

assenti=0
for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  if [ ! -f "$MATERIALI/$nome" ]; then
    errore "file di origine assente: $nome"
    assenti=1
  fi
done
[ -f "$RADICE/$DOCX" ] || nota "avviso: $DOCX non presente, verra' saltato"
[ "$assenti" -eq 0 ] || { errore "manifest e disco non coincidono, controllare prima di trasferire"; exit 1; }
nota "tutti i file del manifest sono presenti"

byte_totali=0
for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  byte_totali=$(( byte_totali + $(stat -c%s "$MATERIALI/$nome") ))
done
[ -f "$RADICE/$DOCX" ] && byte_totali=$(( byte_totali + $(stat -c%s "$RADICE/$DOCX") ))
nota "da trasferire: $(( byte_totali / 1048576 )) MiB in $(( ${#MAPPA[@]} + 1 )) file"

titolo "Raggiungibilita' dell'host"

if ssh -o BatchMode=yes -o ConnectTimeout=10 "$STUDIO_HOST" "echo raggiungibile" >/dev/null 2>&1; then
  nota "$STUDIO_HOST risponde"
else
  errore "$STUDIO_HOST non risponde"
  errore "verificare che la macchina sia accesa, sullo stesso segmento di rete, e con sshd attivo"
  errore "diagnostica: ping dell'indirizzo, presenza in tabella ARP, ascolto sulla porta 22"
  exit 2
fi

spazio_kib="$(ssh -o BatchMode=yes "$STUDIO_HOST" "df -Pk \"\$HOME\" | awk 'NR==2 {print \$4}'")"
nota "spazio disponibile in home sulla destinazione: $(( spazio_kib / 1024 )) MiB"
if [ "$(( spazio_kib * 1024 ))" -lt "$(( byte_totali * 2 ))" ]; then
  errore "spazio insufficiente: serve almeno il doppio dei byte da trasferire per lavorare con margine"
  exit 3
fi

if [ "$SOLO_VERIFICA" -eq 1 ]; then
  titolo "Solo verifica: nessun file copiato"
  exit 0
fi

titolo "Creazione dell'albero di destinazione"
ssh -o BatchMode=yes "$STUDIO_HOST" "mkdir -p \"\$HOME/$STUDIO_BASE\"/{installers,examples,licenze,sorgenti}"
nota "albero creato sotto \$HOME/$STUDIO_BASE"

copia_uno() {
  origine="$1"
  sotto="$2"
  if [ "$COPIA" = rsync ]; then
    rsync -h --partial --progress --times "$origine" "$STUDIO_HOST:\$HOME/$STUDIO_BASE/$sotto/"
  else
    scp -p "$origine" "$STUDIO_HOST:\$HOME/$STUDIO_BASE/$sotto/"
  fi
}

titolo "Trasferimento con $COPIA"
for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  sotto="${voce##*|}"
  nota "$nome -> $sotto/"
  copia_uno "$MATERIALI/$nome" "$sotto"
done
if [ -f "$RADICE/$DOCX" ]; then
  nota "$(basename "$DOCX") -> sorgenti/"
  copia_uno "$RADICE/$DOCX" "sorgenti"
fi

titolo "Verifica delle impronte"

atteso="$(mktemp)"
ottenuto="$(mktemp)"
trap 'rm -f "$atteso" "$ottenuto"' EXIT

for voce in "${MAPPA[@]}"; do
  nome="${voce%%|*}"
  sha256sum "$MATERIALI/$nome" | awk -v n="$nome" '{print $1"  "n}'
done > "$atteso"
if [ -f "$RADICE/$DOCX" ]; then
  sha256sum "$RADICE/$DOCX" | awk -v n="$(basename "$DOCX")" '{print $1"  "n}' >> "$atteso"
fi
sort -k2 -o "$atteso" "$atteso"

ssh -o BatchMode=yes "$STUDIO_HOST" "cd \"\$HOME/$STUDIO_BASE\" && find . -type f -exec sha256sum {} + | sed 's#  \./[^/]*/#  #'" | sort -k2 > "$ottenuto"

if diff -u "$atteso" "$ottenuto"; then
  titolo "Trasferimento verificato: tutte le impronte coincidono"
  nota "la rimozione dei file dall'origine resta manuale e deliberata"
else
  errore "le impronte non coincidono: non rimuovere nulla dall'origine"
  exit 4
fi
